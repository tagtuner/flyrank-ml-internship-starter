# Portfolio Case Studies & Voice Framing

## 1. Voice Card
*   **Active Style**: "direct, technical, precise, plain, specific, no buzzwords"
*   **Prohibited Words**: "passionate", "results-driven", "spearhead", "leverage", "dynamic", "cutting-edge", "synergy", "revolutionary".
*   **Standing Rule**: Write short sentences. Focus on configurations, metrics, and exact protocols. Avoid generic filler.

---

## 2. Case Study: Hardening & Optimizing a Production PfSense Ruleset

### Beat 1: The Problem
A scaling Managed Service Provider reported client-side latency spikes and occasional firewall state table exhaustion. The PfSense ruleset had ballooned to 152 active entries over three years. Over half of these rules were undocumented, overlapping, or obsolete. Open port configurations exposed sensitive local database services directly to public interfaces.

### Beat 2: What I Did (and Decided)
*   I extracted the XML configuration file and wrote a log preparation script to trace active routing connections.
*   I identified and purged 42 duplicate or inactive firewall rules to clear the state tracking workload.
*   I decided to block all direct public database access ports, replacing them with restricted IPSec VPN routing paths.
*   I limited firewall GUI administration access exclusively to a secure local management VLAN, locking down public WAN facing interfaces.

### Beat 3: What Came of It
*   Max state table usage dropped by 35% during peak hours (from 42,000 states to 27,300).
*   Average firewall memory consumption fell by 18%.
*   An external nmap vulnerability scan verified zero unintended ports were open to the public internet.
*   *Next time delta*: I would automate pre-change network latency baselining to capture exact millisecond improvements rather than relying on state-table statistics alone.

---

## 3. Bio & Contact Copy

### Professional Bio
"I design and audit zero-trust enterprise networks using PfSense firewalls. I help Managed Service Providers minimize client downtime and secure WAN-facing routing paths."

### Contact / CTA
"Book a 15-minute network architecture review call."

---

## 4. Copy Contrast: Before / After

| Type | Generic AI Draft (Revise) | Edited Human Draft (Pass) | Rationale |
| :--- | :--- | :--- | :--- |
| **Bio** | "I am a passionate, results-driven, and highly motivated network security professional dedicated to leveraging cutting-edge technologies to spearhead next-generation PfSense architectures and secure client networks." | "I design and audit zero-trust enterprise networks using PfSense firewalls. I help Managed Service Providers minimize client downtime and secure WAN-facing routing paths." | Removed buzzwords ("passionate", "results-driven", "spearhead", "leveraging") and replaced with concrete, verifiable services and audience. |
| **Case Study** | "In this revolutionary project, I leveraged state-of-the-art diagnostic paradigms to synergize and optimize the client's network security rules, successfully mitigating potential vulnerabilities and maximizing performance." | "I identified and purged 42 duplicate or inactive firewall rules to clear the state tracking workload, dropping peak state table usage by 35%." | Replaced high-level assertions ("synergize", "revolutionary", "maximizing performance") with specific actions and audited connection metrics. |
