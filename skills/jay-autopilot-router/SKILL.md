---
name: jay-autopilot-router
description: Route a new product-image conversation triggered by “芝麻开门” through the portable Jay title and reference-faithful image workflow. Use when an agent must coordinate Alibaba title generation, product-image slots, zero-interrupt execution, final QA, and delivery audit.
---

# Jay Autopilot Router

This is the portable coordination layer for the two specialist skills in this repository.

## Master trigger

When a new conversation includes a product image and the user says `芝麻开门`, enter `FULL_AUTOPILOT_ZERO_INTERRUPT`.

The final destination is Alibaba International. Other platforms may be used for research or visual strategy, but they do not replace Alibaba output rules.

## Execution order

1. Read `references/ACTIVE_SKILLS.md`, then the control-plane and zero-interrupt references in this skill.
2. Establish product truth from the current image and explicit user facts. Never invent unseen structure, quantity, dimensions, material, text, or branding.
3. Run `matcha-alibaba-title-engine` for the title and keyword decision.
4. Run `generate-faithful-product-images` for the requested image slots.
5. Execute the image loop one slot at a time: plan → validate → generate/edit → inspect → repair or switch method → pass.
6. Finish with title QA, per-image QA, Final QA, and a Delivery Audit.

## Zero-interrupt behavior

- Do not pause for ordinary missing information when a safe provisional decision is possible.
- Do not claim completion after the first successful image.
- If the runtime forces the assistant turn to end after one image, report the runtime limitation truthfully; never fabricate remaining outputs.
- Ask one focused question only when the missing fact can change SKU identity, BOM, critical geometry, quantity, logo, or a hard dimension.

## Completion contract

Return only `COMPLETE` when the requested title and real image outputs exist, title QA passes, every image has been visibly inspected, Final QA passes, and the Delivery Audit records any provisional facts or remaining optional enhancements.

## Specialist skills

- `../matcha-alibaba-title-engine/SKILL.md`
- `../generate-faithful-product-images/SKILL.md`

## Portable references

- `references/Skill_Router_V1.9.md`
- `references/Title_Skill_Instruction_V1.2.md`
- `references/Control_Plane_Sanitizer_V1.1.md`
- `references/Zero_Interrupt_Adapter_V1.0.md`
- `references/Platform_Profiles_V1.1.md`
- `references/Chat_to_Web_Workflow_Architecture_V1.0.md`
