# MDX Frontmatter Standard

This document defines the standard frontmatter structure required for all Docusaurus MDX chapter files (`.mdx`) within the Physical AI & Humanoid Robotics Textbook. Adherence to this standard ensures consistent metadata, proper rendering in Docusaurus, and correct ordering within the sidebar navigation.

## Required Frontmatter Fields

Each `.mdx` file representing a chapter MUST include the following YAML frontmatter at the top of the file:

```yaml
---
id: [unique-chapter-id]
title: [Chapter Title]
description: [Brief summary of the chapter content for SEO and metadata]
sidebar_position: [numeric-order-within-module]
# keywords: [optional, comma-separated list of keywords]
---
```

### Field Descriptions

-   **`id`** (String, **Mandatory**):
    -   A unique identifier for the chapter. This ID is used for generating URLs and linking.
    -   Should be in `kebab-case` and typically follows a pattern like `chapter-M.C-short-title` (e.g., `chapter-1.1-intro-ros2`).
    -   MUST be unique across all chapters in the textbook.
    -   If not explicitly provided, Docusaurus will infer it from the file name, but explicit definition is preferred for clarity and stability.

-   **`title`** (String, **Mandatory**):
    -   The main title of the chapter. This will be displayed in the chapter page, sidebar, and browser tab.
    -   Should be concise and accurately reflect the chapter's content.

-   **`description`** (String, **Mandatory**):
    -   A brief summary (1-2 sentences) of the chapter's content.
    -   Used for SEO purposes and in any generated summaries or card displays.
    -   Should provide enough context for readers to understand the chapter's focus without reading the entire chapter.

-   **`sidebar_position`** (Number, **Mandatory**):
    -   A numeric value that determines the order of the chapter within its parent module (category) in the Docusaurus sidebar.
    -   Chapters with lower `sidebar_position` values will appear higher in the sidebar.
    -   MUST be sequential within a module to ensure a logical learning progression.

### Example

```yaml
---
id: chapter-1.1-introduction-to-ros2
title: Introduction to ROS 2 & Middleware
description: This chapter introduces the Robot Operating System (ROS) 2, its architecture, and fundamental middleware concepts essential for robotic development.
sidebar_position: 1
keywords: [ROS 2, middleware, robotics, introduction]
---

# Introduction to ROS 2 & Middleware
... (chapter content)
```