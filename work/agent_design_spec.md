# Spec Sheet: Autonomous PfSense Firewall Security Scout

This document outlines the engineering specification for the **Autonomous PfSense Firewall Security Scout**, a local network-auditing agent designed to optimize state tables and isolate zero-trust exposure gaps.

---

## 1. Job to be Done (JTBD)

> **"When I am managing firewall rulesets across multi-site Managed Service Provider (MSP) clients, I want an autonomous agent to continuously analyze configurations, verify external exposures, and flag rule conflicts, so I can minimize state-table exhaustion and prevent brute-force database attacks without manual ruleset tracking."**

*   **Primary User**: MSP Director of IT Operations / Senior Network Security Administrator.
*   **Usage Frequency**: Daily automated scheduled audit run (CRON), and on-demand interactive checks prior to ruleset deployments.

---

## 2. Tools, Data, and Access Plan

The agent runs locally within a secure management VLAN, utilizing the Model Context Protocol (MCP) to interact with firewall artifacts.

| Primitive Name | Type | Access Plan | Purpose |
| :--- | :--- | :--- | :--- |
| `pfsense_rules.xml` | **Resource** | Read-only local file path exposed via MCP files server. | Standard XML representation of active firewall rules. |
| `telemetry.db` | **Resource** | SQLite database connection tool. | Holds state table history counts and bandwidth connection metrics. |
| `run_network_scan` | **Tool** | Python execution script wrapping local `nmap` binaries. | Scans target client WAN boundaries to verify actual port exposure posture. |

---

## 3. Core Agent Instructions

*   **Persona**: You are "OmniTech," a Chief Technology Officer and Lead Creative Engineer with elite expertise in zero-trust network infrastructure and PfSense firewall ruleset operations.
*   **Core Logic**: Apply first-match rule processing mechanics. A broad block rule higher in the interface list renders specific pass rules below it inactive (dead rules).
*   **Tone & Style**: Direct, technical, precise, plain. No conversational filler or corporate buzzwords (do not use: passionate, dynamic, synergy, leverage).
*   **Output Format**: Print findings in a structured Markdown table mapping: Rule ID | Rule Details | Issue Type | Description | Operational Risk.

---

## 4. Five Pre-Build Evaluation Cases (FL-03 Style)

To verify the agent's reasoning prior to active system builds, we define five evaluation cases:

### Case 1: Identical Duplicate Detection
*   *Input ruleset*:
    *   Rule 10: PASS WAN TCP any to 192.168.1.100 port 80
    *   Rule 11: PASS WAN TCP any to 192.168.1.100 port 80
*   *Expected output*: Identify Rule 11 as **Redundant** (duplicate of Rule 10). Recommend pruning.

### Case 2: Dead Rule Rule-Order Conflict
*   *Input ruleset*:
    *   Rule 15: BLOCK WAN TCP any to any port 22
    *   Rule 16: PASS WAN TCP any to 192.168.1.100 port 22
*   *Expected output*: Identify Rule 16 as **Conflicting** (dead rule overridden by Rule 15 block). Recommend cleanup to keep ruleset readable.

### Case 3: Public DB Interface Exposure
*   *Input ruleset*:
    *   Rule 40: PASS WAN TCP any to 192.168.1.200 port 5432 (PostgreSQL)
*   *Expected output*: Identify Rule 40 as **Security Risk**. Flag WAN PostgreSQL exposure. Recommend blocking port 5432 and shifting traffic to an IPSec VPN tunnel.

### Case 4: Duplicate DNS Redirection
*   *Input ruleset*:
    *   Rule 20: PASS LAN UDP any to 192.168.1.1 port 53
    *   Rule 21: PASS LAN UDP any to 192.168.1.1 port 53
*   *Expected output*: Identify Rule 21 as **Redundant**. Flag duplicate local gateway redirect.

### Case 5: Correct Isolation (No False Positive)
*   *Input ruleset*:
    *   Rule 50: PASS LAN TCP any to 10.0.0.10 port 443
    *   Rule 51: PASS DMZ TCP any to 10.0.0.20 port 443
*   *Expected output*: **Null flag** (ignore). Recognize distinct destination subnets/interfaces as valid active rules.

---

## 5. Risks and Guardrails

As a network security agent, execution errors can cause catastrophic service outages. We enforce strict boundaries:

*   **Banned Actions**: The agent is strictly prohibited from modifying the primary `pfsense_rules.xml` file, restarting the firewall engine, or deploying SSH rules directly. All changes must be written as a proposed patch file for review.
*   **Mandatory Checks**: Before suggesting the deletion of any duplicate/conflicting rule, the agent must query `telemetry.db` to verify that active connection state hits on that rule identifier equal **0** over the last 48 hours.

---

## 6. Platform Choice & Justification

*   **Chosen Platform**: Claude Desktop Client connected to a Local MCP Server.
*   **Justification**:
    *   *Custom GPTs (ChatGPT)*: Rejected. Cannot query local, private database files (`telemetry.db`) or run binary command line port scanners (`nmap`) behind the user's firewall subnet due to cloud isolation.
    *   *n8n Workflow*: Rejected. Great for simple sequential steps but lacks a native terminal/filesystem execution loop, exposing API credential keys to external cloud services.
    *   *Claude Desktop with MCP*: Selected. Free standard client. MCP servers provide secure, local file-read capabilities (Resources) and execution sandboxes (Tools) to run `nmap` locally on our private testbed without public internet exposure.
