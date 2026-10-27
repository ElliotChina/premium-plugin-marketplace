## 法律信息数据服务 (server_type="law")

- 面向司法案例与法律法规的检索、阅读，并辅以联网搜索/网页阅读补充现实背景（最新政策监管动态、官方公告、办事规则等）
- 案例检索 query 须传检索语句数组，一次调用建议提供 2-3 组围绕案件事实、法律关系、行为类型、争议焦点、责任承担构造的完整语句，保留用户问句中的关键事实与专有名词；引用时须核验案例内容与问题的相似度，不得将单个案例上升为普遍规则
- 案例详情优先用案号精确定位，案件名称仅作辅助；案号不完整时禁止自行补全
- 法条检索时须将口语化表达转化为法律专业术语，并对同义词、近义词进行列举；已知法规名与条文编号时用 `law_name` + `item` 精确检索；不确定法规标准名称时先检索确认，再凭返回的 `law_id` 阅读法规全文
- 简单法条查询不得调用 `law_content_visit` 阅读全文；不得编造、拼接案号或条文

| 工具名称 | 功能说明 | 典型参数 |
|---------|---------|---------|
| `case_search` | 司法案例检索，返回案号、案由、法院、裁判日期、案件概要、争议焦点、法院观点、裁判结果等摘要 | `{"query": ["检索语句1", "检索语句2"], "area": ["北京"], "time": ["近5年"], "size": 5}` |
| `case_browser` | 案例详情浏览，按案号或案件名称精确检索单个案例，返回裁判文书正文 | `{"case_number": "(2024)京01民初123号"}` 或 `{"case_name": "张三诉李四合同纠纷案"}` |
| `legal_article_search` | 法条综合检索（混合检索、语义检索、精确法条定位、法规名检索），返回法规名称、条文内容、效力层级、效力状态等 | `{"query": "合同解除 法定情形", "law_name": "中华人民共和国民法典", "item": "第五百六十三条", "status": "现行有效", "size": 5}` |
| `law_content_visit` | 阅读指定法规全文，按阅读目的提取、总结、比较制度规则 | `{"law_id": "legal_article_search返回的法规id", "goal": "提取违约责任相关规定", "max_length": 10000}` |
| `webpage_search` | 联网搜索，返回网页内容摘要，用于补充官方公告、最新政策、背景信息 | `{"query": "最高人民法院 关于某某的最新司法解释", "size": 10}` |
| `webpage_visit` | 网页阅读，按阅读目标返回指定URL网页内容摘要 | `{"url": "https://court.gov.cn/xxx", "goal": "核实发布时间与适用范围"}` |

### 脚本调用示例

```javascript
const { call } = require('./call-node.js');

async function main() {
    const result = await call("law", "case_search", {
        query: ["公司股东未按期出资的违约责任", "股东出资纠纷 股东会决议解除股东资格"],
        area: ["北京"],
        size: 5
    });
    console.log(JSON.stringify(result, null, 2));
}

main().catch(console.error);
```

```python
from call import call

result = call("law", "case_search", {
    "query": ["公司股东未按期出资的违约责任", "股东出资纠纷 股东会决议解除股东资格"],
    "area": ["北京"],
    "size": 5
})
print(result)
```

### 法律信息查询示例

```python
# 司法案例检索（query 为检索语句数组，建议2-3组）
call("law", "case_search", {
    "query": ["股权转让合同中约定分期付款未支付的解除条件", "股权转让纠纷 根本违约 解除合同"],
    "time": ["近5年"],
    "size": 5
})

# 按案号浏览案例详情，核验裁判观点
call("law", "case_browser", {"case_number": "(2024)京01民初123号"})

# 法条精确检索：已知法规名与条文编号
call("law", "legal_article_search", {
    "law_name": "中华人民共和国民法典",
    "item": "第五百六十三条"
})

# 法条语义检索：口语化问题转法律术语
call("law", "legal_article_search", {
    "query": "民间借贷 利率保护上限",
    "status": "现行有效",
    "size": 5
})

# 阅读法规全文（law_id 来自 legal_article_search 返回结果）
call("law", "law_content_visit", {
    "law_id": "<检索返回的法规id>",
    "goal": "提取违约责任相关的全部规定",
    "max_length": 10000
})

# 联网补充：最新监管动态与官方公告
call("law", "webpage_search", {"query": "最高人民法院 最新司法解释 发布", "size": 10})
call("law", "webpage_visit", {"url": "https://www.court.gov.cn/xxx", "goal": "核实发布时间与适用范围"})
```
