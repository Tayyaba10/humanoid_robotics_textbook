# Citation Format Standard for Physical AI & Humanoid Robotics Textbook

This document defines the mandatory standard for formatting citations and references within the Physical AI & Humanoid Robotics Textbook. Adherence to this standard ensures academic rigor, proper attribution, and consistency across all chapters.

## General Principles

-   All technical claims MUST be supported by a citation to an official source (documentation) or peer-reviewed robotics/AI papers.
-   A minimum of 40% of all sources MUST be peer-reviewed robotics/AI papers.
-   Citations should be placed at the end of the sentence or paragraph where the information is presented.
-   A dedicated "References" section MUST be included at the end of each chapter.

## In-text Citations

In-text citations will use a numeric-style reference in square brackets, linking to a numbered list in the "References" section of the chapter.

### Examples

-   "Robot Operating System (ROS) 2 provides a flexible framework for robotic software development [1]."
-   "Deep reinforcement learning has shown promising results in complex manipulation tasks [2, 3]."

## References Section

Each chapter MUST include a "References" section at the end, formatted as an ordered list. The format for each entry will follow a simplified version of a common academic style (e.g., IEEE or APA, adapted for Markdown).

### Formatting Guidelines for Reference Entries

-   **Peer-reviewed Papers**:
    `[#] Author(s), "Title of Paper," *Journal/Conference Name*, Volume, Issue, Pages, Year.`
    -   Example: `[1] J. Smith and A. B. Johnson, "Deep Learning for Humanoid Control," *IEEE Transactions on Robotics*, vol. 35, no. 2, pp. 450-462, 2019.`
-   **Official Documentation**:
    `[#] Author/Organization, "Title of Document," Version (if applicable), [Online]. Available: URL.`
    -   Example: `[2] Open Robotics, "ROS 2 Documentation: Foxy Fitzroy," [Online]. Available: https://docs.ros.org/en/foxy/index.html.`
-   **Books**:
    `[#] Author(s), *Title of Book*, Edition (if applicable). Publisher, Year.`
    -   Example: `[3] S. Thrun, W. Burgard, and D. Fox, *Probabilistic Robotics*. MIT Press, 2005.`

### Example References Section

```markdown
## References

[1] J. Smith and A. B. Johnson, "Deep Learning for Humanoid Control," *IEEE Transactions on Robotics*, vol. 35, no. 2, pp. 450-462, 2019.
[2] Open Robotics, "ROS 2 Documentation: Foxy Fitzroy," [Online]. Available: https://docs.ros.org/en/foxy/index.html.
[3] S. Thrun, W. Burgard, and D. Fox, *Probabilistic Robotics*. MIT Press, 2005.
```
**Note**: For online resources, the "Available: URL" format is preferred to ensure the link is clearly identifiable.
