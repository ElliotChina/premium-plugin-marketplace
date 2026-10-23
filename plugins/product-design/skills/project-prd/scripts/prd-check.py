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
SEP_ROW_RE = re.compile(r"^\|[-\s|:]+\|$")

# 表结构对齐规则：(表头识别关键词组, 必含列关键词, 缺失提示)——列集随模板演进同步更新
TABLE_ALIGN_RULES = [
    (("字段", "校验"), "默认值", "字段定义表缺『默认值 / 生成规则』列（模板 §3.3 六列结构）"),
    (("状态", "业务含义"), "是否终态", "状态定义表缺『是否终态』列（模板 §5.1）"),
    (("允许角色",), "无权限", "权限表缺『无权限表现』列（模板 §6）"),
    (("触发行为",), "时机", "触发行为表缺『时机』列（模板 §8）"),
]


def table_headers(text):
    """提取 markdown 表头单元格列表（表头行 + 下一行为分隔行）。"""
    lines = text.splitlines()
    out = []
    for i, line in enumerate(lines):
        if line.startswith("|") and i + 1 < len(lines) and SEP_ROW_RE.match(lines[i + 1]):
            out.append([c.strip() for c in line.strip("|").split("|")])
    return out

errors = []
warns = []


def err(path, msg):
    errors.append(f"[ERROR] {path}: {msg}")


def warn(path, msg):
    warns.append(f"[WARN]  {path}: {msg}")


def find_prd_root(arg):
    if arg:
        return os.path.abspath(arg) if os.path.isdir(arg) else None
    for cand in ("docs/prd", "prd"):
        if os.path.isdir(cand):
            return os.path.abspath(cand)
    return None


def strip_anchor(target):
    return target.split("#", 1)[0]


def resolve(from_dir, target):
    return os.path.normpath(os.path.join(from_dir, target))


def actual_path(path):
    """逐段解析为文件系统实际大小写路径；某段仅大小写不敏感匹配时返回 (实际路径, True)。

    macOS 大小写不敏感卷上 realpath 保留调用者的大小写，不可靠；listdir 返回磁盘实际名。
    入参须为绝对路径（root 已 abspath，resolved 均绝对）。
    """
    cur = []
    mismatch = False
    for part in path.split(os.sep):
        if part in ("", ".", ".."):
            cur.append(part)
            continue
        try:
            # 绝对路径首段 join 后为空串，回退到根目录
            names = os.listdir(os.sep.join(cur) or os.sep)
        except OSError:
            return path, False
        if part in names:
            cur.append(part)
            continue
        hit = next((n for n in names if n.lower() == part.lower()), None)
        if hit is None:
            return path, False
        cur.append(hit)
        mismatch = True
    return os.sep.join(cur), mismatch


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
                # 大小写偏差：macOS 大小写不敏感文件系统上 exists 通过，但推到 Linux CI 会断
                real, mismatch = actual_path(resolved)
                if mismatch:
                    warn(rel, f"链接大小写与实际文件不符（跨平台 CI 会断链）: {target} → {os.path.relpath(real, root)}")

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
                # 表结构对齐：表头与模板列集比对（内容保留、结构映射）
                for header in table_headers(ftext):
                    flat = "".join(header)
                    for keys, must, msg in TABLE_ALIGN_RULES:
                        if all(k in flat for k in keys) and must not in flat:
                            warn(frel, msg)

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
    print("结果: 机械检查通过" + (f"（含 {len(warns)} 条 WARN 待人工确认）" if warns else ""))
    print("注意: 机械检查通过 ≠ 文档质量审查通过——语义一致性（业务对象横向核对、规则冲突、异常闭环）需按 SKILL.md 工作流 C 复核")
    return 0


if __name__ == "__main__":
    sys.exit(main())
