#!/usr/bin/env python3
"""
按数据类型采集数据

支持采集指定类型的所有接口数据，并保存为 CSV 文件。

用法:
    # 采集单个类型
    python collect_by_type.py --type 基础信息 --symbol 000001

    # 采集多个类型
    python collect_by_type.py --type 基础信息 历史行情 --symbol 000001

    # 采集所有类型
    python collect_by_type.py --all --symbol 000001

    # 指定输出目录
    python collect_by_type.py --type 基础信息 --symbol 000001 --output ./data
"""

import argparse
import sys
from datetime import datetime

# 导入数据采集器
from data_collector import DataCollector, load_data_config


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description="按数据类型采集 AKShare 数据",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        "--type", "-t",
        nargs="+",
        help="要采集的数据类型（可多个）。可选值：基础信息、公司主营、历史行情、同行比较、市场热度、个股估值、新闻研报、业绩快报、资产负债表、利润表、现金流量表、财务指标、股东户数、十大股东、持股变动、分红配送"
    )

    parser.add_argument(
        "--all", "-a",
        action="store_true",
        help="采集所有类型的数据"
    )

    parser.add_argument(
        "--symbol", "-s",
        help="股票代码（如：000001）"
    )

    parser.add_argument(
        "--output", "-o",
        default="./data",
        help="输出目录（默认：./data）"
    )

    parser.add_argument(
        "--date",
        help="指定日期（格式：YYYYMMDD），用于某些需要日期参数的接口"
    )

    parser.add_argument(
        "--period", "-p",
        help="数据周期（用于历史行情等接口）"
    )

    parser.add_argument(
        "--start-date",
        help="开始日期（格式：YYYYMMDD）"
    )

    parser.add_argument(
        "--end-date",
        help="结束日期（格式：YYYYMMDD）"
    )

    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="静默模式，减少输出"
    )

    return parser.parse_args()


def validate_types(args, config):
    """验证用户指定的数据类型"""
    if args.all:
        return list(config.keys())

    if not args.type:
        print("错误：必须指定 --type 或 --all")
        print("\n可用的数据类型：")
        for data_type in config.keys():
            print(f"  - {data_type}")
        sys.exit(1)

    # 检查类型是否有效
    invalid_types = set(args.type) - set(config.keys())
    if invalid_types:
        print(f"错误：无效的数据类型：{', '.join(invalid_types)}")
        print(f"\n可用的数据类型：")
        for data_type in sorted(config.keys()):
            print(f"  - {data_type}")
        sys.exit(1)

    return args.type


def main():
    """主函数"""
    # 解析参数
    args = parse_args()

    # 加载配置
    config = load_data_config()

    # 验证数据类型
    types_to_collect = validate_types(args, config)

    # 创建采集器
    collector = DataCollector(
        output_dir=args.output,
        verbose=not args.quiet
    )

    # 构建通用参数
    common_kwargs = {}

    if args.date:
        common_kwargs["date"] = args.date

    if args.period:
        common_kwargs["period"] = args.period

    if args.start_date:
        common_kwargs["start_date"] = args.start_date

    if args.end_date:
        common_kwargs["end_date"] = args.end_date

    # 打印开始信息
    if not args.quiet:
        print("="*70)
        print("AKShare 数据采集工具")
        print("="*70)
        print(f"开始时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"股票代码：{args.symbol or '无需'}")
        print(f"数据类型：{', '.join(types_to_collect)}")
        print(f"输出目录：{args.output}")
        print("="*70)
        print()

    # 采集数据
    try:
        all_results = {}

        for data_type in types_to_collect:
            results = collector.collect_by_type(
                data_type=data_type,
                interfaces=config[data_type],
                symbol=args.symbol,
                **common_kwargs
            )
            all_results[data_type] = results

        # 打印结束信息
        if not args.quiet:
            print("="*70)
            print(f"结束时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("="*70)

            # 打印详细结果
            print("\n详细结果：")
            for data_type, results in all_results.items():
                print(f"\n【{data_type}】")
                for interface, filepath in results.items():
                    if filepath:
                        print(f"  ✓ {interface}")
                    else:
                        print(f"  ✗ {interface}")

        return 0

    except KeyboardInterrupt:
        if not args.quiet:
            print("\n\n⚠️ 用户中断采集")
        return 1

    except Exception as e:
        if not args.quiet:
            print(f"\n❌ 采集过程出错：{e}")
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
