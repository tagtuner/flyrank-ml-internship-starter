# Research Question Framing & Provisional Lane Selection

## 1. Provisional Lane Selection
- **Selected Lane**: `Refresh / Content Opportunity Scoring` (Core Lane 2)
- **Status**: Provisional Selection (Subject to evaluation and final adjustments during active analysis phases)

---

## 2. Core Research Question
*How can we prioritize declining pages for manual review and refresh to maximize potential organic traffic recovery under constrained editorial and writing capacity?*

---

## 3. Unit of Analysis
The unit of analysis is the unique page level for a specific client:
- **Identifier**: `client_hash_id` × `content_hash_id` (representing a single unique URL under a client's site context).

---

## 4. Proposed Output
A prioritized, ranked review queue containing candidate pages for optimization. The queue will output:
1. An **Opportunity Score** indicating priority.
2. **Confidence Level** based on volume signals.
3. Specific **Reason Codes** detailing the triggers for recommendation (e.g., `stale_visible_page`, `page_one_decay_risk`, `low_ctr_visible_page`).

---

## 5. Target Decision & Action
- **Decision Point**: The SEO Manager or Content Editor decides whether a suggested page actually warrants resources for revision, merging, pruning, or if it should be left alone.
- **Action**: A writer/editor revises the page's copy, updates outdated facts, expands thin sections, or merges it with competing sibling pages.

---

## 6. Risk Assessment: Cost of Wrong Recommendations
Because recommendations are directional indicators rather than absolute certainties, we must balance the cost of errors:
- **False Positives (Wasted Effort)**: The model flags a page that does not need a refresh (e.g., dropping due to temporary seasonality or structural site-wide changes). The writer spends hours updating it, resulting in zero traffic recovery and wasted budget.
- **False Negatives (Missed Decay)**: The model fails to identify a critical high-traffic page undergoing quiet, steady search visibility loss. Sibling search terms are lost permanently to competitors, resulting in a sustained decrease in site conversions and revenue.

---

## 7. Why Data and ML are Required
- **Scale**: A typical website inventory spans thousands of unique pages, making manual monitoring impossible.
- **Multi-Variable Complexity**: Traffic decay is rarely caused by a single factor. It is a non-linear combination of position slippage, click-through rate decay, content age, and competitor movement. ML models (like Decision Trees or Random Forests) learn these interactions from historical data without relying on rigid, arbitrary thresholds.

---

## 8. Cautious Framing & Guardrails
- **Observational Limitations**: This model identifies *review opportunities* based on historic correlation; it does not claim to decode Google's proprietary search algorithm.
- **Causal vs. Correlation**: Flagging a page for "decline risk" does not guarantee that writing more words will cause traffic to recover. Editorial updates must be verified through post-action observations or controlled experiments.
- **Client Safety**: All references, inputs, and outputs will remain strictly pseudonymized and free of raw queries, domains, or customer identities.
