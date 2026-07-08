# Signal & Myth Audit — Core Lane 2

This document details the exploratory data analysis and statistical validation of common SEO myths using the real anonymized search dataset (30,000 active pages).

---

## 1. Overall Dataset Context
- **Total mature & active rows audited**: 30,000
- **Audited Target Variable**: `trend_direction == 'down'` (indicates persistent organic traffic/impressions decline).
- **Overall Base Decay Rate**: **54.21%** (percentage of pages showing search traffic decline).

---

## 2. Signal Test 1: Content Freshness vs. Decay
- **SEO Myth**: *"Older content or content that hasn't been updated recently is highly prone to decay."*
- **Verdict**: **MIXED**

### Empirical Data
The decay rate (percentage of pages experiencing traffic drops) is computed across freshness categories:

| Days Since Update (`freshness_tier`) | Total Pages | Decayed Pages | Decay Rate |
|---|---|---|---|
| `0-30` days | 20,480 | 10,473 | 51.14% |
| `31-90` days | 175 | 103 | 58.86% |
| `91-180` days | 9,171 | 5,604 | 61.11% |
| `181+` days | 174 | 82 | 47.13% |

- **Correlation**: The Pearson correlation between `days_since_last_update` and `is_declining` is **`0.081`** (very weak positive correlation).

### Analysis & Interpretation
As content age since update increases from 0 days to 180 days, the decay rate climbs steadily from 51.14% to 61.11%. This supports the "freshness matters" narrative. However, the oldest content (181+ days since update) actually exhibits a drop in decay rate to 47.13%. 
This happens because very old content that has survived 180+ days without decay is usually "evergreen" content that ranks for extremely stable, low-volatility query patterns. Freshness is a signal, but treating it as a raw linear rule is incorrect.

---

## 3. Signal Test 2: Word Count vs. Decay
- **SEO Myth**: *"Longer content (higher word count) ranks better and is less prone to traffic decay."*
- **Verdict**: **OPPOSITE**

### Empirical Data
Decay rate computed across content length categories:

| Content Length (`word_count_tier`) | Total Pages | Decayed Pages | Decay Rate |
|---|---|---|---|
| `<1000` words | 973 | 201 | 20.66% |
| `1000-2000` words | 3,780 | 2,100 | 55.56% |
| `2000-3500` words | 11,263 | 6,627 | 58.84% |
| `3500+` words | 6,285 | 3,751 | 59.68% |
| `unknown` | 7,699 | 3,583 | 46.54% |

- **Correlation**: The Pearson correlation between `word_count` and `is_declining` is **`0.118`** (positive correlation).

### Analysis & Interpretation
This is a critical counter-intuitive finding. Short content under 1,000 words has a remarkably low decay rate of only **20.66%**, whereas long-form content (2,000 to 3,500+ words) has decay rates exceeding **58%**. 
Longer content creates a larger keyword footprint, making it rank for secondary long-tail queries. However, this large footprint is highly volatile and sensitive to search intent shifts or algorithm updates. Short-form pages typically rank for very specific, narrow-intent search queries that are highly stable. The rule "write longer content to prevent drops" is refuted by this data.

---

## 4. Signal Test 3: Average Position vs. Decay
- **SEO Myth**: *"Pages in top average positions (Page 1) are stable and rarely experience sudden traffic drops."*
- **Verdict**: **FALSE** (or **MIXED** depending on exact spot)

### Empirical Data
Decay rate computed across ranking position tiers:

| Position Tier | Average Position | Total Pages | Decayed Pages | Decay Rate |
|---|---|---|---|---|
| `top_3` | $1.0 - 3.0$ | 2,321 | 559 | 24.08% |
| `page_1` | $3.1 - 10.0$ | 11,814 | 6,730 | 56.97% |
| `striking` | $10.1 - 20.0$ (Page 1 bottom / Page 2 top) | 7,304 | 4,452 | 60.95% |
| `page_3_5` | $20.1 - 50.0$ | 7,242 | 4,067 | 56.16% |
| `deep` | $>50.0$ | 1,319 | 454 | 34.42% |

- **Correlation**: Correlation between `avg_position` and `is_declining` is **`-0.029`** (near-zero, confirming ranking level alone does not predict decay stability).

### Analysis & Interpretation
Only the very top positions (`top_3`) show significant decay resistance (24.08%). The rest of Page 1 is highly volatile, with a 56.97% decay rate. Striking distance pages (`striking`) have the highest decay rate at **60.95%**. Deep pages rank so low that they have very little traffic to lose, resulting in a lower statistical decay rate (34.42%). Thus, the idea that a Page 1 ranking protects content from decay is false; the bottom half of Page 1 is a battleground of constant volatility.

---

## 5. Practical Content Team Recommendations
1. **Prioritize Striking Pages**: Do not audit old or long content blindly. Instead, target pages in the **striking tier** (positions 10-20) that are showing traffic slippage. They represent the highest chance of quick recovery and highest decay risk.
2. **Stop Length Obsession**: Avoid adding fluff to articles to force them into 3,000+ words. Focus on search intent fulfillment rather than page word count metrics.
