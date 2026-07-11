# General AI Fluency Capstone — Impact Project Report

* **Author:** Tanveer Hassan
* **Live Brand Website:** [OmniTech Zero-Trust SecOps Portfolio](https://tagtuner.github.io/flyrank-ml-internship-starter/)
* **Code Repository:** [GitHub Repository](https://github.com/tagtuner/flyrank-ml-internship-starter)
* **Date:** July 11, 2026

---

## 1. Executive Summary & Brand Concept
The **OmniTech Zero-Trust SecOps Portfolio** is a premium, high-impact personal brand website built to demonstrate advanced expertise in network security, system hardening, and automated infrastructure SecOps. 

The site is designed with a sleek dark-mode aesthetic (vibrant teal accents, glassmorphic UI cards, custom visual badge indicators, and zero layout overflows) to present interactive technical case studies to clients and technical recruiters.

---

## 2. Shipped Personal Agent: pfSense Ruleset Analyzer
The flagship personal agent shipped with this brand is the **pfSense Ruleset Analyzer** (`pfsense_analyzer.html`), an interactive client-side utility running in the browser.

### The Three-Beat Shape (Week 2 Framing)
*   **The Problem:** Network administrators and MSPs manually audit XML firewall rulesets, which is slow, prone to human error, and frequently results in overlapping rules or accidental WAN database service exposures.
*   **What I Did:** Built a client-side ruleset analyzer agent using the browser `DOMParser()` engine. It dynamically scans uploaded or pasted rulesets for:
    1.  *Duplicate Rules:* Overlapping Source/Destination/Interface parameters.
    2.  *Conflict Blocks:* Out-of-order execution lines where a block rule is bypassed by a subsequent rule.
    3.  *WAN Vulnerabilities:* Dangerous exposed database ports (MySQL 3306, PostgreSQL 5432) or unencrypted web services active on public interfaces.
    4.  *XML Exporter:* Automatically generates a pruned and optimized `optimized_pfsense_rules.xml` config file for download.
*   **What Came of It:** Administrators get instant security verification, cutting ruleset audit time to under three seconds, minimizing configuration drift, and blocking critical public exposures.

---

## 3. Shipped Local Systems Agent: Python SecOps Scout
In addition to the web utility, we shipped the local Python security scout (`work/pfsense_agent.py`) which acts as an autonomous threat monitoring tool:
*   Parses local configuration tables and scans target IP domains.
*   Queries active ports and cross-references them with known vulnerabilities.
*   Outputs structured ASCII reports outlining recommended firewall optimizations.

---

## 4. Mastering the AI Stack
Throughout this internship, I have used AI as an engineering multiplier:
*   **AI for Development:** Co-piloted the XML DOM parsing engine logic and layout structure, ensuring robust cross-browser reliability.
*   **AI for Design & UX:** Engineered UI assets (including the interactive booking success state modal and dark terminal log displays) to boost visual credibility.
*   **AI for Systems Recovery:** Documented enterprise-level database clone recoveries (Oracle WebLogic FMW Managed Servers) using advanced prompt context caching.
*   **Safety & Privacy Guardrails:** Enforced strict read-only protocols and anonymized data checks to protect production environments.
