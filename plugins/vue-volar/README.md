# vue-volar

Vue.js 语言服务（Volar）的 Claude Code 插件，为 `.vue` 单文件组件提供代码智能支持。

基于 [Piebald-AI/claude-code-lsps](https://github.com/Piebald-AI/claude-code-lsps) 的 vue-volar 插件改造，核心增强：**TypeScript SDK 路径动态探测**，解决 monorepo / 嵌套项目场景。

## 前置条件

插件只提供 LSP 集成，语言服务器本体需要全局安装：

```bash
npm install -g @vue/language-server@2
```

> 仅支持 2.x。3.x 需要 tsserver 请求转发，Claude Code 的 LSP 客户端不支持。
> 建议同时全局安装 TypeScript 作为兜底：`npm install -g typescript`（已有 `nvm` 全局 typescript 时无需操作）。

## 与原版的差异

原版的 `initializationOptions.typescript.tsdk` 写死为 `node_modules/typescript/lib`（相对工作目录解析），Web 项目位于工作目录下一级或两级时（如 monorepo 的 `packages/web`、`apps/admin/client`）无法找到 TypeScript。

本插件通过启动器 `scripts/launch.js` 解决：

1. 探测并启动 `vue-language-server` v2.x（PATH 扫描，shim 路径降权）
2. 拦截 LSP `initialize` 请求，按以下顺序探测 tsdk，改写为**绝对路径**：
   1. 工作目录：`./node_modules/typescript/lib`
   2. 两级子目录：`./*/node_modules/typescript/lib`、`./*/*/node_modules/typescript/lib`（monorepo 场景）
   3. npm 全局：`$(npm root -g)/typescript/lib`
3. 其余所有 LSP 消息双向透传，无额外开销

探测结果打印到 stderr（前缀 `[vue-volar-launcher]`），`claude --debug` 可见。

## 安装

```bash
claude plugin add /path/to/premium-plugin-marketplace/plugins/vue-volar
```

或通过 marketplace 安装后，在 Vue 项目中打开 Claude Code 即自动生效。

## 许可证

MIT License
