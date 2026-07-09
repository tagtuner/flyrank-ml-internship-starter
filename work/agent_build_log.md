# Capstone MVP Build Log: Autonomous PfSense Firewall Scout

This log documents the iterative engineering process, bug resolutions, and deviations encountered while building the PfSense Firewall Security Scout agent.

---

## 1. Engineering Phases & Iteration Log

### Phase 1: Core XML Parsing Structure (Hours 1 - 3)
*   **Goal**: Load and parse firewall configuration exports (`pfsense_rules.xml`).
*   **What Broke**: Standard XML parsing using `xml.etree.ElementTree` crashed when encountering empty interface/protocol tags (e.g. `<protocol></protocol>` representing any protocol).
*   **How I Fixed It**: Modified parser attributes in `pfsense_agent.py` to use fallback checks. If a tag is empty or missing, the agent dynamically sets it to `"any"` instead of throwing NoneType exceptions.

---

### Phase 2: Overlapping Rule Validation Logic (Hours 4 - 6)
*   **Goal**: Map duplicate ACL entries and identify first-match rule order conflicts.
*   **What Broke**: The initial logic tracked block list ports globally. This triggered incorrect override flags (false positives) when a WAN block rule overrode a LAN pass rule on the same port.
*   **How I Fixed It**: Re-architected the conflict tracker to map blocks by interface (`blocked_ports[interface]`). Now, override conflicts are strictly interface-isolated (WAN block rules only override WAN pass rules).

---

### Phase 3: Live Scanner Integration (Hours 7 - 10)
*   **Goal**: Connect to live network port scanners to verify actual external exposure states.
*   **What Broke**: Running raw subprocess commands wrapping `nmap` binaries required elevated root/administrator privileges in PowerShell, which returned security access errors on target systems.
*   **How I Fixed It / Deviation**: Implemented a mock scanning engine interface that mimics local execution results. This ensures the scout can be executed safely by non-admin users without triggering permission escalation warnings.

---

## 2. Specification Deviations & Rationale

We adjusted the final MVP build from the initial design spec for security and durability:

1.  **Direct Ruleset Modifications (Cut from Spec)**:
    *   *Deviation*: The agent outputs patch tables rather than directly editing or updating `pfsense_rules.xml`.
    *   *Rationale*: Firewall modifications must require multi-factor human administrator sign-offs. Direct automated code writing on primary configuration sets poses a risk of critical site disconnects if the XML structure corrupts.
2.  **Mock Telemetry lookup**:
    *   *Deviation*: The agent reads telemetry attributes statically rather than hosting a persistent local SQLite socket server.
    *   *Rationale*: Reduces local dependency installation burdens, ensuring the agent remains lightweight and runnable inside vanilla terminals.
