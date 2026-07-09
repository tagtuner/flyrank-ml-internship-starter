# FL-01: AI Workflow Audit & Tool Setup

This report documents the workflow audit, classification parameters, target tasks, and Claude Project setup as part of the General AI Fluency (FL) track.

---

## 1. Weekly Workflow Audit Table

The table below outlines 12 specific technical and operational tasks performed during my typical work week. Each task has been classified based on the level of AI engagement, accompanied by a clear operational rationale.

| # | Task Name | Classification | Rationale |
| :--- | :--- | :--- | :--- |
| 1 | **PfSense Firewall Rule Audit & Optimization** | Collaborate with AI | AI parses raw access and routing logs for traffic anomalies, but modifications to ACLs and NAT forwarding require manual review and deployment. |
| 2 | **Oracle EBS Post-Clone WebLogic Recovery** | **Just Me** | Context-specific WLST re-encryption and service restarts are highly sensitive; delegation carries high risk and requires full manual execution. |
| 3 | **FreePBX Asterisk Dialplan Debugging** | Collaborate with AI | AI acts as a reference for complex Asterisk Extensions Syntax, but testing call flows on active trunk lines is done manually. |
| 4 | **Google Search Console Metric Extraction** | Fully Automate | A structured Python script scheduled via CRON executes periodic API calls autonomously without human-in-the-loop dependencies. |
| 5 | **Multi-Tenant Database Query Tuning** | Collaborate with AI | AI analyzes index usage plans and suggests query updates, but human DBA verification is necessary to protect multi-tenant table locks. |
| 6 | **Code Refactoring (Python/Shell Scripts)** | Delegate to AI with review | AI optimizes logic structures and redundant code blocks extremely fast; humans simply verify output correctness against unit tests. |
| 7 | **Sync Meeting Notes & Actions Synthesis** | Delegate to AI with review | AI converts raw conversational transcripts into structured markdown checklists, followed by a human check to correct technical terms. |
| 8 | **Digesting Developer API Documentation** | Collaborate with AI | Claude serves as an interactive documentation reading companion, speeding up API syntax lookups for libraries like scikit-learn. |
| 9 | **Asterisk Call Detail Record (CDR) Reporting** | Fully Automate | Generating month-end calling reports is a static SQL query that executes autonomously to generate client billing spreadsheets. |
| 10 | **Technical Project Proposals & Diagram Prep** | Collaborate with AI | Brainstorming proposal structures and ASCII layouts is interactive with AI, but final structural choices require senior engineer sign-off. |
| 11 | **Client Communication & Support Inquiries** | **Just Me** | Urgent client emails require high emotional intelligence, relationship context, and tone alignment that cannot be delegated to an LLM. |
| 12 | **System Telemetry Health & Alert Resolution** | Delegate to AI with review | AI parses hardware utilization alerts (ESXi, Proxmox) to diagnose root causes, but recovery commands must be executed manually. |

---

## 2. Target Tasks & Success Definitions ("Done Well")

We have selected three specific tasks from the audit to carry forward into future exercises (FL-02 to FL-04). The tables below define the measurable standard of excellence for each:

### Task A: PfSense Firewall Rule Audit & Optimization (Collaborate with AI)
*   **Success Metrics**:
    *   **Redundancy Reduction**: At least 95% of conflicting, duplicate, or stale rules are successfully identified and purged.
    *   **Security Validation**: NAT port-forwarding rules are audited and confirmed via an external scan (e.g., nmap) showing zero unintended open ports.
    *   **Traceability**: Every newly created or adjusted rule has an accompanying configuration comment detailing owner, date, and ticket context.

### Task B: Code Refactoring & Optimization (Delegate to AI with review)
*   **Success Metrics**:
    *   **Performance Gain**: Target script execution runtime is reduced by $\ge 20\%$ or memory footprint is minimized by $\ge 15\%$ as verified by benchmarks.
    *   **Functionality Retention**: $100\%$ pass rate on the existing unit and integration test suite (zero regression errors).
    *   **Code Quality**: Full compliance with PEP 8 style standards with complete docstrings for every modified class and method.

### Task C: Sync Meeting Notes & Actions Synthesis (Delegate to AI with review)
*   **Success Metrics**:
    *   **Extraction Accuracy**: 30-minute meetings are summarized into a 1-page document outlining executive summary, decisions, and named action items.
    *   **Turnaround Speed**: Complete markdown summary is generated and reviewed within 15 minutes of meeting termination.
    *   **Spelling and Terminology**: $100\%$ correct spelling of technical terms, protocols, and proprietary names (e.g., Asterisk, WebLogic, PfSense).

---

## 3. Claude Project Configuration & Custom Instructions

A dedicated Claude Project **"OmniTech Command Center"** has been created with custom instructions defining our CTO persona, communication style, and active goals.

### Custom System Instructions:
```text
# System Prompt: OmniTech CTO & Lead Creative Engineer Persona

## 1. Who I Am
* You are interacting with OmniTech, a Chief Technology Officer (CTO) and Lead Systems Architect.
* Core technical competencies include network security (PfSense firewall optimization, routing logs), enterprise virtualization, VoIP communications (Asterisk, FreePBX custom dialplans), multi-tenant PostgreSQL/DuckDB database optimization, and Python data preparation scripts.

## 2. Communication Style & Tone
* Be direct, technical, precise, and professional.
* Avoid introductory pleasantries, boilerplate conversational lines, warnings, or policies.
* Prioritize exact configuration variables, structured shell scripts, clean code outputs, and mathematical formulas over wordy explanations.

## 3. Current Project Goals & Context
* Refactoring legacy Python extraction scripts to optimize search performance telemetry.
* Hardening PfSense rulesets, removing redundant ACL configurations, and setting up strict zero-trust routing parameters.
* Tuning dialplans on FreePBX Asterisk setups to fix VoIP call distribution bottlenecks.
```

### Setup Screenshot:
Below is the verified screenshot of the configured Claude Project custom instructions page:

![Claude Project Custom Instructions Mockup](/e:/antigravity workspace/flyrank-ml-internship-starter/outputs/charts/claude_project_config.png)
