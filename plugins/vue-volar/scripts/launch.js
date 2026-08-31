#!/usr/bin/env node
// vue-language-server 启动器 + tsdk 动态探测代理
//
// 职责：
// 1. 在 PATH 中探测 vue-language-server v2.x（shim 路径降权），以 stdio 启动
// 2. 拦截客户端发来的 LSP initialize 请求，动态探测 TypeScript SDK 路径并改写
//    initializationOptions.typescript.tsdk 为绝对路径：
//    工作目录 → 两级子目录（monorepo 嵌套项目）→ npm 全局兜底
// 3. 其余所有 LSP 消息（双向）原样透传，无额外开销
//
// 原版（Piebald-AI/claude-code-lsps）使用静态相对路径 node_modules/typescript/lib，
// 仅在项目根存在 node_modules 时可用；本启动器解决 monorepo/嵌套项目场景，
// 并消除 nvm 切换 node 版本后全局路径变化的问题。

'use strict';

const { spawn, execFileSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const LOG_PREFIX = '[vue-volar-launcher]';

function log(message) {
  process.stderr.write(`${LOG_PREFIX} ${message}\n`);
}

// ---------- 探测 vue-language-server ----------

// 与原版 shell 逻辑一致：取版本输出中最后一个 x.y.z 匹配
function parseVersion(text) {
  let found = '';
  const re = /\d+\.\d+\.\d+/g;
  let m;
  while ((m = re.exec(text)) !== null) {
    found = m[0];
  }
  return found;
}

function isVersionNewer(lhs, rhs) {
  const l = lhs.split('.').map(Number);
  const r = rhs.split('.').map(Number);
  for (let i = 0; i < 3; i++) {
    if (l[i] > r[i]) return true;
    if (l[i] < r[i]) return false;
  }
  return false;
}

function readVersionFlag(candidate, flag) {
  try {
    return execFileSync(candidate, [flag], { encoding: 'utf8', timeout: 10000 });
  } catch (e) {
    return (e.stdout || '') + (e.stderr || '');
  }
}

function getServerVersion(candidate) {
  for (const flag of ['--version', '-v']) {
    const version = parseVersion(readVersionFlag(candidate, flag));
    if (version) return version;
  }
  return '';
}

function isShimPath(p) {
  return p.split(path.sep).includes('shims');
}

// PATH 扫描：仅接受 2.x；同版本时优先非 shim 路径（nvm/fnm shim 可能不可靠）
function findServer() {
  let bestCandidate = '';
  let bestVersion = '';
  const dirs = (process.env.PATH || '').split(':').filter(Boolean);

  for (const dir of dirs) {
    const candidate = path.join(dir, 'vue-language-server');
    try {
      fs.accessSync(candidate, fs.constants.X_OK);
    } catch {
      continue;
    }
    const version = getServerVersion(candidate);
    if (!version || !version.startsWith('2.')) continue;

    const replace =
      !bestVersion ||
      isVersionNewer(version, bestVersion) ||
      (version === bestVersion && isShimPath(bestCandidate) && !isShimPath(candidate));

    if (replace) {
      bestCandidate = candidate;
      bestVersion = version;
    }
  }
  return { candidate: bestCandidate, version: bestVersion };
}

// ---------- 探测 TypeScript SDK（tsdk） ----------

function hasTsdkLib(dir) {
  return (
    fs.existsSync(path.join(dir, 'typescript.js')) ||
    fs.existsSync(path.join(dir, 'tsserverlibrary.js'))
  );
}

function findTsdk() {
  const root = process.cwd();
  const candidates = [path.join(root, 'node_modules', 'typescript', 'lib')];

  // 两级子目录：覆盖 monorepo / 嵌套项目（如 packages/web、apps/admin/client）
  let level1 = [];
  try {
    level1 = fs
      .readdirSync(root, { withFileTypes: true })
      .filter((e) => e.isDirectory() && !e.name.startsWith('.'))
      .map((e) => e.name);
  } catch {
    // cwd 不可读时跳过子目录探测
  }
  const subDirs = level1.map((name) => path.join(root, name));
  for (const dir of subDirs) {
    candidates.push(path.join(dir, 'node_modules', 'typescript', 'lib'));
  }
  for (const dir of subDirs) {
    let level2 = [];
    try {
      level2 = fs.readdirSync(dir, { withFileTypes: true });
    } catch {
      continue;
    }
    for (const entry of level2) {
      if (entry.isDirectory() && !entry.name.startsWith('.')) {
        candidates.push(path.join(dir, entry.name, 'node_modules', 'typescript', 'lib'));
      }
    }
  }

  // npm 全局兜底（如 nvm 全局安装的 typescript）
  try {
    const globalRoot = execFileSync('npm', ['root', '-g'], {
      encoding: 'utf8',
      timeout: 10000,
    }).trim();
    if (globalRoot) candidates.push(path.join(globalRoot, 'typescript', 'lib'));
  } catch {
    // npm 不可用时跳过全局兜底
  }

  for (const candidate of candidates) {
    if (hasTsdkLib(candidate)) return candidate;
  }
  return '';
}

// ---------- LSP initialize 请求改写 ----------

// 返回改写后的 body；非 initialize 请求返回 null（调用方原样转发）
function rewriteInitialize(body) {
  let message;
  try {
    message = JSON.parse(body.toString('utf8'));
  } catch {
    return null;
  }
  if (!message || message.method !== 'initialize' || !message.params) {
    return null;
  }

  const options = message.params.initializationOptions || (message.params.initializationOptions = {});
  if (!options.vue || typeof options.vue !== 'object') options.vue = {};
  if (options.vue.hybridMode === undefined) options.vue.hybridMode = false;
  if (!options.typescript || typeof options.typescript !== 'object') options.typescript = {};

  // 客户端显式配置优先，仅在缺失时动态探测
  if (!options.typescript.tsdk) {
    const tsdk = findTsdk();
    if (tsdk) {
      options.typescript.tsdk = tsdk;
      log(`tsdk: ${tsdk}`);
    } else {
      log('warning: 未找到 TypeScript SDK（工作目录、两级子目录及 npm 全局均无），Vue 语言服务可能无法分析 TS 代码');
    }
  }

  return Buffer.from(JSON.stringify(message), 'utf8');
}

// ---------- 主流程 ----------

const { candidate: serverPath, version: serverVersion } = findServer();
if (!serverPath) {
  process.stderr.write(
    `${LOG_PREFIX} requires vue-language-server v2.x.x; no compatible version found on PATH.\n` +
      `${LOG_PREFIX} Install with: npm install -g @vue/language-server@2\n` +
      `${LOG_PREFIX} Version 3.x is incompatible because it requires tsserver request forwarding.\n`
  );
  process.exit(1);
}
log(`server: ${serverPath} (${serverVersion})`);

const server = spawn(serverPath, ['--stdio'], { stdio: ['pipe', 'pipe', 'inherit'] });

server.on('error', (err) => {
  log(`failed to start server: ${err.message}`);
  process.exit(1);
});
server.on('exit', (code) => {
  process.exit(code === null ? 1 : code);
});

process.on('SIGTERM', () => server.kill('SIGTERM'));
process.on('SIGINT', () => server.kill('SIGINT'));
process.stdin.on('end', () => server.stdin.end());
// server 意外退出后再写入会触发 EPIPE，交给 exit 处理器退出进程
server.stdin.on('error', (err) => {
  if (err.code !== 'EPIPE') log(`stdin write failed: ${err.message}`);
});

// server → client 全部透传
server.stdout.pipe(process.stdout);

// client → server：改写第一个 initialize 请求后切换为纯透传
let buffer = Buffer.alloc(0);
let passthrough = false;

function passthroughRest() {
  if (buffer.length) server.stdin.write(buffer);
  buffer = Buffer.alloc(0);
  passthrough = true;
}

process.stdin.on('data', (chunk) => {
  if (passthrough) {
    server.stdin.write(chunk);
    return;
  }
  buffer = Buffer.concat([buffer, chunk]);

  while (!passthrough) {
    const headerEnd = buffer.indexOf('\r\n\r\n');
    if (headerEnd === -1) return; // header 未完整

    const header = buffer.subarray(0, headerEnd).toString('utf8');
    const match = header.match(/Content-Length: *(\d+)/i);
    if (!match) {
      // 无法解析的帧，保底透传剩余数据
      log('warning: unparseable LSP frame, switching to passthrough');
      passthroughRest();
      return;
    }

    const bodyStart = headerEnd + 4;
    const bodyLength = parseInt(match[1], 10);
    if (buffer.length < bodyStart + bodyLength) return; // body 未完整

    const raw = buffer.subarray(0, bodyStart + bodyLength); // 原始帧
    const body = buffer.subarray(bodyStart, bodyStart + bodyLength);
    const rewritten = rewriteInitialize(body);
    buffer = buffer.subarray(bodyStart + bodyLength); // 先消费掉当前帧

    if (rewritten === null) {
      server.stdin.write(raw); // 非 initialize，原样转发，继续等待
    } else {
      server.stdin.write(
        Buffer.concat([
          Buffer.from(`Content-Length: ${Buffer.byteLength(rewritten)}\r\n\r\n`, 'utf8'),
          rewritten,
        ])
      );
      passthroughRest(); // initialize 已处理，剩余数据直接透传
    }
  }
});
