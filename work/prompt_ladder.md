# The Prompt Ladder: PfSense Rule Auditing

This document records the step-by-step optimization of an AI prompt for auditing PfSense firewall rules, tracing how each layer changes the actual output of the model.

---

## Run 0: The Baseline (Weak Prompt)
### Prompt:
> Help me optimize my PfSense firewall rules.

### Output Excerpt:
> To optimize your PfSense firewall rules, you should follow these general best practices:
> 1. Put your most frequently hit rules at the top of the ruleset to minimize CPU lookup overhead.
> 2. Delete any rules that are duplicate or no longer needed.
> 3. Group rules logically and use aliases for IP ranges.
> 4. Ensure you block WAN administration access.
> Please share your rules if you want a custom review.

### Analysis Notes:
*   **Prompt Change**: None (Baseline).
*   **Output Improvement**: None.
*   **Remaining Failures**: The output is generic textbook theory. It does not review any actual configurations, audit ports, or help resolve a live bottleneck.
*   **Next Step**: Add a clearer goal to focus on redundant/conflicting rules.

---

## Run 1: Version 1 (+ Clearer Goal)
### Prompt:
> Analyze this PfSense configuration ruleset and find any redundant, duplicate, or conflicting rules.

### Output Excerpt:
> Redundant and conflicting rules in PfSense occur when multiple rules cover the same traffic path. To locate them:
> *   **Duplicate Rules**: Look for rules with identical source, destination, protocol, and port parameters.
> *   **Conflicting Rules**: Look for rules where a broad block rule overlaps with a specific pass rule below it.
> Please paste your ruleset (either XML export or text list) so I can parse it for duplicates.

### Analysis Notes:
*   **Prompt Change**: Added a clear goal (identify redundant/conflicting rules).
*   **Output Improvement**: The output stopped giving general firewall best practices and pivoted entirely to definitions and methods for diagnosing rule overlaps.
*   **Remaining Failures**: The model still cannot perform any work because it has no data context.
*   **Next Step**: Add real context by providing a sample configuration ruleset.

---

## Run 2: Version 2 (+ Real Context)
### Prompt:
> Analyze this PfSense configuration ruleset and find any redundant, duplicate, or conflicting rules. Here is the configuration snippet:
> *   Rule 10: PASS WAN TCP any to 192.168.1.100 port 80 (HTTP Web Server)
> *   Rule 11: PASS WAN TCP any to 192.168.1.100 port 80 (Duplicate rule)
> *   Rule 15: BLOCK WAN TCP any to any port 22 (Block SSH Access)
> *   Rule 16: PASS WAN TCP any to 192.168.1.100 port 22 (Conflicting SSH Pass)

### Output Excerpt:
> Based on your ruleset, I found the following issues:
> 1.  **Redundancy**: Rule 11 is a direct duplicate of Rule 10 (same source, destination, and port). You can safely delete Rule 11 to save state tracking overhead.
> 2.  **Conflict**: Rule 16 attempts to pass traffic to port 22, but Rule 15 is a broader block rule that sits above it. In PfSense, rules are processed first-match, so Rule 15 will block all SSH traffic, rendering Rule 16 inactive and useless.

### Analysis Notes:
*   **Prompt Change**: Provided a sample configuration snippet (real context).
*   **Output Improvement**: The output successfully identified the exact redundant HTTP rule (Rule 11) and explained the processing logic that made the SSH rule (Rule 16) fail.
*   **Remaining Failures**: The response is highly conversational and wordy, mixing technical diagnostics with introductory pleasantries.
*   **Next Step**: Define the target audience to enforce operational prioritization.

---

## Run 3: Version 3 (+ Defined Audience - THE FAILURE MOMENT)
### Prompt:
> Analyze this PfSense configuration ruleset and find any redundant, duplicate, or conflicting rules. The review is for a busy Director of IT Operations at a Managed Service Provider (MSP) who needs to sign off on NAT forwarding changes. Here is the configuration snippet:
> *   Rule 10: PASS WAN TCP any to 192.168.1.100 port 80 (HTTP Web Server)
> *   Rule 11: PASS WAN TCP any to 192.168.1.100 port 80 (Duplicate rule)
> *   Rule 15: BLOCK WAN TCP any to any port 22 (Block SSH Access)
> *   Rule 16: PASS WAN TCP any to 192.168.1.100 port 22 (Conflicting SSH Pass)

### Output Excerpt:
> Hello Director! As an IT leader at a scaling MSP, you know how crucial rule optimization is for client security and system compliance. Here is an overview for your team:
> *   **Operational Risk (Rule 11)**: Having duplicate rules can confuse junior technicians auditing configurations.
> *   **Compliance Flaw (Rule 16)**: Rule 16 represents a mismatch in client security posture that will fail auditing audits...

### Analysis Notes:
*   **Prompt Change**: Defined a target audience (Director of IT Operations).
*   **Output Improvement**: None.
*   **Remaining Failures**: **This made the output worse.** The model introduced patronizing pleasantries ("Hello Director!", "As an IT leader, you know...") and filled the analysis with corporate buzzwords instead of focusing on direct firewall mechanics.
*   **Next Step**: Enforce a strict markdown output format to strip out the conversational fluff.

---

## Run 4: Version 4 (+ Specified Output Format)
### Prompt:
> Analyze this PfSense configuration ruleset and find any redundant, duplicate, or conflicting rules. The review is for a busy Director of IT Operations at a Managed Service Provider. Present the results in a clean Markdown table with these columns: Rule ID | Rule Details | Issue Type | Description | Operational Risk. Here is the configuration snippet:
> *   Rule 10: PASS WAN TCP any to 192.168.1.100 port 80 (HTTP Web Server)
> *   Rule 11: PASS WAN TCP any to 192.168.1.100 port 80 (Duplicate rule)
> *   Rule 15: BLOCK WAN TCP any to any port 22 (Block SSH Access)
> *   Rule 16: PASS WAN TCP any to 192.168.1.100 port 22 (Conflicting SSH Pass)

### Output Excerpt:
| Rule ID | Rule Details | Issue Type | Description | Operational Risk |
| :--- | :--- | :--- | :--- | :--- |
| **Rule 11** | PASS WAN TCP to 192.168.1.100:80 | Redundant | Identical to Rule 10. | Increases state table tracking and configuration bloating. |
| **Rule 16** | PASS WAN TCP to 192.168.1.100:22 | Conflicting | Blocked by Rule 15 above it. | SSH access remains blocked; causes operational confusion. |

### Analysis Notes:
*   **Prompt Change**: Requested a structured Markdown table with exact column names.
*   **Output Improvement**: The layout shifted entirely to a dense, structured reference grid. It stripped away the conversational greeting and introductory fluff.
*   **Remaining Failures**: The table descriptions and risks are still slightly verbose and contain narrative explanations.
*   **Next Step**: Apply strict word count constraints and ban corporate buzzwords.

---

## Run 5: Version 5 (+ Constraints & Quality Criteria)
### Prompt:
> Analyze this PfSense configuration ruleset and find any redundant, duplicate, or conflicting rules. The review is for a busy Director of IT Operations at a Managed Service Provider. 
> 
> Present the results in a clean Markdown table with these columns: Rule ID | Rule Details | Issue Type | Description | Operational Risk.
> 
> CONSTRAINTS:
> *   Banned words: 'leverage', 'synergy', 'passionate', 'results-driven'.
> *   Write a maximum of 12 words per table cell.
> *   Do not include any intro, greeting, or outro explanation. Output only the markdown table.
> 
> Here is the configuration snippet:
> *   Rule 10: PASS WAN TCP any to 192.168.1.100 port 80 (HTTP Web Server)
> *   Rule 11: PASS WAN TCP any to 192.168.1.100 port 80 (Duplicate rule)
> *   Rule 15: BLOCK WAN TCP any to any port 22 (Block SSH Access)
> *   Rule 16: PASS WAN TCP any to 192.168.1.100 port 22 (Conflicting SSH Pass)

### Output Excerpt:
| Rule ID | Rule Details | Issue Type | Description | Operational Risk |
| :--- | :--- | :--- | :--- | :--- |
| **Rule 11** | PASS WAN TCP to 192.168.1.100:80 | Redundant | Identical to Rule 10. | Bloats ruleset; state tracking overhead. |
| **Rule 16** | PASS WAN TCP to 192.168.1.100:22 | Conflicting | Blocked by Rule 15. | SSH access remains blocked. |

### Analysis Notes:
*   **Prompt Change**: Banned specific buzzwords, restricted cell length, and prohibited intro/outro text.
*   **Output Improvement**: Banned all conversational filler. The output is a highly concise, production-ready markdown reference table.
*   **Remaining Failures**: None. The prompt is fully optimized for the task.
*   **Next Step**: Package this evolved version into a reusable prompt template.

---

## Final Reusable Prompt Template
Below is the cleaned-up prompt template that any network engineer or MSP technician can use directly:

```text
You are an expert network security auditor specializing in PfSense configuration reviews.

Analyze the PfSense firewall configuration snippet provided below and identify any redundant (duplicate) or conflicting rules.

The audit report is for a Director of IT Operations at a Managed Service Provider who requires a zero-trust posture.

OUTPUT FORMAT:
Generate only a Markdown table with the following columns:
Rule ID | Rule Details | Issue Type | Description | Operational Risk

CONSTRAINTS:
1. Limit text to a maximum of 12 words per table cell.
2. Avoid generic business jargon or buzzwords (do not use: leverage, synergy, passionate, results-driven).
3. Do not include any introductory greeting, conversational explanations, or outro summaries. Output ONLY the raw markdown table.

CONFIGURATION SNIPPET:
[PASTE SNIPPET HERE]
```
