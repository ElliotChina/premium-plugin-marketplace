#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AKShare 接口文档查看工具

使用方法:
    python scripts/get_api_doc.py stock_zh_a_hist
    python scripts/get_api_doc.py stock_individual_info_em --output doc.md
"""

import argparse
import sys
from pathlib import Path

# 添加 scripts 目录到路径
scripts_dir = Path(__file__).parent
sys.path.insert(0, str(scripts_dir))

from utils import extract_api_doc


def main():
    parser = argparse.ArgumentParser(
        description='查看 AKShare 接口的完整文档描述',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s stock_zh_a_hist                    # 直接打印到终端
  %(prog)s stock_individual_info_em -o doc.md # 保存到文件
  %(prog)s stock_yjbb_em --category stock     # 指定文档类别
        """
    )

    parser.add_argument(
        'api_name',
        help='接口名称（如 stock_zh_a_hist）'
    )

    parser.add_argument(
        '-c', '--category',
        default='stock',
        help='文档类别（默认: stock）'
    )

    parser.add_argument(
        '-o', '--output',
        help='输出文件路径（可选，默认打印到终端）'
    )

    args = parser.parse_args()

    # 提取接口文档
    doc = extract_api_doc(args.api_name, args.category)

    if doc is None:
        print(f"❌ 错误: 未找到接口 '{args.api_name}' 的文档")
        print(f"   请检查接口名称是否正确，或使用 search_api.py 搜索相关接口")
        sys.exit(1)

    # 输出文档
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(doc, encoding='utf-8')
        print(f"✓ 接口文档已保存至: {output_path}")
        print(f"  接口名称: {args.api_name}")
        print(f"  文档长度: {len(doc.split(chr(10)))} 行")
    else:
        print(doc)
        print(f"\n--- 文档结束（共 {len(doc.split(chr(10)))} 行）---")


if __name__ == '__main__':
    main()
