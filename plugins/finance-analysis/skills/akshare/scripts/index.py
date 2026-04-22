#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AKShare 技能文档索引生成器

从下载的文档中解析接口信息，生成 CSV 索引文件
"""

import csv
import re
from pathlib import Path
from typing import Optional

from config import DOCS_DIR
from utils import get_latest_doc_path


def parse_table_params(lines: list[str], start_idx: int) -> list[dict]:
    """
    解析 markdown 表格形式的参数

    Args:
        lines: 文档所有行
        start_idx: 表格开始行索引（"输入参数"或"输出参数"标题行）

    Returns:
        参数列表，每个元素包含 {name, type, description}
    """
    params = []

    # 从 start_idx 之后开始查找表格
    i = start_idx + 1
    while i < len(lines):
        line = lines[i].strip()

        # 跳过空行
        if not line:
            i += 1
            continue

        # 检查是否是表格分隔行（|---|---|）
        if re.match(r'^\|[-\s|]+\|$', line):
            i += 1
            continue

        # 检查是否是表格数据行
        if line.startswith('|') and '|' in line[1:]:
            # 解析表格行
            cells = [cell.strip() for cell in line.split('|')]
            # 移除首尾空单元格
            if cells and cells[0] == '':
                cells = cells[1:]
            if cells and cells[-1] == '':
                cells = cells[:-1]

            # 需要至少 3 列：名称、类型、描述
            if len(cells) >= 3:
                # 跳过表头行（包含"名称"的行）
                if cells[0] != '名称':
                    params.append({
                        "name": cells[0],
                        "type": cells[1],
                        "description": cells[2]
                    })
            i += 1
        else:
            # 遇到非表格行，结束解析
            break

    return params


def parse_api_from_md(filepath: Path) -> list[dict]:
    """
    从 markdown 文档中解析接口信息

    Args:
        filepath: 文档路径

    Returns:
        接口信息列表，每个元素包含：
        - api_name: 接口名称
        - description: 接口描述
        - input_params: 输入参数列表（JSON 字符串）
        - output_params: 输出参数列表（JSON 字符串）
        - begin_line_number: 接口开始行号（1-based）
        - end_line_number: 接口结束行号（1-based）
        - line_count: 接口所占总行数
        - source: 数据来源
        - return_type: 返回值类型（DataFrame/Dictionary）
        - query_type: 查询类型（单个查询/批量查询）
    """
    content = filepath.read_text(encoding="utf-8")
    lines = content.split("\n")
    apis = []

    # 匹配接口定义块
    # 格式：接口：xxx 或 接口:xxx
    pattern = r'接口\s*:\s*(\S+)'

    # 先收集所有接口的位置
    api_positions = []
    for i, line in enumerate(lines):
        match = re.search(pattern, line)
        if match:
            api_name = match.group(1).strip()
            # 跳过无效的接口名
            if not api_name or api_name in ["示例", "输入", "输出"]:
                continue
            api_positions.append((i, api_name))

    # 处理每个接口
    for idx, (i, api_name) in enumerate(api_positions):
        # 查找描述（在当前行之后 5 行内查找）
        description = ""
        for j in range(i + 1, min(i + 6, len(lines))):
            desc_line = lines[j]
            if desc_line.startswith("描述"):
                # 提取描述内容
                desc_match = re.search(r'描述\s*:\s*(.+)', desc_line)
                if desc_match:
                    description = desc_match.group(1).strip()
                break

        # 解析输入参数
        input_params = []
        for j in range(i, min(i + 20, len(lines))):
            if lines[j].strip().startswith("输入参数"):
                input_params = parse_table_params(lines, j)
                break

        # 解析输出参数
        output_params = []
        for j in range(i, min(i + 30, len(lines))):
            line_stripped = lines[j].strip()
            # 输出参数行可能有后缀，如"输出参数 - 实时行情数据"
            if line_stripped.startswith("输出参数"):
                output_params = parse_table_params(lines, j)
                break

        # 计算结束行号
        # 如果有下一个接口，结束行号是下一个接口的前一行
        # 如果是最后一个接口，结束行号是文件最后一行
        if idx < len(api_positions) - 1:
            end_line_number = api_positions[idx + 1][0] - 1  # 下一个接口的前一行（0-based）
        else:
            end_line_number = len(lines)  # 文件总行数

        # 计算接口所占的总行数（从开始行到结束行）
        total_lines = end_line_number - i  # 0-based 计算

        # 提取数据来源
        source = extract_source(description)

        # 解析返回值类型
        return_type = parse_example_code(lines, i)

        # 解析查询类型
        query_type = parse_query_type(input_params)

        apis.append({
            "api_name": api_name,
            "description": description,
            "input_params": str(input_params),
            "output_params": str(output_params),
            "begin_line_number": i + 1,  # 转换为 1-based 行号
            "end_line_number": end_line_number + 1,  # 转换为 1-based 行号
            "line_count": total_lines,  # 接口所占总行数
            "source": source,
            "return_type": return_type,
            "query_type": query_type,
        })

    return apis


def parse_example_code(lines: list[str], start_idx: int) -> str:
    """
    解析接口示例代码，获取返回值类型

    Args:
        lines: 文档所有行
        start_idx: 接口开始行索引

    Returns:
        返回值类型：'DataFrame' 或 'Dictionary'
    """
    in_example = False
    # 扩大搜索范围到 100 行
    for j in range(start_idx, min(start_idx + 100, len(lines))):
        line = lines[j].strip()
        if '接口示例' in line:
            in_example = True
            continue
        if in_example:
            # 检查是否是代码行（在 ```python 块内）
            if line.startswith('```'):
                if 'python' in line:
                    continue
                else:
                    # 遇到结束标记，继续查找下一个示例块
                    if 'data' in line.lower() or '数据' in line:
                        in_example = False
                    continue
            # 查找变量赋值
            if '=' in line and 'ak.' in line:
                # 提取等号左边的变量名
                match = re.search(r'(\w+)\s*=\s*ak\.', line)
                if match:
                    var_name = match.group(1)
                    if var_name.endswith('_df'):
                        return 'DataFrame'
                    elif var_name.endswith('_dict'):
                        return 'Dictionary'
                    else:
                        # 默认根据常见模式判断
                        return 'DataFrame'  # 大多数接口返回 DataFrame

    return 'DataFrame'  # 默认返回 DataFrame（大多数接口都返回 DataFrame）


def parse_query_type(input_params: list[dict]) -> str:
    """
    根据输入参数判断查询类型

    Args:
        input_params: 输入参数列表

    Returns:
        查询类型：'单个查询' 或 '批量查询'
    """
    if not input_params:
        return '批量查询'  # 无参数通常是总体数据

    # 检查是否有 symbol 参数
    symbol_params = ['symbol', 'code', 'stock_code', 'security_code']

    for param in input_params:
        name = param.get('name', '').lower()
        # 检查是否有 symbol 类参数
        if any(sp in name for sp in symbol_params):
            return '单个查询'

    return '批量查询'


def extract_source(description: str) -> str:
    """
    从接口描述中提取数据来源

    Args:
        description: 接口描述

    Returns:
        数据来源名称
    """
    if not description:
        return "未知"

    # 按优先级匹配数据源关键词
    source_keywords = [
        ("上海证券交易所", "上交所"),
        ("深圳证券交易所", "深交所"),
        ("北京证券交易所", "北交所"),
        ("东方财富", "东方财富"),
        ("新浪财经", "新浪"),
        ("腾讯财经", "腾讯"),
        ("同花顺", "同花顺"),
        ("雪球", "雪球"),
        ("巨潮资讯", "巨潮"),
        ("百度股市通", "百度"),
        ("乐咕乐股", "乐咕乐股"),
        ("亿牛网", "亿牛网"),
        ("经济通", "经济通"),
        ("富途牛牛", "富途"),
        ("财新网", "财新"),
        ("美港电讯", "美港"),
        ("互动易", "互动易"),
        ("上证 e 互动", "上证 e 互动"),
        ("申万宏源", "申万宏源"),
    ]

    for source, keyword in source_keywords:
        if keyword in description:
            return source

    # 检查是否有其他来源提示
    if "数据" in description or "行情" in description:
        return "其他"

    return "未知"


def generate_index(category: str = "stock") -> Optional[Path]:
    """
    生成某类别的接口索引 CSV 文件

    Args:
        category: 文档类别

    Returns:
        生成的 CSV 文件路径
    """
    doc_path = get_latest_doc_path(category)
    if not doc_path:
        print(f"✗ 未找到 {category} 类别的文档")
        return None

    print(f"正在解析 {category} 文档：{doc_path.name}")

    # 解析接口
    apis = parse_api_from_md(doc_path)
    print(f"  找到 {len(apis)} 个接口")

    # 生成 CSV 文件名
    csv_path = DOCS_DIR / f"akshare_{category}_api_index.csv"
    # 写入 CSV
    with open(csv_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["api_name", "description", "input_params", "output_params", "begin_line_number", "end_line_number", "line_count", "source", "return_type", "query_type"])
        writer.writeheader()
        writer.writerows(apis)

    print(f"✓ 已生成索引：{csv_path}")
    return csv_path


def generate_all_indexes() -> list:
    """
    生成所有类别的接口索引

    Returns:
        生成的 CSV 文件路径列表
    """
    csv_paths = []

    for category in ["stock"]:  # 当前只处理 stock，后续可扩展
        csv_path = generate_index(category)
        if csv_path:
            csv_paths.append(csv_path)

    return csv_paths


if __name__ == "__main__":
    print("生成 AKShare 接口索引...")
    csv_paths = generate_all_indexes()
    if csv_paths:
        print(f"\n已生成 {len(csv_paths)} 个索引文件:")
        for p in csv_paths:
            print(f"  - {p.name}")
