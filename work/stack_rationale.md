# Technology Stack Rationale: OmniTech Portfolio

This document evaluates the options for building and hosting the zero-trust systems portfolio, performing a direct comparison and pressure-test of the chosen stack.

---

## 1. The Three Stack Options

We compared three options, ranging from simplest to most powerful, to determine which fits our constraints best.

| Road | Stack Name | How to Build | Where to Host | Backend Required? | The Real Trade-off |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Road 1 (Simplest)** | **No-Code (Carrd / Framer)** | Drag-and-drop visual builder. | Carrd Free Tier / Framer Hosting. | No. (Not at launch). | Zero code control. Hard to display raw terminal screens and custom interactive JSON files. Free versions carry vendor watermarks. |
| **Road 2 (Medium)** | **Vanilla Code (HTML5/CSS3/JS)** | Write clean HTML, styled with CSS tokens. | GitHub Pages (connected to Git repository). | No. (Not at launch; contact form is static). | **Chosen**. Requires writing layout markup manually, but offers absolute control over fonts and style guides. |
| **Road 3 (Most Powerful)** | **JS Framework (Next.js / Vite)** | NPM packages, modular JS/TypeScript. | Vercel or Netlify Free Tier. | Yes (serverless functions for API endpoints if needed). | Overkill for a static site. Requires managing package dependencies, resolving build-time bundler errors, and ongoing security updates. |

---

## 2. Pressure-Testing the Front-Runner (Vanilla Code)

We evaluated the front-runner stack (Vanilla Code on GitHub Pages) against four critical operational questions:

*   **What breaks if I pick the simplest (No-Code)?**
    *   *Answer*: My ability to display raw technical evidence. A static portfolio for an infrastructure engineer needs to show terminal console outputs (from nmap, IPSec tunnels) and parsed PfSense XML snippets. No-code builders compress images and restrict custom pre/code blocks, making technical documentation look blurry or badly formatted. It also hides version control history, which is itself developer proof.
*   **What do I maintain if I pick the most powerful (Framework)?**
    *   *Answer*: A constant dependency tail. A Next.js build requires periodic package audit runs, React version upgrades, and Vercel pipeline updates. If I leave the site for six months, I will return to compilation warnings. A vanilla HTML/CSS page requires zero maintenance.
*   **Can I finish in two weeks?**
    *   *Answer*: Yes. By using vanilla code, the build time is zero. We don't have to wait for webpack or vite compilation. Writing three pages (Landing, PfSense Case Study, Booking Page) with our styling guides takes a few hours.
*   **Does it show my work the way it needs to be shown?**
    *   *Answer*: Yes, perfectly. Vanilla code allows full pre-formatted text tags (`<pre><code>`) for terminal outputs and CLI dumps. We can load our custom brand fonts (Outfit & Inter) and terracotta colors directly without framework configuration layers.

---

## 3. Rationale & Final Decision

I chose **Vanilla HTML/CSS/JS hosted on GitHub Pages**. I rejected the no-code road because it hides the git commit history which serves as core proof of execution for a dev/infrastructure role. I rejected the framework road because it introduces useless configuration layers that distract from text-focused case studies. I can easily maintain this vanilla setup forever because it has no dependencies to break, and it displays my rulesets, nmap logs, and network metrics with pixel-perfect accuracy.
