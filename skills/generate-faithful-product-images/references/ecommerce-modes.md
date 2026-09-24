# Ecommerce delivery modes

Read this file for platform-facing image sets, multi-SKU work, SKU previews, bulk quantities, or several requested output groups.

## 1. Route by the user's actual request

| Request | Deliverable behavior |
|---|---|
| General product-image request with no count | Use the default six-slot carousel from `workflow.md` |
| One hero or white-background image | Produce one hero only; do not add scenes or text unless requested |
| N scenes or additional scenes | Produce exactly N independent new scenes; do not regenerate the carousel |
| Dimension/spec image | Require reliable values and measurement locations; create a clean product base, then add exact layers deterministically |
| SKU preview | Lock the SKU, pack count, product arrangement, carton role, and exact label before layout |
| Background replacement | Treat the product as immutable unless the user names product changes; classify background-only and product-overlapping watermarks separately |
| Targeted edit | Change only the named target, then inspect the entire image for collateral drift |
| Several styles, colors, sizes, or groups | Create one isolated P0 and plan per SKU/output group; validate the aggregate requested total with `scripts/validate_batch.py` |

Do not silently convert a scene-only request into a full listing set or a single-image request into six images. Do not merge separate requested outputs into a collage merely to finish faster.

## 2. Platform and B2B handling

- The user's current platform, slot order, pixel requirements, and house style override defaults.
- Platform names are routing context, not permission to invent badges, fulfillment claims, certifications, stock status, discounts, or promotional text.
- Add words such as wholesale, custom Logo, factory supplier, MOQ, pack count, warehouse, or delivery claims only when the user requests or confirms them.
- If the user asks for current marketplace-policy compliance, verify official current rules when available. Do not claim compliance based only on memory or common practice.
- A style reference controls composition, background, camera, lighting, and mood only. It cannot donate its product, Logo, packaging, text, pattern, or accessories.
- Default commercial style is clean, credible product photography: accurate scale, natural contact shadows, realistic material response, restrained props, and the product as the first visual subject.
- If the image tool cannot render the exact requested pixels, first create the correct aspect ratio, then use `scripts/finalize_image.py` to resize, crop, or pad without stretching the product. Prefer `contain`; use `cover` only after confirming that its centered crop will not cut the product. Verify the final file before reporting dimensions or file size.

## 3. Multi-SKU isolation

Treat any change in color, size, structure, layer count, slot count, accessory count, pack count, label, or packaging as a possible new SKU.

For separate SKU outputs:

1. Create separate P0 manifests and plans.
2. Use only that SKU's original references in its identity set.
3. Keep its dimensions, quantity text, carton, accessories, and color names mapped to that SKU.
4. Do not use one generated SKU as the product reference for another.
5. Deliver separate files unless the user explicitly requests a comparison image.

For an explicitly combined comparison:

- Record every SKU ID and source.
- Preserve true relative size when reliable dimensions exist.
- Keep labels adjacent to the correct SKU and add them deterministically.
- Do not clone one unit and resize or recolor it to impersonate a distinct SKU when structure or proportion differs.
- If the available references cannot prove the comparison, ask for the missing view or create separate images.

## 4. Bulk multipacks and master cartons

First identify what the number means: individual pieces, sets, packs, cartons, or units per carton. Record nested equations such as `12 sets × 5 sold pieces = 60 sold pieces`; do not flatten a hierarchical bundle into an incorrect piece count.

Use one of four honest visual strategies:

1. `exact_items`: every unit is present and countable in a verified source.
2. `exact_composite`: retained assets are laid out deterministically to the exact count.
3. `representative_stack`: a neat sample group conveys scale while deterministic text states the real quantity.
4. `carton_label`: an intact or blank verified carton plus exact deterministic quantity text communicates the pack.

Rules:

- Never rely on free generation to create a large exact count.
- A representative stack must not be described as individually countable.
- Do not invent carton size, weight, shipping marks, printed brand, barcode, tape pattern, or certification.
- If the user supplies only a product image and asks to add a carton, use a plain proportional carton unless a specific carton reference is provided.
- Put quantity text on the requested surface only and preserve exact capitalization, spacing, slash, unit, and pluralization.
- In the plan, mark the carrying slot with `requires_exact_text: true`, `text_role: "quantity"`, its `text_source`, and `layout_method: "deterministic_layout"`.
- When the user says “only change the text,” preserve product, box, arrangement, background, camera, lighting, and every unmentioned label.

## 5. Exact text, Logo, dimensions, and claims

Create exact layers only from user-confirmed content or a clear current source.

- Lock the final string before layout; preserve punctuation, accents, capitalization, units, and line breaks.
- For a Logo, use the supplied asset. Do not redraw, approximate, stretch, thicken, translate, or replace it unless requested.
- For engraving or print mockups, preserve the Logo geometry and change only the requested material interaction, placement, scale, or color.
- For dimensions, preserve original units. Convert only when requested and calculate from `1 inch = 2.54 cm`.
- Dimension arrows must terminate on the actual measured outer points. Validate product, text, and arrows as separate layers.
- Do not add unverified material, capacity, certification, performance, stock, warehouse, shipping, or compatibility claims.

## 6. Series diversity without identity drift

Keep product identity constant while varying presentation. Across a set, vary purpose first, then camera, composition, light, and environment.

For two scenes, record at least four scene axes and require three differences. Useful axes are:

- environment;
- camera height and crop;
- light direction or time of day;
- action or product state;
- props;
- tone/color temperature;
- intended audience or occasion.

When a current project scene ledger is available, compare the most recent relevant sets. If it is unavailable, do not claim historical de-duplication; differentiate against the current visible task only.

Update a user-maintained scene ledger only after the user confirms final outputs and only when the current environment allows the authorized update. Keep SKU-specific history outside this skill.
