---
name: akshare
description: AKShare 财经数据技能。提供 A 股、港股、美股的历史行情、实时报价、财务报表、股东持仓、资金流向等数据查询和分析能力。**当用户需要查询股票数据、分析公司财务、监控股东变化、获取市场指标、导出金融数据到Excel/CSV，或使用"行情"、"K线"、"财报"、"市盈率"、"龙虎榜"等术语时，立即激活此技能**——即使用户只说"查下平安银行"、"帮我分析这只股票"或"找找腾讯的财务数据"等模糊表达。
compatibility: "required_tools: Bash; dependencies: akshare, pandas"
---

<!-- @format -->

# AKShare 财经数据完整指南

> AKShare 是一个基于 Python 的财经数据接口库，提供 A 股、港股、美股等市场数据。本文档从入门到精通，指导您高效使用 AKShare。

---

## 目录

- [1. 环境准备](#1-环境准备)
  - [1.1 环境安装](#11-环境安装)
  - [1.2 接口文档下载](#12-接口文档下载)
- [2. 接口检索](#2-接口检索)
  - [2.1 常用接口清单](#21-常用接口清单)
  - [2.2 接口搜索方法](#22-接口搜索方法)
- [3. 参数说明](#3-参数说明)
- [4. 调用技巧](#4-调用技巧)
- [5. 错误处理](#5-错误处理)
- [6. 调试技巧](#6-调试技巧)
- [7. 场景案例](#7-场景案例)

---

# 1. 快速开始

## 安装 AKShare

```bash
pip install akshare --upgrade
```

**提示**：使用国内镜像可加速：`-i https://pypi.tuna.tsinghua.edu.cn/simple`

## 下载接口文档

```bash
cd akshare
python scripts/download.py
```

✅ 完成！现在可以使用 `import akshare as ak` 获取数据了。

---

# 2. 接口检索

## 三种检索方法

| 方法 | 适用场景 | 操作 |
|------|----------|------|
| **常用清单** | 90%日常需求，快速查找接口 | 查看 [常用接口清单-A股](references/常用接口清单-A股.md) / [常用接口清单-港股](references/常用接口清单-港股.md) / [常用接口清单-美股](references/常用接口清单-美股.md) |
| **搜索索引** | 常用清单中找不到 | 在 [akshare_stock_api_index.csv](references/akshare_stock_api_index.csv) 中搜索关键词 |
| **详细文档** | 需要完整参数说明 | `python scripts/get_api_doc.py <接口名>` |

## 快速搜索示例

```python
import pandas as pd

# 搜索接口索引
index_df = pd.read_csv("references/akshare_stock_api_index.csv")
results = index_df[index_df['description'].str.contains('股东', case=False, na=False)]
print(results[['api_name', 'description', 'source']])
```

---

# 3. 参数说明

## 各平台参数格式速查表

| 平台 | 股票代码 | 市场前缀 | 日期参数 | 复权参数 |
|------|----------|----------|----------|----------|
| **东方财富** | 6位数字 | 否 | start_date, end_date | adjust |
| **雪球** | 6位数字 | **是（SH/SZ）** | - | - |
| **同花顺** | 6位数字 | 否 | - | - |
| **新浪** | 6位数字 | **是（sh/sz小写）** | start_date, end_date | adjust |
| **巨潮资讯** | 6位数字 | 否 | - | - |

**详细说明**：[各平台参数格式说明.md](references/各平台参数格式说明.md)

## 核心参数要点

- **股票代码**：东方财富/同花顺/巨潮用纯数字，雪球用 SH/SZ 前缀，新浪用 sh/sz 前缀
- **日期格式**：标准格式 YYYYMMDD（如 "20240101"）
- **复权类型（东方财富）**："" 不复权，"qfq" 前复权（推荐），"hfq" 后复权

---

# 4. 调用技巧

## 使用健壮获取器（推荐）

生产环境建议使用内置的 `robust_fetcher.py`，提供完整的错误处理、重试机制和数据验证功能。

### 快速使用

```python
# 导入获取器
import sys
sys.path.append("scripts")
from robust_fetcher import fetch_with_retry, AKShareFetcher

# 单次获取（自动重试 3 次）
df = fetch_with_retry("stock_zh_a_hist", symbol="000001", period="daily")

# 批量获取多只股票
fetcher = AKShareFetcher(verbose=True)
results = fetcher.fetch_multiple(
    "stock_individual_info_em",
    symbols=["000001", "000002", "600000"]
)
```

**脚本位置**：`scripts/robust_fetcher.py`

**功能**：✅ 自动重试  ✅ 错误处理  ✅ 数据验证  ✅ 批量获取

---

## 高效调用技巧

| 技巧 | 说明 | 示例 |
|------|------|------|
| **优先使用主要接口** | 从常用清单选择，参数简单、数据稳定 | 东方财富接口 |
| **减少数据请求量** | 指定日期范围，避免一次性请求过多数据 | `start_date="20240101", end_date="20241231"` |
| **使用适当周期** | 周/月线减少数据量 | `period="weekly"` |
| **批量处理** | 一次获取多只股票，减少调用开销 | 循环调用多个股票 |
| **使用缓存** | 缓存不变数据（如公司基本信息） | `@lru_cache` |

---

## 最佳实践

1. ✅ **生产环境**：使用 `robust_fetcher.py` 确保稳定性
2. ✅ **定期更新**：每周更新接口文档（`python scripts/download.py`）
3. ✅ **错误排查**：先查参数格式，再查接口文档
4. ✅ **数据源优先级**：优先使用 P0/P1/P2 优先级的数据源

---

# 5. 错误处理

> 💡 **推荐使用健壮的获取器**：生产环境建议使用 `scripts/robust_fetcher.py`，它提供了完整的错误处理、重试机制和数据验证功能。详见[使用健壮的获取器](#使用健壮的获取器)章节。

## 常见错误及解决方案

| 错误类型          | 原因                     | 解决方案                   |
| ----------------- | ------------------------ | -------------------------- |
| `EmptyDataError`  | 股票停牌、退市或代码错误 | 检查股票代码，扩大日期范围 |
| `TimeoutError`    | 网络不稳定或数据量大     | 使用重试机制，减少数据量   |
| `KeyError`        | 接口返回结构变化         | 更新文档，使用关键词匹配   |
| `ConnectionError` | IP 被封或网络断开        | 切换数据源，添加延时       |
| `ValueError`      | 参数格式错误             | 查看接口文档确认参数格式   |
| `ProxyError`      | 网络代理配置错误         | 寻找并使用备选接口 |

---

# 6. 调试技巧

## 常见问题快速解决

| 问题 | 可能原因 | 快速解决 |
|------|----------|----------|
| **返回空数据** | 股票代码错误、停牌、日期范围内无交易 | 1. 检查股票代码格式<br>2. 扩大日期范围<br>3. 查看 [常用接口清单-A股.md](references/常用接口清单-A股.md) |
| **参数错误** | 参数格式不正确、缺少必需参数 | `python scripts/get_api_doc.py <接口名>` 查看正确参数 |
| **网络超时** | 网络不稳定、数据量大 | 使用 `robust_fetcher.py` 自动重试 |
| **数据异常** | 数据源变更、接口返回结构变化 | 1. 对比多个数据源<br>2. 更新接口文档<br>3. 使用 `safe_get_column()` 函数 |
| **KeyError** | 列名变化、访问不存在的字段 | 检查 `df.columns`，使用关键词匹配 |

## 基础调试命令

```python
# 查看数据结构
df.shape          # 数据维度
df.columns        # 列名
df.dtypes         # 数据类型
df.head()         # 前5行
df.info()         # 完整信息

# 检查数据质量
df.isnull().sum()           # 空值统计
df.describe()               # 数据统计
df.duplicated().sum()       # 重复行数量
```

## 调试最佳实践

1. ✅ **先查文档**：遇到问题先查看接口文档和参数格式说明
2. ✅ **使用 robust_fetcher**：生产环境自动处理网络错误和重试
3. ✅ **验证数据**：获取数据后检查空值、异常值和数据完整性
4. ✅ **对比验证**：关键数据对比多个数据源确保准确性

---

# 7. 场景案例

完整的场景案例和代码示例请查看：
📖 [使用场景案例](references/使用场景案例说明.md) - 股票投资价值分析、两只股票对比、股东变化监控、财务数据分析等典型场景

---

# 附录

## 快速命令参考

```bash
# 安装/升级 AKShare
pip install akshare --upgrade

# 下载接口文档
python scripts/download.py

# 查看接口文档
python scripts/get_api_doc.py <接口名>

# 检查版本
python -c "import akshare as ak; print(ak.__version__)"
```

## 数据源优先级

| 优先级 | 数据源                   | 说明                      | 接口数 |
| ------ | ------------------------ | ------------------------- | ------ |
| **P0** | 上交所/深交所/北交所     | 官方数据，最权威          | 1+     |
| **P1** | 东方财富                 | 接口最多（54%），覆盖全面，但是不稳定 | 199    |
| **P2** | 新浪财经/同花顺/巨潮资讯 | 稳定可靠                  | 88     |
| **P3** | 雪球/百度/腾讯           | 社区数据                  | 20     |
| **P4** | 其他来源                 | 补充数据源                | 27     |

## 工具脚本和参考文档

### 🔧 工具脚本（可执行程序）

| 脚本 | 何时使用 | 功能说明 |
|------|----------|----------|
| `scripts/robust_fetcher.py` | **生产环境**、需要稳定数据获取 | 提供**完整的错误处理、重试机制、数据验证**，覆盖90%的错误场景 |
| `scripts/download.py` | **首次使用**、**定期更新**接口文档 | 从 AKShare 官方下载最新接口文档和索引 |
| `scripts/get_api_doc.py` | 需要查看**特定接口**的详细文档 | 查看单个接口的完整参数、返回字段、示例代码 |
| `scripts/index.py` | 接口索引损坏或需要重新生成 | 根据 stock 文档重新生成 akshare_stock_api_index.csv |

### 📖 参考文档（按需查阅）

| 文档 | 何时使用 | 内容说明 |
|------|----------|----------|
| [常用接口清单-A股.md](references/常用接口清单-A股.md) | **90%的日常需求**、快速查找接口 | 按功能分类的常用接口列表（基础信息、行情、财务、股东等） |
| [常用接口清单-港股.md](references/常用接口清单-港股.md) | 查询港股数据 | 港股专用接口列表 |
| [常用接口清单-美股.md](references/常用接口清单-美股.md) | 查询美股数据 | 美股专用接口列表 |
| [各平台参数格式说明.md](references/各平台参数格式说明.md) | **参数格式不确定**、不同平台差异 | 各平台（东方财富、雪球、同花顺等）的详细参数格式和注意事项 |
| [使用场景案例说明.md](references/使用场景案例说明.md) | **需要完整示例**、学习最佳实践 | 股票分析、对比、股东监控、财务分析等典型场景的完整代码示例 |
| [akshare_stock_api_index.csv](references/akshare_stock_api_index.csv) | 常用清单中找不到、**搜索接口** | 可搜索的完整接口索引（支持关键词搜索） |
| [stock_*.md](references/stock_*.md) | 需要查看**所有接口**的完整文档 | AKShare 官方完整接口文档（数据量大，谨慎使用） |

### 💡 使用建议

**快速路径（推荐）**：
1. 先查 `常用接口清单-A股.md` 找到接口
2. 不确定参数格式时查 `各平台参数格式说明.md`
3. 代码中使用 `scripts/robust_fetcher.py` 确保稳定性

**完整路径**：
1. 常用清单找不到 → 搜索 `akshare_stock_api_index.csv`
2. 还找不到 → 运行 `python scripts/get_api_doc.py <接口名>`
