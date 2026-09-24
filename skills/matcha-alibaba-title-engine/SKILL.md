---
name: matcha-alibaba-title-engine
description: Generate, audit, and continuously improve traffic-first Alibaba International titles for matcha bowls, whisks, kits, travel sets, and adjacent matcha tea tools. Combine verified product facts and dated user exports with fresh, image-specific marketplace research, then persist evidence-backed learning across title cycles. Use when the user supplies product images, Chinese titles, keyword/product-performance exports, post-publication feedback, or asks to update the versioned title/source ledger. Do not use for unrelated product categories.
---

# Matcha Alibaba Title Engine

Produce one accurate, traffic-first Alibaba title from verified product facts, dated platform evidence, fresh product-specific marketplace research, persistent learning memory, and versioned performance feedback. Optimize for qualified search traffic and downstream inquiries/orders. Treat portfolio coverage as a capped diagnostic and exploration signal, never as the objective.

## Route the request

- For a new product image, Chinese original title, or title rewrite, read [references/title-policy.md](references/title-policy.md), [references/live-market-research.md](references/live-market-research.md), [references/continuous-learning.md](references/continuous-learning.md), [references/evidence-ledger.md](references/evidence-ledger.md), and [references/baseline-evidence.md](references/baseline-evidence.md). Treat the baseline snapshot as dated and let newer valid uploads supersede its current-ranking role.
- For new keyword, product-performance, ledger, or post-publication feedback files, read [references/evidence-ledger.md](references/evidence-ledger.md), [references/traffic-learning.md](references/traffic-learning.md), and [references/continuous-learning.md](references/continuous-learning.md), then inspect them with `scripts/source_registry.py`.
- For a ledger, knowledge-base, or model diagnosis, read [references/continuous-learning.md](references/continuous-learning.md), then audit source boundaries, product/title version linkage, attribution quality, formal-title scope, coverage formulas, similarity rules, and small-sample handling before proposing changes.

## Follow the core workflow

1. Establish product identity and SKU continuity before selecting keywords. Treat additional angles of the same SKU as supplemental evidence, not a new product.
2. Read the current conversation, uploaded files, `assets/current-ledger.xlsx`, `assets/recent-session-titles.json`, `assets/learning-memory.json`, and the source registry. Use uploaded newer data for the current decision without deleting older evidence or mixing unlike windows.
3. Extract only visible or explicitly supplied facts: product type, material, glaze, color, shape, spout, case, tray, and included tools. Resolve contradictions conservatively; omit uncertain claims.
4. Run fresh, image-specific market research before locking the title. Follow [references/live-market-research.md](references/live-market-research.md): check current Alibaba wording first, cross-check at least one relevant marketplace, open the pages that materially affect the decision, and do not reuse generic research from a different SKU.
5. Append qualifying live observations to `assets/learning-memory.json` with `scripts/learning_memory.py`. Keep raw observations separate from synthesized patterns; one page or one research date does not become a learned rule.
6. Apply product relevance as a hard gate. Rank eligible phrases using user-provided quantitative evidence for traffic and funnel signals, and live marketplace evidence for current wording, configuration, and positioning. Coverage may contribute at most five points and must not replace the strongest eligible primary phrase.
7. Lock the highest-value exact primary phrase for the product category. Score internal candidates using the current `模型参数` values and the `候选评分` hard gates. Build one main title by default with a truthful procurement/customization expression near the front, the protected primary phrase, useful differentiators, and only high-value components. An uncovered term is optional, not mandatory.
8. Run `scripts/title_guard.py` with `--primary-phrase` against the current ledger and recent session titles. Restructure attributes before changing the protected core phrase. Rewrite until all hard checks pass: no more than 128 characters, below 60% similarity to each of the latest five active formal titles, and no repeated contiguous six-word sequence.
9. Before returning, record the final title decision, model version, category route, and evidence IDs in the learning memory and recent-title state. Save the skill after validated append-only changes so later cycles can learn from them.
10. Return a concise Chinese product name, one final English title, exact character count, protected primary phrase, user-data source date/window, live-research date/platforms, selected secondary entrances, and validation result. Do not present multiple alternatives unless requested.

## Maintain evidence and state

- `assets/current-ledger.xlsx` is the installed baseline ledger. Preserve its formatting and formulas when updating it; use the Spreadsheets skill for workbook edits.
- `assets/source-registry.json` records immutable source-file versions and hashes. Never replace a historical source merely because a newer export has the same name or keyword.
- `assets/learning-memory.json` is the persistent knowledge base for dated live-research observations, final title decisions, synthesized patterns, and model reviews. Keep it append-only and validate it with `scripts/learning_memory.py`.
- `assets/baseline-sources/` contains archived source snapshots. Do not edit archived originals.
- `assets/recent-session-titles.json` bridges formal titles produced after the workbook snapshot. Include these in similarity checks until they are merged into the workbook.
- When the user feeds data, updates the source pool or ledger, or returns performance, inspect first and then register only genuinely new files. Normalize them by category and title version. Update weights only through the eligibility and stabilization rules in `traffic-learning.md` and `continuous-learning.md`.
- The user has authorized ongoing, append-only maintenance of this skill's research memory, final-title state, performance links, and eligible bounded weight updates during ordinary matcha-title work and scheduled reviews. This standing authorization does not extend to unrelated files, external publishing, or destructive rewrites. Validate and save material learning updates so they persist.
- Add only final titles to rolling coverage. Exclude brainstorming drafts. If a revision supersedes the previous title for the same SKU before a new product begins, retain the audit note but exclude the replaced version from active coverage.
- Preserve model versions and feedback windows. Never use future outcomes to rewrite the score that was recorded at publication time; calculate a new model version for the next round.
- Append every applied category/keyword adjustment to `权重更新日志`, including evidence IDs, old weight, proposed change, capped change, new weight, and effective model version.
- Treat routine live research as dated decision evidence, not a substitute for a platform export. Record pages and access dates when they affect a title, but never register marketplace result counts, review counts, badges, rankings, or snippets as Alibaba search volume, growth, CTR, inquiry, order, or conversion metrics.
- Let dynamic phrase and category weights evolve when repeated research patterns and eligible backend evidence support the same direction. Keep top-level component weights conservative, version every applied change, and preserve the full audit trail.

## Use the bundled checks

Inspect or register source files:

```bash
python scripts/source_registry.py FILES...
python scripts/source_registry.py --commit FILES...
```

Validate or inspect the persistent learning memory:

```bash
python scripts/learning_memory.py validate
python scripts/learning_memory.py summary
python scripts/learning_memory.py --help
```

Validate a title:

```bash
python scripts/title_guard.py \
  --title "FINAL TITLE" \
  --primary-phrase "Matcha Set" \
  --ledger assets/current-ledger.xlsx \
  --recent-json assets/recent-session-titles.json
```

Pass each unsaved title from the current conversation with another `--recent-title`. Pass `--piece-count N` only when the SKU has a fixed, verified count.
