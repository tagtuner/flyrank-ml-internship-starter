# Content Map & CTA Paths: OmniTech

This document maps out the one-line value claim, page sections, action paths, and gather lists to guide the portfolio build.

---

## 1. One-Line Claim Generation (10 Options)

1.  I audit and secure corporate networks by eliminating duplicate PfSense firewall rules and hardening public ports.
2.  I design zero-trust PfSense networks for MSPs to eliminate client downtime and secure WAN routing paths.
3.  I help MSP IT Directors minimize firewall lag and secure external database ports using zero-trust PfSense rulesets.
4.  I secure WAN interfaces and optimize PfSense rule latency for Managed Service Providers.
5.  I prune redundant firewall rules and audit network vulnerability postures for scaling MSPs.
6.  I configure secure IPSec VPN tunnels and optimize PfSense state table tracking for multi-site organizations.
7.  I protect MSP clients from database exposure by replacing open public ports with restricted PfSense routing.
8.  I audit and optimize production PfSense rulesets to drop memory usage and eliminate rule-lookup latency.
9.  I build zero-trust WAN boundaries with PfSense firewalls to protect MSP client infrastructures.
10. I help Managed Service Providers secure their perimeter networks and drop PfSense state table usage by auditing rules.

### Chosen and Sharpened Claim:
> **"I design and audit zero-trust enterprise networks using PfSense firewalls for Managed Service Providers to eliminate client network downtime and secure public routing paths."**

*   *Why this claims works*: It targets a specific buyer (MSP Directors of IT Operations), references the core tool (PfSense firewalls), and names the specific outcomes they pay for (eliminate downtime and secure routing paths).

---

## 2. Page-by-Page Content Map

### Home Page (`/`)
*   **Section 1: Hero Block**
    *   *Content*: Sharpened one-line claim as the H1 title. Short context paragraph describing rule bloating risks.
    *   *Primary CTA*: `"Book a 15-Minute Network Review"` (links to `/audit-booking`).
*   **Section 2: Skill Matrix & Toolkit**
    *   *Content*: Visual monoline cards representing primary engineering services: PfSense rule auditing, IPSec VPN configuration, VLAN segmentation, and Nmap scanning.
*   **Section 3: Featured Case Study Preview**
    *   *Content*: Abstract thumbnail preview of the PfSense case study. Highlight metrics: **35% state table drop**, **42 rules pruned**, **0 open public ports**.
    *   *Secondary CTA*: `"Read Case Study"` (links to `/pfsense-audit`).
*   **Section 4: Global Footer CTA**
    *   *Content*: Urgency text: "Stop waiting for state table exhaustion to crash your client networks."
    *   *Primary CTA*: `"Schedule Your 15-Minute Audit Call"` (links to `/audit-booking`).

---

### Case Study Page (`/pfsense-audit`)
*   **Section 1: Context & Meta**
    *   *Content*: Title ("Hardening & Optimizing a Production PfSense Ruleset") + Client context (multi-site MSP) + My Role (Network Security Auditor).
*   **Section 2: Beat 1 - The Problem**
    *   *Content*: Production network latency and state table capping caused by 152 legacy, duplicate, and undocumented rules. Unprotected database ports exposed directly to public WAN interfaces.
*   **Section 3: Beat 2 - What I Did (and Decided)**
    *   *Content*: Extracted XML configuration parameters, identified and purged 42 duplicate ACL rules, blocked direct database port exposures on WAN interfaces, and locked down firewall GUI access strictly to local management VLANs.
*   **Section 4: Beat 3 - What Came of It**
    *   *Content*: Max state table usage dropped by 35% during peak traffic hours, firewall memory fell by 18%, and an external nmap vulnerability scan confirmed zero unintended open ports.
*   **Section 5: Lessons Learned & Technical Retrospective**
    *   *Content*: Next time, I would automate baseline packet round-trip timing checks prior to the rule change to capture millisecond latency improvements.
*   **Section 6: Footer Bio & Action Card**
    *   *Content*: Short bio framing my zero-trust focus.
    *   *Primary CTA*: `"Book a 15-Minute Audit Call"` (links to `/audit-booking`).

---

### Booking Page (`/audit-booking`)
*   **Section 1: Intake & Scheduling Widget**
    *   *Content*: Integrated scheduling calendar to select a time slot.
*   **Section 2: Pre-Call Scope Checklist**
    *   *Content*: Small checklist detailing prep materials: "1. Do you have access to your client PfSense configuration? 2. Are you experiencing packet drops on WAN boundaries?"
    *   *Primary CTA*: `"Confirm Booking"` (submits meeting reservation).

---

## 3. "Still Need to Gather" Checklist

Before building our code showcase next week, we need to gather/verify these remaining assets:
*   [ ] **PfSense state table console screenshot**: Cropped image of live connection logging showing peak state tracking limits before the audit.
*   [ ] **GitHub parser script repository**: Create a public repository containing the script used to parse XML PfSense configurations.
*   [ ] **High-resolution professional headshot**: Clean, centered portrait with neutral backgrounds matching the Alabaster tone.
*   [ ] **MSP Director testimonial approval**: Get written signoff on the 35% metric improvement quote from the client manager.
