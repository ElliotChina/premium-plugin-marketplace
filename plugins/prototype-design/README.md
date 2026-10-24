# prototype-design

原型设计技能插件：在真实前端项目中构建**可执行、可点击、页面互通**的镜像原型——生产零耦合、晋升不删除，原型随代码库永久归档。

## 技能

### prototype-app

可执行镜像原型技能：在项目 `prototypes/` 目录中按生产页面路径一一对应地构建可点击原型。页面间跳转走真实路由，跨页状态用原型私有内存 store，单页可按需挂多方案翻选（`1–N` 数字键 / `←`/`→` / `R` 重放，`?v=N` URL 持久）。

核心规则：

- **物理隔离 + 零代码耦合**：全部原型代码集中在顶层 `prototypes/` 目录，不 import 生产代码、生产不 import 原型代码；token 值仅作参考复制
- **dev-only 挂载**：生产构建零泄漏（Next.js 路由组 + 404 守卫 / React Router `import.meta.env.DEV` 注册）
- **镜像约定（文件级一一对应）**：`/prototype/dashboard` ↔ `app/dashboard`；路径 = 生产源码根前缀换算（`src/X` → `prototypes/X`），同名、同导出风格，一个原型文件对一个生产文件，禁止 `Proto` 前缀与发明名；每个镜像文件头注释声明对应物，`scripts/mirror-check.py` 机械校验
- **变体命名**：单页多方案默认活在镜像页文件内；需独立文件时用后缀命名（`Login.variant-b.tsx`），头注释注明基准文件与发散轴
- **档案生命周期**：晋升真实代码后原型保留归档，随功能分支提交，无独立原型分支；删除需明确要求
- **两种起点**：从现有生产页面生成（直接镜像其目录组织），或 0→1 新建（路径指向未来路由、结构套用最相近生产页模板、晋升时定锚）

附 LOGIC.md 分支：单文件状态机推演 HTML（自由操作按钮 + 引导式场景），可交给非开发者验证业务逻辑；翻选器逐字规格见 PICKER.md。

### prototype（源自 [emilkowalski/skills](https://github.com/emilkowalski/skills)，MIT）

即抛式 UI 发散对比技能：把一个 UI 件做成 3–5 个在命名轴上真正不同的变体，放进逐字规格的暗色玻璃翻选器（数字键 `1–N` / `←`/`→` / `R` 重放，`?v=N` URL 持久）翻选定胜负。每个变体守 Emil Kowalski 工艺硬指标（`ease-out`、<300ms、仅 `transform`/`opacity`、reduced-motion），支持 `riff`（围绕倾向方向再发散一轮）与 `keep`（晋升选中变体后删除原型面）。

与 prototype-app 分工：prototype 用完即扔、不留档，适合临时探索；要归档、要晋升进生产的原型用 prototype-app。

## 关联插件

`thinking` 插件承载意图访谈、方案拷问、创意打磨、领域建模等思维技能，两插件分工互补。

## 安装

```bash
/plugin marketplace add ElliotChina/premium-plugin-marketplace
/plugin install prototype-design@premium-plugin-marketplace
```
