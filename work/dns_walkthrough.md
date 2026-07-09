# Walkthrough: DNS Routing & HTTPS mapping for FlyRank Subdomain

This document explains the infrastructure mechanics behind pointing our custom program subdomain to our hosting servers, written simply for both technical and non-technical readers.

---

## 1. Core Concepts: What is DNS and CNAME?

### What is DNS (Domain Name System)?
Think of DNS as the **phonebook of the internet**. Computers communicate using numbers called IP addresses (e.g., `185.199.108.153`), which are hard for humans to remember. DNS maps human-readable names (like `omnitech.flyrank.com`) to those numeric IP addresses.

### What is a CNAME (Canonical Name) Record?
A **CNAME record** is an "alias" record. Instead of pointing a domain directly to a numeric IP address, a CNAME points a subdomain to another *name*. 

*   *Value*: In our program, the CNAME record for `omnitech.flyrank.com` is configured to point directly to `tagtuner.github.io` (GitHub's standard hosting domain).
*   *Why this matters*: If GitHub changes the IP addresses of its hosting servers, we don't have to update our DNS records. The alias continues to resolve correctly automatically.

---

## 2. The Journey of a Request

When a visitor types `https://omnitech.flyrank.com` into their browser, the following lookup chain occurs:

```
[Browser] 
   │
   ▼ 1. "Who is omnitech.flyrank.com?"
[DNS Resolver (e.g. 8.8.8.8)] 
   │
   ▼ 2. Checks CNAME record -> "Point to tagtuner.github.io"
[GitHub Pages Servers]
   │
   ▼ 3. Reads 'CNAME' file in repository root -> Serves OmniTech index.html
[User Screen]
```

1.  **Browser Query**: The user's browser asks the local DNS resolver (often provided by their ISP or Google `8.8.8.8`) to locate the target subdomain.
2.  **CNAME Resolution**: The DNS resolver checks the registry and discovers the CNAME record pointing `omnitech.flyrank.com` to `tagtuner.github.io`.
3.  **Host IP Query**: The resolver queries the IP addresses for `tagtuner.github.io`, receiving the active IP addresses for GitHub's content delivery network (CDN).
4.  **HTTP Request Delivery**: The browser establishes a connection with GitHub's IP address, sending a request header specifying `Host: omnitech.flyrank.com`.
5.  **Repository Mapping**: GitHub receives the request, parses the host header, scans repository files for a matching `CNAME` configuration file, and serves our custom `index.html` payload.

---

## 3. How HTTPS Secures the Connection

HTTPS (Hypertext Transfer Protocol Secure) ensures that all traffic between the visitor's browser and the hosting server is encrypted. 

*   **Certificate Provisioning**: When we save our custom domain `omnitech.flyrank.com` in our hosting dashboard, GitHub Pages requests a free SSL/TLS certificate from Let's Encrypt (a public Certificate Authority) on our behalf.
*   **Validation**: Let's Encrypt verifies that our CNAME record correctly points to GitHub Pages, proving we own the domain routing path.
*   **Active Encryption**: Once verified, GitHub installs the certificate at their CDN edge. When visitors connect, they establish a secure cryptographic handshake, marked by the padlock icon in their URL bar.
