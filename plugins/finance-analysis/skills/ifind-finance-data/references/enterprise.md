## 工商企业数据服务 (server_type="enterprise")

- 工商企业数据采用 `先搜后查` 两步逻辑：先通过 `kuaicha_tool_discover` 传入简短中文能力描述检索匹配的数据接口，再依据返回的 `tool_id` 及参数结构，通过 `kuaicha_tool_call` 发起实际数据查询
- 数据覆盖：工商信息（基本信息、股东股权、对外投资、实际控制人、最终受益人、变更记录、年报）、经营与司法风险（经营异常、行政处罚、欠税、股权质押、破产重整、被执行人、失信、限制高消费、裁判文书）、知识产权（商标、专利、软件著作权）、经营动态（融资历史、招聘、招投标中标、客户供应商）、上市公司（十大股东、财务报表、董监高）、新闻公告舆情、企业筛选（按地区、行业、产业链、资质如高新技术企业/专精特新、注册资本规模批量筛选企业名单）
- `kuaicha_tool_discover` 的 query 须传简短中文能力描述（如 `企业股东信息`、`被执行人查询`、`产业链企业筛选`），禁止传用户原句、企业名称或参数对象
- 查具体企业时若仅有简称/品牌名，须先调用 `tool_id=basic_get_enterprise_associate`（参数 `{"query": "简称"}`）模糊搜索归一，从结果中取 orgid 或 creditcode 后再查详情；企业标识优先级：orgid > creditcode > 登记全称
- 同一会话中已成功调用的 tool_id 可直接复用，无需重复 discover
- 返回空结果或调用失败时须如实告知用户，严禁编造数据；向用户呈现结果时，末尾标注：数据来源于同花顺旗下快查企业数据引擎

| 工具名称 | 功能说明 | 典型参数 |
|---------|---------|---------|
| `kuaicha_tool_discover` | 接口发现：按中文能力描述检索匹配的数据查询接口，返回候选接口的 `tool_id`、参数结构等信息 | `{"query": "企业股东信息"}` |
| `kuaicha_tool_call` | 查询执行：基于 discover 返回的 `tool_id` 及参数结构发起实际数据查询 | `{"tool_id": "discover返回的接口标识", "params_to_tool": "{\"orgid\": \"企业orgid\"}"}` |

### 脚本调用示例

```javascript
const { call } = require('./call-node.js');

async function main() {
    // 第一步：接口发现，获取候选 tool_id 与参数结构
    const found = await call("enterprise", "kuaicha_tool_discover", {
        query: "企业股东信息"
    });
    console.log(JSON.stringify(found, null, 2));

    // 第二步：依据返回的 tool_id 与参数结构发起查询
    const result = await call("enterprise", "kuaicha_tool_call", {
        tool_id: "<discover返回的tool_id>",
        params_to_tool: "{\"orgid\": \"<企业orgid>\"}"
    });
    console.log(JSON.stringify(result, null, 2));
}

main().catch(console.error);
```

```python
from call import call

# 第一步：接口发现，获取候选 tool_id 与参数结构
found = call("enterprise", "kuaicha_tool_discover", {"query": "企业股东信息"})
print(found)

# 第二步：依据返回的 tool_id 与参数结构发起查询
result = call("enterprise", "kuaicha_tool_call", {
    "tool_id": "<discover返回的tool_id>",
    "params_to_tool": "{\"orgid\": \"<企业orgid>\"}"
})
print(result)
```

### 工商企业查询示例

```python
# 简称模糊归一：仅有企业简称/品牌名时，先获取 orgid 或 creditcode 再查详情
call("enterprise", "kuaicha_tool_call", {
    "tool_id": "basic_get_enterprise_associate",
    "params_to_tool": "{\"query\": \"茅台\"}"
})

# 接口发现示例
call("enterprise", "kuaicha_tool_discover", {"query": "被执行人查询"})
call("enterprise", "kuaicha_tool_discover", {"query": "产业链企业筛选"})

# 接口执行示例（tool_id 与 params_to_tool 均以 discover 返回为准）
call("enterprise", "kuaicha_tool_call", {
    "tool_id": "<discover返回的tool_id>",
    "params_to_tool": "{\"orgid\": \"<企业orgid>\"}"
})
```
