# Chat-to-Web Workflow Architecture V1.0

日期：2026-09-04
目标：当前先让普通聊天成为稳定的“执行内核”；未来网页只做输入、参数、状态、审批和结果展示，不重新发明业务逻辑。

## 1. 核心链
Input
→ Platform Profile
→ Product Truth
→ Research Hub
→ Domain Engines
→ QA Gates
→ Human Approval
→ Execution
→ Run Log / Learning

## 2. 数据对象
### ProductTruth
单SKU唯一事实源。标题和图片只能读取，不可各自修改。
### ResearchPacket
分 TitleResearch 与 ImageResearch；包含来源、日期窗口、权重、结论。
### Candidate
标题候选/图片计划，未批准不进入正式台账。
### RunState
每个节点 PASS / FAIL / WAITING / BLOCKED。
### ErrorRecord
只保存可复用错误，不保存具体SKU私有事实。

## 3. 当前聊天已实现
- Skill Manifest/版本锁
- Platform识别
- Product Truth/P0
- 标题调研/去重/QA
- 图片调研/风险/逐槽/QA
- Approval Gate
- Run State
- 两版熔断

## 4. 网页第一版建议界面
左侧 Input：
- 平台
- 上传产品图/细节图/尺寸图
- SKU/件数/尺寸/备注
- 可选后台数据
- “开始工作流”

中间 Workflow：
- Product Truth卡
- Title Research
- Image Research
- Risk
- QA
- Approval

右侧 Output：
- 3条标题
- 关键词
- P1–P6卡片
- PASS/FAIL状态
- 返工按钮
- 确认入台账按钮

## 5. 参数层
- 平台配置
- 数据窗口
- 关键词权重
- 相似度阈值
- 图片槽位规则
- 风险阈值
均应版本化，不写死在前端。

## 6. 未来插件
Product Selection / Pricing / Inventory / Publishing 都应通过同一接口：
`ProductTruth + ResearchPacket -> Result + Evidence + QA`
未激活的插件不能影响当前双引擎。

## 7. 当前阶段判断
标题+图片双引擎在普通聊天中已经可以作为网页V1的后端逻辑原型。
在真正开发网页前，应该先用普通聊天连续测试多种SKU，记录：
- Product Truth误判率
- 标题返工率
- 图片P1–P6一次通过率
- 高风险槽位失败原因
- 用户人工修改点
这些数据再决定网页默认参数，而不是先把错误逻辑固化进网页。
