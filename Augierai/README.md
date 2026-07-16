# 🚀 Founding ML Engineer — Agentic Quote Parser Code Walkthrough

This repository contains a production-grade agentic quote parsing and validation pipeline designed to parse messy logistics text inputs (emails, sheets) into structured, validated quotes.

---

## 🎥 Loom Video Presentation Outline (5–10 Minutes)

Use the following outline when recording your Loom screen-share to demonstrate professional-grade engineering maturity:

### 1. Introduction (1 Minute)
*   Show your face, introduce yourself briefly, and set the goal: *"Today, I am walking through my solution for the agentic quote extraction and pricing verification pipeline."*
*   Show the files in the directory (`quote_agent.py`, `README.md`).

### 2. Architecture Choices (2.5 Minutes)
*   **The Problem:** Raw inputs from logistics carriers are highly unstructured (different formats, units, missing fields).
*   **The Split Design:** We separate **LLM extraction** from **strict data validation**.
    *   *Why?* Relying solely on LLMs to output valid data ranges causes silently corrupted inputs. We use **Pydantic** to enforce strong type verification (`weight_kg` must be positive, `container_count` must be $\ge 1$).
    *   *Business Rules Separation:* Once validated, data is passed to a deterministic pricing logic layer, ensuring safety checks (like checking if total weight exceeds container limits) are executed with 100% reliability, rather than letting the LLM estimate rates.

### 3. Live Execution Demo (2 Minutes)
*   Open your terminal and run: `python quote_agent.py`
*   Show the console output showing:
    1. The raw input email.
    2. The simulated extraction phase.
    3. The successful Pydantic validation log.
    4. The final structured JSON output containing pricing rates and validation approval.

### 4. Evaluation Strategy (Evals) (1.5 Minutes)
*   **The Script:** Open and run `run_evals.py` on the screen.
*   **Show the Test Cases:** Explain that we run a structured regression test suite:
    *   *TC-01:* A standard valid request (Karachi to Jebel Ali) yields an Approved quote.
    *   *TC-02:* A negative cargo weight typo triggers Pydantic's structural validation schema.
    *   *TC-03:* Heavy machinery (28,000 kg) triggers the downstream business-rules check and gets rejected as overweight.
    *   *TC-04:* Zero containers triggers Pydantic count validation.
*   Explain that this regression table evaluates prompt edits or framework logic shifts automatically.

### 5. Production Hardening (1 Minute)
*   Explain what you would do before pushing this to production:
    1.  **Rate Limiting & Retries:** Implement exponential backoff with jitter on API connections (e.g., using `tenacity`) to handle API timeouts.
    2.  **Telemetry:** Connect log structures to tools like LangFuse or Datadog to log agent reasoning traces.
    3.  **Local Inference Fallback:** Configure a local llama-3 instance (Ollama) to act as a fallback node if the external Anthropic API hits rate limits or experiences downtime.
