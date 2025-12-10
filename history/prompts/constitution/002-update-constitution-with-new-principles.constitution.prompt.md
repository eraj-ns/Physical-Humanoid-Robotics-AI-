---
id: 002
title: Update Constitution with new principles
stage: constitution
date: 2025-12-09
surface: agent
model: gemini-pro
feature: none
branch: 008-ros2-nervous-system
user: {{USER}}
command: /sp.constitution
labels: [constitution, documentation]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
- .specify/memory/constitution.md
- .specify/templates/plan-template.md
tests:
null
---

## Prompt

/sp.constitution

Project: Physical AI & Humanoid Robotics Textbook (Hackathon)

Core Principles:
- Technical accuracy via primary sources (ROS, NVIDIA, IEEE, arXiv)
- Engineering clarity for CS & Robotics students
- Full reproducibility (all claims cited)
- Academic + industry rigor

Standards:
- Every factual claim must be source-backed
- Citation style: APA (strict)
- ≥50% peer-reviewed sources
- Zero plagiarism tolerance
- Writing level: Undergraduate–Graduate (Grade 11–14)

Content Constraints:
- Modular textbook format (per module)
- Markdown for Docusaurus
- Code + simulations must be reproducible on Ubuntu 22.04
- RAG, personalization, and Urdu readiness required

Success Criteria:
- All chapters pass fact-check
- All sources verifiable
- Zero plagiarism
- Deployment-ready for GitHub Pages

Authority:
- This constitution overrides all plans, tasks, and implementations.
END

## Response snapshot

I have updated the constitution to version 1.1.0, incorporating your more detailed and structured guidelines. This involved a minor version bump as it refines the existing principles.

I also updated the `.specify/templates/plan-template.md` to reflect the new constitution.

## Outcome

- ✅ Impact: Updated the project constitution to version 1.1.0 and ensured that the plan template is consistent with the new constitution.
- 🧪 Tests: No tests were run.
- 📁 Files: 
  - .specify/memory/constitution.md
  - .specify/templates/plan-template.md
- 🔁 Next prompts: null
- 🧠 Reflection: The `create-phr.ps1` script failed, so I had to fall back to the agent-native method of creating the PHR. This indicates a potential issue with the script or its environment that should be investigated.

## Evaluation notes (flywheel)

- Failure modes observed: The `create-phr.ps1` script failed to execute.
- Graders run and results (PASS/FAIL): null
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): null
