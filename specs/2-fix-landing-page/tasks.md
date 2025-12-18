# Tasks: Fix Docusaurus Landing Page

**Input**: Design documents from `/specs/2-fix-landing-page/`
**Prerequisites**: plan.md, spec.md

## Phase 1: User Story 1 - View Landing Page (Priority: P1) 🎯 MVP

**Goal**: Create and display a new landing page at the root URL.

**Independent Test**: Visiting the root URL (`/`) shows the new landing page with all expected elements.

### Implementation for User Story 1

- [ ] T001 [US1] Modify `humanoid-robotics-textbook/docusaurus.config.ts` to set the `routeBasePath` for the docs plugin to `'docs'`.
- [ ] T002 [US1] Create the landing page component file `humanoid-robotics-textbook/src/pages/index.tsx`.
- [ ] T003 [US1] In `humanoid-robotics-textbook/src/pages/index.tsx`, add the book title, subtitle, and a short description.
- [ ] T004 [US1] In `humanoid-robotics-textbook/src/pages/index.tsx`, add two CTA buttons: "Start Reading" linking to `/docs/intro` and "View Modules" linking to `/docs`.

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently.

---

## Phase 2: User Story 2 - Navigate between Home and Docs (Priority: P2)

**Goal**: Ensure seamless navigation between the new homepage and the documentation via the navbar.

**Independent Test**: The navbar should contain a "Docs" link that correctly navigates to the documentation section.

### Implementation for User Story 2

- [X] T005 [US2] Update the `navbar` configuration in `humanoid-robotics-textbook/docusaurus.config.ts` to include a link to the "Docs" section.

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently.

---

## Phase 3: Polish & Cross-Cutting Concerns

**Purpose**: Final validation and verification.

- [X] T006 Run all validation steps outlined in `specs/2-fix-landing-page/quickstart.md` to confirm the feature is working as expected.

---

## Dependencies & Execution Order

- **T001** and **T002** can be done in parallel.
- **T003** and **T004** depend on **T002**.
- **T005** can be done in parallel with User Story 1 tasks.
- **T006** depends on all other tasks being complete.
