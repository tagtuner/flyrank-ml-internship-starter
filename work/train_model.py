import pandas as pd
import numpy as np
from pathlib import Path
import sys
import matplotlib.pyplot as plt
from sklearn.model_selection import GroupKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, average_precision_score

sys.path.append(str(Path(__file__).resolve().parents[1]))
from scripts.ml_utils import simple_svg_bar_chart, ensure_dirs, RAW_PATH, CHART_DIR, MODEL_NUMERIC_FEATURES, MODEL_CATEGORICAL_FEATURES, precision_at_k

# Dynamic baseline score helper
def get_baseline_scores(df_subset):
    scores = []
    for idx, row in df_subset.iterrows():
        score = 0
        # 1. Position component
        pos = row["avg_position"]
        if 10.0 <= pos <= 20.0:
            score += 40
        elif 3.0 < pos < 10.0:
            score += 25
        elif pos <= 3.0:
            score += 10
        else:
            score += 15
            
        # 2. Freshness component
        days_since_update = row["days_since_last_update"]
        if days_since_update > 180:
            score += 30
        elif days_since_update > 90:
            score += 20
        elif days_since_update > 30:
            score += 10
            
        # 3. Quality/CTR component
        ctr_pct = row["ctr"]
        if ctr_pct < 1.5:
            if pos <= 10:
                score += 30
            else:
                score += 15
        elif ctr_pct < 3.0:
            score += 10
        scores.append(score)
    return np.array(scores)

def main():
    ensure_dirs()
    
    # Load dataset
    df = pd.read_csv(RAW_PATH)
    
    # Filter active and mature pages (leakage & privacy guard)
    df_filtered = df[(df["impressions_90d"] > 0) & (df["content_age_days"] >= 90)].copy()
    
    # Create target y: persistent traffic decay
    df_filtered["is_declining"] = (df_filtered["trend_direction"] == "down").astype(int)
    
    # Log transformations for heavily right-skewed variables
    df_filtered["log_impressions_90d"] = np.log1p(df_filtered["impressions_90d"])
    df_filtered["log_clicks_90d"] = np.log1p(df_filtered["clicks_90d"])
    df_filtered["log_sessions_90d"] = np.log1p(df_filtered["sessions_90d"])
    df_filtered["log_ai_sessions_90d"] = np.log1p(df_filtered["ai_sessions_90d"])

    
    # Extract client list for grouped validation
    groups = df_filtered["client_id"].values
    
    # Preprocessing numerical columns
    X_num = df_filtered[MODEL_NUMERIC_FEATURES].copy()
    for col in MODEL_NUMERIC_FEATURES:
        X_num[col] = pd.to_numeric(X_num[col], errors="coerce").fillna(0)
        
    # Preprocessing categorical columns
    X_cat = df_filtered[MODEL_CATEGORICAL_FEATURES].copy()
    for col in MODEL_CATEGORICAL_FEATURES:
        X_cat[col] = X_cat[col].fillna("unknown")
    
    # One-hot encode categorical features
    X_cat_encoded = pd.get_dummies(X_cat, drop_first=True)
    
    # Combine numerical and categorical features
    X = pd.concat([X_num, X_cat_encoded], axis=1)
    y = df_filtered["is_declining"].values
    
    print(f"Features dimension: {X.shape}")
    print(f"Total positive labels: {y.sum()} / {len(y)} ({y.mean():.2%})")
    
    # GroupKFold Validation Split (client-level validation)
    gkf = GroupKFold(n_splits=5)
    
    baseline_precisions = []
    rf_precisions = []
    gb_precisions = []
    
    baseline_aucs, rf_aucs, gb_aucs = [], [], []
    baseline_aps, rf_aps, gb_aps = [], [], []
    
    # Define models
    rf_model = RandomForestClassifier(n_estimators=100, max_depth=6, random_state=42, n_jobs=-1)
    gb_model = HistGradientBoostingClassifier(max_depth=5, random_state=42)
    
    fold = 1
    for train_idx, test_idx in gkf.split(X, y, groups=groups):
        X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
        y_train, y_test = y[train_idx], y[test_idx]
        df_test_subset = df_filtered.iloc[test_idx]
        
        # 1. Baseline heuristic scores
        baseline_scores = get_baseline_scores(df_test_subset)
        
        # 2. Train and predict with Random Forest
        rf_model.fit(X_train, y_train)
        rf_probs = rf_model.predict_proba(X_test)[:, 1]
        
        # 3. Train and predict with Gradient Boosting
        gb_model.fit(X_train, y_train)
        gb_probs = gb_model.predict_proba(X_test)[:, 1]
        
        # Compute metrics for this fold
        bp = precision_at_k(y_test, baseline_scores, k=50)
        rfp = precision_at_k(y_test, rf_probs, k=50)
        gbp = precision_at_k(y_test, gb_probs, k=50)
        
        baseline_precisions.append(bp)
        rf_precisions.append(rfp)
        gb_precisions.append(gbp)
        
        # Compute AUC-ROC & AP
        rf_aucs.append(roc_auc_score(y_test, rf_probs))
        gb_aucs.append(roc_auc_score(y_test, gb_probs))
        baseline_aucs.append(roc_auc_score(y_test, baseline_scores))
        
        rf_aps.append(average_precision_score(y_test, rf_probs))
        gb_aps.append(average_precision_score(y_test, gb_probs))
        baseline_aps.append(average_precision_score(y_test, baseline_scores))
        
        print(f"Fold {fold}: Baseline P@50 = {bp:.2%}, RF P@50 = {rfp:.2%}, GB P@50 = {gbp:.2%}")
        fold += 1
        
    print("\n--- OVERALL COMPARATIVE METRICS ---")
    print(f"Heuristic Baseline: Mean P@50 = {np.mean(baseline_precisions):.2%}, Mean ROC AUC = {np.mean(baseline_aucs):.4f}, Mean AP = {np.mean(baseline_aps):.4f}")
    print(f"Random Forest     : Mean P@50 = {np.mean(rf_precisions):.2%}, Mean ROC AUC = {np.mean(rf_aucs):.4f}, Mean AP = {np.mean(rf_aps):.4f}")
    print(f"Gradient Boosting : Mean P@50 = {np.mean(gb_precisions):.2%}, Mean ROC AUC = {np.mean(gb_aucs):.4f}, Mean AP = {np.mean(gb_aps):.4f}")
    
    # Train Random Forest on full dataset to calculate feature importances
    rf_model.fit(X, y)
    importances = rf_model.feature_importances_
    
    # Group feature importances for one-hot encoded categories
    importance_series = pd.Series(importances, index=X.columns)
    
    # Consolidate categorical columns
    grouped_importance = {}
    for col in X.columns:
        original_name = col
        for cat_col in MODEL_CATEGORICAL_FEATURES:
            if col.startswith(cat_col + "_"):
                original_name = cat_col
                break
        grouped_importance[original_name] = grouped_importance.get(original_name, 0.0) + importance_series[col]
        
    grouped_importance_series = pd.Series(grouped_importance).sort_values(ascending=False)
    print("\n--- Consolidated Feature Importances ---")
    print(grouped_importance_series)
    
    # Export feature importance chart as SVG
    simple_svg_bar_chart(
        title="Random Forest Feature Importance",
        labels=grouped_importance_series.index.tolist()[:10],
        values=grouped_importance_series.values.tolist()[:10],
        path=CHART_DIR / "top_feature_importance.svg",
        color="#8B5FBF"
    )
    print("Feature importance SVG chart exported successfully!")

if __name__ == "__main__":
    main()
