# Week 10 Capstone: Next Case Study Plan

This document outlines the technical planning, layout integration steps, and the scheduled reminder for adding our next case study, turning the static portfolio into a living, evolving career platform.

---

## 1. The Shipped Case Study: VoIP SecOps
We have planned our next security engineering project:

### Project Title
**VoIP SecOps: Hardening Asterisk SIP Server with Fail2Ban & Automated Python API Intrusion Blocking**

### The Three-Beat Shape (Week 2 Framing)
1.  **The Problem (The Hook):** A mid-sized corporate client hosting a public-facing Asterisk SIP PBX server experienced continuous, aggressive SIP registration brute-force scans (SIP Register Flooding). These scans risked account credential compromises, call toll fraud billing risks, and degraded SIP server CPU performance.
2.  **What I Did (The Action):** 
    *   Hardened VoIP networking layouts by restricting WAN SIP registrations exclusively to the upstream SIP trunk provider IP subnets.
    *   Configured Fail2Ban log monitoring filters with custom security regex variables targeting failed registration patterns in Asterisk security logs.
    *   Wrote a lightweight Python log monitoring daemon that automatically calls the network's Edge Firewall API (Palo Alto) to apply dynamic null-routing blocks on malicious scanning subnets.
3.  **What Came of It (The Outcome):** Reduced unauthorized VoIP registration attempts to absolute zero, dropped CPU log-analysis overhead on the PBX server to <1%, and successfully blocked malicious scanners before they could compromise credentials, saving the client from thousands in potential toll-fraud charges.

---

## 2. Technical Steps: How to Add the Case Study
To add this new case study to the portfolio without breaking the existing static build layout:

1.  **Create Page File:** Create a new page file named `pfsense_voip_secops.html` in the root repository.
2.  **Clone Visual Layout:** Copy the layout of `pfsense_audit.html` (the PfSense Case Study page) to preserve the dark-mode CSS system, navigation links, header responsive grid, and footer structures.
3.  **Inject Content Content:** Replace the case study copy with the VoIP SecOps text (specifying problems, firewall rules, logging triggers, and results).
4.  **Update Homepage Navigation:** Edit `index.html` (homepage) and all other pages (`pfsense_audit.html`, `pfsense_analyzer.html`, `audit_booking.html`) to add `pfsense_voip_secops.html` to the main navigation header and the dropdown menus.
5.  **Analytics Tracking:** Ensure the Cloudflare Web Analytics beacon is injected in the `<head>` of `pfsense_voip_secops.html` to track traffic.

---

## 3. Preservation of AI Build Context
To ensure future portfolio upgrades are cheap and efficient:
*   We preserve the **Long-Term Memory Logs** (`long_term_memory.md`) outlining all previous builds, packages, directories, and stack decisions.
*   This context allows any future AI pair-programming agent to immediately understand the portfolio's visual styling patterns, security safeties, and repository guidelines.
