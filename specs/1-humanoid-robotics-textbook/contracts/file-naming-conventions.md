# File Naming Conventions for Physical AI & Humanoid Robotics Textbook

This document outlines the mandatory file naming conventions for all content and asset files within the Physical AI & Humanoid Robotics Textbook project. Consistent naming ensures clarity, ease of navigation, and proper functioning within the Docusaurus framework.

## General Principles

-   All file names MUST be lowercase.
-   Words MUST be separated by hyphens (`-`) (kebab-case).
-   File names should be descriptive yet concise, reflecting the content of the file.
-   Avoid special characters, spaces, and underscores.

## Content Files (`.mdx`)

-   **Chapters**: `[module-number]-[chapter-number]-[short-descriptive-title].mdx`
    -   Example: `01-01-introduction-to-ros2.mdx`
    -   The module and chapter numbers ensure logical ordering within directories, even without explicit `sidebar_position`.
-   **Module Index/Category Files**: `_category_.json` for Docusaurus category metadata.
    -   Example: `docs/01-module-ros2/_category_.json`

## Image and Asset Files (`.svg`, `.png`, `.jpg`, etc.)

-   All image files MUST be stored in the `static/img/` directory or a subdirectory within it.
-   File names for images and other static assets should be descriptive of their content.
-   Example: `robot-kinematics-diagram.svg`, `gazebo-screenshot-module-2.png`

## Example Directory Structure

```text
humanoid-robotics-textbook/
├── docs/
│   ├── _category_.json                      # Main docs category
│   ├── 01-module-ros2/
│   │   ├── _category_.json                  # Module 1 category metadata
│   │   ├── 01-01-introduction-to-ros2.mdx   # Chapter 1.1
│   │   └── 01-02-ros2-nodes-topics.mdx      # Chapter 1.2
│   ├── 02-module-simulation/
│   │   ├── _category_.json                  # Module 2 category metadata
│   │   └── 02-01-gazebo-basics.mdx          # Chapter 2.1
├── static/
│   └── img/
│       ├── robot-kinematics-diagram.svg
│       └── gazebo-screenshot-module-2.png
└── ...
```