#!/usr/bin/env python3
"""prd-check.py — PRD 体系交付前机械检查。

用法: python3 prd-check.py [prd目录]   # 缺省依次探测 ./docs/prd、./prd

分级:
  [ERROR] 阻断交付，必须清零或经用户明确确认豁免
  [WARN]  提示人工确认，不阻断

退出码: 有 ERROR → 1；仅 WARN 或通过 → 0
"""

import os
import re
import sys

# 阈值常量（按项目体量可调）
MODULE_OVERVIEW_MAX_LINES = 200   # 模块 overview 超过 → 功能混入嫌疑
MODULE_OVERVIEW_MAX_SECTIONS = 8  # 模块 overview ## 章节数超过 → 功能混入嫌疑
FEATURE_PRD_MIN_LINES = 30      # 功能 PRD 低于 → 结构未补全嫌疑

KNOWN_TOP = {"index.md", "00-overview", "01-foundation", "02-modules", "03-workflows"}
FORBIDDEN_TOP = {"changes", "releases", "decisions"}  # 规范明令禁止的目录

LINK_RE = re.compile(r"\]\(([^)\s]+)\)")
PLACEHOLDER_RE = re.compile(r"【[^】]*】")
GUIDE_RE_LIST = [
    re.compile(r"仅当.{0,40}时填写"),
    re.compile(r"与第\s*\d+\s*章.{0,12}分工"),
]
PENDING_RE = re.compile(r"<!--\s*待确认")
RULE_SECTION_RE = re.compile(r"^#+\s*(\d+[.\s]*)?业务规则", re.M)
H2_RE = re.compile(r"^## ", re.M)

errors = []
warns = []


def err(path, msg):
    errors.append(f"[ERROR] {path}: {msg}")


def warn(path, msg):
    warns.append(f"[WARN]  {path}: {msg}")


def find_prd_root(arg):
    if arg:
        return arg if os.path.isdir(arg) else None
    for cand in ("docs/prd", "prd"):
        if os.path.isdir(cand):
            return cand
    return None


def strip_anchor(target):
    return target.split("#", 1)[0]


def resolve(from_dir, target):
    return os.path.normpath(os.path.join(from_dir, target))


def main():
    root = find_prd_root(sys.argv[1] if len(sys.argv) > 1 else None)
    if not root:
        print("[ERROR] 未找到 prd 目录（可显式传入路径）")
        return 1

    all_md = []
    for dirpath, _dirnames, filenames in os.walk(root):
        for name in filenames:
            if name.endswith(".md"):
                all_md.append(os.path.join(dirpath, name))
    if not all_md:
        print(f"[ERROR] {root} 下没有 .md 文件")
        return 1

    # E0 顶层结构漂移
    for name in sorted(os.listdir(root)):
        if name in KNOWN_TOP or name.startswith("."):
            continue
        if name.lower() in FORBIDDEN_TOP:
            err(root, f"禁止的顶层目录 {name}/（规范 3.1：不设 changes/releases/decisions）")
        else:
            warn(root, f"未识别的顶层条目 {name}（标准结构仅四层目录 + index.md）")

    # 遍历文件：链接、占位符、指引残留、待确认标记
    referenced = set()  # 被 .md 链接引用的文件（绝对规范路径）
    contents = {}
    for path in sorted(all_md):
        rel = os.path.relpath(path, root)
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
        contents[path] = text

        for m in LINK_RE.finditer(text):
            target = strip_anchor(m.group(1))
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            resolved = resolve(os.path.dirname(path), target)
            if not os.path.exists(resolved):
                if target.endswith(".md"):
                    err(rel, f"悬空链接 → {target}")
            else:
                referenced.add(resolved)

        ph = PLACEHOLDER_RE.search(text)
        if ph:
            err(rel, f"占位符残留 {ph.group(0)}（模板未填写完整）")
        for guide_re in GUIDE_RE_LIST:
            if guide_re.search(text):
                err(rel, f"模板指引残留（套用模板时应删除说明性文字）")
                break
        if PENDING_RE.search(text):
            err(rel, "存在 <!-- 待确认 --> 标记（门禁要求清零，或经用户确认保留后豁免）")

    # 模块层检查
    modules_dir = os.path.join(root, "02-modules")
    if os.path.isdir(modules_dir):
        for entry in sorted(os.listdir(modules_dir)):
            mdir = os.path.join(modules_dir, entry)
            if not os.path.isdir(mdir):
                continue
            mrel = f"02-modules/{entry}"
            overview = os.path.join(mdir, "overview.md")
            if not os.path.isfile(overview):
                err(mrel, "缺少模块 overview.md（模块索引与路由入口）")
                continue
            rtext = contents.get(overview, "")
            lines = rtext.count("\n") + 1
            if lines > MODULE_OVERVIEW_MAX_LINES:
                warn(f"{mrel}/overview.md", f"{lines} 行，超过 {MODULE_OVERVIEW_MAX_LINES}（功能混入嫌疑，应拆为独立功能 PRD）")
            if len(H2_RE.findall(rtext)) > MODULE_OVERVIEW_MAX_SECTIONS:
                warn(f"{mrel}/overview.md", f"## 章节数超过 {MODULE_OVERVIEW_MAX_SECTIONS}（功能章节混入嫌疑）")

            # 功能文件必须登记在模块 overview 功能清单
            overview_refs = set()
            for m in LINK_RE.finditer(rtext):
                t = strip_anchor(m.group(1))
                if t.endswith(".md"):
                    overview_refs.add(resolve(mdir, t))
            for name in sorted(os.listdir(mdir)):
                if name == "overview.md" or not name.endswith(".md"):
                    continue
                fpath = os.path.join(mdir, name)
                if fpath not in overview_refs:
                    err(f"{mrel}/{name}", "未登记在模块 overview 功能清单表（路由断链）")

            # 功能 PRD 结构与体量
            for name in sorted(os.listdir(mdir)):
                if name == "overview.md" or not name.endswith(".md"):
                    continue
                fpath = os.path.join(mdir, name)
                ftext = contents.get(fpath, "")
                flines = ftext.count("\n") + 1
                frel = f"{mrel}/{name}"
                if flines < FEATURE_PRD_MIN_LINES:
                    warn(frel, f"仅 {flines} 行，低于 {FEATURE_PRD_MIN_LINES}（结构未补全嫌疑：状态/异常/验收章节应按功能类型展开）")
                if not RULE_SECTION_RE.search(ftext):
                    warn(frel, "缺少「业务规则」章节（功能 PRD 的最低结构要求）")

    # 跨模块流程孤儿检测
    wf_dir = os.path.join(root, "03-workflows")
    if os.path.isdir(wf_dir):
        for name in sorted(os.listdir(wf_dir)):
            if not name.endswith(".md"):
                continue
            fpath = os.path.join(wf_dir, name)
            if fpath not in referenced:
                warn(f"03-workflows/{name}", "未被任何文档引用（应在相关模块 overview 的关联跨模块流程登记）")

    # 输出
    for line in errors:
        print(line)
    for line in warns:
        print(line)
    print(f"\n检查完成: {len(all_md)} 个文件 | ERROR {len(errors)} | WARN {len(warns)}")
    if errors:
        print("结果: FAIL — ERROR 必须清零或经用户明确确认豁免后方可交付")
        return 1
    print("结果: PASS" + (f"（含 {len(warns)} 条 WARN 待人工确认）" if warns else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
