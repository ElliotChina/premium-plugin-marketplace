#!/usr/bin/env python3
"""mirror-check.py — prototypes/ 与生产源码的镜像一致性、完全独立与状态纪律校验（prototype-app 硬规则 1/2/3/6）
用法: python3 mirror-check.py [项目根目录] [生产源码根，默认 src]

镜像检查（fail）:
  「镜像生产 <路径>」: 生产对应物必须存在，一个生产文件只被映射一次，导出风格一致（default 形态一致、原型导出 ⊆ 生产导出）
  「镜像生产 <路径>」+「待建」: 0→1 页面专用——对应物尚未存在，豁免存在性与导出检查，每次运行提示待建清单
  「原型私有」:       挂具/私有实现，必须位于白名单位置（proto-harness/、proto-logic/）
  变体文件（*.variant-*.tsx?）: 首部必须声明「基准 <同目录同名镜像文件路径>」与「轴」；基准须存在、为已登记镜像文件，其生产映射计入一对多查重
  PrototypeRoot.* 为挂具入口，自动豁免
状态纪律（fail）:
  持久化 API 禁入（localStorage/sessionStorage/indexedDB/document.cookie；覆盖 ts/tsx/js/jsx/mjs/html，词法匹配——字符串拼接绕过不检测）
  测试文件禁入（*.test.*、*.spec.*、__tests__/）
  HTML 仅允许顶层 prototypes/proto-logic/ 下（LOGIC 分支产物；嵌套 proto-logic/ 目录不在豁免内）
  prototypes/README.md 必须存在，且 pages/ 下每个页面在映射表中登记
独立性检查（fail）:
  原型 → 生产: 原型文件不得 import 生产源码（相对路径越出 prototypes/、'src/'、'@/'、'~/' 均违规）
  生产 → 原型: 生产源码不得 import prototypes/，桥接文件豁免
  桥接豁免: 路径匹配 BRIDGE_ALLOW 正则（默认覆盖 App/main/router/layout 与 route-group shim），可用环境变量覆盖
人工确认（warning，不计失败）:
  占位内容粗筛（lorem/TODO/FIXME/占位）；桥接文件未检出 dev 门控字样
"""

import os
import re
import sys

MIRROR_RE = re.compile(r"镜像生产[（(待建)）： ]*([A-Za-z0-9_./-]+)")
BASE_RE = re.compile(r"基准[ ：]*([A-Za-z0-9_./-]+)")
VARIANT_RE = re.compile(r"\.variant-[^/]*\.(ts|tsx|css)$")
EXPORT_DEFAULT_RE = re.compile(r"^export default", re.M)
EXPORT_NAMED_RE = re.compile(r"^export (?:const|function|class|type|interface|let|var) ([A-Za-z0-9_]+)", re.M)
IMPORT_RE = re.compile(r"(?:from|import)\s*\(?\s*['\"]([^'\"]+)['\"]")
PROTO_IMPORT_RE = re.compile(r"(?:from|import)[^\"']*['\"][^\"']*prototypes/")
PERSIST_RE = re.compile(r"localStorage|sessionStorage|indexedDB|document\.cookie", re.I)
PLACEHOLDER_RE = re.compile(r"lorem ipsum|TODO|FIXME", re.I)
DEV_GATE_RE = re.compile(r"import\.meta\.env\.DEV|NODE_ENV")

CODE_EXT = {".ts", ".tsx", ".js", ".jsx", ".mjs"}


def walk_files(base, exts):
    out = []
    for dirpath, _dirs, names in os.walk(base):
        for name in names:
            if os.path.splitext(name)[1] in exts:
                out.append(os.path.join(dirpath, name))
    return sorted(out)


def head_text(path, lines=6):
    with open(path, encoding="utf-8", errors="replace") as fh:
        return "".join(fh.readline() for _ in range(lines))


def read(path):
    with open(path, encoding="utf-8", errors="replace") as fh:
        return fh.read()


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    src = sys.argv[2] if len(sys.argv) > 2 else "src"
    proto = os.path.join(root, "prototypes")
    bridge_allow = os.environ.get(
        "BRIDGE_ALLOW",
        r"\(prototype\)|/prototype/|(App|main|router|routes?|layout)\.(ts|tsx|js|jsx)$",
    )
    bridge_re = re.compile(bridge_allow)
    fail = False

    if not os.path.isdir(proto):
        print(f"未找到 {proto}")
        return 1

    # ---- 镜像检查 ----
    targets = []
    mirror_files = [
        f for f in walk_files(proto, {".ts", ".tsx", ".css"})
        if not os.path.basename(f).startswith("PrototypeRoot.")
    ]
    for f in mirror_files:
        rel = os.path.relpath(f, proto)
        head = head_text(f)

        # 变体文件: 验证式豁免——基准须存在、同目录同名前缀、为已登记镜像文件,且声明发散轴
        if VARIANT_RE.search(rel):
            vstem = rel.split(".variant-")[0]
            if "轴" not in head:
                print(f"变体文件缺发散轴声明: {rel}")
                fail = True
            m = BASE_RE.search(head)
            base = m.group(1) if m else ""
            if base not in (vstem + ".ts", vstem + ".tsx"):
                print(f"变体基准须为同目录同名镜像文件: {rel} -> {base or '未声明'}")
                fail = True
                continue
            base_file = os.path.join(proto, base)
            if not os.path.isfile(base_file):
                print(f"变体基准不存在: {rel} -> {base}")
                fail = True
                continue
            base_head = head_text(base_file)
            if "原型私有" in base_head:
                print(f"变体基准必须是镜像文件而非原型私有: {rel} -> {base}")
                fail = True
                continue
            if not MIRROR_RE.search(base_head):
                print(f"变体基准文件缺镜像声明: {rel} -> {base}")
                fail = True
                continue
            # 变体与基准页同源,不重复计入一对多查重
            continue

        if "原型私有" in head:
            if not (rel.startswith("proto-harness/") or rel.startswith("proto-logic/")):
                print(f"原型私有文件不在白名单位置(proto-harness/|proto-logic/): {rel}")
                fail = True
            continue

        m = MIRROR_RE.search(head)
        target = m.group(1) if m else ""
        if not target:
            print(f"缺失声明: {rel}")
            fail = True
            continue
        if not (target.startswith(src + "/") or target.startswith("/")):
            target = f"{src}/{target}"
        if "待建" in head:
            print(f"待建对应物(生产就位前豁免,就位后请移除待建标记): {rel} -> {target}")
            targets.append(target)
            continue
        prod_file = os.path.join(root, target)
        if not os.path.isfile(prod_file):
            print(f"对应物不存在: {rel} -> {target}")
            fail = True
            continue
        targets.append(target)

        # 导出风格比对: default 形态一致 + 原型导出 ⊆ 生产导出（签名偏离应写入头注释）
        if os.path.splitext(f)[1] in (".ts", ".tsx"):
            p_text, s_text = read(f), read(prod_file)
            if len(EXPORT_DEFAULT_RE.findall(p_text)) != len(EXPORT_DEFAULT_RE.findall(s_text)):
                print(f"导出风格不一致(default): {rel} vs {target}")
                fail = True
            p_named = set(EXPORT_NAMED_RE.findall(p_text))
            s_named = set(EXPORT_NAMED_RE.findall(s_text))
            for n in sorted(p_named - s_named):
                print(f"原型导出不在生产对应物中(签名偏离须头注释说明): {rel} 导出 {n}")
                fail = True

    if targets:
        seen, dups = set(), []
        for t in targets:
            if t in seen and t not in dups:
                dups.append(t)
            seen.add(t)
        if dups:
            print("同一生产文件被多个原型文件映射(合并嫌疑):")
            for t in sorted(dups):
                print(t)
            fail = True

    # ---- 状态纪律 ----
    persist_hits = []
    for f in walk_files(proto, CODE_EXT | {".html"}):
        for i, line in enumerate(read(f).splitlines(), 1):
            if PERSIST_RE.search(line):
                persist_hits.append(f"{f}:{i}:{line.strip()}")
    if persist_hits:
        print("持久化 API 禁入:")
        for h in persist_hits:
            print(h)
        fail = True

    test_hits = []
    for dirpath, dirs, _names in os.walk(proto):
        if "__tests__" in dirs:
            test_hits.append(os.path.relpath(os.path.join(dirpath, "__tests__"), proto))
    for f in walk_files(proto, {".ts", ".tsx", ".js", ".jsx", ".css", ".html", ".mjs"}):
        name = os.path.basename(f)
        if ".test." in name or ".spec." in name:
            test_hits.append(os.path.relpath(f, proto))
    if test_hits:
        print("原型目录禁入测试文件:")
        for h in test_hits:
            print(h)
        fail = True

    stray_html = [
        os.path.relpath(f, proto)
        for f in walk_files(proto, {".html"})
        if not os.path.relpath(f, proto).startswith("proto-logic/")
    ]
    if stray_html:
        print("HTML 仅允许出现在 prototypes/proto-logic/ 下:")
        for h in stray_html:
            print(h)
        fail = True

    readme = os.path.join(proto, "README.md")
    if not os.path.isfile(readme):
        print("缺 prototypes/README.md（路由映射表）")
        fail = True
    else:
        readme_text = read(readme)
        pages_dir = os.path.join(proto, "pages")
        if os.path.isdir(pages_dir):
            for f in walk_files(pages_dir, {".tsx"}):
                rel = os.path.relpath(f, proto)
                if ".variant-" in os.path.basename(f):
                    continue
                if rel not in readme_text:
                    print(f"README 映射表未登记页面: {rel}")
                    fail = True

    # ---- 独立性检查: 原型 → 生产 ----
    for f in walk_files(proto, CODE_EXT):
        rel = os.path.relpath(f, proto)
        depth = rel.count("/")
        for imp in IMPORT_RE.findall(read(f)):
            hit = None
            if imp.startswith(("@/", "~/", src + "/")):
                hit = imp
            elif imp.startswith(("./", "../")):
                m = re.match(r"(?:\.\./)+", imp)
                ups = m.end() // 3 if m else 0
                if ups > depth:
                    hit = imp
            if hit:
                print(f"越界 import(原型→生产): {rel} -> {imp}")
                fail = True

    # ---- 独立性检查: 生产 → 原型 ----
    src_dir = os.path.join(root, src)
    if os.path.isdir(src_dir):
        for f in walk_files(src_dir, {".ts", ".tsx", ".js", ".jsx"}):
            text = read(f)
            if not PROTO_IMPORT_RE.search(text):
                continue
            rel_root = os.path.relpath(f, root)
            if bridge_re.search(f):
                if not DEV_GATE_RE.search(text):
                    print(f"桥接未检出 dev 门控字样(人工确认): {rel_root}")
                continue
            print(f"生产 import 原型(非桥接): {rel_root}")
            fail = True

    # ---- 占位内容粗筛（warning）----
    for f in walk_files(proto, {".ts", ".tsx", ".css", ".html"}):
        for i, line in enumerate(read(f).splitlines(), 1):
            if PLACEHOLDER_RE.search(line):
                print(f"占位内容粗筛(人工确认): {f}:{i}:{line.strip()}")

    print("人工/运行时项不在脚本覆盖内: 工艺硬指标(ease-out/时长/reduced-motion)、变体轴发散、PICKER 逐字一致、mock 只读、晋升纪律")

    if not fail:
        print("mirror check 通过")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
