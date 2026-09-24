---
name: generate-faithful-product-images
description: Generate or edit reference-faithful ecommerce product images when product identity, SKU mapping, set contents, bulk quantity, packaging, accessories, structure, surface finish, dimensions, text, Logo, or correct use must remain accurate. Use for Alibaba, Amazon, Temu, Wayfair, or B2B hero images, carousel sets, detail views, lifestyle scenes, dimension graphics, SKU previews, background replacement, targeted edits, single products, 2–11-piece mixed sets, multi-SKU variants, and bulk multipacks. Do not use for copywriting-only requests, catalog documents, or standalone logo/vector extraction.
---

# Generate Faithful Product Images

Prioritize product truth over visual appeal. Treat the user's current reference images and confirmed facts as authoritative; never let a generated image, old SKU, prior chat, aesthetic reference, or marketplace convention redefine the product.

## Required workflow

1. Inspect every current product reference that materially affects identity. Use visual inspection rather than filenames or prior verbal descriptions; enlarge count-critical or structure-critical details when needed.
2. Classify the request before planning: task mode, SKU scope, set or quantity mode, requested output count, slot order, platform/destination, canvas, pixels, file-size limit, and exact text or Logo requirements.
3. Read [references/workflow.md](references/workflow.md) before a set, multi-image delivery, variant series, bulk pack, dimension graphic, SKU preview, background replacement, or targeted edit. Also read [references/ecommerce-modes.md](references/ecommerce-modes.md) for platform-facing, multi-SKU, bulk-quantity, or multi-group work.
4. Build a fresh P0 identity manifest for every new product or SKU. Reuse a confirmed manifest only while continuing the same active SKU with no conflicting new reference or fact.
5. For every set, multi-image group, multi-SKU view, bulk pack, exact text/dimension output, background replacement, or targeted edit, validate each SKU/output-group plan with `scripts/validate_plan.py` before generating. For several groups, also validate their aggregate count with `scripts/validate_batch.py`. A simple low-risk single image may use the same P0 checks without serializing JSON. Fix every validation error or ask one focused blocking question; never invent a capability merely because the task needs it.
6. Select generation, editing, extraction, source retention, or deterministic compositing only after passing the method-capability gate below.
7. Generate or edit one slot at a time, keeping an original current reference as the identity authority for every slot. Continue until the requested count is complete unless a blocking fidelity limit is reached.
8. Actually open and inspect every output. A successful tool response, prompt wording, or earlier verbal approval is not visual QA. When local files exist and exact pixels or file size matter, finalize the approved visual base with `scripts/finalize_image.py`, then use `scripts/validate_outputs.py` for deterministic file checks.
9. Deliver exactly the requested final versions as separate outputs unless the user explicitly requests a collage. Mark failed attempts as discarded and provide a final slot-to-version map.

For matcha bowls, whisks, holders, scoops, sieves, pouring, frothing, or matcha sets, also read [references/matcha.md](references/matcha.md).

When an error occurs or the product contains a known fragile feature, search only the matching tags or terms in [references/failure-index.md](references/failure-index.md). Do not load the entire index into an image prompt.

## Intent and continuity gate

- A current explicit instruction overrides defaults without erasing unrelated confirmed identity facts.
- “继续” plus a new product or changed SKU starts a new P0. “继续” with the same active SKU continues unfinished slots or the specifically requested extension; it does not silently replace approved outputs.
- “再生成 N 张场景图” means N new scene images only. “只改 X” means a targeted edit of X only. Do not regenerate a full set unless asked.
- Build separate P0 manifests and plans for separate colors, sizes, pack counts, or structures. Combine SKUs in one image only when the user explicitly asks for a comparison or combined preview.
- One plan represents one SKU/output group. For requests such as several styles with several images each, validate each group separately and track the aggregate requested count.

## P0 blocking gate

Do not generate until these facts are stable:

- task mode, SKU/output-group scope, destination, requested count/order, and delivery specifications;
- product category and real use;
- quantity mode: single product, 2–11-piece mixed set, bulk multipack, or explicitly combined multi-SKU view;
- declared count, its counting basis, exact sales-item equation, and how that quantity will be represented visually;
- separation of sales items, fixed components, packaging, and scene props;
- each sales item's structure, proportions, material, color, surface, direction, and authoritative reference;
- exact Logo, label, pattern, decoration count, or dimension data when relevant;
- correct placement, assembly, storage, grip, action, and contents;
- confidence for every count-critical or structure-critical fact.

Ask one necessary question when a low-confidence fact can change the BOM, SKU, critical geometry, Logo, or dimension result. Do not guess from industry convention. If a package or storage case is confirmed as one of the sold pieces, classify it as a sales item and retain its packaging role as a note.

For bulk multipacks, do not conflate pack quantity with the number of distinct item types. Show every unit only when the source or a deterministic composition can prove the count. Otherwise use a truthful grouped display, intact pack, or carton representation with exact quantity text added deterministically.

## Method-capability gate

Treat any of these as automatically high risk:

- an 8–11-piece mixed set or an exact high-unit-count display;
- an explicitly combined multi-SKU image;
- a request to change only one element while everything else remains unchanged;
- exact or distinctive glaze, wood grain, gradient, transparency, pattern, Logo, label, text, or decoration count;
- a single source angle paired with a materially new requested angle or hidden surface;
- any previous identity drift in the current slot.

For high-risk work:

- Prefer actual cutouts, masks, retained product assets, or deterministic layered compositing.
- Distinguish `reference_faithful` from `pixel_locked`. Reference-faithful work may use a source-anchored generative edit when the view stays within proven geometry and the whole output can be inspected; pixel-locked work requires a genuinely pixel-preserving method.
- Use generative editing only as a best-effort transformation and recheck the entire image; it does not prove unchanged pixels or exact quantities.
- Claim pixel preservation only when a pixel-preserving method was actually used.
- For transparent or translucent products, recognize that the visible background is already mixed into their pixels. A new seen-through background and zero changed product pixels may be mutually incompatible; surface that conflict rather than promise both.
- Add exact words, numbers, units, arrows, tables, and Logos with deterministic layout after the product base passes QA.
- Use this fallback order when the ideal method is unavailable: retain the intact original product/set; composite verified assets; reduce the angle/action to a proven view; change only the scene narrative; then ask one blocking question or stop the slot. Do not substitute repeated generation for missing capability.

## Invariants

- Default to six separate square images only when the user does not specify another count, order, ratio, or size.
- Keep complete sales-item visibility in full-set slots; do not force all items into detail or action scenes.
- For a mixed 2–11-piece set, complete-set slots must make every sales item independently countable. For a bulk multipack, follow the confirmed quantity-representation mode instead of pretending a representative stack contains an exact visible unit count.
- Never add, remove, duplicate, merge, mirror, or exchange products or accessories without explicit permission.
- Never invent an unseen back, interior, underside, connector, pattern, label, or Logo.
- Default to no newly added text, icons, borders, watermarks, or fictitious branding.
- Add exact quantity labels, dimensions, marketing copy, and Logos only when requested and source-confirmed; lay them out deterministically after the product base passes QA.
- Preserve the same SKU across the set. A generated output may become an approved edit target only after full inspection; it never becomes the identity authority.
- After a targeted edit, revalidate the whole image, not only the edited region.
- For a targeted edit, separate immutable product pixels, the explicitly mutable target region, and incidental overlays. A watermark entirely inside a background that must become clean or pure white belongs to the mutable background; if it overlaps the product, surface the conflict before editing.
- After the same error survives v1 and one targeted v2 correction, change method. If the changed method still fails a high-risk identity requirement, stop rather than continue indefinite retries.
- Never report exact output dimensions before reading the finished file's actual width and height.
- Never declare a slot complete without an actual visible output.
- Never claim marketplace compliance from habit. If the user requests current policy compliance, verify current official platform requirements when available and distinguish verified rules from the user's house style.

## Prompt discipline

Give each image one primary job. Include only the current slot's sales-item IDs, authoritative reference roles, identity invariants, composition, and three to five highest-risk exclusions. Describe the correct surface or structure positively; avoid repeating long families of negative texture terms that can reinforce the artifact.

Keep P0 records and validation results outside the image-generation prompt. Use them to control the task, not as prose to overload the model.
