# Glossary Term Tagging Convention for Physical AI & Humanoid Robotics Textbook

This document establishes the convention for identifying and tagging key technical terms within the textbook chapters that are intended to be included in a comprehensive glossary. Adhering to this convention will streamline the automated (or semi-automated) generation and maintenance of the textbook's glossary.

## General Principle

Any term that is a key technical concept, acronym, or specialized vocabulary, and whose meaning might not be immediately clear to a beginner-intermediate student in CS/AI/Robotics, SHOULD be tagged for inclusion in the glossary.

## Tagging Mechanism

Terms intended for the glossary MUST be enclosed in a specific inline Markdown/HTML tag. This allows for easy extraction and processing.

### Recommended Tagging Structure

Use a custom Docusaurus component or a consistent Markdown extension (if available and configured) to highlight glossary terms. For simplicity and broad compatibility, we will initially use a standard HTML `<span>` tag with a specific class that can be targeted by a script.

```html
<span class="glossary-term" data-term="[Term]">Description/Context where term is used</span>
```

**Field Descriptions**:

-   **`class="glossary-term"`**: A fixed class name that identifies the `<span>` element as a glossary term.
-   **`data-term="[Term]"`**: An HTML `data` attribute storing the canonical form of the term. This is the exact term that will appear in the glossary.
-   **`Description/Context where term is used`**: The actual text in the chapter where the term appears. This will be visible to the reader.

### Example

Within a chapter, if the term "Robot Operating System (ROS)" is introduced and needs to be in the glossary:

```markdown
The <span class="glossary-term" data-term="Robot Operating System (ROS)">Robot Operating System (ROS)</span> is a flexible framework for writing robot software.
```

Or, for an acronym:

```markdown
This approach leverages <span class="glossary-term" data-term="Sim-to-Real">sim-to-real</span> transfer learning.
```

## Glossary Generation (Future State)

A script (to be developed) will:
1.  Scan all `.mdx` chapter files.
2.  Extract all `<span>` elements with `class="glossary-term"`.
3.  Collect the `data-term` attribute values.
4.  Optionally, collect the surrounding text for context.
5.  Generate the main glossary file (e.g., `docs/glossary.mdx`) in an alphabetical, descriptive format.

## Responsibility

Authors are responsible for correctly tagging terms. Reviewers are responsible for ensuring appropriate terms are tagged and that `data-term` values are consistent (e.g., "ROS" vs "Robot Operating System (ROS)").
