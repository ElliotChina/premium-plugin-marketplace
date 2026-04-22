#!/usr/bin/env python3
"""
AKShare 健壮的数据获取器

提供完整的错误处理、重试机制、数据验证等功能，
用于稳定可靠地获取财经数据。
"""

import akshare as ak
import time
import pandas as pd
from typing import Optional, Callable, List, Dict, Any
from datetime import datetime


class AKShareFetcher:
    """AKShare 数据获取器（带完整错误处理）"""

    def __init__(
        self,
        max_retries: int = 3,
        retry_delay: float = 1.0,
        backoff_factor: float = 2.0,
        verbose: bool = True
    ):
        """
        初始化获取器

        Args:
            max_retries: 最大重试次数
            retry_delay: 初始重试延迟（秒）
            backoff_factor: 退避因子，每次重试延迟乘以此因子
            verbose: 是否打印详细日志
        """
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.backoff_factor = backoff_factor
        self.verbose = verbose

    def fetch(
        self,
        interface_name: str,
        symbol: str = None,
        **kwargs
    ) -> Optional[pd.DataFrame]:
        """
        获取数据（带完整错误处理）

        Args:
            interface_name: 接口名称
            symbol: 股票代码（可选）
            **kwargs: 其他参数

        Returns:
            DataFrame 或 None（如果所有重试都失败）
        """
        # 1. 验证参数
        if symbol:
            symbol = self._validate_symbol(symbol)

        # 2. 构建调用函数
        func = lambda: getattr(ak, interface_name)(symbol=symbol, **kwargs) if symbol else getattr(ak, interface_name)(**kwargs)

        # 3. 带重试的调用
        df = self._fetch_with_retry(func, interface_name)

        # 4. 验证返回数据
        if df is not None:
            df = self._validate_data(df, interface_name)

        return df

    def fetch_multiple(
        self,
        interface_name: str,
        symbols: List[str],
        **kwargs
    ) -> Dict[str, Optional[pd.DataFrame]]:
        """
        批量获取多只股票数据

        Args:
            interface_name: 接口名称
            symbols: 股票代码列表
            **kwargs: 其他参数

        Returns:
            字典，key 为股票代码，value 为对应的 DataFrame
        """
        results = {}
        for i, symbol in enumerate(symbols, 1):
            if self.verbose:
                print(f"[{i}/{len(symbols)}] 获取 {symbol}...")

            df = self.fetch(interface_name, symbol=symbol, **kwargs)
            results[symbol] = df

            # 避免请求过快
            if i < len(symbols):
                time.sleep(0.5)

        return results

    def _validate_symbol(self, symbol: str) -> str:
        """验证股票代码"""
        symbol = str(symbol).strip()

        if not symbol.isdigit():
            if self.verbose:
                print(f"⚠️ 警告：股票代码包含非数字字符 '{symbol}'")

        if len(symbol) != 6 and len(symbol) != 5:
            if self.verbose:
                print(f"⚠️ 警告：股票代码长度异常 '{symbol}'（通常为 5 或 6 位）")

        return symbol

    def _fetch_with_retry(
        self,
        func: Callable,
        interface_name: str = "接口"
    ) -> Optional[pd.DataFrame]:
        """带重试的调用"""
        for attempt in range(self.max_retries):
            try:
                result = func()

                # 检查返回结果是否有效
                if result is None:
                    raise ValueError("接口返回 None")
                if hasattr(result, 'empty') and result.empty:
                    raise ValueError("接口返回空 DataFrame")

                if self.verbose and attempt > 0:
                    print(f"✓ {interface_name} 重试成功")

                return result

            except Exception as e:
                error_msg = str(e)
                is_last_attempt = attempt == self.max_retries - 1

                # 最后一次尝试失败
                if is_last_attempt:
                    if self.verbose:
                        print(f"❌ {interface_name} 失败（已重试 {self.max_retries} 次）：{error_msg}")
                    return None

                # 根据错误类型决定是否重试
                should_retry = any(keyword in error_msg for keyword in [
                    "网络", "timeout", "连接", "Connection", "Timeout",
                    "HTTP", "5", "502", "503", "504"
                ])

                if not should_retry:
                    # 参数错误等不需要重试
                    if self.verbose:
                        print(f"⚠️ {interface_name} 参数错误，不重试：{error_msg}")
                    return None

                # 计算退避延迟
                current_delay = self.retry_delay * (self.backoff_factor ** attempt)
                if self.verbose:
                    print(f"⚠️ {interface_name} 网络错误，{current_delay:.1f}秒后重试 ({attempt+1}/{self.max_retries})...")
                time.sleep(current_delay)

        return None

    def _validate_data(self, df: pd.DataFrame, interface_name: str) -> pd.DataFrame:
        """验证返回数据"""
        # 检查空值比例
        null_ratio = df.isnull().sum() / len(df)
        high_null_cols = null_ratio[null_ratio > 0.5]

        if not high_null_cols.empty and self.verbose:
            print(f"⚠️ {interface_name} 以下列空值比例超过 50%：")
            for col, ratio in high_null_cols.items():
                print(f"  - {col}: {ratio:.1%}")

        return df


# 便捷函数
def fetch_with_retry(
    interface_name: str,
    symbol: str = None,
    max_retries: int = 3,
    **kwargs
) -> Optional[pd.DataFrame]:
    """
    便捷函数：带重试的单次获取

    Args:
        interface_name: 接口名称
        symbol: 股票代码（可选）
        max_retries: 最大重试次数
        **kwargs: 其他参数

    Returns:
        DataFrame 或 None

    Example:
        >>> df = fetch_with_retry("stock_zh_a_hist", symbol="000001")
        >>> df = fetch_with_retry("stock_sse_summary")  # 无参数接口
    """
    fetcher = AKShareFetcher(max_retries=max_retries, verbose=False)
    return fetcher.fetch(interface_name, symbol=symbol, **kwargs)


def safe_get_column(df: pd.DataFrame, keywords: List[str]) -> pd.Series:
    """
    根据关键词查找列名（避免接口返回结构变化导致的 KeyError）

    Args:
        df: DataFrame
        keywords: 关键词列表

    Returns:
        对应的列

    Example:
        >>> close_price = safe_get_column(df, ['收', '盘'])  # 查找包含"收"和"盘"的列
    """
    for col in df.columns:
        if all(kw in col for kw in keywords):
            return df[col]

    available_cols = ", ".join(df.columns.tolist())
    raise KeyError(
        f"找不到包含关键词 {keywords} 的列。"
        f"可用列：{available_cols}"
    )


if __name__ == "__main__":
    # 示例用法
    print("=== AKShare 健壮获取器示例 ===\n")

    # 示例 1：基础调用
    print("1. 基础调用：获取平安银行历史行情")
    df = fetch_with_retry(
        "stock_zh_a_hist",
        symbol="000001",
        period="daily",
        start_date="20240101",
        end_date="20241231"
    )

    if df is not None:
        print(f"✓ 成功获取 {len(df)} 条记录")
        print(f"  列名：{df.columns.tolist()}\n")
    else:
        print("✗ 获取失败\n")

    # 示例 2：批量获取
    print("2. 批量获取：获取多只股票信息")
    fetcher = AKShareFetcher(verbose=True)
    results = fetcher.fetch_multiple(
        "stock_individual_info_em",
        symbols=["000001", "000002", "600000"]
    )

    for symbol, data in results.items():
        if data is not None:
            print(f"✓ {symbol}: 获取成功")
        else:
            print(f"✗ {symbol}: 获取失败")

    print("\n示例完成！")
