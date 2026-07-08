# Case Study: Predictive Content Decay & Portfolio Prioritization

**Author**: TagTuner ML Engineering Team  
**Subject**: Applied Search Intelligence — Refresh / Content Opportunity Scoring  
**Focus**: Machine learning decision-support framework to prioritize content updates across multi-tenant SEO portfolios.

---

## 1. Executive Summary

In organic search marketing, content represents a depreciating asset. As competition intensifies and search intent shifts, older content experiences traffic decay, leading to lost visibility and reduced return on investment. Managing content updates across a portfolio of tens of thousands of active pages is historically executed using simple static heuristics (e.g., refreshing pages older than 6 months), which leads to significant waste in copywriting resources.

This case study presents a **predictive opportunity scoring framework** trained on 30,000 active, mature search pages. By replacing static heuristics with a machine learning classification pipeline, we **improved Precision@50 from 58.40% to 82.80%**, representing a **24.4% absolute gain** in prioritization accuracy. This decision-support tool allows editorial teams to target pages at high risk of decay, maximizing organic traffic recovery while minimizing editorial waste.

---

## 2. The Business & Search Intelligence Problem

Within a large multi-tenant SEO portfolio, editorial teams face a resource allocation problem. They possess the capacity to refresh only a small fraction of their content portfolio (e.g., 50 pages per week) out of a pool of over 30,000 active URLs. 

### Core Challenges:
*   **Static Prioritization Failures**: Traditional heuristics prioritize refreshes based on age alone, ignoring volatile ranking movements or specific user engagement signals (such as CTR). This results in "over-refreshing" stable, high-value pages while ignoring rapidly decaying assets in striking positions.
*   **Tenant Scale and Variance**: Multi-tenant SEO portfolios contain clients with radically different traffic scales and seasonal trends. Memorizing individual client performance patterns leads to models that fail when applied to new clients.
*   **Causal Ambiguity**: Search engines operate as black boxes. Directly claiming that structural page parameters (like word count or header tags) cause rank drops is unscientific and legally risky. The framework must operate purely as a predictive decision-support system based on observed historical trends.

---

## 3. Data-Driven Methodology & Preprocessing

The model operates on a safe, fully anonymized dataset consisting of 30,000 search pages.

### Data Split Strategy (GroupKFold):
*   To evaluate the model's ability to generalize to new customers, we implemented a **5-fold GroupKFold cross-validation split grouped strictly by `client_id`**.
*   This design ensures that a client's pages are never shared between training and validation sets, preventing the model from memorizing client-specific query profiles and forcing it to learn generalized SEO performance patterns.

### Preprocessing and Pre-empting Leakage:
*   **Row Filters**: We selected active pages (`impressions_90d > 0`) and mature pages (`content_age_days >= 90`) to exclude indexing volatility.
*   **Log-Compression**: Applied $\log(x + 1)$ transforms to highly skewed metrics (impressions, clicks, sessions) to prevent tree splitting imbalances.
*   **Leakage Controls**: Dropped all client hashes, prospective target window metrics (next 30-day GSC clicks/impressions), and existing hand-coded quality flags (such as `health_score`).

---

## 4. Key Model Findings (Public-Safe)

We evaluated a Heuristic Baseline, a Random Forest Classifier, and a HistGradientBoosting Classifier. 

### Comparative Performance:

| Model / Heuristic | Mean Precision@50 | Mean ROC AUC | Mean Average Precision (AP) |
| :--- | :---: | :---: | :---: |
| **Heuristic Baseline** | 58.40% | 0.5600 | 0.5891 |
| **Random Forest** | 72.00% | 0.6583 | 0.6637 |
| **Gradient Boosting (HistGB)** | **82.80%** | **0.6808** | **0.6848** |

*   **Precision@50 Uplift**: Replacing static rules with Gradient Boosting increased Precision@50 by **24.4% absolute**. Out of 50 pages recommended for updates, 41 pages are verified true decay cases compared to only 29 for the baseline.
*   **Feature Drivers**: The most predictive feature was `days_with_impressions` (20.36% importance), highlighting that search footprint consistency over time is the strongest indicator of content decay risk.

### Myth-Busting: Word Count vs. Traffic Decay
*   *Popular SEO Myth*: "Long-form content is always evergreen and decays less than short-form content."
*   *Measured Data*: Short-form pages (<1,000 words) experienced a decay rate of **20.00%**, whereas long-form pages (>2,000 words) experienced a decay rate of **58.12%**.
*   *Verdict*: **OPPOSITE**.
*   *Directional Interpretation*: In our observed sample, longer content exhibits higher decay rates. This does not prove that length causes decay, but it suggests that long articles are more susceptible to search intent drift, keyword cannibalization, or targeted competitor entries.

---

## 5. Connecting to Business Outcomes

Deploying this predictive engine directly optimizes marketing efficiency:

1.  **Editorial Waste Reduction**: In a portfolio of 30,000 active pages, an editorial team refreshing 50 pages per week will save an estimated **620 copywriting hours annually** by avoiding false-positive recommendations flagged by the heuristic.
2.  **Client Churn Prevention**: By targeting and refreshing pages before they experience persistent ranking drops, client accounts preserve their organic lead pipeline, directly reducing client churn.

---

## 6. Demo Outline (Final Presentation Script)

This structured outline defines a **5-minute live talk** presenting the Search Intelligence Capstone to stakeholders:

### Slide 1: The Content Decay Challenge (0:00 - 1:00)
*   **Hook**: Portfolio search traffic decays silently. Simple age-based heuristics lead to wasted writer hours.
*   **Objective**: Build a predictive scoring engine to rank pages by decay risk, measuring success strictly on **Precision@50** to align with copywriter bandwidth.

### Slide 2: Data Preprocessing & Leakage Control (1:00 - 2:00)
*   **Data Prep**: Explain the need to log-compress right-skewed GSC metrics and filter out pages under 90 days old to avoid indexing volatility.
*   **Leakage Audit**: Detail the dropped prospective metrics (e.g. target window clicks) and product flags (e.g. health score) to ensure zero future-data overlap.
*   **GroupKFold Split**: Highlight why we split validation folds grouped by `client_id` to verify cross-tenant generalization.

### Slide 3: Model Evaluation & Results (2:00 - 3:15)
*   **Uplift Table**: Present the Precision@50 uplift from baseline (58.40%) to Gradient Boosting (**82.80%**).
*   **Interpretability**: Discuss feature importance rankings, emphasizing that `days_with_impressions` is the top predictor.
*   **Myth-Busting**: Share the "Word Count" myth-busting results (longer content decaying more frequently in our observed dataset).

### Slide 4: Content Playbook & Guardrails (3:15 - 4:30)
*   **Playbook Actions**: Explain how we map pages to operational actions (`rewrite metadata`, `refresh`, `merge/trim`, `prune/monitor`) based on performance archetypes and reason codes.
*   **Guardrails**: Detail no-go automation rules (no automated page deletions or money-page redirects) and monitoring triggers.

### Slide 5: Business Impact & Wrap-up (4:30 - 5:00)
*   **ROI**: Show the copywriter hour savings and the value of proactive client churn mitigation.
*   **Closing**: Emphasize that the system is public-safe, anonymized, and ready to deploy as an advisory decision-support system.
