---
id: 001
title: Create Project Constitution for Humanoid Robotics Textbook
stage: constitution
date: 2025-12-15
surface: agent
model: gemini-pro
feature: none
branch: master
user: Tayyaba10
command: /sp.constitution Create a complete technical textbook on Physical AI & Humanoid Robotics using Docusaurus v2, Spec-Kit Plus, and Claude Code, and deploy it to GitHub Pages.
labels: ["constitution", "setup"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
 - .specify/templates/plan-template.md
 - .specify/templates/tasks-template.md
tests:
 (none)
---

## Prompt

/sp.constitution Create a complete technical textbook on Physical AI & Humanoid Robotics using Docusaurus v2, Spec-Kit Plus, and Claude Code, and deploy it to GitHub Pages.

Core Rules

Spec-first only: All chapters must be written from approved Spec-Kit Plus specifications.

Physical AI focus: All AI concepts must be embodied (sensors, actuators, closed-loop systems).

Verified content: All technical claims must be checked against official docs or robotics research.

Reproducible: Every step, command, and setup must be executable by readers.

Audience: Beginner–intermediate CS/AI/Robotics students.

Mandatory Coverage

The book must cover the full humanoid robotics stack:

Perception & Sensing

World Modeling

Control & Locomotion

Manipulation

Planning & Decision Making

Learning (RL / IL / Foundation Models)

Simulation & Sim-to-Real

Hardware–Software Co-Design

Safety & Failure Modes

Docusaurus Standards

Docusaurus v2, docs-only

Content lives in /docs

1 Part = 1 category, 1 Chapter = 1 MDX file

Required frontmatter: id, title, description, sidebar_position

Sidebar order = learning order

Diagrams via Mermaid preferred; images in /static/img

Sources & Quality

≥ 40% peer-reviewed robotics/AI papers

Remaining sources: official documentation

Code must be runnable and clean

Readability: Flesch-Kincaid grade 8–12

Zero plagiarism

Constraints & Outcome

10–15 chapters, 15k–25k words

Format: Docusaurus MDX

Successful GitHub Pages deployment with complete navigation

## Response snapshot

I have successfully created the project constitution and updated the relevant templates.

- **Created:** `.specify/memory/constitution.md` (Version 1.0.0)
- **Updated:** `.specify/templates/plan-template.md` with a new Constitution Check section.
- **Updated:** `.specify/templates/tasks-template.md` with a Constitution Reminder.

## Outcome

- ✅ Impact: High - Established the foundational principles for the project.
- 🧪 Tests: None
- 📁 Files: 3 files modified
- 🔁 Next prompts: The user can now proceed with other setup tasks or start creating specifications for the textbook chapters.
- 🧠 Reflection: The user provided a very detailed prompt, which made it easy to create a comprehensive constitution. The process of updating the templates ensures that the constitution will be referenced throughout the development lifecycle.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): n/a
