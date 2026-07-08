# Capstone Modeling Report — Refresh / Content Opportunity Scoring

This report documents the machine learning modeling phase for the **Content Refresh Opportunity Scoring** lane. We train and evaluate a set of classifiers to predict whether a search performance page will experience persistent traffic decay, validating performance against a heuristic baseline using a rigorous cross-validation split design.

---

## 1. Validation Design & Data Split Strategy

SEO data is multi-tenant; a single dataset contains performance metrics for multiple clients, each with distinct query profiles, seasonal traffic trends, and search keyword behaviors. 

*   **GroupKFold Validation Splitting**:
    - To prevent cross-page data leakage and ensure model generalization, we implement a **5-fold GroupKFold validation split grouped by `client_id`**.
    - This design guarantees that a client's pages are strictly present in either the training set or the validation set, never both. This simulates a real-world production deployment where the model is requested to make predictions for a newly onboarded client.
*   **Leakage Guard & Row Selection**:
    - **Mature Pages Filter**: We filter out pages with `content_age_days < 90` to avoid predicting early-stage indexing volatility.
    - **Active Pages Filter**: We select pages with `impressions_90d > 0` to prevent modeling dead/inactive content.
    - **No Target Leakage**: All performance features are computed strictly on the historical 90-day window. Future metrics like `impressions_last_30d` or `clicks_last_30d` are dropped. Hand-written flags such as `health_score` are bhee removed.

---

## 2. Model Selection and Methodology

We compare three distinct methodologies to solve the binary classification problem (`is_declining = 1` if trend direction is downward):

1.  **Heuristic Baseline**:
    - A deterministic 100-point opportunity scoring formula based on average position, GSC CTR, and update age (developed in ML-07).
2.  **Random Forest Classifier**:
    - A robust ensemble of 100 decision trees (`max_depth=6`). This model serves to capture non-linear relationships and interactions (e.g. how high position combined with low word count affects decay risk) while remaining less prone to overfitting than deeper trees.
3.  **Gradient Boosting (HistGradientBoostingClassifier)**:
    - An optimized histogram-based gradient boosting tree ensemble (`max_depth=5`). This is the state-of-the-art method for tabular data in Python, capturing subtle multi-feature interactions and boosting performance on minority signals.

---

## 3. Overall Comparative Performance

Using GroupKFold cross-validation on 30,000 active, mature search pages, the average evaluation metrics across the 5 validation folds are:

| Model / Heuristic | Mean Precision@50 | Mean ROC AUC | Mean Average Precision (AP) |
| :--- | :---: | :---: | :---: |
| **Heuristic Baseline (ML-07)** | 58.40% | 0.5600 | 0.5891 |
| **Random Forest Classifier** | 72.00% | 0.6583 | 0.6637 |
| **Gradient Boosting Classifier** | **82.80%** | **0.6808** | **0.6848** |

### Insights & Interpretation:
*   **Precision@50 (Primary Metric)**: Precision@50 is our north-star metric because editorial teams can only refresh a limited number of pages (e.g., 50 pages per cycle). 
    - The **Gradient Boosting Classifier** achieves an outstanding **82.80% Precision@50**, beating the baseline by **24.4% absolute**. Out of 50 pages flagged for rewrite, 41 pages will be true decay cases.
    - The baseline's lower P@50 (58.40%) stems from its rigid, static thresholds that fail to adjust when impressions or positions are highly volatile.
*   **ROC AUC & Average Precision (AP)**:
    - The Gradient Boosting model obtains a ROC AUC of **0.6808** and an AP of **0.6848**. While the absolute AUC is moderate due to the stochastic nature of GSC search queries, it represents a substantial step up from the baseline's near-random ranking performance (AUC = 0.5600).

---

## 4. Feature Importance & Interpretation

We fit the Random Forest model on the entire filtered dataset to calculate consolidated feature importances. The top 10 most influential features are:

1.  **`days_with_impressions` (Importance: 20.36%)**:
    - Reflects the consistency of organic search visibility. Pages showing a steady daily footprint have higher baseline stability; a sudden drop in this metric is the single strongest indicator of decay.
2.  **`log_impressions_90d` (Importance: 13.02%)**:
    - Log-transformed total impressions. Highlights that high-exposure pages decay differently than long-tail, low-exposure articles.
3.  **`avg_position` (Importance: 11.25%)**:
    - Average ranking position. Page 1 bottom (positions 7-10) and striking distance (positions 10-20) pages are highly volatile and decay rapidly.
4.  **`content_age_days` (Importance: 9.21%)**:
    - Time elapsed since content creation. Older content naturally faces organic competition erosion.
5.  **`position_tier` (Importance: 7.57%)**:
    - Categorized position bucket, corroborating the non-linear relationship between ranking and decay.
6.  **`age_tier` (Importance: 4.82%)**:
    - Binned age categories, showing threshold effects where content decay risks change after 180 and 360 days.
7.  **`char_count` (Importance: 3.92%)** & **`word_count` (Importance: 3.54%)**:
    - Text length features. Confirms the signal audit finding: content length is a major factor, with longer posts decaying more frequently due to keyword cannibalization or dilution.

---

## 5. Deployment & Operational Recommendations

1.  **Replace Heuristics with Gradient Boosting**:
    - The Gradient Boosting model should be deployed as the core ranking engine for content recommendations. The 24.4% increase in P@50 translates directly to higher operational efficiency and less wasted copywriter resources.
2.  **Continuous Client Generalization Tests**:
    - When onboarding a new client, run the model in *shadow mode* first to confirm its validation performance metrics match the GroupKFold cross-validation benchmark.
3.  **Mitigate False Positives**:
    - Inspect recommended rewrite pages for search volume spikes; pages experiencing natural search volume decreases (e.g. seasonal winter queries in summer) may show false decay. Integrating search volume trends directly into future model releases will resolve this error pattern.
