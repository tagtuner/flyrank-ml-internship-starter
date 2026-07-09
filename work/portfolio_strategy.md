# Portfolio Strategy & Proof Statement

## 1. The Proof Statement
"I design and audit zero-trust enterprise networks using PfSense firewalls for a Director of IT Operations at a scaling Managed Service Provider, so they will book a 15-minute network architecture review call to resolve their routing and security bottlenecks."

*   **The One Claim**: I design and audit zero-trust enterprise networks using PfSense firewalls.
*   **The One Person**: A Director of IT Operations at a scaling Managed Service Provider (MSP).
*   **The One Action**: Book a 15-minute network architecture review call.

---

## 2. Why This Needs to Exist
"A static CV or LinkedIn profile only lists high-level credentials and keyword dumps like 'PfSense' or 'Firewalls', but fails to prove my actual diagnostic process in auditing live firewall rulesets, resolving state table exhaustions, and verifying network security postures under simulated external scans."

---

## 3. Portfolio Sitemap
*   **`/` (Landing Page)**: 
    *   *Goal*: State the core claim instantly and hook the visitor.
    *   *Content*: A bold headline outlining the PfSense zero-trust claim, a high-level summary of network optimization achievements (e.g., duplicate rule reduction, port hardening stats), and a clear "Book Review Call" call-to-action (CTA).
*   **`/pfsense-audit` (Case Study)**: 
    *   *Goal*: Prove the claim with technical depth.
    *   *Content*: A step-by-step technical case study showing the auditing of a production PfSense ruleset, identifying redundant configurations, hardening NAT port forwards, and confirming the zero-trust posture via external vulnerability scanning.
*   **`/about`**: 
    *   *Goal*: Establish professional credibility.
    *   *Content*: Technical summary of experience, active certifications (e.g., netsec, routing), and zero-trust design philosophy.
*   **`/audit-booking` (Action Page)**: 
    *   *Goal*: Complete the target action.
    *   *Content*: Simple inline calendar interface to schedule the 15-minute network architecture review call.

---

## 4. Claude Project Custom Instructions
```text
You are a technical tutor helping me build a portfolio. Act as a critical advisor. 
My profile context:
- Proof Statement: "I design and audit zero-trust enterprise networks using PfSense firewalls for a Director of IT Operations at a scaling Managed Service Provider, so they will book a 15-minute network architecture review call."
- Focus areas: PfSense rule tuning, state table optimization, zero-trust routing.
- Tone preferences: Direct, brief, technical, engineering-focused. Avoid encouraging fluff; give critical pushback.
```

---

## 5. Pressure-Test Prompt & Output
### Prompt:
> This is my proof statement: "I design and audit zero-trust enterprise networks using PfSense firewalls for a Director of IT Operations at a scaling Managed Service Provider, so they will book a 15-minute network architecture review call."
> 
> This is my sitemap:
> 1. Landing Page (`/`): Headline declaring the claim, metrics overview, CTA to book.
> 2. Case Study (`/pfsense-audit`): Auditing and hardening a production PfSense ruleset, zero-trust validation.
> 3. Profile (`/about`): Certifications, network architecture background, zero-trust philosophy.
> 4. Booking Page (`/audit-booking`): Simple calendar booking interface.
> 
> Does this sitemap walk my one person from landing, to believing me, to taking my one action, and does it actually prove my claim? Tell me which pages earn their place, which are wasted, and what is missing. Be specific, not encouraging.

### Output (Claude Tutor):
> *   **Earn Their Place**: 
>     *   `/pfsense-audit` (Case Study) is the absolute core. For an MSP Director of IT Operations, the biggest fear is a security breach or configuration error causing client downtime. Seeing a step-by-step audit of a complex PfSense configuration with before-and-after proof is exactly what builds belief.
>     *   `/audit-booking` earns its place as the single destination for the target action.
> *   **Wasted / Needs Work**:
>     *   `/` (Landing Page): If it only repeats the claim and shows generic metrics, it is weak. It needs to lead directly with a snippet of the PfSense rule audit or a visual visualization of a hardened rule layout to hook a technical reviewer in 5 seconds.
>     *   `/about`: For an MSP Director, your generic philosophy matters less than your tool-specific expertise. Merge this content directly into the landing page or case study. An independent page here is a wasted click.
> *   **What is Missing**:
>     *   An interactive "Rule Auditor Mockup" or live tool. Since your claim is "design and audit zero-trust networks using PfSense", having a simple interactive client-side ruleset checker widget directly on the landing page would instantly prove capability before they even click the case study.
> 
> **Decision / Change noted based on pressure test**:
> I will remove the standalone `/about` page and merge the relevant certifications/background directly into the footer of the Landing Page and Case Study. Every page must lead directly to the `/audit-booking` action. I will add an interactive log parsing mock component to the Landing Page to hook the visitor immediately.
