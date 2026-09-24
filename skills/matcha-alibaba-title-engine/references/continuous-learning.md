# Continuous Learning and Knowledge Base

Use this reference whenever a title cycle produces new live research, the user supplies new backend data, a scheduled review returns performance, or a model/weight change is considered.

## Knowledge architecture

- `assets/source-registry.json` and `assets/baseline-sources/`: immutable user-supplied keyword, product-performance, and ledger files.
- `assets/current-ledger.xlsx`: formal titles, candidate scores, parameters, linked performance, and applied weight-change history.
- `assets/recent-session-titles.json`: active formal titles not yet merged into the workbook.
- `assets/learning-memory.json`: dated live-research observations, final title decisions, recurring patterns, and model reviews.

Link records with evidence IDs. Do not copy raw quantitative tables into the learning memory or collapse unlike platforms and windows into one metric.

## Standing update scope

The user has authorized persistent, append-only learning for this matcha-title skill. During ordinary title work and scheduled reviews, append verified research observations, final title decisions, returned performance links, synthesized patterns, and eligible bounded model reviews without asking again. Validate and save the skill after a material update.

This authority is narrow. Do not rewrite historical records, alter unrelated skills or files, publish externally, or treat a draft as a formal learning event. The system learns when this skill is invoked or an authorized scheduled review runs; do not claim unscheduled background collection.

## Learning loop

1. Identify the SKU and category route from verified facts.
2. Read the newest comparable user data and existing learning memory.
3. Run image-specific live research and append materially useful pages as raw observations.
4. Generate one guarded final title and append its title decision with the model version and evidence IDs.
5. On a later review, link non-overlapping backend results to the exact SKU, title version, publication window, and confounders.
6. Synthesize recurring patterns only across multiple observations; retain contrary evidence and limitations.
7. Apply a bounded weight change only when the eligibility rules below pass. Create a new model version and record both the old and new state.

Use the supplied product ID or SKU as the stable link. If none exists yet, create a stable temporary identifier from the product route and current image/session; replace it by appending a linkage note when the platform ID becomes available rather than rewriting history.

## Evidence promotion

Use these states:

- `raw`: one dated page, query, product match, or returned observation.
- `directional`: a plausible pattern that is useful for wording or controlled exploration but is not strong enough for an automatic weight change.
- `eligible`: evidence that satisfies the applicable backend sample rules and has sufficient product/category comparability.
- `retired`: superseded or no longer current, retained for audit rather than deleted.

As a starting threshold, require at least three closely matched observations spanning at least two platforms and two research dates before calling a marketplace pattern recurring. Equivalent stronger evidence may qualify when limitations are explicit. A single bestseller badge, result count, review count, rank, price, or competitor title is always raw evidence.

## Hybrid weight updates

Use live research and backend data for different jobs:

- User keyword exports provide current demand and trend evidence.
- User product-performance exports provide search exposure, CTR, inquiries, orders, and downstream validation.
- Repeated live research provides current buyer language, configuration, positioning, and cross-platform consistency.

Dynamic category/phrase weights may change when the evidence points in the same direction under either path:

1. At least one eligible backend performance window plus corroborating current keyword or recurring-research evidence.
2. Two comparable eligible backend windows, with live research used to explain or challenge the interpretation.

When a current keyword export and recurring research support a new phrase but eligible backend performance does not yet exist, allow only a provisional adjustment of at most ±0.05 and keep the phrase in a secondary controlled-exploration position. Research alone never receives Traffic or Conversion points and cannot demote an established primary phrase.

Keep the existing ±0.10 maximum per ingestion cycle for evidence-backed dynamic category/phrase weights. Require the stricter demotion rule in `traffic-learning.md` for established phrases. Review the top-level Traffic/Conversion/Evidence/Differentiation weights only after at least three comparable SKUs and three eligible non-overlapping windows show a stable relationship; prefer a holdout or later-period check before retaining that change.

Every applied change must include the old value, proposed value, capped applied value, affected category route, evidence IDs, effective date, reason, and new model version in both the workbook log and model-review memory. Never back-edit the score recorded at publication.

## Contradictions and decay

Prefer the newest directly comparable Alibaba evidence for current decisions, but preserve older observations for trend analysis. Apply the configured recency decay to quantitative evidence. If live-market language conflicts with backend outcomes, keep both: use live wording as a hypothesis and let clean performance windows decide whether the phrase earns or loses numeric weight.
