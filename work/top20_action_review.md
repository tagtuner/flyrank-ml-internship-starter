# Baseline Action Scoring & Top-20 Review — Core Lane 2

This document explains the hand-crafted scoring heuristic used to build the baseline model, and audits the top 20 prioritized content items for validation.

---

## 1. Scoring Logic Explanation
To establish an honest, transparent baseline, we developed a deterministic scoring formula $\text{Score} \in [0, 100]$ using only **safe historical features** ($[t-90, t]$):

1. **Position Volatility Component (Max 40 points)**:
   - Pages in the *striking tier* (positions $10.0 \le \text{avg\_position} \le 20.0$) represent volatile opportunities. We assign them **40 points**.
   - Page 1 middle/bottom (positions $3.0 < \text{avg\_position} < 10.0$) gets **25 points**.
   - Stable top positions ($\le 3.0$) get **10 points**.
   - Deep pages ($> 20.0$) get **15 points**.
2. **Freshness Component (Max 30 points)**:
   - `days_since_last_update` $> 180$: **30 points** (high review priority).
   - $90 < \text{days\_since\_last\_update} \le 180$: **20 points**.
   - $30 < \text{days\_since\_last\_update} \le 90$: **10 points**.
3. **CTR Opportunity Component (Max 30 points)**:
   - Ranks in Page 1 ($\le 10$) but has a low CTR ($< 1.5\%$): **30 points** (indicates title/meta tag mismatches).
   - Else, if CTR is $< 3.0\%$: **10 points**.

---

## 2. Action Mapping Rules
Our baseline maps pages to one of these operational actions:
- **`prune`**: If `impressions_90d < 50` and `content_age_days > 180` (low-value, dead pages).
- **`rewrite metadata`**: If `avg_position <= 10.0` but `ctr < 1.5%` (high rankings, poor click capture).
- **`expand`**: If ranking is striking ($10.0 \le \text{pos} \le 20.0$) but `word_count < 800` (thin content).
- **`refresh`**: If ranking is striking and content has not been updated in $> 90$ days.
- **`merge`**: If ranking is striking, word count is high ($>3000$), but CTR is very low ($<1.0\%$) (potential cannibalization).
- **`protect`**: Ranks top 3 with CTR $\ge 3.0\%$ (evergreen high-performers).
- **`monitor`**: Normal behavior.

---

## 3. Top-20 Priority Audit

Here is the audit of the top 20 rows from [[baseline_action_score.csv](file:///e:/antigravity%20workspace/flyrank-ml-internship-starter/work/baseline_action_score.csv)]:

| Rank | Content ID | Baseline Score | Baseline Action | Reason Code | Pos | Days Since Update | CTR (%) | Word Count | Impressions | Confidence Note & "What Would Make It Wrong" |
|---|---|---|---|---|---|---|---|---|---|---|
| **1** | `content_b928313b1f13` | 90 | `rewrite metadata` | `LOW_CTR_ON_PAGE_1` | 10.0 | 104 | 0.00% | 4,940 | 1 | **Wrong (Low Volume)**: Ranks 10.0, but only has 1 impression. 0% CTR is statistically meaningless. Reviewing this is a waste of time. |
| **2** | `content_460e2d90ecfa` | 90 | `prune` | `LOW_IMPRESSIONS_OLD_PAGE` | 10.0 | 104 | 0.00% | 4,571 | 1 | **Wrong (Low Volume)**: Old page with only 1 impression in 90 days. Pruning it is fine but has zero real business value/impact. |
| **3** | `content_d0532868ad11` | 90 | `rewrite metadata` | `LOW_CTR_ON_PAGE_1` | 10.0 | 104 | 0.11% | NaN | 898 | **Confidence**: High. 898 impressions is a solid sample. CTR of 0.11% at position 10 is terrible. **Wrong if**: Page has technical rendering issues. |
| **4** | `content_c06a2fe22f4f` | 90 | `rewrite metadata` | `LOW_CTR_ON_PAGE_1` | 10.0 | 104 | 0.00% | NaN | 1,579 | **Confidence**: High. 1,579 impressions, 0 clicks. Needs urgent title tag rewrite. **Wrong if**: Page is a login page or utility page that shouldn't rank. |
| **5** | `content_838ce89e04f2` | 90 | `rewrite metadata` | `LOW_CTR_ON_PAGE_1` | 10.0 | 104 | 0.00% | 1,576 | 332 | **Confidence**: Medium. Decent impressions, clear metadata issue. **Wrong if**: Primary query is highly transactional and page intent is purely informational. |
| **6** | `content_ee9bf1dc39ac` | 90 | `rewrite metadata` | `LOW_CTR_ON_PAGE_1` | 10.0 | 104 | 0.14% | NaN | 6,499 | **Confidence**: High. 6,499 impressions with 0.14% CTR is a massive leak of potential traffic. **Wrong if**: Snippet is cannibalized by another page. |
| **7** | `content_1b1fc63709a3` | 90 | `rewrite metadata` | `LOW_CTR_ON_PAGE_1` | 10.0 | 104 | 0.00% | 1,725 | 62 | **Wrong (Low Volume)**: 62 impressions is too low to confidently declare CTR is broken. |
| **8** | `content_aea21c6e219f` | 90 | `rewrite metadata` | `LOW_CTR_ON_PAGE_1` | 10.0 | 104 | 0.88% | 6,035 | 3,524 | **Confidence**: High. Large content page (6k words), high impressions. CTR is below 1%. **Wrong if**: Target query intent is answered in SERP directly. |
| **9** | `content_b1fe4f67e498` | 90 | `rewrite metadata` | `LOW_CTR_ON_PAGE_1` | 10.0 | 104 | 0.31% | NaN | 2,275 | **Confidence**: High. 2,275 impressions, low CTR. **Wrong if**: Ranks for mismatched queries that are irrelevant to page topic. |
| **10** | `content_bc5ec602d0b6` | 90 | `rewrite metadata` | `LOW_CTR_ON_PAGE_1` | 10.0 | 104 | 0.28% | 5,031 | 27,509 | **Confidence**: Extremely High. 27k+ impressions, ranks at 10.0, CTR is 0.28%. Re-writing titles will drive major traffic. **Wrong if**: Competitor ads push fold down. |
| **11** | `content_85bf6763d5c5` | 90 | `rewrite metadata` | `LOW_CTR_ON_PAGE_1` | 10.0 | 104 | 0.00% | NaN | 573 | **Confidence**: Medium. 573 impressions with zero clicks. **Wrong if**: URL has been redirected and GSC is reporting lag data. |
| **12** | `content_b41fb554d71c` | 90 | `rewrite metadata` | `LOW_CTR_ON_PAGE_1` | 10.0 | 104 | 0.00% | 1,681 | 162 | **Confidence**: Low. Only 162 impressions. CTR could easily fluctuate. |
| **13** | `content_00b467976cbd` | 90 | `prune` | `LOW_IMPRESSIONS_OLD_PAGE` | 10.0 | 104 | 0.00% | 1,319 | 1 | **Wrong (Low Volume)**: Only 1 impression. Pruning has zero business impact. |
| **14** | `content_a14ef0a34e81` | 90 | `rewrite metadata` | `LOW_CTR_ON_PAGE_1` | 10.0 | 104 | 0.12% | NaN | 6,736 | **Confidence**: High. 6,736 impressions, ranks at 10.0. High priority. **Wrong if**: Word count is NaN because it's a PDF or non-text document. |
| **15** | `content_f45a1dec11bc` | 90 | `rewrite metadata` | `LOW_CTR_ON_PAGE_1` | 10.0 | 104 | 0.00% | NaN | 231 | **Confidence**: Medium. 231 impressions, 0 clicks. **Wrong if**: Main target search queries are informational questions. |
| **16** | `content_42db64fba733` | 90 | `rewrite metadata` | `LOW_CTR_ON_PAGE_1` | 10.0 | 104 | 0.25% | 5,804 | 17,359 | **Confidence**: Extremely High. 17k impressions, position 10.0. Needs urgent rewrite. **Wrong if**: Target query has massive zero-click search layout. |
| **17** | `content_28ce9207afa4` | 90 | `prune` | `LOW_IMPRESSIONS_OLD_PAGE` | 10.0 | 104 | 0.00% | 4,182 | 5 | **Wrong (Low Volume)**: Only 5 impressions. Expose zero-volume pages. |
| **18** | `content_9d52d957232b` | 90 | `rewrite metadata` | `LOW_CTR_ON_PAGE_1` | 10.0 | 104 | 0.18% | 1,299 | 2,817 | **Confidence**: High. 2,817 impressions, position 10.0, 1.2k words. Excellent candidate. **Wrong if**: Competitors bid heavily on this query. |
| **19** | `content_7bba5d83959a` | 90 | `rewrite metadata` | `LOW_CTR_ON_PAGE_1` | 10.0 | 106 | 0.33% | 3,052 | 2,724 | **Confidence**: High. 2,724 impressions, 3k words. **Wrong if**: Content matches user search query but needs fresh layout. |
| **20** | `content_fbbacf50108d` | 90 | `rewrite metadata` | `LOW_CTR_ON_PAGE_1` | 10.0 | 92 | 0.09% | 1,723 | 1,130 | **Confidence**: High. 1,130 impressions, CTR of 0.09%. **Wrong if**: Content was recently updated (92 days ago) and is still in search indexing flux. |

---

## 4. Key Takeaways & Weak Pick Identification
1. **The Low-Volume Trap**: The baseline heuristic ranks pages based on exact CTR thresholds. However, when impressions are extremely low ($\le 5$), CTR is highly unstable (often exactly 0.0%). These represent "weak picks" that should be filtered out by adding a volume threshold (e.g. `impressions_90d >= 100`) to the model scoring queue.
2. **Action Validation**: Ranks at 10.0 with extremely high impressions (e.g. `content_bc5ec602d0b6` and `content_42db64fba733`) are the highest value targets for `rewrite metadata` because even a small 1% increase in CTR will drive thousands of clicks immediately.
