# Technology Stack Rationale: OmniTech Portfolio

This document outlines the selected technology stack for hosting and presenting the zero-trust systems portfolio, comparing it against alternative platforms.

---

## 1. Chosen Stack: Plain HTML / CSS / JS (Hosted on GitHub Pages)

*   **Hosting Provider**: GitHub Pages (Free, integrated directly with git repository).
*   **Build Pipeline**: Vanilla HTML5, CSS3, and modern Vanilla JS (no build compilation steps required).
*   **Live Portfolio URL**: `https://tagtuner.github.io/flyrank-ml-internship-starter/`
*   **Database / Backend**: None at launch (standard static site; contact form uses static mailto/formspree routing).

---

## 2. Alternatives Considered & Rejected

### Alternative A: No-Code Builders (Carrd / Framer)
*   **Pros**: Visual drag-and-drop, extremely fast design iteration.
*   **Cons**: Free tiers have branding badges, limit custom code integrations (like embedding complex CLI terminal logs or formatting custom JSON files), and do not show version control history.
*   **Reason for Rejection**: As a network systems architect and administrator, showing an active git repository with clean commit history is itself a core technical proof point. No-code abstracts this away, which fails to show raw technical execution.

### Alternative B: Frontend Framework (React / Next.js on Vercel)
*   **Pros**: Highly dynamic, support for complex client-side applications.
*   **Cons**: High configuration overhead, dependency vulnerability updates, build engine configuration issues, and overkill for a three-page static document layout.
*   **Reason for Rejection**: A Next.js stack introduces unnecessary maintenance. I would spend valuable internship hours resolving NPM version mismatches and bundle errors instead of writing case studies.

---

## 3. Maintainability & Feasibility
*   **Can I maintain this?** Yes. By choosing vanilla HTML and CSS, there are zero dependencies to update. Changes are instantly previewed locally and published live via a simple `git push`. 
*   **How does it display my work?** It allows total layout styling freedom matching our Outfit/Inter style guide, displays terminal outputs in native code blocks, and allows embedding raw PfSense XML ruleset snippets cleanly.
