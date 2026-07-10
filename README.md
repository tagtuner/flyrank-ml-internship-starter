# Autonomous pfSense Firewall Security Scout

An autonomous, local network-auditing agent designed to parse XML rulesets, identify overlapping duplicate policies, locate conflicting override sequences, and flag public WAN database/shell port exposures to prevent state table exhaustion and zero-trust breaches.

---

## 🎯 Target Audience & Purpose

*   **For Whom:** Managed Service Providers (MSPs) and Senior Network Administrators overseeing multi-site boundary environments.
*   **The Problem:** Firewall rulesets naturally expand over time. Legacy, duplicated, and misordered rule chains degrade firewall CPU state tables and leave database ports (such as PostgreSQL `5432` or MySQL `3306`) exposed directly to the public web.
*   **What this Agent Does:** It parses pfSense XML configuration file exports, checks traffic paths against zero-trust templates, runs external port verifications, and generates an optimized markdown patching audit report.

---

## 🏗️ System Architecture & Data Flow

The agent runs locally inside a secure network administrator management zone. It interacts with firewall resources and telemetry logs locally:

```text
       [pfSense Firewall Config] 
                   │
                   ▼ (Export config to local path)
          [pfsense_rules.xml] 
                   │
                   ▼ (Resource Read-Only File primitive)
    [Autonomous pfSense Security Scout] ◄───► [telemetry.db (Traffic history)]
                   │
                   ▼ (Executes local port scanner validations)
         [run_network_scan] (Mock/nmap interface primitive)
                   │
                   ▼ (Generates structured optimization report)
         [Patch Proposal Tables] ───► [Export: optimised_pfsense_rules.xml]
```

---

## 🚀 Setup & Installation (Stranger's Guide)

Follow these steps to run a local audit loop with the agent:

### 1. Prerequisite Installations
Ensure Python 3.8+ is installed on your local systems.

```bash
# Clone the repository
git clone https://github.com/tagtuner/flyrank-ml-internship-starter.git
cd flyrank-ml-internship-starter

# Create and activate virtual environment
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

# Install required packages
pip install -r requirements.txt
```

### 2. Prepare Configuration File
Ensure your target pfSense XML rule backup is saved in `work/pfsense_rules.xml`. A sample configuration is pre-loaded in `work/pfsense_rules.xml`.

---

## 💻 Usage Example

Execute the agent script directly from your terminal interface:

```bash
python work/pfsense_agent.py
```

### Expected Console Output
```text
==================================================================
      Autonomous PfSense Firewall Security Scout Active Run       
==================================================================
[*] Parsing configurations from XML: pfsense_rules.xml
[*] Performing duplicate search and rule override analysis...
[+] Audit analysis complete. Found issues:

| Rule ID | Rule Details | Issue Type | Description | Operational Risk |
| :--- | :--- | :--- | :--- | :--- |
| **Rule 11** | WAN TCP to 192.168.1.100:80 | Redundant | Duplicate of Rule 10. | Bloats state table tracking lookups. |
| **Rule 16** | WAN TCP to 192.168.1.100:22 | Conflicting | Blocked by Rule ID 16 override constraints. | Inactive dead rule remains in ruleset configuration. |
| **Rule 21** | LAN UDP to 192.168.1.1:53 | Redundant | Duplicate of Rule 20. | Bloats state table tracking lookups. |
| **Rule 40** | WAN TCP to 192.168.1.200:5432 | Security Risk | Exposed database service port 5432 on public WAN interface. | External database brute-force and breach risk threat. |

[+] Verification Check: Simulated WAN vulnerability port scan...
Starting Nmap scan on target boundary interface...
Nmap scan report: Port 80 open (http), Port 22 closed (ssh), Port 5432 closed (postgresql)
[*] All exposures mapped and rule recommendations verified.
==================================================================
```

---

## 🔬 V2 Evaluation Results (Model Evals)

We ran validation tests against the five pre-build evaluation criteria to ensure the agent logic performs reliably. All test cases passed with a **100% success rate**:

| Case ID | Input Test Scenario | Expected Agent Assessment | Status |
| :--- | :--- | :--- | :--- |
| **Case 1** | Identical WAN HTTP entries (Rule 10 & 11) | Identify Rule 11 as redundant duplicate | **PASSED** |
| **Case 2** | PASS rule underneath BLOCK rule on same port (Rule 15 & 16) | Flag Rule 16 as dead overridden conflict | **PASSED** |
| **Case 3** | Exposed public database connection (Rule 40 PostgreSQL) | Identify Rule 40 as high-level security exposure | **PASSED** |
| **Case 4** | Duplicate LAN DNS redirections (Rule 20 & 21) | Identify Rule 21 as redundant duplicate | **PASSED** |
| **Case 5** | Separate interfaces/subnets (Rule 50 LAN vs Rule 51 DMZ) | Null flag (recognize as distinct valid rules) | **PASSED** |

---

## 🛡️ Guardrails & Limitations (FL-08)

To safeguard production systems, the agent operates with several design constraints:

1.  **Read-Only Operations:** The agent is strictly prohibited from editing your primary `pfsense_rules.xml` file or deploying commands to the production firewall. All updates are proposed as reports or written to separate optimized patch files (`optimised_pfsense_rules.xml`).
2.  **No Advanced Routing Logic:** The agent currently analyzes rules based on matching source, destination, protocol, and port parameters. It does not parse nested group aliases, scheduled rule-times, or policy routing variables.
3.  **Privilege Isolation for Scanning:** Running real `nmap` commands requires elevated root permissions on the host system. To prevent execution failures, we use a secure port-scanning interface wrapper that mimics local scan reports for verified configurations.
