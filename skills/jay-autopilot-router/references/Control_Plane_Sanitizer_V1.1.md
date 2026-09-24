# Control Plane Sanitizer V1.1

版本：V1.1
日期：2026-09-07
作用：隔离控制词，同时避免误伤真实产品本身。

## 1. CONTROL-PLANE ONLY
`芝麻开门`、开始工作流、开始生成、继续工作流、FULL_AUTOPILOT、PRECHECK、COMPLETE、PASS、FAIL、BLOCKED、P0-P6、Router、Skill、Agent、QA、RunState 等，不得作为创作主题进入标题、关键词、图片、包装、道具、背景标牌。

## 2. 语义隐喻禁止
不得因为控制词自动生成门、门牌、芝麻、开门动作、魔法、中文标语、流程状态牌等。

## 3. Product Truth Exception
若“门、熊猫、动物、人物、文字、标牌”等本身就是当前 Product Truth / 原始产品的一部分，则必须保留，不得因为 Sanitizer 自动删除。
禁止的是“由控制词或研究结果新增的元素”，不是原产品真实元素。

## 4. Image Content Firewall
允许：Product Truth 中 S/C/K、当前槽明确允许的 D、必要真实动作/内容物。
默认禁止新增：角色/IP/动物玩偶、营销标牌、竞品Logo/图案/包装文案、控制词衍生物。
P1/P4 道具尽量少；P5/P6 道具必须服务真实用途。

## 5. Research Firewall
跨平台研究只转化为构图、光线、镜头、场景类型、卖点优先级、买家关注点。
不得复制竞品角色、图案、Logo、文案、包装设计、标牌、道具组合。

## 6. Sanitized Slot Spec
每槽调用前内部形成：Product Identity / Slot Goal / Allowed Props / Forbidden Content / Original References。
若控制词仍以视觉内容存在，禁止调用图片模型。
