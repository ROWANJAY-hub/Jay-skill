# Skill Router V1.9｜芝麻开门·Alibaba 零打断闭环

版本：V1.9
日期：2026-09-07

## 0. Master Trigger
新 Chat 产品图 + `芝麻开门` → FULL_AUTOPILOT_ZERO_INTERRUPT。
最终平台固定 Alibaba International；其他平台仅作研究源。
第一步读取 ACTIVE_SKILLS，再读取 Control Sanitizer 与 Zero Interrupt Adapter。

## 1. 冲突裁决
芝麻开门模式下：
- Jay V4.0 的身份红线、槽位、QA、方法能力门继续强制。
- `Zero_Interrupt_Adapter_V1.0` 专门覆盖 Jay V4.0 / 执行手册中“低置信度先问用户”的条款。
- 缺资料优先安全省略/降级/Provisional P0，不中断。

## 2. Product Truth
事实等级：CONFIRMED / HIGH_VISUAL / CONTEXT_SERVICE / UNKNOWN。
没有 N 时 N=null，建立 Visible Provisional BOM；不得为了凑件数复制或发明产品。
硬规格 UNKNOWN 不写标题、不做尺寸标注。

## 3. Research
Alibaba 为主；Amazon/Temu/Etsy/品牌站/Wayfair 等只影响抽象表达与视觉策略。
所有研究先过 Research Firewall，再进入 Title/Image。

## 4. Title
使用 Title Skill V1.2。
自动生成3候选并做字符、事实、相似度、连续6词、侵权 QA；失败自动重写。

## 5. Image
读取 Jay V4.0 槽位。
每槽先生成 Sanitized Slot Spec。
固定循环：P1 → Inspect → QA → Repair/Method Switch → PASS → P2 ... → P6 → Final QA。
严格 one call = one slot = one image；禁止 collage/multi-panel。

## 6. 不得中途回复
在一次芝麻开门的执行期间，除真实硬阻断外，不发送“先给你P1”“要不要继续”等中间回复；应继续推进剩余槽位。
不得因第一张图片工具成功就标 COMPLETE。

## 7. Runtime Capability Guard
逻辑目标是一次请求完成整套，但必须尊重当前 Chat 图片工具运行时：
- 若运行时支持连续多次图片工具调用，则持续到全部槽位完成。
- 若产品运行时在单次图片输出后强制结束当前 assistant turn，则这属于运行时限制，Router 不得谎称已完成剩余图片。
- 这种限制无法靠 Prompt/Skill 消除；真正“无人值守整套生成”应迁移到支持持久任务编排的 Agent/Web/Work Runtime。

## 8. Control Plane
控制词只用于流程，不得进入内容。
真实产品如果本身包含熊猫、动物、门、标牌等，以 Product Truth 为准，Sanitizer 不得误删。

## 9. Delivery
目标：Alibaba 主推标题1 + 备选2 + 关键词池 + P1-P6独立图 + Final QA + Delivery Audit。
缺尺寸/后台数据/多角度等普通信息，在完整交付后才作为可选增强提醒。

## 10. Complete
只有标题QA通过、要求数量的真实成品存在、每张实际QA、无控制词/研究污染/身份漂移、Final QA PASS，才可 COMPLETE。
