# Product image failure index

Search this file by tag, symptom, or ID only when the current product has that risk or an output fails. Core execution remains in `SKILL.md` and `workflow.md`.

## Tags

`BOM` counting and classification · `GEO` geometry · `SURF` surface · `ACC` accessories · `ACT` use/action · `TEXT` exact content · `SCENE` staging · `EDIT` targeted changes · `QA` validation and versions

| ID | Tag | Failure | Preventive rule |
|---|---|---|---|
| IMG-001 | SCENE | Same or near-identical outputs | Give every slot a distinct purpose, camera, arrangement, light, and selling focus |
| IMG-002 | SCENE | Generic scene mismatch | Design the scene around current material, color, use, and customer |
| IMG-003 | SCENE | Different SKUs reuse one template | Rebuild the current SKU plan and change at least three scene dimensions |
| IMG-004 | SCENE | Props or people dominate | Keep the product as the first visual subject |
| IMG-005 | ACT | Hand obscures product | Keep hand coverage near or below 25% and expose key geometry |
| IMG-006 | SCENE | Accessory layout repeats across SKUs | Redesign relationships for the current SKU |
| IMG-007 | SCENE | Two scenes differ only by hand pose | Change at least three of environment, camera, light, action, props, tone, audience |
| IMG-008 | QA | Single images pass but set repeats | Review content, composition, scene, camera, and purpose across the whole set |
| IMG-009 | SURF | Unseen face gains pattern or label | Infer nothing on hidden faces |
| IMG-010 | SURF | Pattern position drifts | Map pattern position, direction, and count before generation |
| IMG-011 | GEO | Decorative rim becomes a spout | Depict a spout only when the source proves a real outlet |
| IMG-012 | ACC | Hardware becomes generic | Use the relevant original close-up to lock the structure |
| IMG-013 | BOM | Packaging, cloth, tray, or tube miscounted | Build S/C/K/D classification and the exact set equation |
| IMG-014 | TEXT | Small label is wrong or garbled | Avoid frontal display or add it deterministically after base approval |
| IMG-015 | BOM | Correct functional fitting hides an item | Allow necessary occlusion but preserve identifying outline |
| IMG-016 | BOM | Scene prop looks included in sale | Separate it through distance, depth, position, and visual weight |
| IMG-017 | ACT | Action hides SKU identity | Expose at least two SKU-specific features |
| IMG-018 | TEXT | Dimension graphic has layered errors | Validate product, text, and arrow layers separately |
| IMG-019 | SCENE | Fixed slot roles become a visual template | Keep function stable but rotate the actual visual solution |
| IMG-020 | QA | Retry versions corrupt final count | Use fixed slot IDs and explicitly discard failed versions |
| IMG-021 | BOM | High-count set BOM drifts | Block generation until the equation is confirmed |
| IMG-022 | BOM | One occluded item counted twice | Trace connected outline before splitting an object |
| IMG-023 | GEO | Low bowl becomes tall or deep | Use measured ratio when available, otherwise retain source silhouette |
| IMG-024 | GEO | Pouring stretches a short spout | Switch to whisking or result scene after first distortion |
| IMG-025 | SURF | Solid surface gains random pattern | Treat unsupported pattern as a critical failure |
| IMG-026 | ACT | Ice appears in mixing bowl | Put ice only in the finished drinking glass |
| IMG-027 | TEXT | Dimension arrows target wrong edges | Add arrows deterministically to correct outer measurement points |
| IMG-028 | EDIT | Local fix damages another feature | Run full-image QA after every local edit |
| IMG-029 | QA | Same error survives many versions | Apply the two-version fuse and truly change method |
| IMG-030 | EDIT | Generated output becomes identity authority | Return every identity decision to original references |
| IMG-031 | EDIT | Multiple generated references contaminate identity | Use the minimum original references; generated images are not identity inputs |
| IMG-032 | SURF | Repeated negative texture words reinforce artifact | Use a positive original surface reference and few exclusions |
| IMG-033 | EDIT | Background edit redraws product | Inspect every item; use extraction/compositing for high-risk identity |
| IMG-034 | QA | Contaminated output called a clean master | Compare against originals item by item before approval |
| IMG-035 | GEO | Exact decoration count changes | Record the count in P0 and use original detail or deterministic composite |
| IMG-036 | BOM | 8–11-piece full redraw drifts | Use retained line-item assets or intact-set extraction |
| IMG-037 | QA | Slot definitions conflict | Let the skill core define defaults; P6 changes only with reliable dimensions or user override |
| IMG-038 | QA | One SKU's facts enter universal rules | Keep SKU facts only in the current P0 manifest |
| IMG-039 | ACT | Every high-count item is forced into an action scene | Let P1/P4 prove BOM; show only action-relevant products elsewhere |
| IMG-040 | QA | Attractive image hides identity error | Reject critical identity errors regardless of aesthetics |
| IMG-041 | QA | False pixel-lock claim | Make the claim only after actual mask, extraction, or deterministic compositing |
| IMG-042 | EDIT | Required method is unavailable but generation continues | Pass the capability gate; stop, obtain assets, or adjust the requirement |
| IMG-043 | QA | Old and new rule versions both apply | Use only the installed skill as the active rule set |
| IMG-044 | QA | Automatic high risk is diluted by scoring | Apply hard gates before auxiliary score |
| IMG-045 | QA | Output is approved without being opened | Inspect the actual image; no visible output means incomplete |
| IMG-046 | EDIT | Background watermark is wrongly preserved or removed | Treat background-only watermark as mutable when a clean background is requested; clarify if it overlaps product pixels |
| IMG-047 | EDIT | Transparent product is promised a new background with zero pixel change | Explain that seen-through background is embedded in current product pixels; relax one requirement or use approved recompositing |
| IMG-048 | QA | “Continue” carries the previous SKU into a newly uploaded product | Rebuild P0 whenever a new product or changed SKU appears; reuse only the same active confirmed SKU |
| IMG-049 | BOM | Separate colors, sizes, structures, or pack counts contaminate one another | Use one P0 and plan per SKU unless the user explicitly requests a combined comparison |
| IMG-050 | BOM | Bulk pack count is faked by an approximate generated pile | Use exact retained composition, representative stack, or carton label and state the representation honestly |
| IMG-051 | BOM | Pack count and nested carton equation are flattened incorrectly | Record declared unit, per-pack units, total sales units, and the hierarchical equation |
| IMG-052 | QA | Only one output or a collage is delivered for a multi-image request | Track requested outputs by group and slot; complete each as a separate output unless collage was requested |
| IMG-053 | TEXT | Exact quantity, Logo, or dimensions are entrusted to free generation | Approve the product base first, then use deterministic layout and verify the exact source string |
| IMG-054 | QA | Pixel size, ratio, format, or file-size compliance is claimed without file inspection | Read actual output metadata or state that exact file validation was unavailable |
| IMG-055 | QA | Marketplace compliance is claimed from remembered conventions | Verify current official rules when compliance is requested and separate them from user house style |
| IMG-056 | SCENE | Historical scene de-duplication is claimed without an accessible ledger | Compare an available current-project ledger or state that only current-task de-duplication was possible |
