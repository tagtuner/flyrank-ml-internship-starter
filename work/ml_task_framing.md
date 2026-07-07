# ML Task Framing — Core Lane 2: Refresh & Opportunity Scoring

This document defines the formal mapping of the **Refresh / Content Opportunity Scoring** lane into a structured Machine Learning task.

---

## 1. ML Task Type: Binary Classification & Ranking
This problem is framed as a **Supervised Binary Classification** task coupled with a **Ranking/Scoring** layer:
- **Core Classification**: The model outputs a probability score $p \in [0, 1]$ indicating the likelihood that a page will experience a persistent traffic decline.
- **Ranking Layer**: Candidate pages are sorted in descending order of their predicted probabilities (optionally blended with baseline opportunity rules) to generate a prioritized work queue.

---

## 2. Target Label Definition (The $y$ variable)
The target label $y$ is defined over a **future-looking outcome window** (e.g., $t + 30$ days), using inputs from a **prior historical feature window** (e.g., $t - 90$ days to $t$):

$$
y = \begin{cases} 
1 & \text{if impressions or sessions drop by } > 20\% \text{ in the target window } [t+1, t+30] \\
0 & \text{otherwise (traffic remains stable, fluctuates normally, or grows)} 
\end{cases}
$$

### Leakage Guardrails:
- Features are calculated *strictly* from the feature window $[t-90, t]$.
- Suffix trend indicators (like `trend_direction` and `trend_pct` in the target window) are strictly excluded from the training feature set.
- Minimum volume thresholds (e.g., $\ge 500$ impressions in GSC over 90 days) are applied to filter out low-volume search noise from the label calculations.

---

## 3. Success Metrics
To evaluate the model's effectiveness, we use metrics that match the operational capacity of the review team:

1. **Primary Metric: Precision@K (e.g., Precision@50)**
   - *Formula*: Of the top $K$ pages ranked highest by the model, what fraction actually experienced a traffic decline in the future window?
   - *Why it matters*: Reviewing content takes human hours. If the editorial team has the capacity to audit $50$ pages per week, we must guarantee that those $50$ candidates represent high-value opportunities.
2. **Secondary Metrics: Average Precision (AP) & ROC AUC**
   - *Why they matter*: To assess the ranking quality across the entire website inventory and ensure the model separates stable/growing pages from declining ones.

---

## 4. Operational Actions Supported
The ranked output queue directly supports content managers and editors in executing one of the following concrete actions:
- **Content Refresh (Optimize)**: Updating outdated statistics, expanding thin sections, or rewriting sections showing intent mismatch.
- **Content Consolidation (Merge)**: Merging pages that exhibit internal cannibalization (sibling URLs ranking for the same keyword cluster).
- **Pruning**: Removing or redirecting low-value pages that fail to capture demand and have decayed beyond recovery.

---

## 5. Why ML Beats Fixed Rules
A typical rule-based threshold (e.g., `if age > 180 days AND clicks < 10 then flag`) fails in complex real-world search environments:
1. **Non-Linear Feature Interaction**: A page might be new (`age < 90`) but experiencing position slippage on page one alongside collapsing CTR—a critical decay risk that static rules miss. ML trees automatically model these interactions.
2. **Domain & Client Generalization**: Traffic scales vary enormously between clients. A "low traffic" page on a major enterprise domain might be a "high traffic" page on a small blog. ML models adapt to client-group parameters (`client_hash_id` grouping) rather than relying on arbitrary hardcoded counts.
3. **Continuous Probability Scoring**: ML outputs a continuous probability, allowing flexible capacity adjustments (e.g. pulling the top 20 pages this week, 100 pages next week) instead of binary true/false classifications.
