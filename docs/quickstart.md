---
slug: /
---
# Quickstart Guide: Physical AI & Humanoid Robotics Textbook Development

This guide provides instructions for setting up your development environment and getting started with contributing to the Physical AI & Humanoid Robotics Textbook.

## 1. Prerequisites

Before you begin, ensure you have the following installed:

-   **Operating System**: Ubuntu 22.04 LTS (Recommended for ROS 2 Jazzy compatibility)
-   **Git**: Version control system.
    -   `sudo apt update && sudo apt install git -y`
-   **Node.js & npm**: For Docusaurus.
    -   Follow official Node.js installation instructions (e.g., using `nvm` or `apt` for the latest LTS version).
-   **Python 3.10+ & pip**: For ROS 2 and AI/ML code examples.
    -   `sudo apt update && sudo apt install python3 python3-pip -y`
-   **ROS 2 Jazzy Jalisco**: The Robot Operating System 2 (LTS release).
    -   Follow the official ROS 2 Jazzy installation guide for Ubuntu. Ensure the `ros-dev-tools` are installed.
-   **Gazebo Harmonic**: The simulation environment (comes with ROS 2 Jazzy).
    -   Install alongside ROS 2 Jazzy, or separately if needed, ensuring compatibility.
-   **NVIDIA Isaac Sim**: A compatible version with ROS 2 Jazzy and Gazebo Harmonic.
    -   Follow NVIDIA's official installation guide for Isaac Sim, ensuring ROS 2 bridge and Gazebo integration.
-   **Code Editor**: VS Code with recommended extensions (e.g., Markdown All in One, Python, YAML).

## 2. Clone the Repository

Clone the textbook repository from GitHub:

```bash
git clone https://github.com/your-username/ai-and-robotics.git
cd ai-and-robotics
```

## 3. Setup Docusaurus Development Environment

Navigate to the `humanoid-robotics-textbook` directory and install dependencies:

```bash
cd humanoid-robotics-textbook
npm install
```

## 4. Build and Run Docusaurus Locally

To start the local development server:

```bash
npm run start
```

This will open the textbook in your browser at `http://localhost:3000`. Any changes you make to the `.mdx` files or other Docusaurus configuration will automatically reload the page.

## 5. Running Example Simulations

To test ROS 2 nodes or Gazebo/Isaac Sim simulations mentioned in the chapters, refer to the specific instructions within each chapter.

### Example ROS 2 Command

```bash
source /opt/ros/jazzy/setup.bash
ros2 launch my_robot_bringup my_robot_launch.py
```

### Example Gazebo Command

```bash
gazebo --verbose worlds/my_robot_world.sdf
```

## 6. Contributing

-   Follow the file naming conventions and MDX frontmatter standard.
-   Ensure all technical claims are backed by citations.
-   Tag glossary terms using the glossary term tagging convention.
-   Adhere to the project's constitution and specification.