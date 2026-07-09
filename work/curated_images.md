# Image Curation & Discernment Log: OmniTech

This log records the complete image inventory for the portfolio, detailing which assets are real screenshots, which are generated, and our discernment decisions (rejections).

---

## 1. Image Inventory (Content Map Alignment)

| File Name | Source Type | Sitemap Location | Description |
| :--- | :--- | :--- | :--- |
| **headshot.jpg** | Real Photograph | Footer / Contact Card | A cropped, high-quality, professional headshot of the engineer to establish personal credibility. |
| **pfsense_dashboard.png** | Real Capture | `/pfsense-audit` Case Study | High-resolution, cropped screenshot of the PfSense dashboard showing state table utilization and CPU metrics. |
| **nmap_scan_result.png** | Real Capture | `/pfsense-audit` Case Study | A cropped CLI capture of the final nmap scan showing 0 public ports open on the WAN interface. |
| **network_nodes_vector.png** | AI Generated | `/` Hero Graphic | Minimalist, monoline geometric vector of network nodes matching the terracotta/charcoal palette. |

---

## 2. Deciding: Real Captures vs. AI Stand-ins

*   **Decision**: We chose real captures of the PfSense web console and terminal CLI for the case study rather than AI mockups.
*   **Rationale**: Directors of IT Operations at Managed Service Providers value technical verification. Showing a real terminal dump of `nmap` or a real PfSense metrics widget immediately establishes that the work actually occurred. An AI-generated dashboard would destroy all technical credibility.

---

## 3. Discernment: The Rejection Note (Ruthless Curation)

### The Rejected Visual (AI Slop)
*   **Prompt**: `"glowing 3D cyber security shield, glassmorphism, hyper-detailed neon light trails, cyber defense concept, dark background"`
*   **Asset Filename**: `work/rejected_cyber_shield.png`
*   **Reason for Rejection**: The image has the classic "AI slop" look. The glowing pink/blue neon colors clash violently with our clean Alabaster and Terracotta color kit. The complex 3D rendering is loud and competes with the ruleset analysis. It screams "generic stock theme page" rather than a custom systems audit.

---

## 4. The Keeper (Visual Framework)

### The Accepted Visual (Flat Vector)
*   **Prompt**: `"minimalist monoline vector illustration of network nodes and routing paths. thin dark charcoal lines on Alabaster off-white background, with subtle terracotta accent dots. flat design, no gradients, no 3D depth, clean geometric aesthetic."`
*   **Asset Filename**: `work/network_nodes_vector.png`
*   **Reason for Acceptance**: The flat, monoline geometry aligns perfectly with the quiet, structured aesthetic defined in our style kit. It does not try to steal the show; it frames the text and matches our hex code tokens.

---

## 5. Model Generation Prompt Log
To keep our style steady, we iterated the generation prompt across these versions:
*   *Attempt 1*: "network nodes vector illustration, terracotta colors" -> Rejected (contained random color splotches and gradients).
*   *Attempt 2*: "minimalist monoline vector illustration of network nodes, thin dark charcoal lines, flat design, no gradients" -> Better, but lacked accent contrast.
*   *Attempt 3 (Final)*: "minimalist monoline vector illustration of network network routing paths, thin dark charcoal lines on Alabaster off-white background, subtle terracotta accent dots, flat design, no gradients, clean geometric" -> Output matched style guide.
