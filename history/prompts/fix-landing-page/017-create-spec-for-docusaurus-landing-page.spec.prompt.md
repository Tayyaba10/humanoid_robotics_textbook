---
id: 017
title: Create Spec for Docusaurus Landing Page
stage: spec
date: 2025-12-17
surface: agent
model: gemini-cli
feature: fix-landing-page
branch: 2-fix-landing-page
user: unspecified
command: /sp.specify
labels: [spec, docusaurus, landing-page]
links:
  spec: specs/2-fix-landing-page/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/2-fix-landing-page/spec.md
  - specs/2-fix-landing-page/checklists/requirements.md
tests:
  - none
---

## Prompt

## Context Book already generated via **SpecKitPlus / Claude** and deployed on **Docusaurus**. Current issue: **Landing page (homepage) not showing**, site opens **directly on book modules/docs**. ## Goal Enable a **proper Docusaurus landing page** (`/`) before docs/modules, with clear navigation to the book. ## Requirements 1. Create a **custom homepage** using `src/pages/index.tsx` (or `index.js`). 2. Homepage should include: - Book title & subtitle - Short description - CTA buttons: - **Start Reading** → `/docs/intro` - **View Modules** → `/docs` 3. Ensure **docs are not set as the default route**. ## Configuration Changes - Update `docusaurus.config.js`: - `routeBasePath: 'docs'` (NOT `/`) - Enable navbar link to Docs - Ensure `docs/intro.md` exists as entry point. ## Acceptance Criteria - Visiting `/` shows landing page - Visiting `/docs` shows book modules - Navbar allows switching between Home & Docs - GitHub Pages / live deployment reflects changes ## Output Expected - Homepage component code - Updated `docusaurus.config.js` - Minimal, clean UI (no extra content)

## Response snapshot

Created a new feature branch `2-fix-landing-page` and generated the feature specification `specs/2-fix-landing-page/spec.md` and a validation checklist. The specification outlines the user stories, functional requirements, and success criteria for creating a new landing page for the Docusaurus site.

## Outcome

- ✅ Impact: High. This change is critical for establishing a proper user entry point to the website.
- 🧪 Tests: None run.
- 📁 Files: Created `specs/2-fix-landing-page/spec.md` and `specs/2-fix-landing-page/checklists/requirements.md`.
- 🔁 Next prompts: /sp.plan
- 🧠 Reflection: The process of manually creating the feature files after the script failure was straightforward.

## Evaluation notes (flywheel)

- Failure modes observed: PowerShell script execution was blocked by system policy.
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): n/a
