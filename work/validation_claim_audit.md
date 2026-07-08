# Validation & Research Claim Audit — Content Refresh Opportunity Scoring

This document presents a comprehensive audit of our machine learning models, validation architecture, potential leakages, failure modes, and claims validity for the **Content Refresh Opportunity Scoring** lane.

---

## 1. Validation Design & Split Architecture

To evaluate the predictive accuracy of our models, we implement a **5-fold GroupKFold validation split grouped by `client_id`**.

### Rationale:
*   **Preventing Domain-Specific Keyword Leakage**: Standard random train/test splits would allocate pages belonging to the same client to both training and test sets. Since pages under the same client often target identical topics or share domain authority, the model would overfit to specific client signatures instead of learning generalizable SEO signals.
*   **Real-world Deployment Emulation**: Grouping by `client_id` ensures that the model is always evaluated on clients it has never seen during training, simulating how the ranking engine behaves when a new company integrates with the FlyRank ecosystem.
*   **Time-Aware Validation Alternative**: While time-series validation (e.g. rolling-window split) is a common design, our feature matrix uses a **strict historical 90-day window** (GSC performance prior to prediction date) to predict target labels in a **prospective 30-day target window** (traffic trend after prediction date). Because features and target variables are separated by a temporal boundary, data leakage from overlap is naturally mitigated, making GroupKFold a robust and generalizable validation strategy.

---

## 2. Feature Leakage & Privacy Audit

We conducted a strict audit of the features fed into the model. The following variables were identified as hazardous and were **completely dropped** during preprocessing:

| Dropped Field | Leakage / Privacy Risk Type | Prevention Rationale |
| :--- | :--- | :--- |
| `client_id` / `content_id` | Private Identifiers | Prevents the model from memorizing specific client or content properties. |
| `trend_direction` / `trend_pct` | Target Window Leakage | These indicators are derived directly from target-window performance; including them would lead to near-perfect but fraudulent training metrics. |
| `impressions_last_30d` / `clicks_last_30d` | Target Window GSC Metrics | Direct prospective GSC outcomes. Including these features leaks future test outcomes back into the historical training phase. |
| `health_score` | Product-Flag Leakage | An existing, hand-coded heuristic indicator. Training on this would cause the model to copy the existing heuristic rules rather than finding novel data signals. |

---

## 3. Failure Modes & Error Analysis

A detailed inspection of the model's predictions revealed two primary failure modes:

### Failure Mode A: Low-Impression Volatile CTR (Noise-driven Error)
*   **Description**: The model frequently prioritizes low-traffic pages (e.g. pages with 1 impression and 0 clicks) for rewrite actions because they exhibit a "0% CTR" profile, which looks highly sub-optimal.
*   **Why it occurs**: The mathematical calculation of CTR ($\frac{\text{Clicks}}{\text{Impressions}}$) becomes highly volatile at low volumes. A single click change swings CTR from 0% to 100%.
*   **Mitigation**: Implement a minimum impression threshold filter (e.g. `impressions_90d >= 100`) before running predictions, or use additive smoothing (e.g., Laplace CTR smoothing) to pull low-volume pages back toward the client's average CTR.

### Failure Mode B: Seasonal Traffic Volatility (Volume-driven Error)
*   **Description**: High-ranking pages targeting seasonal keywords (e.g., "tax return deadlines" or "summer pool safety tips") are incorrectly flagged as decaying (`is_declining = 1`) when their traffic drops off-season.
*   **Why it occurs**: The model's historical features do not capture search demand seasonality. It sees a drop in traffic and assumes the page's ranking or content quality has decayed.
*   **Mitigation**: Integrate external search volume trend ratios or binned seasonal indices as features to teach the model to distinguish between search volume demand drops and ranking position decay.

---

## 4. Practical Effect Size & Ranking Value

The operational benefit of replacing the heuristic baseline with the Gradient Boosting Classifier is substantial:

*   **Precision@50 Metric**:
    - **Heuristic Baseline (ML-07)**: **58.40%**
    - **Gradient Boosting Classifier (ML-08)**: **82.80%**
*   **Uplift & Waste Reduction**:
    - The Gradient Boosting model yields a **24.4% absolute increase in Precision@50**.
    - For an editorial team with resources to refresh 50 pages per week, the baseline flags **21 healthy pages** as decaying (wasted writing effort). The ML model reduces this to **9 healthy pages**, saving copywriters from rewriting content that is still performing well.

---

## 5. Re-Testing the SEO Myth: Word Count vs. Traffic Decay

A common SEO narrative asserts: *"Long-form content is always evergreen and decays less than short-form content."*

### Empirical Audit:
We tested this myth against our active, mature pages:

*   **Measured Decay Rate (Short Content: < 1,000 words)**: **20.00%**
*   **Measured Decay Rate (Long Content: > 2,000 words)**: **58.12%**

### Verdict: OPPOSITE
*   Our data shows that **longer pages decay at a significantly higher frequency** than short, focused pages.
*   **Directional Interpretation**: While length does not *cause* decay, we *observe* that long-form content is more vulnerable to performance erosion. This could indicate that bloated articles suffer from keyword cannibalization, dilution of search intent focus, or increased surface area for competitors to target.

---

## 6. Public-Safe Claim Language Guidelines

To align with corporate policy and maintain scientific integrity, we enforce strict rules on research claims:

*   **No Causal Proof Claims**: We never claim that a feature (e.g., word count or age) *causes* search engine rank drops. We use terms like **"observed correlation"** or **"measured directional indicator"**.
*   **No Claims of Google Algorithm Reverse-Engineering**: We do not claim to know or prove how Google's ranking algorithms work. Our model is purely a **decision-support tool** to prioritize client content portfolios based on observed historical patterns.
*   **Anonymization Rules**: No client names, raw URLs, or private query strings are documented. All data is reported in aggregate ratios, ensuring zero disclosure of confidential client assets.
