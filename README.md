# Physical AI & Humanoid Robotics Textbook

A comprehensive technical textbook on Physical AI & Humanoid Robotics, built with Docusaurus. This textbook targets beginner-intermediate CS/AI/Robotics students, covering the full humanoid robotics stack, including ROS 2, Gazebo, NVIDIA Isaac, and LLM integration.

## Table of Contents

- [Introduction](#introduction)
- [Modules Overview](#modules-overview)
- [Hardware Requirements](#hardware-requirements)
- [Deployment](#deployment)
- [Repository Structure](#repository-structure)
- [Contribution](#contribution)
- [License](#license)

## Introduction

This textbook aims to provide a foundational understanding and practical skills in the rapidly evolving field of Physical AI and Humanoid Robotics. Through a blend of theoretical concepts, hands-on exercises, and real-world examples, learners will gain proficiency in key technologies and methodologies essential for designing, programming, and deploying humanoid robots.

## Modules Overview

The textbook is structured into several modules, each focusing on a critical aspect of humanoid robotics:

-   **Module 1: Robotic Nervous System (ROS 2)**: Fundamentals of ROS 2 for robotic software development.
-   **Module 2: Digital Twin (Gazebo & Unity)**: Simulation of humanoid robots in virtual environments.
-   **Module 3: AI-Robot Brain (NVIDIA Isaac)**: Implementing AI algorithms using NVIDIA Isaac SDK for simulated robots.
-   **Module 4: Vision-Language-Action (VLA)**: Integrating LLMs with simulated robots for voice-controlled autonomous systems.

## Hardware Requirements

To effectively follow along with the exercises and simulations, the following hardware is recommended:

-   **Operating System**: Ubuntu 22.04 LTS (for ROS 2 Jazzy compatibility)
-   **Processor**: Intel i5/i7 (or equivalent AMD)
-   **RAM**: 16GB or more
-   **GPU**: NVIDIA GPU with 8GB VRAM or more (e.g., RTX series) for NVIDIA Isaac Sim.

## Deployment

The textbook is deployed as a static website to GitHub Pages.

**Live Version**: [https://Tayyaba10.github.io/humanoid_robotics_textbook/](https://Tayyaba10.github.io/humanoid_robotics_textbook/)

## Repository Structure

```
.
├── .github/workflows/         # GitHub Actions workflows
│   └── deploy.yml             # Docusaurus deployment to GitHub Pages
├── humanoid-robotics-textbook/  # Docusaurus project root
│   ├── docs/                  # All textbook content (modules/chapters in MDX)
│   ├── src/                   # Custom Docusaurus components and styling
│   ├── static/                # Static assets (images, models)
│   ├── docusaurus.config.ts   # Docusaurus configuration
│   └── sidebars.ts            # Docusaurus sidebar configuration
├── specs/                     # Project specifications, plans, and contracts
│   └── 1-humanoid-robotics-textbook/
│       ├── plan.md            # Overall implementation plan
│       ├── tasks.md           # Detailed task breakdown
│       └── contracts/         # Content and formatting guidelines
└── README.md                  # This file
```

## Contribution

We welcome contributions! Please refer to the `specs/1-humanoid-robotics-textbook/tasks.md` for the task breakdown and follow the guidelines outlined in the `specs/1-humanoid-robotics-textbook/contracts/` directory for content creation and formatting.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
