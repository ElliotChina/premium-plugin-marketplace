# 数据采集脚本使用说明

本目录包含用于采集 AKShare 股票数据的脚本，支持按数据类型批量采集并保存为 CSV 文件。

## 文件说明

### 核心文件

- `data_collector.py` - 数据采集器基础类，提供统一的采集接口
- `collect_by_type.py` - 按数据类型采集的通用脚本
- `collect_fundamental.py` - 全量数据采集脚本（16种类型，56个接口）
- `robust_fetcher.py` - 健壮的数据获取器（带重试、错误处理）

## 快速开始

### 1. 安装依赖

```bash
pip install akshare pandas
```

### 2. 基本用法

#### 方式一：全量采集所有数据（推荐）

```bash
# 采集所有16种数据类型（56个接口）
python collect_fundamental.py --symbol 000001
```

#### 方式二：排除特定类型

```bash
# 排除某些类型（如不需要市场热度、新闻研报）
python collect_fundamental.py --symbol 000001 --exclude 市场热度 新闻研报
```

#### 方式三：只采集特定类型

```bash
# 只采集指定的几种类型
python collect_fundamental.py --symbol 000001 --include-only 基础信息 财务指标 历史行情
```

#### 方式四：使用通用脚本

```bash
# 采集单个类型
python collect_by_type.py --type 基础信息 --symbol 000001

# 采集多个类型
python collect_by_type.py --type 基础信息 历史行情 --symbol 000001

# 采集所有类型
python collect_by_type.py --all --symbol 000001
```

### 3. 命令行参数

#### collect_fundamental.py 参数（全量采集脚本）

| 参数 | 简写 | 说明 | 示例 |
|------|------|------|------|
| `--symbol` | `-s` | 股票代码（必填） | `--symbol 000001` |
| `--exclude` | - | 排除的数据类型（可多个） | `--exclude 市场热度 新闻研报` |
| `--include-only` | - | 只采集指定的类型（可多个） | `--include-only 基础信息 财务指标` |
| `--output` | `-o` | 输出目录（默认：./data） | `--output ./mydata` |
| `--start-date` | - | 历史行情开始日期 | `--start-date 20240101` |
| `--end-date` | - | 历史行情结束日期 | `--end-date 20241231` |
| `--quiet` | `-q` | 静默模式 | `--quiet` |

#### collect_by_type.py 参数（通用采集脚本）

| 参数 | 简写 | 说明 | 示例 |
|------|------|------|------|
| `--type` | `-t` | 指定数据类型（可多个） | `--type 基础信息 历史行情` |
| `--all` | `-a` | 采集所有类型 | `--all` |
| `--symbol` | `-s` | 股票代码 | `--symbol 000001` |
| `--output` | `-o` | 输出目录（默认：./data） | `--output ./mydata` |
| `--date` | - | 指定日期（格式：YYYYMMDD） | `--date 20240101` |
| `--period` | `-p` | 数据周期（默认：daily） | `--period daily` |
| `--start-date` | - | 开始日期 | `--start-date 20240101` |
| `--end-date` | - | 结束日期 | `--end-date 20241231` |
| `--quiet` | `-q` | 静默模式 | `--quiet` |

## 支持的数据类型

### 1. 基础信息
- 公司概况、简介等基本信息

### 2. 公司主营
- 主营业务、机构调研等

### 3. 历史行情
- 日K线、历史价格数据

### 4. 同行比较
- 成长性、估值、杜邦分析、规模对比

### 5. 市场热度
- 机构参与度、用户关注、市场参与意愿

### 6. 个股估值
- 估值分析数据

### 7. 新闻研报
- 研究报告、新闻资讯

### 8. 业绩快报
- 业绩报表、快报、预告

### 9. 资产负债表
- 资产负债表数据（多数据源）

### 10. 利润表
- 利润表数据（多数据源）

### 11. 现金流量表
- 现金流量表数据（多数据源）

### 12. 财务指标
- 关键财务指标（多数据源）

### 13. 股东户数
- 股东户数及持股集中度

### 14. 十大股东
- 十大股东、十大流通股东

### 15. 持股变动
- 高管持股变动、股东持股变动

### 16. 分红配送
- 分红、送股、转增等

## 输出文件命名规则

采集的数据将保存为 CSV 文件，命名格式：

```
[数据类型]_[数据来源]_[接口名称].csv
```

示例：
```
基础信息_巨潮资讯_stock_profile_cninfo.csv
历史行情_东方财富_stock_zh_a_hist.csv
财务指标_同花顺_stock_financial_abstract_new_ths.csv
```

## 高级用法

### 使用 Python 代码

```python
from data_collector import DataCollector, load_data_config

# 创建采集器
collector = DataCollector(output_dir="./data")

# 加载配置
config = load_data_config()

# 采集特定类型
results = collector.collect_by_type(
    data_type="基础信息",
    interfaces=config["基础信息"],
    symbol="000001"
)

# 采集所有类型
all_results = collector.collect_all(
    data_config=config,
    symbol="000001"
)
```

### 自定义配置

如果需要自定义接口配置，可以创建自己的配置文件：

```python
custom_config = {
    "我的数据": [
        {"name": "stock_zh_a_hist", "source": "东方财富", "description": "历史行情"},
        {"name": "stock_individual_info_em", "source": "东方财富", "description": "股票信息"}
    ]
}

collector = DataCollector(output_dir="./data")
results = collector.collect_by_type(
    data_type="我的数据",
    interfaces=custom_config["我的数据"],
    symbol="000001"
)
```

## 错误处理

脚本内置了完整的错误处理机制：

1. **自动重试**：网络错误自动重试（最多3次）
2. **指数退避**：重试延迟逐步增加（1秒 → 2秒 → 4秒）
3. **数据验证**：检查返回数据是否为空或空值比例过高
4. **参数验证**：验证股票代码格式

## 注意事项

1. **股票代码格式**：A股代码为6位数字（如000001、600000）
2. **日期格式**：使用 YYYYMMDD 格式（如20240101）
3. **网络限制**：部分接口可能有频率限制，建议控制请求速度
4. **数据时效**：部分数据可能有延迟，建议获取最新数据
5. **权限要求**：部分接口可能需要登录或特殊权限

## 常见问题

### Q: 为什么某些接口采集失败？
A: 可能原因：
- 网络连接问题
- 股票代码不存在或格式错误
- 接口暂时不可用
- 需要特殊权限或参数

脚本会自动重试，并在失败时记录错误信息。

### Q: 如何查看采集统计？
A: 脚本执行完成后会显示统计信息：
```
====================================================================
采集统计
====================================================================
✓ 成功：45 个
✗ 失败：2 个
⊘ 跳过：3 个
====================================================================
```

### Q: 如何批量采集多只股票？
A: 可以在代码中使用循环或调用 `fetch_multiple` 方法：

```python
from data_collector import DataCollector, load_data_config

collector = DataCollector(output_dir="./data")
config = load_data_config()

symbols = ["000001", "000002", "600000"]

for symbol in symbols:
    print(f"\n正在采集：{symbol}")
    results = collector.collect_by_type(
        data_type="基础信息",
        interfaces=config["基础信息"],
        symbol=symbol
    )
```

## 更新日志

### 2025-03-18
- 初始版本
- 支持16种数据类型采集
- 完整的错误处理和重试机制
- 自动保存为 CSV 文件
