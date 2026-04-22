#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AKShare 技能文档下载工具

下载指定类别的在线文档到本地
"""

import requests
from pathlib import Path
from typing import Optional, List

from config import DOCS_DIR, DOC_SOURCES
from utils import get_today_str, get_local_docs, get_latest_doc_date


def download_doc(category: str, url: str) -> Optional[Path]:
    """
    下载单个文档并保存到本地

    Args:
        category: 文档类别
        url: 文档 URL

    Returns:
        保存的文件路径，下载失败时返回 None
    """
    today = get_today_str()

    try:
        print(f"正在下载 {category} 文档：{url}")
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        content = response.text

        # 保存文件
        filename = f"{category}_{today}.md"
        filepath = DOCS_DIR / filename
        filepath.write_text(content, encoding="utf-8")

        print(f"✓ 已保存：{filepath}")
        return filepath

    except requests.RequestException as e:
        print(f"✗ 下载失败 {category}: {e}")
        return None


def delete_old_docs(category: str, keep_date: str) -> int:
    """
    删除某类别的旧文档，只保留指定日期的文档

    Args:
        category: 文档类别
        keep_date: 要保留的日期 (YYYYMMDD)

    Returns:
        删除的文档数量
    """
    docs = get_local_docs()
    deleted = 0

    if category not in docs:
        return deleted

    for doc in docs[category]:
        doc_date = doc.stem.rsplit("_", 1)[1]
        if doc_date != keep_date:
            try:
                doc.unlink()
                print(f"  已删除旧文档：{doc.name}")
                deleted += 1
            except Exception as e:
                print(f"  删除失败 {doc.name}: {e}")

    return deleted


def generate_indexes() -> List[Path]:
    """
    下载完成后生成接口索引 CSV

    Returns:
        生成的 CSV 文件路径列表
    """
    try:
        from index import generate_index
    except ImportError:
        print("⚠ 无法导入索引生成模块，跳过索引生成")
        return []

    csv_paths = []
    for category in ["stock"]:
        csv_path = generate_index(category)
        if csv_path:
            csv_paths.append(csv_path)

    return csv_paths


def check_and_update_docs(force: bool = False, cleanup: bool = True,
                          generate_index: bool = True) -> list:
    """
    检查并更新所有文档

    Args:
        force: 是否强制更新所有文档
        cleanup: 是否下载后清理旧文档
        generate_index: 是否生成接口索引 CSV

    Returns:
        已更新的文档路径列表
    """
    today = get_today_str()
    updated = []

    # 确保目录存在
    DOCS_DIR.mkdir(parents=True, exist_ok=True)

    for category, url in DOC_SOURCES.items():
        latest_date = get_latest_doc_date(category)

        if force or latest_date != today:
            filepath = download_doc(category, url)
            if filepath:
                updated.append(filepath)
                # 删除旧文档
                if cleanup:
                    deleted = delete_old_docs(category, today)
                    if deleted > 0:
                        print(f"  已清理 {deleted} 个旧文档")
        else:
            print(f"✓ {category} 文档已是最新 ({latest_date})")

    # 生成索引
    if generate_index and updated:
        print("\n生成接口索引...")
        csv_paths = generate_indexes()
        if csv_paths:
            print(f"已生成 {len(csv_paths)} 个索引文件:")
            for p in csv_paths:
                print(f"  - {p.name}")

    return updated


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="下载/更新 AKShare 文档")
    parser.add_argument("--force", "-f", action="store_true", help="强制更新所有文档")
    parser.add_argument("--no-cleanup", "-n", action="store_true", help="下载后不删除旧文档")

    args = parser.parse_args()

    print("检查并更新 AKShare 文档...")
    updated = check_and_update_docs(force=args.force, cleanup=not args.no_cleanup)
    if updated:
        print(f"\n已更新 {len(updated)} 个文档:")
        for p in updated:
            print(f"  - {p.name}")
    else:
        print("\n所有文档已是最新")
