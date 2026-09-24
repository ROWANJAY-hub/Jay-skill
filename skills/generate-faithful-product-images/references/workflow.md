# Reference-faithful product image workflow

## Contents

1. Source authority and isolation
2. Task brief and P0 identity manifest
3. SKU, BOM, and quantity model
4. Risk and method routing
5. Output groups and slots
6. Reference roles and prompt structure
7. Visual QA, retries, and completion
8. Plan and file validation

## 1. Source authority and isolation

Resolve conflicts in this order:

1. User's explicit current request.
2. User-designated current main product reference.
3. Current original detail references.
4. Current dimension reference and explicit measurements.
5. Confirmed current P0 identity manifest and BOM.
6. `SKILL.md`.
7. This workflow and the relevant mode-specific reference.
8. Only matching entries in `failure-index.md`.
9. Aesthetic or platform references explicitly supplied or requested by the user; these control style only.

Use only the current task's files, current project sources, current conversation, and files the user explicitly designates. Do not import product facts from another project, old SKU, unrelated chat, or an aesthetic reference. A generated image never outranks an original reference.

When references conflict in quantity, SKU, geometry, Logo, or dimensions and the current request does not resolve the conflict, ask one focused question. Do not average or merge incompatible variants.

## 2. Task brief and P0 identity manifest

Before item-level inspection, record the task brief:

```text
Task mode:
Platform/destination:
Output group ID:
Requested output count and order:
User-specified slots or default:
Canvas ratio:
Exact or minimum pixels:
Maximum file size and format:
SKU mode:
Set mode:
Declared count and counting basis:
Quantity representation:
Reliable dimensions present:
Exact text or Logo present:
Main reference R0:
```

Allowed task modes are `carousel_set`, `hero`, `scene_only`, `detail_only`, `dimension_graphic`, `sku_preview`, `background_edit`, `targeted_edit`, and `custom`.

For every sales item, record:

| Field | Required observation |
|---|---|
| ID, SKU, and quantity | One stable ID per distinguishable line item; repeated identical units may share an ID and quantity |
| Outline and ratio | Shape, width/height/depth, thickness, capacity impression |
| Geometry | Opening, lip, spout, handle, lid, base, groove, hole, connector, hardware |
| Material and surface | Ceramic, bamboo, wood, metal, glass, acrylic, fabric; solid, glaze, grain, gradient, matte, clear, mirror |
| Color | Main and secondary colors, edge color, gradient direction |
| Marking | Pattern, Logo, label, decoration position, direction, and exact count |
| Orientation | Front/back, left/right, top/bottom, outlet and installation direction |
| Use | Correct placement, nesting, grip, assembly, storage, action, and contents |
| Authority | Original R0–R5 reference that proves the fact |
| Confidence | `high`, `medium`, or `low` |

Do not infer hidden faces. Stay within known viewing angles when source coverage is incomplete. If a tiny or occluded part changes the count or critical geometry, inspect it enlarged and trace connected outlines before deciding.

## 3. SKU, BOM, and quantity model

Use four classes:

| Class | Meaning | Counts as a sales unit |
|---|---|---|
| S | Independently sold product or confirmed counted packaging/accessory | Yes |
| C | Fixed component or attached decoration | No |
| K | Packaging, protection, insert, or storage item not confirmed as counted | No |
| D | Scene prop or explanatory object | No |

Rules:

- A fixed bow, handle, lid, foot, or attached decoration is not automatically a separate piece.
- Nested placement does not merge two confirmed sales items.
- Packaging counts only when current text, a sales list, or unambiguous current material says it does. Then classify it as S and note its packaging role.
- A cloth, cup, tray, tube, stand, or case may be S, K, or D. Do not decide by habit.
- Build a separate plan for each color, size, pack count, or structural SKU unless the user explicitly asks to combine them.
- A combined multi-SKU preview must map every visible product and every label to the correct SKU. Do not duplicate one size or color to impersonate another.

Choose one set mode:

| Set mode | Meaning |
|---|---|
| `single_product` | One sold product; fixed parts are C, not extra pieces |
| `heterogeneous_set` | A 2–11-piece set of one or more distinct sold line items |
| `bulk_multipack` | Many identical or repeated units, a master carton, or packs-of-packs |
| `multi_sku_combined` | Two or more SKUs shown together by explicit user request |

Choose a quantity equation:

- `piece_sum`: the sum of S quantities equals `declared_count`.
- `hierarchical_pack`: `declared_count` is packs, sets, or cartons; record `units_per_pack`, `total_sales_units`, and an explicit equation. The sum of S quantities must equal `total_sales_units`, and `declared_count × units_per_pack = total_sales_units`.

Choose one representation:

| Representation | Use when |
|---|---|
| `exact_items` | Every unit can be shown and individually counted from verified source coverage |
| `exact_composite` | Verified retained assets can be duplicated and laid out deterministically to the exact count |
| `representative_stack` | The display is intentionally representative; an exact quantity label carries the pack claim |
| `carton_label` | An intact package or carton plus deterministic quantity text conveys the pack count |
| `not_applicable` | Quantity is not a visual claim in the requested output |

For `single_product` and `heterogeneous_set`, normally use `piece_sum` and `exact_items`. For bulk multipacks, never imply that a representative stack is individually countable. Do not invent carton dimensions, printing, labels, or shipping marks.

## 4. Risk and method routing

Automatic high-risk triggers:

- eight to eleven pieces in a heterogeneous set;
- an exact display of many units or a hierarchical pack;
- a combined multi-SKU image;
- a targeted/background edit that must leave everything else unchanged;
- exact or distinctive glaze, grain, gradient, transparency, pattern, Logo, label, text, or decoration count;
- a materially new angle or hidden surface from limited source coverage;
- identity drift in the current slot.

If no automatic trigger applies, add one point for each:

- five to seven sold pieces;
- highly similar items that may merge or duplicate;
- reflective, transparent, translucent, or acrylic surfaces;
- nesting, functional fitting, or heavy occlusion;
- hands, liquid, pouring, sieving, whisking, installation, or another contact-heavy action;
- dimensions, arrows, tables, or multiple exact labels;
- multiple presentation goals in one image.

| Score | Risk | Default route |
|---:|---|---|
| 0–2 | Low | Source-anchored generation may be used; inspect every identity attribute |
| 3–4 | Medium | R0 plus one critical original detail; limit angle change; prefer editing over redraw |
| 5+ | High | Retain the intact source or verified product assets; generate scene/background separately |

Automatic high risk overrides scoring.

Separate fidelity demand from risk:

| Fidelity mode | Meaning | Allowed claim |
|---|---|---|
| `reference_faithful` | Visually match the source after full QA; best-effort generative edits may be used | Do not claim unchanged pixels |
| `pixel_locked` | Unnamed regions or the whole product must remain pixel-identical | Requires actual source reuse, masking, cutout, or layered compositing |

Method routing:

| Request | Preferred route |
|---|---|
| Change only background | Immutable product mask plus mutable background; if only generative editing exists, use `reference_faithful`, disclose no pixel lock, and recheck every item |
| Change one named object or text | Isolate immutable, mutable, and incidental-overlay regions; use deterministic text/Logo layout when possible |
| New scene with exact product | Generate the empty scene separately and composite retained product assets |
| New angle | Use only with sufficient original multi-angle coverage; otherwise remain within known views |
| 8–11-piece full set | Retain the intact original set or layer extracted line items; do not freely redraw the full set |
| Exact Logo, quantity, dimensions, or copy | Approved product base plus deterministic layout |
| Bulk multipack | Exact retained composite, representative stack, or carton label according to the confirmed representation |
| Use action | One action per image; minimize hand coverage and unnecessary products |

If the preferred method is unavailable, move through the fallback ladder in `SKILL.md`. Do not list a mask, cutout, or layered-composite capability unless it actually exists in the current environment and is used.

## 5. Output groups and slots

The user's count, order, ratio, and content always win. Otherwise, use six independent square outputs:

| Slot | No reliable dimensions | Reliable dimensions present |
|---|---|---|
| P1 | Complete product or complete-set hero | Same |
| P2 | First core product or feature detail | Same |
| P3 | Second product, accessory group, or second feature | Same |
| P4 | Complete product or set, differentiated second presentation | Same |
| P5 | First valid use scene | Same |
| P6 | Second scene, different in at least three dimensions | Deterministically laid-out dimension graphic |

Adapt rather than forcing the default:

- A request for one hero, three scenes, one dimension graphic, or a targeted edit uses exactly those outputs and sets `user_slot_override: true`.
- “再生成” creates only the named additional outputs. It does not rebuild already approved slots.
- For several styles or SKU groups, use G1, G2, and so on, with a separate P1…Pn plan inside each group.
- P1/P4 prove the complete BOM only in the default carousel. Detail and action slots may show a relevant subset.
- Full-set images for 2–11-piece mixed sets keep every item independently countable and normally at least 70% visible, except necessary functional fitting that preserves an identifying outline.
- Bulk multipack slots follow the representation mode and may use a carton or representative group rather than counterfeit exact visibility.
- If dimensions are absent, never invent a dimension slot. If dimensions are supplied, preserve their original units unless the user requests a verified conversion.

For two scene slots, change at least three of: environment, camera, light, action, props, tone, and audience. Record those axes in the plan so validation can reject near-duplicate scene concepts before generation.

Differentiate P1 and P4 in at least two of camera height, subject placement, accessory arrangement, background depth, or light direction. With only one source angle, do not reveal unknown surfaces; differentiate within the proven view.

## 6. Reference roles and prompt structure

Assign roles:

| Role | Controls |
|---|---|
| R0 | Original overview: category, BOM, overall geometry, colors, relationships |
| R1 | Core geometry: outline, ratio, opening, spout, base, handle |
| R2 | Surface: glaze, grain, gradient, transparency, finish |
| R3 | Accessory detail: hardware, mesh, connector, support |
| R4 | Logo, label, and exact decoration |
| R5 | Dimensions and measurement locations |
| R6 | Style only: composition, scene, lighting, mood |

Usually use R0 plus one relevant original detail. Add the current edit target only for an edit. Prefer explicit original file paths when available so generated conversation images are not accidentally included as identity references. If only conversation-image selection is available, use the smallest source set that contains all required originals and do not treat intervening generated images as authority.

Build the image prompt in this order:

1. One slot objective.
2. Original reference roles.
3. Sales-item IDs and quantities visible in this slot.
4. Positive identity statement: outline, geometry, proportions, material, surface, color, direction.
5. Scene, camera, placement, and lighting.
6. Named immutable regions for a local edit.
7. Three to five highest-risk exclusions.

Keep P0 records, risk scores, and validation output outside the image prompt.

## 7. Visual QA, retries, and completion

Open every finished image and check:

- required SKU, sales IDs, quantities, and representation mode;
- outline, proportions, geometry, material, color, surface, transparency, pattern, Logo, and package;
- no addition, deletion, copy, merge, mirror, SKU mixing, deformation, or invented hidden structure;
- real contact, grip, fitting, pouring, contents, and scene logic;
- props are visibly separate from sold contents;
- no random text, watermark, competitor element, or fabricated branding;
- exact text and dimensions match their sources;
- scene differentiation and slot purpose;
- actual ratio, pixel width/height, format, and file size when available;
- method claims match the method actually used;
- targeted-edit regions were classified correctly and the entire image still passes.

Severity:

- Critical identity, count, SKU, Logo, or dimension error: discard immediately.
- Major isolated error: allow one targeted correction.
- Minor aesthetic issue: accept only if identity and requested purpose are unaffected.

Retry rule:

1. v1 fails: make one targeted v2 correction from original references or a genuinely approved edit target.
2. The same error survives v2: discard both, stop the method, and switch to source retention, compositing, safer view/action, deterministic layout, or one blocking question.
3. A high-risk identity error remains after the method switch: stop that slot and report that it did not meet the delivery standard.

Never propagate a contaminated version into later slots. Final delivery must list exactly one accepted version for every requested slot and explicitly exclude failed versions. A successful tool call without a visible accepted image does not fill a slot.

## 8. Plan and file validation

Store the current plan outside the skill directory and run:

```bash
python3 <skill_root>/scripts/validate_plan.py /absolute/path/to/plan.json
```

Minimal two-piece default-plan schema:

```json
{
  "plan_version": 2,
  "task_mode": "carousel_set",
  "platforms": ["custom"],
  "group_id": "G1",
  "sku_mode": "single_sku",
  "combined_sku_requested": false,
  "set_mode": "heterogeneous_set",
  "declared_count": 2,
  "count_basis": "sales pieces",
  "quantity_model": {
    "mode": "piece_sum",
    "representation": "exact_items",
    "equation": "1 bowl + 1 holder = 2"
  },
  "requested_output_count": 6,
  "has_dimensions": false,
  "dimension_source": null,
  "output_spec": {"aspect_ratio": "1:1"},
  "fidelity_mode": "reference_faithful",
  "fragile_features": ["distinctive glaze"],
  "requests_new_angle": false,
  "previous_identity_drift": false,
  "user_slot_override": false,
  "method": {
    "risk_level": "high",
    "automatic_triggers": ["fragile_identity"],
    "route": "generative_edit",
    "available_capabilities": ["generative_edit"],
    "claims_pixel_preservation": false,
    "original_reference_used": true,
    "full_visual_qa": true
  },
  "skus": [
    {"id": "SKU-A", "reference": "R0", "confidence": "high"}
  ],
  "items": [
    {
      "id": "S01", "sku_id": "SKU-A", "name": "bowl", "class": "S", "quantity": 1,
      "reference": "R0", "confidence": "high", "critical": true,
      "identity": {
        "outline": "low wide bowl", "geometry": "short spout and foot",
        "material": "ceramic", "surface": "fine glaze", "color": "pink and ivory",
        "orientation": "spout right", "use": "mixing bowl"
      }
    },
    {
      "id": "S02", "sku_id": "SKU-A", "name": "holder", "class": "S", "quantity": 1,
      "reference": "R0", "confidence": "high", "critical": true,
      "identity": {
        "outline": "curved holder", "geometry": "stable base",
        "material": "ceramic", "surface": "matching glaze", "color": "pink and ivory",
        "orientation": "upright", "use": "whisk holder"
      }
    }
  ],
  "slots": [
    {"id": "P1", "kind": "full_set", "objective": "complete hero", "product_ids": ["S01", "S02"]},
    {"id": "P2", "kind": "detail", "objective": "bowl detail", "product_ids": ["S01"]},
    {"id": "P3", "kind": "detail", "objective": "holder detail", "product_ids": ["S02"]},
    {"id": "P4", "kind": "full_set", "objective": "second complete view", "product_ids": ["S01", "S02"]},
    {"id": "P5", "kind": "scene", "objective": "home cafe use", "product_ids": ["S01"], "scene_axes": {"environment": "home cafe", "camera": "eye level", "light": "morning", "action": "mixing"}},
    {"id": "P6", "kind": "scene", "objective": "gift display", "product_ids": ["S02"], "scene_axes": {"environment": "gift table", "camera": "high angle", "light": "evening", "action": "display"}}
  ],
  "final_outputs": ["P1", "P2", "P3", "P4", "P5", "P6"]
}
```

When `user_slot_override` is `false`, validation enforces the default six-slot carousel. When true, the user's requested count and slot choices replace the defaults while BOM, SKU, reference, confidence, method, and output-count checks still apply.

For several output groups, store one plan per group and validate an aggregate manifest:

```json
{
  "batch_version": 1,
  "requested_group_count": 5,
  "outputs_per_group": 6,
  "requested_total_outputs": 30,
  "groups": [
    {"group_id": "G1", "plan": "plans/G1.json"},
    {"group_id": "G2", "plan": "plans/G2.json"},
    {"group_id": "G3", "plan": "plans/G3.json"},
    {"group_id": "G4", "plan": "plans/G4.json"},
    {"group_id": "G5", "plan": "plans/G5.json"}
  ]
}
```

Run:

```bash
python3 <skill_root>/scripts/validate_batch.py /absolute/path/to/batch.json
```

This validates every group plan, unique group IDs, group count, per-group count, and aggregate output count.

If an approved image needs exact pixels or a file-size cap, finalize it without stretching:

```bash
python3 <skill_root>/scripts/finalize_image.py input.png output.jpg \
  --width 800 --height 800 --fit contain --background '#FFFFFF' \
  --format JPEG --max-bytes 1500000
```

Use `cover` only after verifying that the centered crop cannot remove product content. Upscaling changes pixel dimensions but does not create new source detail.

Then add an `output_files` mapping to the plan and run:

```bash
python3 <skill_root>/scripts/validate_outputs.py /absolute/path/to/plan.json
```

This checks file existence, output count, dimensions, aspect ratio, format, file-size limits, and exact duplicate files. It does not replace visual QA.
