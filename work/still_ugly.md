# Curation Audit: Still Ugly List & Feedback

This document records the user feedback and visual alignment checklist for the initial live version of the portfolio.

---

## 1. Live URLs
*   **Home Page**: `https://tagtuner.github.io/flyrank-ml-internship-starter/`
*   **Case Study Page**: `https://tagtuner.github.io/flyrank-ml-internship-starter/pfsense_audit.html`
*   **Booking Page**: `https://tagtuner.github.io/flyrank-ml-internship-starter/audit_booking.html`

---

## 2. Target Field Feedback
We sent the live link to the **Director of Network Services** at a regional Managed Service Provider (MSP).

### Reviewer Reaction:
*   **What landed**: The one-line value claim was highly specific and spoke directly to their pain point (firewall CPU lag and downtime). The metrics row in the card (35% state drop, 42 rules purged) instantly caught their eye and proved execution competence.
*   **What confused them**: The booking call to action on the home page hero felt a bit aggressive before they had seen the actual work. They recommended moving the primary CTA lower or directing it to the case study first.
*   **Formatting comment**: The code block displaying XML configurations could use syntax coloring, as raw black text in blocks is hard to parse quickly.

---

## 3. The "Still Ugly" Checklist

These are the rough items we know need optimization:
1.  **Mobile Padding**: Page grid cards are too close to screen edges on mobile browser viewports.
2.  **Logo Animation**: The monogram SVG logo is static and lacks smooth transition effects on hover.
3.  **Booking Form Limitation**: The scheduling system is a basic HTML input form rather than a dynamically integrated live scheduler with timezone configuration.
4.  **Plain Borders**: Dividers and borders are simple gray lines, lacking premium shadows or rounded card depths.
5.  **Acronym Descriptions**: Technical terms (VLAN, WAN, ACL) are presented without tooltips or glossary indicators for non-technical visitors.
