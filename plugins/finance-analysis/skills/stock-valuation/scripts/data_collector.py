#!/usr/bin/env python3
"""
数据采集基础类

提供统一的数据采集接口，支持批量采集、错误处理、数据保存等功能。
"""

import sys
import pandas as pd
from pathlib import Path
from typing import Optional, Dict, List, Any

# 添加 references 目录到路径，以便导入 robust_fetcher
script_dir = Path(__file__).parent
references_dir = script_dir.parent.parent / "akshare" / "scripts"
sys.path.insert(0, str(references_dir))

from robust_fetcher import AKShareFetcher


class DataCollector(AKShareFetcher):
    """
    数据采集器（带完整错误处理和数据保存功能）

    扩展自 AKShareFetcher，增加数据保存、批量采集等功能。
    """

    # 接口参数配置：定义每个接口需要的参数
    INTERFACE_PARAMS = {
        # 不支持 symbol 参数的接口
        "no_symbol": [
            # 业绩快报类 - 这些接口不需要 symbol 参数
            "stock_yjbb_em",
            "stock_yjkb_em",
            "stock_yjyg_em",
        ],
        # 需要市场前缀的 symbol (sh/sz 前缀)
        "market_prefix_symbol": [
            "stock_zh_a_daily",      # 新浪财经 - 需要 sh000001 格式
            "stock_zh_a_hist_tx",    # 腾讯证券 - 需要 sz000001 格式
        ],
        # 需要市场后缀的 symbol (000001.SZ 格式)
        "market_suffix_symbol": [
            "stock_financial_analysis_indicator_em",  # 需要 000001.SZ 格式
        ],
        # 需要特定参数的接口
        "special_params": {
            # 历史行情接口 - 需要 adjust 参数
            "stock_zh_a_hist": {"adjust": "qfq"},  # 默认前复权
            "stock_zh_a_daily": {"adjust": "qfq"},
            "stock_zh_a_hist_tx": {"adjust": "qfq"},

            # 财务指标接口 - 需要特定参数
            "stock_financial_analysis_indicator": {"start_year": "1900"},
            "stock_financial_analysis_indicator_em": {"indicator": "按报告期"},
        },
        # 参数别名映射（将通用参数映射到接口特定参数）
        "param_aliases": {
            # 某些接口可能需要不同的参数名
        }
    }

    def __init__(
        self,
        output_dir: str = "./data",
        max_retries: int = 3,
        retry_delay: float = 1.0,
        backoff_factor: float = 2.0,
        verbose: bool = True
    ):
        """
        初始化数据采集器

        Args:
            output_dir: 数据保存目录
            max_retries: 最大重试次数
            retry_delay: 初始重试延迟（秒）
            backoff_factor: 退避因子
            verbose: 是否打印详细日志
        """
        super().__init__(max_retries, retry_delay, backoff_factor, verbose)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # 采集结果统计
        self.stats = {
            "success": 0,
            "failed": 0,
            "skipped": 0
        }

    def save_to_csv(
        self,
        df: pd.DataFrame,
        data_type: str,
        source: str,
        interface_name: str
    ) -> Optional[str]:
        """
        保存数据为 CSV 文件

        Args:
            df: 要保存的数据
            data_type: 数据类型
            source: 数据来源
            interface_name: 接口名称

        Returns:
            保存的文件路径，如果保存失败则返回 None
        """
        if df is None or df.empty:
            if self.verbose:
                print(f"⚠️ 数据为空，跳过保存：{data_type}_{source}_{interface_name}")
            self.stats["skipped"] += 1
            return None

        # 构建文件名
        filename = f"{data_type}_{source}_{interface_name}.csv"
        filepath = self.output_dir / filename

        try:
            # 保存为 CSV
            df.to_csv(filepath, index=False, encoding="utf-8-sig")

            if self.verbose:
                print(f"✓ 已保存：{filepath} ({len(df)} 条记录)")

            self.stats["success"] += 1
            return str(filepath)

        except Exception as e:
            if self.verbose:
                print(f"❌ 保存失败：{filepath}")
                print(f"   错误：{e}")

            self.stats["failed"] += 1
            return None

    def _add_market_suffix(self, symbol: str, interface_name: str) -> str:
        """
        为股票代码添加市场后缀

        Args:
            symbol: 股票代码（如 000001）
            interface_name: 接口名称

        Returns:
            带后缀的股票代码（如 000001.SZ, 000001.SH）
        """
        if not symbol:
            return symbol

        # 如果已经带有后缀，直接返回
        if '.' in symbol:
            return symbol

        # 移除可能存在的前缀
        clean_symbol = symbol
        if symbol.startswith(('sh', 'sz', 'bj')):
            clean_symbol = symbol[2:]

        # 根据股票代码首位数字判断市场
        first_digit = clean_symbol[0]

        if first_digit in ['0', '2', '3']:
            # 深交所
            return f"{clean_symbol}.SZ"
        elif first_digit in ['6', '7']:
            # 上交所
            return f"{clean_symbol}.SH"
        elif first_digit in ['8', '4']:
            # 北交所
            return f"{clean_symbol}.BJ"
        else:
            # 默认按深交所处理
            return f"{clean_symbol}.SZ"

    def _add_market_prefix(self, symbol: str, interface_name: str) -> str:
        """
        为股票代码添加市场前缀

        Args:
            symbol: 股票代码（如 000001）
            interface_name: 接口名称

        Returns:
            带前缀的股票代码（如 sh000001, sz000001）
        """
        if not symbol:
            return symbol

        # 如果已经带有前缀，直接返回
        if symbol.startswith(('sh', 'sz', 'bj')):
            return symbol

        # 根据股票代码首位数字判断市场
        first_digit = symbol[0]

        if first_digit in ['0', '2', '3']:
            # 深交所：000xxx, 002xxx, 300xxx, 301xxx
            return f"sz{symbol}"
        elif first_digit in ['6', '7']:
            # 上交所：600xxx, 601xxx, 603xxx, 605xxx, 688xxx
            return f"sh{symbol}"
        elif first_digit in ['8', '4']:
            # 北交所：8xxxxx, 43xxxx
            return f"bj{symbol}"
        else:
            # 默认按深交所处理
            return f"sz{symbol}"

    def _build_interface_params(
        self,
        interface_name: str,
        symbol: str = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        为接口构建正确的参数

        Args:
            interface_name: 接口名称
            symbol: 股票代码
            **kwargs: 其他参数

        Returns:
            参数字典
        """
        params = {}

        # 1. 处理 symbol 参数（根据接口需求）
        if interface_name not in self.INTERFACE_PARAMS["no_symbol"]:
            if symbol:
                # 检查是否需要添加市场前缀
                if interface_name in self.INTERFACE_PARAMS["market_prefix_symbol"]:
                    symbol = self._add_market_prefix(symbol, interface_name)
                # 检查是否需要添加市场后缀
                elif interface_name in self.INTERFACE_PARAMS["market_suffix_symbol"]:
                    symbol = self._add_market_suffix(symbol, interface_name)

                params["symbol"] = symbol

        # 2. 添加接口特定的必需参数
        if interface_name in self.INTERFACE_PARAMS["special_params"]:
            special_params = self.INTERFACE_PARAMS["special_params"][interface_name]
            params.update(special_params)

        # 3. 处理历史行情类接口的日期参数
        # 如果用户提供了 date 但没有 start_date/end_date，进行转换
        if "date" in kwargs and "start_date" not in kwargs:
            # 对于历史行情接口，将 date 转换为 start_date 和 end_date
            if interface_name in ["stock_zh_a_daily", "stock_zh_a_hist_tx", "stock_zh_a_hist"]:
                date_value = kwargs["date"]
                # 假设查询当天数据
                params["start_date"] = date_value
                params["end_date"] = date_value

        # 4. 添加通用参数（period, start_date, end_date 等）
        # 只添加非 None 的参数
        for key, value in kwargs.items():
            if value is not None and key not in ["date"]:  # date 已在上面处理
                params[key] = value

        return params

    def collect_by_type(
        self,
        data_type: str,
        interfaces: List[Dict[str, Any]],
        symbol: str = None,
        **kwargs
    ) -> Dict[str, Optional[str]]:
        """
        按数据类型采集所有接口数据

        Args:
            data_type: 数据类型
            interfaces: 接口列表，每个接口包含 name、source、description
            symbol: 股票代码（可选）
            **kwargs: 其他参数

        Returns:
            字典，key 为接口名称，value 为保存的文件路径
        """
        if self.verbose:
            print(f"\n{'='*60}")
            print(f"开始采集：{data_type}")
            print(f"{'='*60}")

        results = {}

        for interface in interfaces:
            interface_name = interface["name"]
            source = interface["source"]
            description = interface.get("description", "")

            if self.verbose:
                print(f"\n▶ {interface_name} ({source})")
                if description:
                    print(f"  {description}")

            # 构建接口参数
            interface_params = self._build_interface_params(
                interface_name, symbol, **kwargs
            )

            # 获取数据（使用定制参数）
            df = self._fetch_with_params(interface_name, interface_params)

            # 保存数据
            filepath = self.save_to_csv(df, data_type, source, interface_name)
            results[interface_name] = filepath

        return results

    def _fetch_with_params(
        self,
        interface_name: str,
        params: Dict[str, Any]
    ) -> Optional[pd.DataFrame]:
        """
        使用指定参数获取数据

        Args:
            interface_name: 接口名称
            params: 参数字典

        Returns:
            DataFrame 或 None
        """
        import akshare as ak

        # 构建调用函数
        func = lambda: getattr(ak, interface_name)(**params)

        # 带重试的调用
        df = self._fetch_with_retry(func, interface_name)

        # 验证返回数据
        if df is not None:
            df = self._validate_data(df, interface_name)

        return df

    def collect_all(
        self,
        data_config: Dict[str, List[Dict[str, Any]]],
        symbol: str = None,
        **kwargs
    ) -> Dict[str, Dict[str, Optional[str]]]:
        """
        采集所有类型的数据

        Args:
            data_config: 数据配置，格式为 {数据类型: [接口列表]}
            symbol: 股票代码（可选）
            **kwargs: 其他参数

        Returns:
            字典，key 为数据类型，value 为该类型下各接口的采集结果
        """
        all_results = {}

        for data_type, interfaces in data_config.items():
            results = self.collect_by_type(data_type, interfaces, symbol, **kwargs)
            all_results[data_type] = results

        # 打印统计信息
        self._print_summary()

        return all_results

    def _print_summary(self):
        """打印采集统计摘要"""
        if self.verbose:
            print(f"\n{'='*60}")
            print("采集统计")
            print(f"{'='*60}")
            print(f"✓ 成功：{self.stats['success']} 个")
            print(f"✗ 失败：{self.stats['failed']} 个")
            print(f"⊘ 跳过：{self.stats['skipped']} 个")
            print(f"{'='*60}\n")


def load_data_config(config_file: str = None) -> Dict[str, List[Dict[str, Any]]]:
    """
    加载数据采集配置

    Args:
        config_file: 配置文件路径（可选）

    Returns:
        数据配置字典
    """
    # 默认配置（从 SKILL.md 提取）
    default_config = {
        "基础信息": [
            {"name": "stock_profile_cninfo", "source": "巨潮资讯", "description": "巨潮资讯-个股-公司概况"},
            {"name": "stock_individual_basic_info_xq", "source": "雪球", "description": "雪球财经-个股-公司概况-公司简介"},
            {"name": "stock_individual_info_em", "source": "东方财富", "description": "东方财富-个股-股票信息"},
        ],
        "公司主营": [
            {"name": "stock_zyjs_ths", "source": "同花顺", "description": "同花顺-机构调研详细"},
            {"name": "stock_zygc_em", "source": "东方财富", "description": "东方财富-机构调研详细"},
        ],
        "历史行情": [
            {"name": "stock_zh_a_hist", "source": "东方财富", "description": "东方财富-沪深京A股日频率数据"},
            {"name": "stock_zh_a_daily", "source": "新浪财经", "description": "新浪财经-沪深京A股数据"},
            {"name": "stock_zh_a_hist_tx", "source": "腾讯证券", "description": "腾讯证券-日频股票历史数据"},
        ],
        "同行比较": [
            {"name": "stock_zh_growth_comparison_em", "source": "东方财富", "description": "东方财富-同行比较-成长性比较"},
            {"name": "stock_zh_valuation_comparison_em", "source": "东方财富", "description": "东方财富-同行比较-估值比较"},
            {"name": "stock_zh_dupont_comparison_em", "source": "东方财富", "description": "东方财富-同行比较-杜邦分析比较"},
            {"name": "stock_zh_scale_comparison_em", "source": "东方财富", "description": "东方财富-同行比较-公司规模"},
        ],
        "市场热度": [
            {"name": "stock_comment_detail_zlkp_jgcyd_em", "source": "东方财富", "description": "东方财富-千股千评-机构参与度"},
            {"name": "stock_comment_detail_scrd_focus_em", "source": "东方财富", "description": "东方财富-千股千评-用户关注指数"},
            {"name": "stock_comment_detail_scrd_desire_em", "source": "东方财富", "description": "东方财富-千股千评-市场参与意愿"},
        ],
        "个股估值": [
            {"name": "stock_value_em", "source": "东方财富", "description": "东方财富-估值分析-每日互动"},
        ],
        "新闻研报": [
            {"name": "stock_research_report_em", "source": "东方财富", "description": "东方财富-数据中心-研究报告-个股研报"},
            {"name": "stock_news_em", "source": "东方财富", "description": "东方财富-沪深港通持股-个股详情"},
        ],
        "业绩快报": [
            {"name": "stock_yjbb_em", "source": "东方财富", "description": "东方财富-年报季报-业绩报表"},
            {"name": "stock_yjkb_em", "source": "东方财富", "description": "东方财富-年报季报-业绩快报"},
            {"name": "stock_yjyg_em", "source": "东方财富", "description": "东方财富-年报季报-业绩预告"},
        ],
        "资产负债表": [
            {"name": "stock_zcfz_em", "source": "东方财富", "description": "东方财富-年报季报-资产负债表"},
            {"name": "stock_zcfz_bj_em", "source": "东方财富", "description": "东方财富-年报季报-资产负债表(北交所)"},
            {"name": "stock_financial_debt_new_ths", "source": "同花顺", "description": "同花顺-财务指标-资产负债表"},
            {"name": "stock_balance_sheet_by_report_em", "source": "东方财富", "description": "东方财富-财务分析-资产负债表-按报告期"},
            {"name": "stock_balance_sheet_by_yearly_em", "source": "东方财富", "description": "东方财富-财务分析-资产负债表-按年度"},
            {"name": "stock_financial_report_sina", "source": "新浪财经", "description": "新浪财经-财务报表-三大报表"},
        ],
        "利润表": [
            {"name": "stock_lrb_em", "source": "东方财富", "description": "东方财富-年报季报-利润表"},
            {"name": "stock_financial_benefit_new_ths", "source": "同花顺", "description": "同花顺-财务指标-利润表"},
            {"name": "stock_profit_sheet_by_report_em", "source": "东方财富", "description": "东方财富-财务分析-利润表-按报告期"},
            {"name": "stock_profit_sheet_by_yearly_em", "source": "东方财富", "description": "东方财富-财务分析-利润表-按年度"},
            {"name": "stock_financial_report_sina", "source": "新浪财经", "description": "新浪财经-财务报表-三大报表"},
        ],
        "现金流量表": [
            {"name": "stock_xjll_em", "source": "东方财富", "description": "东方财富-年报季报-现金流量表"},
            {"name": "stock_financial_cash_new_ths", "source": "同花顺", "description": "同花顺-财务指标-现金流量表"},
            {"name": "stock_cash_flow_sheet_by_report_em", "source": "东方财富", "description": "东方财富-财务分析-现金流量表-按报告期"},
            {"name": "stock_cash_flow_sheet_by_yearly_em", "source": "东方财富", "description": "东方财富-财务分析-现金流量表-按年度"},
            {"name": "stock_financial_report_sina", "source": "新浪财经", "description": "新浪财经-财务报表-三大报表"},
        ],
        "财务指标": [
            {"name": "stock_financial_abstract_new_ths", "source": "同花顺", "description": "同花顺-财务指标-重要指标"},
            {"name": "stock_financial_abstract", "source": "新浪财经", "description": "新浪财经-财务报表-关键指标"},
            {"name": "stock_financial_analysis_indicator_em", "source": "东方财富", "description": "东方财富-A股-财务分析-主要指标"},
            {"name": "stock_financial_analysis_indicator", "source": "新浪财经", "description": "新浪财经-财务分析-主要指标"},
        ],
        "股东户数": [
            {"name": "stock_zh_a_gdhs_detail_em", "source": "东方财富", "description": "东方财富-股东户数详情"},
            {"name": "stock_hold_num_cninfo", "source": "巨潮资讯", "description": "巨潮资讯-股东人数及持股集中度"},
        ],
        "十大股东": [
            {"name": "stock_gdfx_free_top_10_em", "source": "东方财富", "description": "东方财富-十大流通股东"},
            {"name": "stock_gdfx_top_10_em", "source": "东方财富", "description": "东方财富-十大股东"},
            {"name": "stock_circulate_stock_holder", "source": "新浪财经", "description": "新浪财经-流通股东"},
        ],
        "持股变动": [
            {"name": "stock_management_change_ths", "source": "同花顺", "description": "同花顺-高管持股变动"},
            {"name": "stock_shareholder_change_ths", "source": "同花顺", "description": "同花顺-股东持股变动"},
            {"name": "stock_hold_management_person_em", "source": "东方财富", "description": "东方财富-高管持股变动明细"},
            {"name": "stock_share_hold_change_sse", "source": "上交所", "description": "上交所-董监高人员股份变动"},
            {"name": "stock_share_hold_change_szse", "source": "深交所", "description": "深交所-董监高人员股份变动"},
            {"name": "stock_share_hold_change_bse", "source": "北交所", "description": "北交所-董监高及相关人员持股变动"},
        ],
        "分红配送": [
            {"name": "stock_dividend_cninfo", "source": "巨潮资讯", "description": "巨潮资讯-历史分红"},
            {"name": "stock_fhps_detail_em", "source": "东方财富", "description": "东方财富-分红送配详情"},
            {"name": "stock_fhps_detail_ths", "source": "同花顺", "description": "同花顺-分红情况"},
            {"name": "stock_history_dividend_detail", "source": "新浪财经", "description": "新浪财经-分红配股"},
        ],
    }

    return default_config


if __name__ == "__main__":
    # 示例用法
    print("=== 数据采集器示例 ===\n")

    # 创建采集器
    collector = DataCollector(output_dir="./test_data")

    # 加载配置
    config = load_data_config()

    # 只采集"基础信息"类型作为示例
    if "基础信息" in config:
        results = collector.collect_by_type(
            data_type="基础信息",
            interfaces=config["基础信息"],
            symbol="000001"  # 平安银行
        )

        print("\n采集结果：")
        for interface, filepath in results.items():
            if filepath:
                print(f"✓ {interface}: {filepath}")
            else:
                print(f"✗ {interface}: 失败")
