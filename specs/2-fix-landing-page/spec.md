# Feature Specification: Fix Docusaurus Landing Page

**Feature Branch**: `2-fix-landing-page`
**Created**: 2025-12-17
**Status**: Draft
**Input**: User description: "## Context Book already generated via **SpecKitPlus / Claude** and deployed on **Docusaurus**. Current issue: **Landing page (homepage) not showing**, site opens **directly on book modules/docs**. ## Goal Enable a **proper Docusaurus landing page** (`/`) before docs/modules, with clear navigation to the book. ## Requirements 1. Create a **custom homepage** using `src/pages/index.tsx` (or `index.js`). 2. Homepage should include: - Book title & subtitle - Short description - CTA buttons: - **Start Reading** → `/docs/intro` - **View Modules** → `/docs` 3. Ensure **docs are not set as the default route**. ## Configuration Changes - Update `docusaurus.config.js`: - `routeBasePath: 'docs'` (NOT `/`) - Enable navbar link to Docs - Ensure `docs/intro.md` exists as entry point. ## Acceptance Criteria - Visiting `/` shows landing page - Visiting `/docs` shows book modules - Navbar allows switching between Home & Docs - GitHub Pages / live deployment reflects changes ## Output Expected - Homepage component code - Updated `docusaurus.config.js` - Minimal, clean UI (no extra content)"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - View Landing Page (Priority: P1)

As a new visitor, I want to see a landing page when I visit the root URL, so I can get an overview of the book before diving into the content.

**Why this priority**: This is the most critical user journey as it affects every new user's first impression and navigation experience.

**Independent Test**: Can be fully tested by navigating to the root URL (`/`) and verifying that the landing page is displayed.

**Acceptance Scenarios**:

1. **Given** a user navigates to the root URL (`/`), **When** the page loads, **Then** the landing page with the book title, subtitle, description, and CTA buttons is displayed.
2. **Given** a user is on the landing page, **When** they click the "Start Reading" button, **Then** they are navigated to the `/docs/intro` page.
3. **Given** a user is on the landing page, **When** they click the "View Modules" button, **Then** they are navigated to the `/docs` page.

---

### User Story 2 - Navigate between Home and Docs (Priority: P2)

As a user, I want to easily navigate between the homepage and the documentation using the navigation bar.

**Why this priority**: This provides a consistent and expected navigation experience for users.

**Independent Test**: Can be tested by clicking the navigation links on both the homepage and the docs pages.

**Acceptance Scenarios**:

1. **Given** a user is on the landing page, **When** they click the "Docs" link in the navbar, **Then** they are navigated to the `/docs` page.
2. **Given** a user is on a docs page (e.g., `/docs/intro`), **When** they click the "Home" link or site logo in the navbar, **Then** they are navigated back to the landing page (`/`).

### Edge Cases

- What happens when a user tries to access a non-existent page? (A standard 404 page should be shown).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST display a custom homepage when a user visits the root URL (`/`).
- **FR-002**: The homepage MUST include the book title, a subtitle, a short description, and two Call-to-Action (CTA) buttons.
- **FR-003**: The "Start Reading" CTA button MUST link to `/docs/intro`.
- **FR-004**: The "View Modules" CTA button MUST link to `/docs`.
- **FR-005**: The documentation content MUST be accessible under the `/docs` route path.
- **FR-006**: The navigation bar MUST contain a link to the documentation.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of users visiting the root URL are shown the landing page.
- **SC-002**: Users can navigate from the landing page to the documentation in a single click.
- **SC-003**: The live deployment on GitHub Pages correctly reflects the new landing page and routing configuration.
