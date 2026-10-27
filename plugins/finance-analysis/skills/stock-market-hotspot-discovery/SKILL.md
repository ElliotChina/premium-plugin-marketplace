---
name: stock-market-hotspot-discovery
description: 面向A股市场热点发现的综合能力。适用于用户提出“今日热点是什么”“当前热股有哪些”等泛化问题时，返回结构化的Markdown热点报告。覆盖热点资讯、热门股票等维度。触发核心条件：用户关注市场层面的热门方向或事件热度，而非单一标的的深度诊断或指标计算。
version: 1.2.1
category: investment-finance
author: 东方财富
license: proprietary
agent_created: true
---

# 股市热点发现

通过**自然语言问句**识别当前市场热点，返回 Markdown 热点报告，适用场景包括：
- **今日市场热点总览（资讯/事件/话题）**
- **热门股票与活跃方向识别**
- **交易日内快速捕捉情绪变化与关注焦点**


## 功能范围

### 基础热点能力
- 输入自然语言问句，调用热点发现接口生成结构化结论
- 覆盖热门资讯、热门股票等市场级热点信息
- 返回可读 Markdown 报告（优先提取 `data.displayData`）
- 支持将结果保存为本地 `.md` 文件，便于盘后复盘

### 触发规则（何时使用本技能）
- 用户问题是**市场层面的热点发现**：如“今日热点”“热股有哪些”
- 用户未指定单只股票/基金做深度诊断，也未要求具体指标计算
- 用户关注“热门、热搜、大事、活跃赛道、关注方向”等泛化主题

### 不触发规则（何时不要使用本技能）
- 用户明确询问单只股票深度分析（应走 stock-diagnosis）
- 用户明确询问单只基金深度分析（应走 fund-diagnosis）
- 用户要求具体指标计算或量化建模（MACD、回测、组合优化等）

### 触发示例

| 触发（热点发现） | 不触发（诊断/指标） |
|---|---|
| 今日热点是什么？ | 海康威视怎么样？ |
| 今天最热的股票有哪些？ | 丹化科技的MACD金叉了吗？ |
| 最近流行哪些投资赛道？ | 帮我建一个基金组合优化模型 |


## 授权与依赖

本 Skill 依赖 `EM_API_KEY`。授权检查已内联到 `scripts/get_data.py`，**直接执行热点查询，不要先单独运行 `auth.py ensure`**，也不要把授权作为另一轮前置工具调用。凭据按 `EM_API_KEY` 环境变量、`~/.mx-skills/em_api_key` 文件的顺序读取，不再使用内置兜底 key。

### 退出码与授权输出

| 退出码 | 含义 | 处理方式 |
|---|---|---|
| `0` | 查询成功 | 读取 Markdown 正文及可选 `Saved:` 路径 |
| `10` | 需要用户授权 | 展示二维码并停止本轮调用 |
| `2` | 网络或业务错误 | 返回明确失败原因，不编造热点报告 |
| `1` | 缺少 query/stdin | 补充有效问句后再调用 |

需要授权时，stdout 输出带标签文本：

```text
need_auth: true
authUrl: https://...
apiKeyUrl: https://...
```


授权、凭据持久化及 401 失效处理必须遵循 [授权协议](references/auth_protocol.md)。安装依赖时运行 `pip3 install -r requirements.txt`。


## 快速开始

### 1. 命令行调用

```bash
python3 scripts/get_data.py --query "今日热点"
```

**输出示例**
```text
Saved: /path/to/workspace/stock_market_hotspot_discovery/stock_market_hotspot_discovery_90bf169c.md
source_trace_path: /path/to/workspace/miaoxiang/sourceTrace_3df2b7d9.json
（随后输出 Markdown 热点内容）
```

**参数说明：**

| 参数 | 说明 | 必填 |
|---|---|---|
| `--query` | 用户原始自然语言问句 | ✅（`--query` 或 stdin 二选一） |
| `--no-save` | 不保存 Markdown 报告；溯源 JSON 仍按接口返回保存 | 否 |

### 2. 代码调用

```python
import asyncio
from pathlib import Path
from scripts.get_data import discover_hotspot

async def main():
    result = await discover_hotspot(
        question="今日热点",
        output_dir=Path("workspace/stock_market_hotspot_discovery"),
        save_to_file=True,
    )
    if "error" in result:
        print(result["error"])
    else:
        print(result["content"])
        if result.get("output_path"):
            print("已保存至:", result["output_path"])
        if result.get("source_trace_path"):
            print("溯源JSON:", result["source_trace_path"])

asyncio.run(main())
```

## 输出规范
通过脚本或工具拿到诊股结果后，**对用户的可见回复必须以接口返回的 Markdown 正文为主体**，避免模型二次转述。仅当接口/脚本明确返回 `error`、或正文为空时，才用简短文字说明失败原因；**禁止**在失败时杜撰报告内容。

接口 `data.sourceTraceList` 会原样保存到当前工作目录下 `miaoxiang/sourceTrace_<articleId>.json`；接口未返回 `articleId` 时使用随机 ID 兜底。脚本返回字段和命令行成功输出统一使用 `source_trace_path`。

## 常见问题

**为什么有时候不会保存 md 文件？**  
→ 当返回为不支持场景或失败结构（如 `code/status` 异常、`data` 为空）时，脚本会只输出内容而不落盘。

**如何只看输出，不落盘？**
```bash
python3 -m scripts.get_data --query "今日热点" --no-save
```

## 合规说明

- 热点信息具有时效性，结果反映接口调用时刻的市场状态。
- 热点信息仅供参考，不构成投资建议，输出时应附风险提示。
- 禁止在代码或提示词中硬编码账号 ID、会话 ID 或 token。
- 接口失败时不得编造结论，应返回明确错误或不确定性说明。

## 用户可见回复中的文件地址

文件仍按原流程保存，内部可使用脚本返回的路径读取、校验和处理。最终答复不得展示任何本地文件地址或目录，包括绝对/相对路径、`Saved:`、`output_path`、`files.*`、`attachments[].path`、`source_trace_path`，也不得把路径放入 Markdown 链接、图片链接或代码块
