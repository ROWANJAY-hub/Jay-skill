# Traffic-First Learning Model

Use this reference when ranking candidate titles, ingesting returned performance, updating category weights, or preparing the future web workflow. Apply it together with [continuous-learning.md](continuous-learning.md) whenever persistent research memory or model adaptation is involved.

## Objective hierarchy

1. Product truth and category relevance are hard gates.
2. Maximize qualified search opportunity and downstream inquiries/orders.
3. Prefer recent, direct, comparable evidence and stable estimates.
4. Use differentiation and uncovered phrases only after the primary traffic entrance is protected.

Portfolio coverage is a diagnostic. It is not a success KPI.

## Provisional title score

Score eligible candidate titles on a 0–100 scale:

`Score = 0.45 × Traffic + 0.30 × Conversion + 0.15 × Evidence + 0.10 × Differentiation`

- `Traffic`: current platform search-index percentile, comparable store search-impressions-per-day percentile, and capped trend signal. When all are available, start with 60% / 25% / 15% inside this component. Cap extreme growth before normalization so a low-base 400% jump cannot outrank durable demand by itself.
- `Conversion`: smoothed funnel evidence. Start with 20% CTR, 50% inquiries per 1,000 search impressions, and 30% submitted orders per 1,000 search impressions. Treat orders as decisive qualitative evidence when counts are sparse, but do not let one event create an unstable large numeric jump.
- `Evidence`: source directness, same-category/SKU comparability, sample confidence, and recency. A public marketplace page receives no numeric traffic credit; repeated cross-date, cross-platform research may strengthen wording or positioning confidence under the continuous-learning rules.
- `Differentiation`: truthful product fit and useful distinction. Uncovered-portfolio coverage may supply no more than half of this component, so its total contribution is capped at 5 points.

If a component is unavailable, renormalize only the non-coverage components with valid evidence. Do not convert blanks to observed zeros. Product relevance remains a gate, and coverage can never select the primary phrase.

Record internal candidates in `候选评分` when maintaining the workbook. A candidate is eligible only when the product-relevance gate and protected-primary-phrase formula both pass. Missing component scores intentionally block ranking rather than acting as zero. If a category prior or documented renormalization is used, enter the resulting score and cite that method plus its source IDs or dated windows; do not invent precision when evidence is sparse.

## Primary phrase protection

Choose the primary phrase before composing the title. It must be the highest-scoring eligible core route for the actual product category. Record it with the model version and pass it to `title_guard.py --primary-phrase`.

When similarity is high, change ordering, attributes, packaging wording, or low-value components first. Do not swap the protected phrase for a weaker uncovered term. If the traffic phrase and duplicate constraint cannot both pass without inaccurate wording, stop and disclose the conflict.

## Small-sample smoothing and recency

For a funnel event rate, use a category prior rather than raw rates:

`Smoothed Rate = (Events + Prior Rate × Prior Strength) / (Exposure + Prior Strength)`

- Derive the prior rate from comparable active products in the same category and window.
- Start with prior strength 50 impressions until enough project history supports recalibration.
- Keep CTR, inquiry rate, and order rate separate; do not add raw percentages with different denominators.
- Suggested recency half-life: 28 days for hot-keyword snapshots and 56 days for product-performance observations. Preserve older evidence for trends and audit.

Do not attribute a multi-keyword title's result to one contained phrase unless there is a controlled title-version comparison or repeated cross-SKU evidence.

## Feedback eligibility and attribution

Append feedback by product/SKU and title version. Record the source/evidence ID, publication date, observation start/end, search impressions, clicks, inquiries, submitted orders, and whether price, main image, promotion, ad status, availability, or fulfillment changed. Reject overlapping observation windows for the same SKU and title version so outcomes are not counted twice.

- `Eligible for update`: valid source/version linkage, a non-overlapping window of at least 7 observed days, no material confounder, and either at least 100 search impressions or at least 2 combined inquiries/orders.
- `Directional only`: smaller clean samples. Retain them, but do not automatically demote a protected phrase.
- `Reference only`: missing title-version linkage, mixed windows, or material confounders.

These thresholds are starting controls, not universal truths. Recalibrate them by category once enough data accumulates.

## Stable weight updates

- Maintain separate category priors for set-led, bowl-led, whisk-led, travel-led, and adjacent-product routes.
- Separate dynamic category/phrase weights from the top-level 45/30/15/10 component weights. Update category/phrase weights routinely when eligible evidence accumulates; recalibrate the top-level components only after multi-SKU evidence shows a stable improvement.
- Store dynamic keyword/category weights on a normalized 0–1 scale and limit each ingestion cycle to ±0.10, or 10 percentage points. This still allows a new zero-weight keyword to enter while preventing a large jump.
- A repeated research pattern may nominate or support a phrase, but it cannot by itself receive Traffic or Conversion credit. Pair it with current keyword evidence or eligible backend performance before applying a numeric weight change.
- Require two comparable underperforming windows before demoting an established primary phrase, unless a large clean sample provides strong contrary evidence.
- Never learn from draft titles, supplemental images, or superseded versions outside their actual publication windows.
- Store the old and new weights, evidence IDs, reason, effective date, and model version. Do not rewrite history.
- Use `权重更新日志` for every applied change. The workbook formula caps the proposed adjustment; never bypass the cap by editing the resulting new-weight cell.

## Controlled exploration

Reserve about 10% of new-title opportunities for learning when product volume permits. Test a rising or uncovered phrase in a secondary position while keeping the strongest core phrase intact. For small portfolios, use sequential title versions rather than simultaneous variants and avoid changing other conversion drivers during the observation window.

## Decision metrics

- Primary outcome: submitted orders per 1,000 search impressions.
- Earlier outcome: qualified inquiries per 1,000 search impressions.
- Driver: search CTR.
- Diagnostic: total search impressions and position/category mix.
- Guardrails: product accuracy, title policy compliance, version attribution, sample confidence, and absence of material confounders.
- Portfolio coverage: reporting and experiment-planning only.
