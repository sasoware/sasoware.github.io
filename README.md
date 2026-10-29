# SASOWARE — Official Website Infrastructure

**SASOWARE** is an independent software developer brand. This repository contains the **pre-publication source templates and a controlled GitHub Pages pipeline** for its app information and privacy policies, including **DANBI (단비)**, a grocery value calculator.

> **Not a live publication.** The website and privacy policy are not approved for public release. The template contains review-only content; never publish it directly.

## Brand website transition

This repository prepares the official **SASOWARE** website. The existing staging repository remains available during the transition.

## Controlled publication

- **Publishing:** manual GitHub Actions only; no push-triggered website publication.
- **Privacy officer:** owner-provided `PRIVACY_OFFICER` Actions secret; never commit the person's name to repository source or logs. The name will be visible **in the final published policy**.
- **Date:** effective date is set to the South Korea calendar date of the approved deployment.
- **Legal approval:** `POLICY_APPROVED=YES` must reflect a genuinely completed review, not a workaround; keep it unset until then.
- **Deployment confirmation:** a manual workflow dispatch requires `publish_confirmed=YES`.
- **Verification:** the build checks required content, internal routes, Korean/English policy sections, data-deletion links, and `app-ads.txt`. Structural validation is not legal clearance.

**Current status:** publication is held pending final legal-disclosure verification, owner-provided identity and an explicit publication decision. Do not deploy review templates or set approval flags speculatively. This project must not affect DANBI Android development, MAGABI or P2W Online.
