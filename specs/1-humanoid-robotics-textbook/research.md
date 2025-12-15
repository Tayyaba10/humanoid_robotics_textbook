# Research for Physical AI & Humanoid Robotics Textbook

This document will contain the findings from the research tasks identified in the implementation plan.

## Research Tasks

1.  **Identify compatible NVIDIA Isaac Sim version**: Determine the specific NVIDIA Isaac Sim version that is officially compatible with ROS 2 Jazzy Jalisco and Gazebo Harmonic.
2.  **Docusaurus integration best practices**: Research best practices for integrating complex code examples, interactive elements, and external simulation environments within a Docusaurus v2 site.
3.  **Docusaurus sidebar structure**: Investigate optimal strategies for structuring Docusaurus sidebars to represent a multi-module, multi-chapter textbook with a clear learning progression.
4.  **Mermaid diagram integration**: Research the best way to incorporate Mermaid diagrams into Docusaurus MDX files for clear, maintainable visualizations.
5.  **Troubleshooting documentation**: Identify effective strategies and best practices for documenting troubleshooting steps, common error messages, and debugging guidance within an educational textbook context.
6.  **Citation management**: Research robust methods for managing citations and integrating references (especially peer-reviewed papers) within Docusaurus.

## Findings

### T008: Compatible NVIDIA Isaac Sim version for ROS 2 Jazzy Jalisco and Gazebo Harmonic

**Decision**: The exact compatible version of NVIDIA Isaac Sim with ROS 2 Jazzy Jalisco and Gazebo Harmonic needs to be manually verified against the latest official NVIDIA Isaac Sim documentation, ROS 2 release notes, and Gazebo compatibility matrices. This information is dynamic and requires real-time lookup.

**Rationale**: Compatibility matrices for complex robotics software stacks (ROS 2, Gazebo, NVIDIA Isaac Sim) are frequently updated. Relying on static information could lead to outdated or incorrect guidance for students, causing frustration and setup issues. Direct consultation of official vendor documentation is the most reliable method.

**Alternatives Considered**:
-   Assuming a specific version: Rejected due to the risk of providing outdated or incorrect information.
-   Leaving it unspecified: Rejected as this would hinder reproducibility and setup for students.

**Action for implementation**: Refer to the official NVIDIA Isaac Sim documentation and ROS 2 Jazzy Jalisco / Gazebo Harmonic release notes for the most up-to-date compatibility information during setup.

### T009: Docusaurus integration best practices for complex code examples and simulation environments

**Decision**: A multi-faceted approach leveraging Docusaurus's native Markdown features for static code examples and custom React components/iframes for interactive/embedded simulations is the recommended best practice.

**Rationale**: This approach balances ease of authoring for static content with the need for interactive and dynamic experiences where appropriate, while also addressing performance and maintainability concerns.

**Alternatives Considered**:
-   Only static code blocks: Rejected as it limits interactive learning for complex robotics concepts.
-   Heavy reliance on external platforms (e.g., CodeSandbox): Rejected as it introduces external dependencies and potential breakage.
-   Building all simulations from scratch as web apps: Rejected as it's overly complex and out of scope for a textbook focused on robotics rather than web development.

**Best Practices for Code Examples**:
-   **Static Examples**: Use Markdown code blocks with language specification for syntax highlighting, line highlighting (`{1,3-5}`), line numbering (`showLineNumbers`), and titles (`title="filename.ext"`). Keep examples concise and focused.
-   **Interactive Examples**:
    -   Embed external platforms like CodeSandbox/StackBlitz for runnable front-end examples via `iframe`.
    -   Develop custom React components (`src/components/`) for in-page runnable code snippets (e.g., using `react-live`) or to display/run code imported from separate files.
-   **Monorepo Integration**: If code snippets are part of a larger codebase, use build scripts or relative paths to keep examples in sync and link to full source files.

**Strategies for Simulation Integration**:
-   **`iframe` Embedding**: For existing web-based simulations (e.g., deployed Gazebo web UI, external scientific simulations), use an `<iframe>`. Ensure responsiveness and be mindful of security.
-   **Custom React Components**: For in-page interactive simulations built with JavaScript/TypeScript, create dedicated React components (`src/components/`). This allows for dynamic data flow and control.
-   **WebAssembly (Wasm)**: For performance-intensive simulations in C++/Rust, compile to Wasm and integrate via React components for near-native performance.
-   **Static Visualizations with Playback**: For complex simulations, generate static assets (GIFs, videos) from runs and add simple playback controls via React components.

**General Tips**:
-   **Performance**: Optimize assets, lazy-load heavy components, and manage expensive operations.
-   **Accessibility**: Ensure interactive elements are accessible (keyboard navigation, screen readers).
-   **Responsiveness**: Adapt content to various screen sizes.
-   **Clear Instructions**: Always provide explicit instructions for using interactive elements.

### T010: Docusaurus sidebar structure for multi-module textbook

**Decision**: The multi-module textbook structure will be implemented using Docusaurus categories in `sidebars.ts`, leveraging `generated-index` links for each module.

**Rationale**: This approach provides a clear, hierarchical navigation structure that is intuitive for a multi-module textbook format. `generated-index` links automatically create landing pages for each module, enhancing discoverability and organization.

**Alternatives Considered**:
-   Flat list of all chapters: Rejected as it would not scale well for a textbook with multiple modules and would make navigation difficult.
-   Using multiple `docs` plugins in `docusaurus.config.ts`: Rejected as it's typically for entirely separate documentation instances, and a single `docs` plugin with category-based sidebars is more appropriate for a single, multi-module textbook.

**Implementation Details**:
-   Each module will be defined as a `type: 'category'` in `sidebars.ts`.
-   Each category will have a `label` corresponding to the module title.
-   A `link` object with `type: 'generated-index'` will be used for each module to automatically create a landing page.
-   `items` array within each category will contain the list of chapters belonging to that module. Chapters will be added sequentially using their `id` or file path.
-   The `sidebar_position` frontmatter in each chapter MDX file will control the order of chapters within their respective modules.

### T011: Mermaid diagram integration in Docusaurus MDX

**Decision**: Mermaid diagrams will be integrated into Docusaurus MDX using a client-side rendering approach. This involves Docusaurus parsing `mermaid` code blocks into a specific HTML structure, and then a client-side script initializing and running the Mermaid library to render these diagrams.

**Rationale**: This approach leverages Docusaurus's native markdown processing capabilities and the Mermaid library's client-side rendering, providing a robust and maintainable solution for embedding diagrams.

**Alternatives Considered**:
-   Pre-rendering Mermaid diagrams to images: Rejected as it loses the benefits of editable text-based diagrams and makes updates cumbersome.
-   Using a custom Docusaurus plugin that handles server-side rendering: Considered but client-side rendering is simpler and generally sufficient for static site generators.

**Implementation Details**:
-   Use markdown code blocks with the `mermaid` language identifier:
    ````markdown
    ```mermaid
    graph TD
        A[Node A] --> B(Node B)
    ```
    ````
-   Docusaurus (potentially with a remark plugin) will transform this into a `<div class="mermaid">...</div>` structure.
-   A client-side script will load the Mermaid library, initialize it with any desired configuration (e.g., theme), and then call `mermaid.run()` to render the diagrams within these `div` elements.
-   Configuration options for Mermaid (e.g., theme, flowchart definitions) can be passed via `mermaid.initialize()`.

### T012: Troubleshooting documentation strategies

**Decision**: Effective troubleshooting documentation will be user-centric, structured, actionable, and include diagnostic information.

**Rationale**: A well-structured troubleshooting guide improves the learning experience for students by empowering them to solve common problems independently, reduces frustration, and reinforces their understanding of the underlying systems.

**Best Practices for Troubleshooting Documentation**:
-   **User-Centric Approach**:
    -   Tailor language and detail to the beginner-intermediate student audience.
    -   Describe problems using terms students would recognize (symptoms-first).
-   **Clear Structure and Navigation**:
    -   Categorize issues (e.g., "Installation Issues," "Simulation Errors").
    -   Use clear headings and subheadings.
    -   Ensure searchable format and clear table of contents.
-   **Actionable and Concise Solutions**:
    -   Provide clear, numbered step-by-step instructions.
    -   Include exact command examples, code snippets, or configuration examples.
    -   Describe expected outcomes after each step.
    -   Reference specific error messages.
    -   Explain *why* a step is necessary.
    -   Cross-reference other documentation for deeper understanding.
-   **Diagnostic Information**:
    -   Instruct students on how to collect relevant logs, configuration files, or version numbers.
    -   Highlight common pitfalls.
-   **Maintainability and Accessibility**:
    -   Regularly update the troubleshooting guide.
    -   Provide a feedback mechanism.
    -   Clearly indicate applicable product versions.
    -   Ensure accessibility best practices.
-   **"What to do next"**:
    -   Clearly state escalation paths if troubleshooting steps fail.
    -   Suggest further reading.

### T013: Citation management and integration within Docusaurus

**Decision**: Citation management will utilize a combination of manual Markdown for in-text numeric references and a custom React component for rendering the "References" section at the end of each chapter. This approach aligns with the specified numeric-style citation format and provides flexibility for detailed reference entries.

**Rationale**: While Docusaurus doesn't have native academic citation features, this hybrid approach allows for consistent in-text referencing and a structured, formatted bibliography per chapter, which is crucial for a technical textbook requiring academic rigor. Custom React components provide the necessary control over rendering complex data structures like bibliographies.

**Alternatives Considered**:
-   Purely manual formatting of references within Markdown: Rejected as it would be prone to errors, difficult to maintain, and would not easily support future automation or styling changes.
-   Developing a full Docusaurus plugin for BibTeX integration: Considered but deemed overly complex for the initial implementation and potentially unnecessary if the custom React component approach can handle the required formatting.

**Implementation Details**:
-   **In-text Citations**: Authors will manually insert numeric references in square brackets (e.g., `[1]`, `[2, 3]`) within the Markdown text.
-   **References Section**:
    -   Each chapter's MDX file will include a dedicated `## References` section at the end.
    -   A custom React component (e.g., `<ReferencesList sources={...} />` in `humanoid-robotics-textbook/src/components/ReferencesList/`) will be created.
    -   This component will accept a data structure (e.g., an array of JSON objects or a JavaScript array of strings) representing the references for that chapter.
    -   The component will render these references as an ordered list, formatted according to the standard defined in `citation-format.md` (e.g., for peer-reviewed papers, official documentation, books).
    -   The `id` attribute of each reference list item in the rendered HTML can be linked to from in-text citations.
