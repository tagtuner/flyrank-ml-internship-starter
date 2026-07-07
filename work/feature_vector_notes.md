# Feature Vector & Leakage/Privacy Check — Core Lane 2

This document details the signal properties, data transformations, missingness handling, and privacy/leakage audit for the **Refresh / Content Opportunity Scoring** lane.

---

## 1. Feature Vector Analysis

### Active Numerical Features (18 columns)
These features represent historical metrics observed in the 90-day feature window ($[t-90, t]$):
- **GSC Search Metrics**:
  - `search_volume`: The monthly query demand (volume) associated with the page's primary keyword.
  - `competition` / `cpc`: Keyword competitiveness index and AdWords Cost-Per-Click.
  - `log_impressions_90d` / `log_clicks_90d`: Log-transformed counts ($log(x+1)$) to compress search traffic right-skew.
  - `days_with_impressions`: Frequency of visibility (number of days with impressions $> 0$).
  - `ctr`: Historical click-through rate ($\text{clicks} / \text{impressions}$).
  - `avg_position`: Page's average ranking position in search results.
- **Analytics & Engagement Metrics**:
  - `log_sessions_90d` / `log_ai_sessions_90d`: Log-transformed GSC/GA4 session metrics.
  - `days_with_sessions`: Frequency of traffic engagement (number of days with traffic $> 0$).
  - `engagement_rate` / `scroll_rate`: Page's user focus rates (engaged sessions and scroll triggers).
  - `ai_traffic_pct`: Percentage of traffic referred by AI answer engines.
- **Content Metadata**:
  - `word_count` / `char_count`: Structural page dimensions.
  - `content_age_days`: Total time since page creation (in days).
  - `days_since_last_update`: Days elapsed since the content was last updated or refreshed.

### Categorical Features (8 columns)
Categorical features are mapped to ordinals or one-hot encoded:
- `competition_level` (high, medium, low)
- `content_type` (informational, transactional, etc.)
- `main_intent` (search intent category)
- `age_tier` / `freshness_tier` (derived time brackets)
- `word_count_tier` / `impression_tier` / `position_tier` (quantized value buckets)

---

## 2. Cleansing, Imputation & Missingness
- **Row Filter Constraints**:
  - Pages with `impressions_90d == 0` are excluded to filter out zero-demand noise.
  - Pages with `content_age_days < 90` are dropped since they do not have a complete 90-day history.
- **Missing Value Handling**:
  - Missing numeric metrics (NaNs) are imputed with `0` (e.g. `fillna(0)`).
  - Infinite values (caused by division by zero in rate metrics) are replaced with NaNs and imputed to `0` to prevent model execution failures.
- **Categorical Handling**:
  - Unobserved or empty categorical strings are filled with an `'unknown'` tier to ensure consistent category dimensions across training and test folds.

---

## 3. Prediction-Time Availability
- Every active feature is computed exclusively from observations in the **historical feature window** ($[t-90, t]$).
- All signals are 100% available and recorded *before* the content editor makes the decision to refresh, ensuring no dependency on future events.

---

## 4. Leakage & Privacy Audit (The Droplist)

To ensure model compliance, validity, and safety, the following fields are strictly excluded from features:

| Excluded Field | Category | Wajah / Rationale for Dropping |
|---|---|---|
| `client_hash_id` | Private Identifier | Join-only. Excluded to prevent the model from memorizing specific site properties and violating client privacy. |
| `content_hash_id` | Private Identifier | Excluded. Carries no generalizable predictive power and risks memorization. |
| `url_hash_id` / `keyword_hash_id` | Private Identifier | Excluded. High-cardinality join keys that can leak site structure or private keywords. |
| `impressions_last_30d` | Future Leakage | Excluded. Overlaps with the target prediction window ($[t+1, t+30]$), leading to direct outcome leakage. |
| `clicks_last_30d` / `sessions_last_30d` | Future Leakage | Excluded. Contains post-decision outcome data. |
| `trend_pct` / `trend_direction` | Future Leakage | Excluded. Direct derivative of the target label ($y = \text{trend} < 0$). Inclusion results in circular, artificial accuracy. |
| `health_score` | Product-Flag Leakage | Excluded. Hand-written SQL output from the dashboard. Model would simply learn to replicate the old rule instead of discovering raw patterns. |
| `priority_score` / `is_quick_win` | Product-Flag Leakage | Excluded. Direct product decisions. Inclusion defeats the purpose of ML-based signal discovery. |
| `needs_ctr_fix` / `refresh_tier` | Product-Flag Leakage | Excluded. Composite product rule outcomes. |

---

## 5. Cautious Framing & Causal Guardrails
- **No Causal Claims**: We must never state that our model proves "what factors cause Google search drops" or that "refreshing a page guarantees traffic recovery." 
- **Observational Status**: The model ranks candidates based on historical correlation. We describe the output as a *prioritized review list of opportunities*, recognizing that actual recovery requires human content validation or A/B experiment verification.
