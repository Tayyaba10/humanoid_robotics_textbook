# Image and Asset Path Guidelines for Physical AI & Humanoid Robotics Textbook

This document specifies the mandatory guidelines for referencing image and other static asset files within the Physical AI & Humanoid Robotics Textbook. Proper path management ensures that all assets are correctly displayed across the Docusaurus site and during local development.

## Asset Storage Location

-   All static assets, including images (`.png`, `.jpg`, `.svg`, `.gif`), videos, and other media files, MUST be stored in the `static/img/` directory or its subdirectories.
-   Organize `static/img/` with subfolders if necessary for large numbers of assets (e.g., `static/img/module1/`, `static/img/diagrams/`).

## Referencing Assets in MDX Files

-   When referencing an image or any static asset within an `.mdx` chapter file, absolute paths relative to the Docusaurus base URL MUST be used.
-   The Docusaurus static directory is served at the root of the site, so references should start with `/`.

### Examples

#### Markdown Image Syntax

```markdown
![Alt text for image](/img/my-diagram.svg)
![ROS 2 Node Graph](/img/ros2/node_graph.png "Caption for ROS 2 Node Graph")
```

#### JSX Image Component (within MDX)

If using a custom React component within MDX for more advanced image handling (e.g., lazy loading, captions):

```jsx
import Image from '@theme/IdealImage'; // Example custom component

<Image img={require('/img/gazebo/simulation_environment.jpg').default} alt="Gazebo Simulation Environment" />
```

**Note**: When using `require()` within MDX for images, the path still references the `static/img/` directory implicitly via the root `/img/`.

## Why these Guidelines?

-   **Consistency**: Ensures all asset paths are handled uniformly.
-   **Portability**: Works correctly in both local development environments and after deployment to GitHub Pages.
-   **Docusaurus Best Practice**: Aligns with how Docusaurus typically handles static assets.
