# Explainer: Agent Concepts & Model Context Protocol (MCP)

This explainer clarifies the core structural differences between AI workflows and autonomous agents, analyzes the three primitives of the Model Context Protocol (MCP), and outlines the upgrade steps required to evolve a static network audit pipeline into an autonomous security agent.

---

## 1. Workflows vs. Agents: The Core Distinction

In the current artificial intelligence landscape, the term "agent" is frequently used as a marketing buzzword for any system that calls an LLM. However, in technical architecture, there is a fundamental dividing line between a **Workflow** and an **Agent**.

### What is a Workflow?
A **workflow** is a deterministic, step-by-step pipeline where the routing, control flow, and sequencing are hardcoded. The developer defines exactly what happens at Step A, how the data is transformed, and where it is passed for Step B. The LLM acts purely as a local text processor or translator inside a fixed step (e.g., summarizing an input or parsing a format). 

In a workflow, the model has no autonomy to decide *which* tool to run next, *whether* to exit the loop, or *how* to change the execution path based on runtime findings. It is a linear assembly line.

### What is an Agent?
An **agent** is a non-deterministic, autonomous system where the LLM functions as the central routing engine (the "brain"). Instead of following a hardcoded path, the agent is given a high-level goal, access to a suite of external tools, and a feedback loop. 

The model dynamically decides:
1.  Which tool to call based on the current state.
2.  What arguments to pass to that tool.
3.  How to interpret the tool's output.
4.  Whether the goal has been achieved or if it needs to choose a different action path.

The control flow is emergent, routing itself dynamically based on real-time environmental input.

### Classifying the Week 5 Rules Audit Pipeline
The PfSense ruleset auditing pipeline built in Week 5 (Draft -> Critique -> Revise) is strictly a **workflow**, not an agent. The pipeline follows a hardcoded linear chain: it takes raw configuration text, drafts a summary, feeds it to a validator, and formats the output into a markdown table. 

At no point does the LLM decide to skip the critique, write an automation script to fix the rule itself, or query active connection states from the firewall. The routing is entirely pre-defined by the developer.

---

## 2. Model Context Protocol (MCP): The USB-C of AI

The Model Context Protocol (MCP) is an open-standard protocol designed to give LLMs secure, standardized access to external data sources and tools. Rather than writing custom integration APIs for every new application, MCP acts like a universal connector (the "USB-C port") for AI models.

MCP is structured around three core primitives:

1.  **Tools**: Executable functions that the model can invoke to perform active operations in the real world (e.g., executing a command-line utility, creating a directory, writing a file, or calling an API). Tools require explicit model decisions and parameter construction.
2.  **Resources**: Read-only data points that are exposed to the model as context (e.g., log files, configuration settings, database schemas, or documentation pages). Resources provide the background facts the model needs to reason accurately.
3.  **Prompts**: Standardized templates or pre-configured system instructions that guide the model's interaction style, formatting, and operational guardrails.

Through these primitives, a model can transcend the boundaries of its static training data, reading live system files (resources) and modifying the environment (tools) in real time.

---

## 3. Upgrading the PfSense Workflow to an Autonomous Agent

To upgrade our static PfSense audit workflow into an autonomous network security agent, we would need to replace our hardcoded prompt chain with an **agentic loop** backed by live MCP tool access:

1.  **Direct Tool Integration (Live Connection)**:
    We must provide the model with a live SSH or API tool connector (e.g., `execute_pfsense_command` or `fetch_xml_config`) so it can autonomously pull rules directly from the production firewall rather than relying on manual file pastes.
2.  **Telemetry Resource Feeds**:
    Expose live network telemetry (like `/var/log/filter.log` or state table metrics) as read-only MCP resources. This allows the agent to continuously monitor live traffic volume.
3.  **Autonomous Analysis & Routing Loop**:
    Instead of a linear chain, we instruct the model: *"Your goal is to maintain state table usage below 70%. If it spikes, audit the ruleset, run an nmap scan on the source IP, and decide whether to drop the connection."*
    
    The agent can now dynamically execute this loop:
    *   *Step A*: Detects state table exhaustion by reading the telemetry resource.
    *   *Step B*: Decides to run `nmap` (using the command tool) to audit the source.
    *   *Step C*: Evaluates the nmap scan results.
    *   *Step D*: Dynamically constructs and deploys a temporary block rule to neutralize the attack.
    *   *Step E*: Verifies that state table metrics return to normal, closing the loop.

This upgrade transforms the system from a passive reporting utility into an active, self-healing network security guard.
