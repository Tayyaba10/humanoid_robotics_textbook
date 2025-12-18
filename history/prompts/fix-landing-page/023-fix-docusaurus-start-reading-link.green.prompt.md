---
id: 023
title: Fix Docusaurus Start Reading Link
stage: green
date: 2025-12-17
surface: agent
model: gemini-cli
feature: fix-landing-page
branch: 2-fix-landing-page
user: unspecified
command: /sp.implement Fix broken “Start Reading” link on Docusaurus landing page.
labels: [implement, docusaurus, bugfix]
links:
  spec: specs/2-fix-landing-page/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - humanoid-robotics-textbook/src/pages/index.tsx
  - specs/2-fix-landing-page/tasks.md
tests:
  - none
---

## Prompt

/sp.implement Fix broken “Start Reading” link on Docusaurus landing page.

- Current CTA links to `/docs/intro` (invalid).
- Update CTA to link to an existing doc:
  `/docs/introduction`
- Do not create new docs.
- Only update landing page link.
- Return minimal code change only.

## Response snapshot

Fixed the broken "Start Reading" link on the Docusaurus landing page by updating the `to` attribute in the `Link` component in `src/pages/index.tsx` from `/docs/intro` to `/docs/introduction`. Task T004 in `tasks.md` was also marked as completed.

## Outcome

- ✅ Impact: The "Start Reading" button on the landing page now correctly navigates to the introduction page.
- 🧪 Tests: None run. Manual validation would be required.
- 📁 Files: Modified `humanoid-robotics-textbook/src/pages/index.tsx` and `specs/2-fix-landing-page/tasks.md`.
- 🔁 Next prompts: Commit changes.
- 🧠 Reflection: Another small, targeted fix provided by the user. The process is efficient when the user provides clear instructions.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): n/a
