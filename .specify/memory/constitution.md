<!--
Sync Impact Report:
Version change: 0.0.0 → 1.0.0
Modified principles: None (initial creation)
Added sections: Core Principles, Mandatory Coverage, Docusaurus Standards, Sources & Quality, Constraints & Outcome, Governance
Removed sections: None
Templates requiring updates:
- ✅ .specify/templates/plan-template.md
- ✅ .specify/templates/spec-template.md
- ✅ .specify/templates/tasks-template.md
Follow-up TODOs: None
-->
# Physical AI & Humanoid Robotics Textbook Constitution

## Core Principles

### I. Spec-First Only
All chapters must be written from approved Spec-Kit Plus specifications.

### II. Physical AI Focus
All AI concepts must be embodied (sensors, actuators, closed-loop systems).

### III. Verified Content
All technical claims must be checked against official docs or robotics research.

### IV. Reproducible
Every step, command, and setup must be executable by readers.

### V. Audience-Centric
Content must be tailored for beginner–intermediate CS/AI/Robotics students.

### VI. Mandatory Coverage
The book must cover the full humanoid robotics stack:
- Perception & Sensing
- World Modeling
- Control & Locomotion
- Manipulation
- Planning & Decision Making
- Learning (RL / IL / Foundation Models)
- Simulation & Sim-to-Real
- Hardware–Software Co-Design
- Safety & Failure Modes

### VII. Docusaurus Standards
- Docusaurus v2, docs-only mode.
- All content resides in the `/docs` directory.
- One Part corresponds to one category; one Chapter corresponds to one MDX file.
- All documents must include `id`, `title`, `description`, and `sidebar_position` frontmatter.
- The sidebar order must follow a logical learning progression.
- Diagrams should be created using Mermaid where possible; other static images are stored in `/static/img`.

### VIII. Sources & Quality
- A minimum of 40% of sources must be from peer-reviewed robotics and AI papers.
- The remaining sources should be official documentation for hardware or software.
- All code examples must be runnable, clean, and well-documented.
- Content must meet a Flesch-Kincaid grade level of 8–12 for readability.
- There is a zero-tolerance policy for plagiarism.

### IX. Constraints & Outcome
- The final textbook will consist of 10–15 chapters.
- The total word count will be between 15,000 and 25,000 words.
- The content will be written in Docusaurus MDX format.
- The project will be considered complete upon successful deployment to GitHub Pages with complete and correct navigation.

## Governance

This Constitution is the single source of truth for project standards and supersedes all other practices. Amendments require formal documentation, review, and an approved migration plan. All contributions, pull requests, and reviews must verify compliance with these principles. Any deviation or increase in complexity from these standards must be explicitly justified and approved.

**Version**: 1.0.0 | **Ratified**: 2025-12-15 | **Last Amended**: 2025-12-15