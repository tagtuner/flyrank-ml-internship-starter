# Capstone Project Package — Applied Search Intelligence

This document serves as the official **Capstone Model Card & Demo Outline** summarizing the entire Search Intelligence internship work. It organizes all deliverables, outlines reproducibility instructions, and provides a structured script for demonstrating the system to technical stakeholders.

---

## 1. Directory of Deliverables

All deliverables are checked in and public-safe within the GitHub repository:

*   **Research & Modeling Lane Framing**:
    - [Research Question Framing](file:///e:/antigravity%20workspace/flyrank-ml-internship-starter/work/research_question_framing.md) (Research focus, unit of analysis, outputs, and risk parameters).
    - [ML Task Framing](file:///e:/antigravity%20workspace/flyrank-ml-internship-starter/work/ml_task_framing.md) (Lane mapping, target labels, and metrics definition).
*   **Data, Signals, & Audits**:
    - [Feature Vector & Leakage Notes](file:///e:/antigravity%20workspace/flyrank-ml-internship-starter/work/feature_vector_notes.md) (Schema parameters, missingness rules, and dropped leakages).
    - [Signal Audit & Hypotheses Report](file:///e:/antigravity%20workspace/flyrank-ml-internship-starter/work/signal_audit.md) (Empirical tests of freshness, word count, and position myths).
*   **Heuristic Baseline**:
    - [Baseline Scored Queue (CSV)](file:///e:/antigravity%20workspace/flyrank-ml-internship-starter/work/baseline_action_score.csv) (deterministic scored list of 30,000 pages).
    - [Top-20 Action Review Audit](file:///e:/antigravity%20workspace/flyrank-ml-internship-starter/work/top20_action_review.md) (Granular audit of top-prioritized content assets).
*   **Machine Learning Models**:
    - [Training Script (`train_model.py`)](file:///e:/antigravity%20workspace/flyrank-ml-internship-starter/work/train_model.py) (GroupKFold logic, log-compression, models fit).
    - [Capstone Modeling Report](file:///e:/antigravity%20workspace/flyrank-ml-internship-starter/work/model_or_analysis_report.md) (Validation metrics, RF vs. GB vs. Baseline, feature importances).
*   **Validation & Operations**:
    - [Validation & Research Claim Audit](file:///e:/antigravity%20workspace/flyrank-ml-internship-starter/work/validation_claim_audit.md) (GroupKFold split design, leakage protection, failure modes).
    - [Content Action Playbook](file:///e:/antigravity%20workspace/flyrank-ml-internship-starter/work/content_action_playbook.md) (Archetypes, reason codes, human review, no-go rules).
*   **Visualizations**:
    - [Feature Importance SVG](file:///e:/antigravity%20workspace/flyrank-ml-internship-starter/outputs/charts/top_feature_importance.svg) (Top predictive features for traffic decay).

---

## 2. Capstone Model Card

### Model Description
*   **Developers**: TagTuner ML Engineering
*   **Model Type**: HistGradientBoostingClassifier (optimized gradient-boosted trees) & RandomForestClassifier (100 trees, max_depth=6).
*   **Objective**: Binary classification predicting page-level organic search performance decay over a prospective 30-day target window.

### Intended Use
*   **Primary Scope**: Decision-support prioritize tool for human copywriters and content editors to schedule content refreshes.
*   **Out-of-Scope**: Automated direct content updates or meta tag publishing without editorial review.

### Preprocessing & Training
*   **Feature Vectors**: 18 numeric and 8 binned categorical features computed over historical 90-day Search Console data.
*   **Log-Compression**: Log1p applied to impressions, clicks, and sessions to stabilize splitting.
*   **Validation Design**: 5-fold GroupKFold validation split grouped strictly by `client_id` to prove generalization on unseen tenants.

### Evaluation Metrics (Averages over 5 Folds)
*   **Heuristic Baseline**: Precision@50 = **58.40%** | ROC AUC = 0.5600
*   **Random Forest**: Precision@50 = **72.00%** | ROC AUC = 0.6583
*   **HistGradient Boosting**: Precision@50 = **82.80%** | ROC AUC = 0.6808

### Limitations & Failure Modes
*   **Low-Volume Instability**: Swings in CTR due to low click/impression counts can lead to false-positive recommendations.
*   **Seasonality Sensitivity**: Natural off-season traffic drops may be misclassified as ranking position decay.

---

## 3. Capstone Demo Outline

This structured outline defines a **5-minute executive demo** of the project:

### Phase 1: Problem Definition & Framing (1 min)
*   **Hook**: Content decay is the silent killer of organic traffic. Manual prioritization is slow and inefficient.
*   **Solution Selection**: Show [Ml Task Framing](file:///e:/antigravity%20workspace/flyrank-ml-internship-starter/work/ml_task_framing.md). Explain why we selected the **Refresh Opportunity Scoring Lane**, target metrics, and defined Precision@50 as the primary grading metric.

### Phase 2: Heuristic Baseline vs. ML Performance (1.5 mins)
*   **Heuristic Baseline**: Explain the simple position/CTR scoring engine and open the top 20 manual audit [top20_action_review.md](file:///e:/antigravity%20workspace/flyrank-ml-internship-starter/work/top20_action_review.md).
*   **The ML Uplift**: Show the comparative metrics table from the [Capstone Modeling Report](file:///e:/antigravity%20workspace/flyrank-ml-internship-starter/work/model_or_analysis_report.md). Highlight that Gradient Boosting achieves **82.80% Precision@50** (a 24.4% absolute gain over the baseline), which drastically cuts content writer wastage.
*   **Generalization**: Explain the importance of GroupKFold validation grouped by client domain to ensure cross-tenant generalization.

### Phase 3: Insights & Myth-Busting (1.5 mins)
*   **Feature Importance**: Show the feature importance chart `outputs/charts/top_feature_importance.svg`. Highlight that keyword exposure and search impressions consistency (`days_with_impressions`) drive decay predictions.
*   **Myth-Busting**: Share the **Word Count Myth** test results. Show that long content (>2,000 words) decays at a **58.12% rate** compared to short content's **20.00% decay rate** (Verdict: OPPOSITE).

### Phase 4: Operational Action Playbook & Wrap-up (1 min)
*   **Playbook**: Show [Content Action Playbook](file:///e:/antigravity%20workspace/flyrank-ml-internship-starter/work/content_action_playbook.md). Explain archetype mapping, reason codes, manual seasonality/intent checks, and strict no-go rules (e.g., no automated deletions or money-page updates).
*   **Closing**: Emphasize that the system is public-safe, anonymized, and ready to be deployed as a decision-support module for the content team.

---

## 4. How to Rerun the Pipeline

Follow these commands to recreate all feature vectors, heuristic scores, charts, and evaluations locally:

```bash
# 1. Setup virtual environment and dependencies
pip install -r requirements.txt

# 2. Run the full model training and evaluations pipeline
python work/train_model.py
```
This script will load the datasets, prepare log-transformations, perform the GroupKFold evaluations, and export the feature importance SVG to `outputs/charts/top_feature_importance.svg`.
