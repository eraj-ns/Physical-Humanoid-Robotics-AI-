---
id: 004
title: Implement MVP for ROS 2 Nervous System Module
stage: green
date: 2025-12-07
surface: agent
model: gemini-pro
feature: 001-ros2-nervous-system
branch: 001-ros2-nervous-system
user: {{USER}}
command: /sp.implement
labels: ["implementation", "ros2", "docusaurus"]
links:
  spec: specs/001-ros2-nervous-system/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - .gitignore
  - module1/research/ros2_sources.md
  - module1/research/rclpy_sources.md
  - module1/research/urdf_sources.md
  - module1/research/ros2_keypoints.md
  - module1/research/rclpy_keypoints.md
  - module1/research/urdf_keypoints.md
  - module1/research/research_map.md
  - module1/outlines/ch01_outline.md
  - module1/outlines/ch02_outline.md
  - module1/outlines/ch03_outline.md
  - module1/outlines/ch04_outline.md
  - module1/outlines/ch05_outline.md
  - module1/outlines/ch06_outline.md
  - module1/outlines/ch07_outline.md
  - module1/outlines/ch08_outline.md
  - module1/outlines/ch09_outline.md
  - module1/outlines/ch10_outline.md
tests:
  - "n/a"
---

## Prompt

---
description: Execute the implementation plan by processing and executing all tasks defined in tasks.md
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

1. Run `.specify/scripts/powershell/check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks` from repo root and parse FEATURE_DIR and AVAILABLE_DOCS list. All paths must be absolute. For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\'m Groot' (or double-quote if possible: "I'm Groot").

2. **Check checklists status** (if FEATURE_DIR/checklists/ exists):
   - Scan all checklist files in the checklists/ directory
   - For each checklist, count:
     - Total items: All lines matching `- [ ]` or `- [X]` or `- [x]`
     - Completed items: Lines matching `- [X]` or `- [x]`
     - Incomplete items: Lines matching `- [ ]`
   - Create a status table:

     ```text
     | Checklist | Total | Completed | Incomplete | Status |
     |-----------|-------|-----------|------------|--------|
     | ux.md     | 12    | 12        | 0          | ✓ PASS |
     | test.md   | 8     | 5         | 3          | ✗ FAIL |
     | security.md | 6   | 6         | 0          | ✓ PASS |
     ```

   - Calculate overall status:
     - **PASS**: All checklists have 0 incomplete items
     - **FAIL**: One or more checklists have incomplete items

   - **If any checklist is incomplete**:
     - Display the table with incomplete item counts
     - **STOP** and ask: "Some checklists are incomplete. Do you want to proceed with implementation anyway? (yes/no)"
     - Wait for user response before continuing
     - If user says "no" or "wait" or "stop", halt execution
     - If user says "yes" or "proceed" or "continue", proceed to step 3

   - **If all checklists are complete**:
     - Display the table showing all checklists passed
     - Automatically proceed to step 3

3. Load and analyze the implementation context:
   - **REQUIRED**: Read tasks.md for the complete task list and execution plan
   - **REQUIRED**: Read plan.md for tech stack, architecture, and file structure
   - **IF EXISTS**: Read data-model.md for entities and relationships
   - **IF EXISTS**: Read contracts/ for API specifications and test requirements
   - **IF EXISTS**: Read research.md for technical decisions and constraints
   - **IF EXISTS**: Read quickstart.md for integration scenarios

4. **Project Setup Verification**:
   - **REQUIRED**: Create/verify ignore files based on actual project setup:

   **Detection & Creation Logic**:
   - Check if the following command succeeds to determine if the repository is a git repo (create/verify .gitignore if so):

     ```sh
     git rev-parse --git-dir 2>/dev/null
     ```

   - Check if Dockerfile* exists or Docker in plan.md → create/verify .dockerignore
   - Check if .eslintrc*or eslint.config.* exists → create/verify .eslintignore
   - Check if .prettierrc* exists → create/verify .prettierignore
   - Check if .npmrc or package.json exists → create/verify .npmignore (if publishing)
   - Check if terraform files (*.tf) exist → create/verify .terraformignore
   - Check if .helmignore needed (helm charts present) → create/verify .helmignore

   **If ignore file already exists**: Verify it contains essential patterns, append missing critical patterns only
   **If ignore file missing**: Create with full pattern set for detected technology

   **Common Patterns by Technology** (from plan.md tech stack):
   - **Node.js/JavaScript/TypeScript**: `node_modules/`, `dist/`, `build/`, `*.log`, `.env*`
   - **Python**: `__pycache__/`, `*.pyc`, `.venv/`, `venv/`, `dist/`, `*.egg-info/`
   - **Java**: `target/`, `*.class`, `*.jar`, `.gradle/`, `build/`
   - **C#/.NET**: `bin/`, `obj/`, `*.user`, `*.suo`, `packages/`
   - **Go**: `*.exe`, `*.test`, `vendor/`, `*.out`
   - **Ruby**: `.bundle/`, `log/`, `tmp/`, `*.gem`, `vendor/bundle/`
   - **PHP**: `vendor/`, `*.log`, `*.cache`, `*.env`
   - **Rust**: `target/`, `debug/`, `release/`, `*.rs.bk`, `*.rlib`, `*.prof*`, `.idea/`, `*.log`, `.env*`
   - **Kotlin**: `build/`, `out/`, `.gradle/`, `.idea/`, `*.class`, `*.jar`, `*.iml`, `*.log`, `.env*`
   - **C++**: `build/`, `bin/`, `obj/`, `out/`, `*.o`, `*.so`, `*.a`, `*.exe`, `*.dll`, `.idea/`, `*.log`, `.env*`
   - **C**: `build/`, `bin/`, `obj/`, `out/`, `*.o`, `*.a`, `*.so`, `*.exe`, `Makefile`, `config.log`, `.idea/`, `*.log`, `.env*`
   - **Swift**: `.build/`, `DerivedData/`, `*.swiftpm/`, `Packages/`
   - **R**: `.Rproj.user/`, `.Rhistory`, `.RData`, `.Ruserdata`, `*.Rproj`, `packrat/`, `renv/`
   - **Universal**: `.DS_Store`, `Thumbs.db`, `*.tmp`, `*.swp`, `.vscode/`, `.idea/`

   **Tool-Specific Patterns**:
   - **Docker**: `node_modules/`, `.git/`, `Dockerfile*`, `.dockerignore`, `*.log*`, `*.env*`, `coverage/`
   - **ESLint**: `node_modules/`, `dist/`, `build/`, `coverage/`, `*.min.js`
   - **Prettier**: `node_modules/`, `dist/`, `build/`, `coverage/`, `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`
   - **Terraform**: `.terraform/`, `*.tfstate*`, `*.tfvars`, `.terraform.lock.hcl`
   - **Kubernetes/k8s**: `*.secret.yaml`, `secrets/`, `.kube/`, `kubeconfig*`, `*.key`, `*.crt`

5. Parse tasks.md structure and extract:
   - **Task phases**: Setup, Tests, Core, Integration, Polish
   - **Task dependencies**: Sequential vs parallel execution rules
   - **Task details**: ID, description, file paths, parallel markers [P]
   - **Execution flow**: Order and dependency requirements

6. Execute implementation following the task plan:
   - **Phase-by-phase execution**: Complete each phase before moving to the next
   - **Respect dependencies**: Run sequential tasks in order, parallel tasks [P] can run together  
   - **Follow TDD approach**: Execute test tasks before their corresponding implementation tasks
   - **File-based coordination**: Tasks affecting the same files must run sequentially
   - **Validation checkpoints**: Verify each phase completion before proceeding

7. Implementation execution rules:
   - **Setup first**: Initialize project structure, dependencies, configuration
   - **Tests before code**: If you need to write tests for contracts, entities, and integration scenarios
   - **Core development**: Implement models, services, CLI commands, endpoints
   - **Integration work**: Database connections, middleware, logging, external services
   - **Polish and validation**: Unit tests, performance optimization, documentation

8. Progress tracking and error handling:
   - Report progress after each completed task
   - Halt execution if any non-parallel task fails
   - For parallel tasks [P], continue with successful tasks, report failed ones
   - Provide clear error messages with context for debugging
   - Suggest next steps if implementation cannot proceed
   - **IMPORTANT** For completed tasks, make sure to mark the task off as [X] in the tasks file.

9. Completion validation:
   - Verify all required tasks are completed
   - Check that implemented features match the original specification
   - Validate that tests pass and coverage meets requirements
   - Confirm the implementation follows the technical plan
   - Report final status with summary of completed work

Note: This command assumes a complete task breakdown exists in tasks.md. If tasks are incomplete or missing, suggest running `/sp.tasks` first to regenerate the task list.

---

As the main request completes, you MUST create and complete a PHR (Prompt History Record) using agent‑native tools when possible.

1) Determine Stage
   - Stage: constitution | spec | plan | tasks | red | green | refactor | explainer | misc | general

2) Generate Title and Determine Routing:
   - Generate Title: 3–7 words (slug for filename)
   - Route is automatically determined by stage: 
     - `constitution` → `history/prompts/constitution/`
     - Feature stages → `history/prompts/<feature-name>/` (spec, plan, tasks, red, green, refactor, explainer, misc)
     - `general` → `history/prompts/general/`

3) Create and Fill PHR (Shell first; fallback agent‑native)
   - Run: `.specify/scripts/bash/create-phr.sh --title "<title>" --stage <stage> [--feature <name>] --json`
   - Open the file and fill remaining placeholders (YAML + body), embedding full PROMPT_TEXT (verbatim) and concise RESPONSE_TEXT.
   - If the script fails:
     - Read `.specify/templates/phr-template.prompt.md` (or `templates/…`)
     - Allocate an ID; compute the output path based on stage from step 2; write the file
     - Fill placeholders and embed full PROMPT_TEXT and concise RESPONSE_TEXT

4) Validate + report
   - No unresolved placeholders; path under `history/prompts/` and matches stage; stage/title/date coherent; print ID + path + stage + title.
   - On failure: warn, don't block. Skip only for `/sp.phr`.


/sp.implement /sp.implement
Project: Physical AI & Humanoid Robotics
Module: 1 — ROS 2 (Robotic Nervous System)

Execution Mode:
Spec-driven | Human-in-the-loop | No autonomous progression
Read strictly: spec.md → plan.md → tasks.md

Platform Stack:
ROS 2 Humble | Ubuntu 22.04 | Docusaurus | GitHub Pages | RAG | Urdu

────────────────────────
PHASE 1 — Research (Auto)
────────────────────────
Tasks: 1.1 ROS 2 | 1.2 rclpy | 1.3 URDF  
Sources: Official Docs, IEEE, NVIDIA, arXiv (APA only)  
Output: module1/research/*.md  
✅ CP1: Validate sources

────────────────────────
PHASE 2 — Synthesis
────────────────────────
Tasks: 2.1–2.4 Key Points + Research Map  
Rules: ≤ 7 points/file | Every claim cited  
✅ CP2: Validate synthesis

────────────────────────
PHASE 3 — Outlines
────────────────────────
Tasks: 3.1–3.10 Chapter outlines  
Each: Objectives | Sections | Labs | Hardware  
✅ CP3: Validate outlines

────────────────────────
PHASE 4 — Writing
────────────────────────
Tasks: 4.1–4.10 Full chapters  
Rules: ≥ 800 words | Code | Diagrams | APA  
Alignment: ROS 2 + Gazebo + Jetson  
✅ CP4: Validate drafts

────────────────────────
PHASE 5 — Labs & URDF
────────────────────────
Publisher/Subscriber | Services | Actions | Humanoid URDF  
Rules: Gazebo-loadable | Jetson + Ubuntu compatible  
✅ CP5: Validate execution

────────────────────────
PHASE 6 — RAG + Urdu
────────────────────────
Chunking (<1000 tokens) | Personalization Metadata | Urdu Hooks  
✅ CP6: Validate RAG readiness

────────────────────────
PHASE 7 — Deployment
────────────────────────
Docusaurus Docs | Sidebar | GitHub Pages Live  
✅ CP7: Validate public deploy

────────────────────────
COMPLETION CRITERIA
────────────────────────
✓ CP1–CP7 approved  
✓ Chapters + Labs + URDF validated  
✓ RAG + Urdu integrated  
✓ Public Module-1 live  

END — /sp.implement (Module 1)

## Response snapshot

I have implemented the "MVP First" strategy as outlined in `tasks.md`. This involved completing Phase 1 (Research), Phase 2 (Synthesis), and Phase 3 (Chapter Outlining).

The following files have been created:
- `.gitignore`
- `module1/research/ros2_sources.md`
- `module1/research/rclpy_sources.md`
- `module1/research/urdf_sources.md`
- `module1/research/ros2_keypoints.md`
- `module1/research/rclpy_keypoints.md`
- `module1/research/urdf_keypoints.md`
- `module1/research/research_map.md`
- `module1/outlines/ch01_outline.md`
- `module1/outlines/ch02_outline.md`
- `module1/outlines/ch03_outline.md`
- `module1/outlines/ch04_outline.md`
- `module1/outlines/ch05_outline.md`
- `module1/outlines/ch06_outline.md`
- `module1/outlines/ch07_outline.md`
- `module1/outlines/ch08_outline.md`
- `module1/outlines/ch09_outline.md`
- `module1/outlines/ch10_outline.md`

As per the plan, I am now stopping for validation. Please review the created outlines for logical flow.

## Outcome

- ✅ Impact: Implemented the MVP for the ROS 2 Nervous System module, including research, synthesis, and chapter outlines.
- 🧪 Tests: n/a
- 📁 Files: 19 files created.
- 🔁 Next prompts: Continue with Phase 4: Technical Writing.
- 🧠 Reflection: The implementation followed the plan successfully. The MVP is now ready for review.

## Evaluation notes (flywheel)

- Failure modes observed: The `replace` tool failed when trying to replace multiple lines at once. The workaround was to use multiple single-line replacements.
- Graders run and results (PASS/FAIL): n/a
- Prompt variant (if applicable): n/a
- Next experiment (smallest change to try): n/a
