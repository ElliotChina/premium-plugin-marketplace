#!/usr/bin/env python3
"""
快捷脚本：采集所有支持的数据类型

包括全部16种数据类型和56个接口：
- 基础信息 (3个接口)
- 公司主营 (2个接口)
- 历史行情 (3个接口)
- 同行比较 (4个接口)
- 市场热度 (3个接口)
- 个股估值 (1个接口)
- 新闻研报 (2个接口)
- 业绩快报 (3个接口)
- 资产负债表 (6个接口)
- 利润表 (5个接口)
- 现金流量表 (5个接口)
- 财务指标 (4个接口)
- 股东户数 (2个接口)
- 十大股东 (3个接口)
- 持股变动 (6个接口)
- 分红配送 (4个接口)

用法:
    python collect_fundamental.py --symbol 000001
    python collect_fundamental.py --symbol 000001 --output ./data
    python collect_fundamental.py --symbol 000001 --exclude 市场热度 新闻研报
"""

import argparse
import sys
from datetime import datetime

from data_collector import DataCollector, load_data_config


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description="快捷脚本：采集所有支持的数据类型（16种类型，56个接口）",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        "--symbol", "-s",
        required=True,
        help="股票代码（如：000001）"
    )

    parser.add_argument(
        "--output", "-o",
        default="./data",
        help="输出目录（默认：./data）"
    )

    parser.add_argument(
        "--exclude",
        nargs="+",
        help="排除的数据类型（可多个），如：--exclude 市场热度 新闻研报"
    )

    parser.add_argument(
        "--include-only",
        nargs="+",
        help="只采集指定的数据类型（可多个），如：--include-only 基础信息 财务指标"
    )

    parser.add_argument(
        "--start-date",
        help="历史行情开始日期（格式：YYYYMMDD）"
    )

    parser.add_argument(
        "--end-date",
        help="历史行情结束日期（格式：YYYYMMDD）"
    )

    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="静默模式，减少输出"
    )

    return parser.parse_args()


def main():
    """主函数"""
    args = parse_args()

    # 加载配置
    config = load_data_config()

    # 定义所有支持的数据类型（16种）
    all_types = [
        "基础信息",
        "公司主营",
        "历史行情",
        "同行比较",
        "市场热度",
        "个股估值",
        "新闻研报",
        "业绩快报",
        "资产负债表",
        "利润表",
        "现金流量表",
        "财务指标",
        "股东户数",
        "十大股东",
        "持股变动",
        "分红配送",
    ]

    # 根据 --include-only 或 --exclude 参数过滤类型
    if args.include_only:
        # 只采集指定的类型
        types_to_collect = [t for t in args.include_only if t in config]
        invalid_types = set(args.include_only) - set(types_to_collect)
        if invalid_types and not args.quiet:
            print(f"⚠️ 警告：无效的数据类型：{', '.join(invalid_types)}")
    elif args.exclude:
        # 排除指定的类型
        types_to_collect = [t for t in all_types if t not in args.exclude]
        invalid_types = set(args.exclude) - set(all_types)
        if invalid_types and not args.quiet:
            print(f"⚠️ 警告：无效的数据类型：{', '.join(invalid_types)}")
    else:
        # 采集所有类型
        types_to_collect = all_types

    # 创建采集器
    collector = DataCollector(
        output_dir=args.output,
        verbose=not args.quiet
    )

    # 构建通用参数
    common_kwargs = {}
    if args.start_date:
        common_kwargs["start_date"] = args.start_date
    if args.end_date:
        common_kwargs["end_date"] = args.end_date

    # 打印开始信息
    if not args.quiet:
        print("="*70)
        print("AKShare 全量数据采集工具")
        print("="*70)
        print(f"股票代码：{args.symbol}")
        print(f"数据类型：{len(types_to_collect)}/16")
        print(f"  包含：{', '.join(types_to_collect)}")
        print(f"输出目录：{args.output}")
        print(f"开始时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*70)
        print()

    # 采集数据
    try:
        all_results = {}

        for data_type in types_to_collect:
            if data_type not in config:
                if not args.quiet:
                    print(f"⚠️ 警告：数据类型 '{data_type}' 不在配置中，跳过")
                continue

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

            # 统计总体情况
            total_interfaces = sum(len(results) for results in all_results.values())
            success_interfaces = sum(
                sum(1 for fp in results.values() if fp)
                for results in all_results.values()
            )

            print(f"\n总体统计：")
            print(f"  数据类型：{len(all_results)}/{len(types_to_collect)}")
            print(f"  接口总数：{success_interfaces}/{total_interfaces}")

            # 打印详细结果
            print(f"\n详细结果：")
            for data_type, results in all_results.items():
                print(f"\n【{data_type}】")
                success_count = sum(1 for fp in results.values() if fp)
                total_count = len(results)
                print(f"  成功率：{success_count}/{total_count}")

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
