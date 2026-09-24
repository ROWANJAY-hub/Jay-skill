# Evidence and Ledger Rules

## Contents

- Source hierarchy and boundaries
- Persistent knowledge base
- Installed baseline
- Periodic source ingestion
- Ledger structure
- Traffic model and feedback state
- Rolling coverage and duplicate control
- Formal-title lifecycle

## Source hierarchy and boundaries

Use evidence in this order:

1. User-provided platform keyword and product-performance exports.
2. User-confirmed product facts, images, specifications, and assortment rules.
3. Fresh, product-specific Alibaba and cross-platform marketplace research for current wording, positioning, configuration, and observable page signals only.
4. Rolling uncovered terms from the title ledger.
5. General language knowledge.

Attach every numeric claim to its source date and time window. Do not merge unlike metrics: search index, search impressions, clicks, CTR, inquiries, orders, seller index, and growth are separate fields. A marketplace result page can confirm that `Leather Carrying Case` or `Snowflake Glaze` is current wording; it cannot prove search volume, growth, or conversion.

Complete the workflow in [live-market-research.md](live-market-research.md) for every genuinely new SKU image, original title, or rewrite before locking the primary phrase. User-provided Alibaba exports remain the strongest quantitative evidence. Public pages may corroborate current nouns, configurations, positioning, popularity badges, reorder labels, ranks, reviews, and prices only with the platform, access date, product match, and limitations recorded. Never convert those visible signals, result counts, or snippets into fabricated search-volume or conversion scores.

When sources disagree, prefer the newest directly comparable platform window. Keep the older row for audit and possible trend analysis. Never silently overwrite history.

## Persistent knowledge base

Use `assets/learning-memory.json` as the append-only bridge between live marketplace research, final title decisions, returned backend performance, and later model reviews. Follow [continuous-learning.md](continuous-learning.md) for evidence promotion and weight-update rules. Raw source files remain in the source registry; formal titles, performance, parameters, and applied weight changes remain in `assets/current-ledger.xlsx`. Do not duplicate raw workbooks inside the knowledge base.

## Installed baseline

The installed baseline contains:

- `HotKeyword-2026-08-20-matcha bowl`: keyword, search index/growth, CTR/growth, seller index/growth.
- `Products-2026-08-15`: product performance for 2026-08-09 through 2026-08-15.
- `HotKeyword-2026-08-20-matcha kit`: the same hot-keyword metric family.
- `matcha set` export created 2026-08-22 and labeled as a recent-seven-day source in the supplied filename/context.
- `current-ledger.xlsx`: 31 formal titles through 2026-08-31 plus keyword detail, rolling coverage, usage notes, and source evidence.
- `recent-session-titles.json`: formal titles generated after that workbook snapshot and therefore included separately until merge.

Baseline values are dated evidence, not permanent rankings. New valid exports may change keyword priority.

## Periodic source ingestion

Inspect workbook contents and headers, not filenames alone. Supported signatures include:

- Hot keyword: `关键词`, `搜索指数`, `搜索涨幅`, `点击率`, `卖家规模指数`.
- Product performance: `产品ID`, `产品名称`, `搜索曝光次数`, `搜索点击次数`, `搜索点击率`, `询盘个数` and related outcome columns.
- Rolling ledger: sheets named `标题台账`, `关键词明细`, `覆盖汇总`, `使用说明`, and `Source证据`.

For each periodic feed:

1. Run `scripts/source_registry.py FILES...` without `--commit`.
2. Review detected source type, sheet/header mapping, data dates, time windows, and duplicate status.
3. If a required metric is ambiguous or the file is malformed, stop and ask only about that consequential ambiguity.
4. When a new file is supplied for title learning or the user asks to feed/update data, rerun with `--commit`. The script archives the original bytes and appends a hash-keyed version record under the standing learning scope.
5. Use the newest valid source for current optimization while preserving every older version.
6. Add normalized evidence rows to `Source证据` when updating the workbook. Record the source name, data date, time range, keyword/title, metric type, raw metrics, evidence level, and a boundary note.
7. Link performance rows to product/SKU, title version, publication date, and model version before using them for learning. Mark price, main-image, promotion, and ad changes as possible confounders.
8. Recalculate coverage only after formal titles change; source ingestion alone must not fabricate title coverage or automatically change keyword weights.

Do not register a byte-identical file twice. A same-named file with a different hash is a new version and must be appended, not substituted.

## Ledger structure

Maintain these sheets and fields:

- `标题台账`: number, date, Chinese product name, English title, procurement expression, protected core phrase, optional new coverage phrase, verified attributes, formula-driven character count, evidence tier, latest-five maximum similarity, contiguous-six-word result, notes, product/SKU, category route, title version, model version, formula-driven core-phrase protection, version status, and publication date.
- `关键词明细`: title number/date, tier, phrase, category, coverage note.
- `覆盖汇总`: tier, phrase, category, weight, evidence status, cumulative/day/7-day/30-day counts and statuses.
- `使用说明`: scope, exclusions, metric boundaries, formula definitions, update date, and changes made.
- `Source证据`: immutable dated source evidence and public-wording evidence with explicit limitations.
- `模型参数`: model version, objective, component weights, recency half-lives, coverage cap, exploration share, learning threshold, and maximum per-cycle adjustment.
- `候选评分`: product/SKU, category route, candidate title, protected primary phrase, relevance gate, traffic/conversion/evidence component scores, product-differentiation points, capped coverage bonus, formula-driven core protection, hard-gate result, composite score, and evidence IDs.
- `表现回传`: product/SKU, category route, title version, title number/text, primary and secondary entrances, model version, publication and observation dates, impressions, clicks, inquiries, submitted orders, derived funnel rates, price/image/ad/availability confounder flags, comparability, confidence, learning eligibility, source/evidence ID, data validation, overlap validation, and notes.
- `权重更新日志`: model version, effective date, category route, keyword, old weight, proposed change, formula-capped applied change, new weight, eligible-window count, evidence IDs, reason, and status.
- `assets/learning-memory.json`: linked baseline evidence, raw dated research observations, final title decisions, recurring learned patterns, and model reviews. Store evidence IDs rather than copying quantitative source tables.

Preserve formulas, formats, and the established sheet structure. Use spreadsheet formulas for derived counts and character length where practical. Inspect and render the workbook after edits.

## Traffic model and feedback state

Read [traffic-learning.md](traffic-learning.md) before updating category weights or using returned performance. Keep separate models or priors for set-led, bowl-led, whisk-led, travel-led, and adjacent-product routes; do not let a high-volume broad set phrase automatically govern a bowl-only SKU.

The title-generation record stores the model version and protected phrase used at that time. Returned outcomes are appended as observations and may inform only a later model version. Raw observations are immutable; corrections append a replacement note rather than silently rewriting the original source.

Use portfolio coverage as a monitoring view and controlled exploration budget. It must never be used as the success KPI or as a reason to demote the strongest relevant phrase.

## Rolling coverage and duplicate control

- Coverage windows: current day, trailing 7 days, and trailing 30 days based on formal-title dates.
- Legacy coverage weights A=3, B=2, C=1 remain only for reporting continuity; they are not traffic-ranking weights.
- Similarity scope: the latest five active formal titles plus any newer formal titles in the current conversation or `recent-session-titles.json`.
- Similarity metric in the bundled guard: Python `SequenceMatcher` on lowercase, whitespace-normalized title text.
- Rewrite threshold: 60% or higher against any comparison title.
- Phrase collision: any exact contiguous sequence of six or more normalized word tokens is a hard failure.

Use uncovered terms to diversify secondary wording within the exploration budget, but never sacrifice product accuracy, primary traffic phrase, or proven conversion-bearing language to satisfy coverage statistics.

## Formal-title lifecycle

- Count only the single title presented as the final output for a product.
- Exclude internal candidates and brainstorming drafts.
- A product image without a final title creates no title row.
- A supplemental image of the same SKU creates no new row.
- If the final title is revised before work begins on another SKU, mark the earlier version as superseded and exclude it from active similarity and coverage while retaining an audit note.
- If a new SKU genuinely differs in bowl shape, glaze, color, case, configuration, or target search path, create a new formal row after validation.
