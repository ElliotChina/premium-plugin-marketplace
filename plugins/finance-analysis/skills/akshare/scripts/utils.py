#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AKShare 技能文档工具函数
"""

from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict

from config import DOCS_DIR


def get_today_str() -> str:
    """获取今日日期字符串"""
    return datetime.now().strftime("%Y%m%d")


def get_local_docs() -> Dict[str, List[Path]]:
    """
    获取本地所有文档，按类别分组

    Returns:
        Dict[str, List[Path]]: {category: [Path, ...], ...}
    """
    docs = {}
    if not DOCS_DIR.exists():
        DOCS_DIR.mkdir(parents=True, exist_ok=True)
        return docs

    for f in DOCS_DIR.glob("*.md"):
        # 解析文件名：category_YYYYMMDD.md
        name = f.stem
        parts = name.rsplit("_", 1)
        if len(parts) == 2 and parts[1].isdigit() and len(parts[1]) == 8:
            category = parts[0]
            if category not in docs:
                docs[category] = []
            docs[category].append(f)
    return docs


def get_latest_doc_date(category: str) -> Optional[str]:
    """
    获取某类别最新的文档日期

    Args:
        category: 文档类别

    Returns:
        最新的文档日期 (YYYYMMDD)，无文档时返回 None
    """
    docs = get_local_docs()
    if category not in docs or not docs[category]:
        return None

    # 按日期排序，返回最新的
    sorted_docs = sorted(docs[category], key=lambda x: x.stem.rsplit("_", 1)[1], reverse=True)
    return sorted_docs[0].stem.rsplit("_", 1)[1]


def get_latest_doc_path(category: str) -> Optional[Path]:
    """
    获取某类别的最新文档路径

    Args:
        category: 文档类别

    Returns:
        最新文档路径，无文档时返回 None
    """
    docs = get_local_docs()
    if category not in docs or not docs[category]:
        return None

    sorted_docs = sorted(docs[category], key=lambda x: x.stem.rsplit("_", 1)[1], reverse=True)
    return sorted_docs[0]


def extract_api_doc(api_name: str, category: str = "stock") -> Optional[str]:
    """
    从文档中提取指定接口的完整描述

    Args:
        api_name: 接口名称（如 stock_zh_a_hist）
        category: 文档类别，默认为 stock

    Returns:
        接口完整描述字符串，未找到时返回 None

    Example:
        >>> doc = extract_api_doc("stock_zh_a_hist")
        >>> print(doc)  # 打印接口的完整描述
    """
    doc_path = get_latest_doc_path(category)
    if not doc_path:
        return None

    # 读取文档内容
    with open(doc_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # 查找接口位置
    start_idx = None
    end_idx = None

    for i, line in enumerate(lines):
        # 查找接口开始行（格式：接口: api_name）
        if line.strip().startswith(f"接口: {api_name}"):
            start_idx = i
            # 从接口名称行开始，向前查找所属章节标题（作为起始边界）
            # 这样可以包含接口的完整上下文
            for j in range(i - 1, -1, -1):
                if lines[j].strip().startswith("#####"):
                    start_idx = j
                    break
                elif lines[j].strip().startswith("####"):
                    start_idx = j
                    break
            break

    if start_idx is None:
        return None

    # 查找接口结束位置（下一个同级或更高级标题）
    for i in range(start_idx + 1, len(lines)):
        line = lines[i].strip()
        # 遇到下一个接口或章节标题时停止
        if line.startswith("#####") or line.startswith("####") or line.startswith("###"):
            end_idx = i
            break

    # 如果没找到结束标记，读取到文件末尾
    if end_idx is None:
        end_idx = len(lines)

    # 提取接口描述
    api_doc = ''.join(lines[start_idx:end_idx])
    return api_doc
