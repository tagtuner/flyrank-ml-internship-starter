import json
import os

# 1. Populate Notebook 01
nb1_path = "notebooks/01_first_look_and_discovery.ipynb"
with open(nb1_path, "r", encoding="utf-8") as f:
    nb1 = json.load(f)

for cell in nb1["cells"]:
    if cell["cell_type"] == "code" and "# Your discovery here" in "".join(cell["source"]):
        cell["source"] = [
            "# Your discovery here\n",
            "active_pages = df[df['impressions_90d'] > 0]\n",
            "corr_active = active_pages['search_volume'].corr(active_pages['impressions_90d'])\n",
            "print(f\"Correlation between search_volume and impressions_90d for active pages (impressions > 0): {corr_active:.3f}\")\n",
            "print(\"Directional observation: Even when limiting to active pages with > 0 impressions, the correlation remains extremely low (near zero). Search volume remains a poor predictor of actual traffic.\")\n"
        ]

with open(nb1_path, "w", encoding="utf-8") as f:
    json.dump(nb1, f, indent=1, ensure_ascii=False)

# 2. Populate Notebook 02
nb2_path = "notebooks/02_your_first_readable_model.ipynb"
with open(nb2_path, "r", encoding="utf-8") as f:
    nb2 = json.load(f)

for cell in nb2["cells"]:
    if cell["cell_type"] == "code" and "# Your experiment here" in "".join(cell["source"]):
        cell["source"] = [
            "# Your experiment here\n",
            "for depth in [3, 4]:\n",
            "    tree_model = DecisionTreeClassifier(max_depth=depth, class_weight='balanced', random_state=42)\n",
            "    tree_model.fit(X, y)\n",
            "    preds = tree_model.predict_proba(X)[:, 1]\n",
            "    p50 = precision_at_k(preds, y, 50)\n",
            "    print(f\"Decision Tree (max_depth={depth}) Precision@50: {p50:.3f}\")\n",
            "    print(export_text(tree_model, feature_names=features))\n",
            "    print('-' * 50)\n"
        ]

with open(nb2_path, "w", encoding="utf-8") as f:
    json.dump(nb2, f, indent=1, ensure_ascii=False)

print("Notebooks populated successfully!")
