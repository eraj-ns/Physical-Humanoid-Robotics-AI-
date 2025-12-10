---
id: 003
title: Generate Tasks for ROS2 Nervous System Module
stage: tasks
date: 2025-12-06
surface: agent
model: gemini-pro
feature: 001-ros2-nervous-system
branch: main
user: {{USER}}
command: /sp.tasks
labels: ["task-generation", "planning", "ros2"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - specs/001-ros2-nervous-system/tasks.md
tests:
 - None
---

## Prompt

description: Generate an actionable, dependency-ordered tasks.md for the feature based on available design artifacts.
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

1. **Setup**: Run `.specify/scripts/powershell/check-prerequisites.ps1 -Json` from repo root and parse FEATURE_DIR and AVAILABLE_DOCS list. All paths must be absolute. For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot").

2. **Load design documents**: Read from FEATURE_DIR:
   - **Required**: plan.md (tech stack, libraries, structure), spec.md (user stories with priorities)
   - **Optional**: data-model.md (entities), contracts/ (API endpoints), research.md (decisions), quickstart.md (test scenarios)
   - Note: Not all projects have all documents. Generate tasks based on what's available.

3. **Execute task generation workflow**:
   - Load plan.md and extract tech stack, libraries, project structure
   - Load spec.md and extract user stories with their priorities (P1, P2, P3, etc.)
   - If data-model.md exists: Extract entities and map to user stories
   - If contracts/ exists: Map endpoints to user stories
   - If research.md exists: Extract decisions for setup tasks
   - Generate tasks organized by user story (see Task Generation Rules below)
   - Generate dependency graph showing user story completion order
   - Create parallel execution examples per user story
   - Validate task completeness (each user story has all needed tasks, independently testable)

4. **Generate tasks.md**: Use `.specify.specify/templates/tasks-template.md` as structure, fill with:
   - Correct feature name from plan.md
   - Phase 1: Setup tasks (project initialization)
   - Phase 2: Foundational tasks (blocking prerequisites for all user stories)
   - Phase 3+: One phase per user story (in priority order from spec.md)
   - Each phase includes: story goal, independent test criteria, tests (if requested), implementation tasks
   - Final Phase: Polish & cross-cutting concerns
   - All tasks must follow the strict checklist format (see Task Generation Rules below)
   - Clear file paths for each task
   - Dependencies section showing story completion order
   - Parallel execution examples per story
   - Implementation strategy section (MVP first, incremental delivery)

5. **Report**: Output path to generated tasks.md and summary:
   - Total task count
   - Task count per user story
   - Parallel opportunities identified
   - Independent test criteria for each story
   - Suggested MVP scope (typically just User Story 1)
   - Format validation: Confirm ALL tasks follow the checklist format (checkbox, ID, labels, file paths)

Context for task generation: /sp.tasks Project: Physical AI & Humanoid Robotics Textbook Module: Module 1 — The Robotic Nervous System (ROS 2) Purpose: Break Module 1 into atomic, checkpoint-controlled work units following the Spec-Kit Plus checkpoint pattern. Each task is:
   - 15–30 minutes
   - Has ONE acceptance criterion
   - Produces ONE verifiable output
   - Is individually reviewable
   - Has explicit dependencies 
──────────────────────────────────────────── PHASE 1 — RESEARCH FOUNDATION (Establish credible technical sources) 
──────────────────────────────────────────── Task 1.1 — Research ROS 2 Fundamentals Sources Duration: 20 min Depends on: Nothing Action: Identify 5+ authoritative or peer-reviewed sources on ROS 2 architecture, DDS, and middleware. Acceptance: "At least 5 credible ROS 2/DDS sources identified with full APA citations." Output: `module1/research/ros2_sources.md` Task 1.2 — Research rclpy & Python ROS Interface Sources Duration: 20 min Depends on: Task 1.1 Action: Identify 5+ authoritative sources for rclpy, Python ROS 2 API, and node programming. Acceptance: "5+ rclpy/Python ROS sources with full citations and credibility notes." Output: `module1/research/rclpy_sources.md` Task 1.3 — Research URDF & Robot Modeling Sources Duration: 20 min Depends on: Task 1.2 Action: Identify 5+ authoritative URDF and humanoid modeling references. Acceptance: "5+ URDF and kinematics sources documented with citations." Output: `module1/research/urdf_sources.md` ✅ **CHECKPOINT 1 — Research Source Validation** Human reviews credibility of all sources. If approved → Commit Phase 1 → Proceed. 
──────────────────────────────────────────── PHASE 2 — RESEARCH SYNTHESIS (Extract verified technical knowledge) 
──────────────────────────────────────────── Task 2.1 — Synthesize ROS 2 Architecture Key Points Duration: 20 min Depends on: Task 1.1 Action: Extract DDS, nodes, topics, services, QoS key concepts from sources. Acceptance: "5–7 ROS 2 architecture points with source attribution." Output: `module1/research/ros2_keypoints.md` Task 2.2 — Synthesize rclpy Programming Key Points Duration: 20 min Depends on: Task 1.2 Action: Extract publisher, subscriber, timers, callbacks, async execution patterns. Acceptance: "5–7 rclpy programming points with citations." Output: `module1/research/rclpy_keypoints.md` Task 2.3 — Synthesize URDF & Kinematics Key Points Duration: 20 min Depends on: Task 1.3 Action: Extract link-joint modeling, inertial tags, collision modeling concepts. Acceptance: "5–7 URDF modeling principles documented with citations." Output: `module1/research/urdf_keypoints.md` Task 2.4 — Organize All Research by Chapter Duration: 15 min Depends on: Tasks 2.1–2.3 Action: Map research points to Module 1 chapters. Acceptance: "All 10 chapters mapped with no research gaps." Output: `module1/research/research_map.md` ✅ **CHECKPOINT 2 — Research Coverage Approval** Human verifies technical coverage. If approved → Commit Phase 2 → Proceed. 
──────────────────────────────────────────── PHASE 3 — CHAPTER OUTLINING (Structure before writing) 
──────────────────────────────────────────── Task 3.1 — Create Chapter 1 Outline (Robot Nervous System) Duration: 15 min Depends on: Task 2.4 Acceptance: "Chapter 1 has 5–7 ordered learning points." Output: `module1/outlines/ch01_outline.md` Task 3.2 — Create Chapter 2 Outline (ROS 2 Architecture) Duration: 15 min Depends on: Task 3.1 Acceptance: "Chapter 2 has nodes, topics, services, QoS sections." Output: `module1/outlines/ch02_outline.md` Task 3.3 — Create Chapter 3 Outline (Installation) Duration: 15 min Depends on: Task 3.2 Acceptance: "Ubuntu + ROS 2 Humble + workspace steps defined." Output: `module1/outlines/ch03_outline.md` Task 3.4 — Create Chapter 4 Outline (rclpy Programming) Duration: 15 min Depends on: Task 3.3 Acceptance: "Publisher, subscriber, timers defined." Output: `module1/outlines/ch04_outline.md` Task 3.5 — Create Chapter 5 Outline (Topics, Services, Actions) Duration: 15 min Depends on: Task 3.4 Acceptance: "All 3 communication types covered." Output: `module1/outlines/ch05_outline.md` Task 3.6 — Create Chapter 6 Outline (AI to ROS Bridge) Duration: 15 min Depends on: Task 3.5 Acceptance: "AI agent to ROS translation pipeline defined." Output: `module1/outlines/ch06_outline.md` Task 3.7 — Create Chapter 7 Outline (URDF for Humanoids) Duration: 15 min Depends on: Task 3.6 Acceptance: "Links, joints, inertial, collision included." Output: `module1/outlines/ch07_outline.md` Task 3.8 — Create Chapter 8 Outline (Launch & Parameters) Duration: 15 min Depends on: Task 3.7 Acceptance: "Multi-node orchestration outlined." Output: `module1/outlines/ch08_outline.md` Task 3.9 — Create Chapter 9 Outline (Jetson Deployment) Duration: 15 min Depends on: Task 3.8 Acceptance: "Edge deployment & DDS networking covered." Output: `module1/outlines/ch09_outline.md` Task 3.10 — Create Chapter 10 Outline (Mini Capstone) Duration: 15 min Depends on: Task 3.9 Acceptance: "Capstone objectives & success criteria defined." Output: `module1/outlines/ch10_outline.md` ✅ **CHECKPOINT 3 — Structural Approval** Human reviews logical learning flow. If approved → Commit Phase 3 → Proceed. 
──────────────────────────────────────────── PHASE 4 — TECHNICAL WRITING (Produce textbook content) 
──────────────────────────────────────────── Task 4.1–4.10 — Write Chapters 1–10 Individually Duration: 30 min each Depends on: Corresponding outline Acceptance: "Each chapter ≥ 800 words, includes diagrams references, code blocks, and APA citations." Outputs:
   - `module1/chapters/ch01.md`
   - `module1/chapters/ch02.md`
   - ...
   - `module1/chapters/ch10.md` ✅ **CHECKPOINT 4 — Content Accuracy Review** Human verifies clarity, correctness, and hardware alignment. If approved → Commit Phase 4 → Proceed. 
──────────────────────────────────────────── PHASE 5 — LABS, CODE & URDF (Hands-on validation) 
──────────────────────────────────────────── Task 5.1 — Create ROS 2 Publisher/Subscriber Lab Duration: 25 min Acceptance: "Code runs successfully on Humble." Output: `module1/labs/pub_sub_lab/` Task 5.2 — Create ROS 2 Services Lab Duration: 25 min Acceptance: "Request/response works." Output: `module1/labs/services_lab/` Task 5.3 — Create ROS 2 Actions Lab Duration: 25 min Acceptance: "Action goal executes with feedback." Output: `module1/labs/actions_lab/` Task 5.4 — Build Humanoid URDF Model Duration: 30 min Acceptance: "URDF loads in Gazebo without errors." Output: `module1/urdf/humanoid.urdf` ✅ **CHECKPOINT 5 — Lab & URDF Execution Test** Human runs all labs. If approved → Commit Phase 5 → Proceed. 
──────────────────────────────────────────── PHASE 6 — RAG & AI-NATIVE PREPARATION 
──────────────────────────────────────────── Task 6.1 — Chunk Chapters for RAG Indexing Duration: 20 min Acceptance: "All sections <1000 tokens and logically isolated." Output: `module1/rag/chunks/` Task 6.2 — Add Metadata for Personalization Duration: 15 min Acceptance: "Beginner/intermediate/advanced tags added." Output: `module1/rag/metadata.json` Task 6.3 — Urdu Translation Hooks Duration: 15 min Acceptance: "All chapters include translation placeholders." Output: `module1/translation/hooks.json` ✅ **CHECKPOINT 6 — AI-Native Readiness Approval** 
──────────────────────────────────────────── PHASE 7 — Docusaurus & GitHub Pages 
──────────────────────────────────────────── Task 7.1 — Convert Module 1 to Docusaurus Docs Duration: 20 min Acceptance: "All chapters render correctly in Docusaurus." Output: `/docs/module1/` Task 7.2 — Navigation & Sidebar Wiring Duration: 15 min Acceptance: "Sidebar navigation complete." Output: `sidebars.js` Task 7.3 — GitHub Pages Deployment Test Duration: 20 min Acceptance: "Module visible on public GitHub Pages." Output: Live deployment URL ✅ **CHECKPOINT 7 — DEPLOYMENT APPROVAL (MODULE 1 COMPLETE)** 
──────────────────────────────────────────── END OF /sp.tasks 
────────────────────────────────────────────


The tasks.md should be immediately executable - each task must be specific enough that an LLM can complete it without additional context.

## Task Generation Rules

**CRITICAL**: Tasks MUST be organized by user story to enable independent implementation and testing.

**Tests are OPTIONAL**: Only generate test tasks if explicitly requested in the feature specification or if user requests TDD approach.

### Checklist Format (REQUIRED)

Every task MUST strictly follow this format:

```text
- [ ] [TaskID] [P?] [Story?] Description with file path
```

**Format Components**:

1. **Checkbox**: ALWAYS start with `- [ ]` (markdown checkbox)
2. **Task ID**: Sequential number (T001, T002, T003...) in execution order
3. **[P] marker**: Include ONLY if task is parallelizable (different files, no dependencies on incomplete tasks)
4. **[Story] label**: REQUIRED for user story phase tasks only
   - Format: [US1], [US2], [US3], etc. (maps to user stories from spec.md)
   - Setup phase: NO story label
   - Foundational phase: NO story label  
   - User Story phases: MUST have story label
   - Polish phase: NO story label
5. **Description**: Clear action with exact file path

**Examples**:

- ✅ CORRECT: `- [ ] T001 Create project structure per implementation plan`
- ✅ CORRECT: `- [ ] T005 [P] Implement authentication middleware in src/middleware/auth.py`
- ✅ CORRECT: `- [ ] T012 [P] [US1] Create User model in src/models/user.py`
- ✅ CORRECT: `- [ ] T014 [US1] Implement UserService in src/services/user_service.py`
- ❌ WRONG: `- [ ] Create User model` (missing ID and Story label)
- ❌ WRONG: `T001 [US1] Create model` (missing checkbox)
- ❌ WRONG: `- [ ] [US1] Create User model` (missing Task ID)
- ❌ WRONG: `- [ ] T001 [US1] Create model` (missing file path)

### Task Organization

1. **From User Stories (spec.md)** - PRIMARY ORGANIZATION:
   - Each user story (P1, P2, P3...) gets its own phase
   - Map all related components to their story:
     - Models needed for that story
     - Services needed for that story
     - Endpoints/UI needed for that story
     - If tests requested: Tests specific to that story
   - Mark story dependencies (most stories should be independent)

2. **From Contracts**:
   - Map each contract/endpoint → to the user story it serves
   - If tests requested: Each contract → contract test task [P] before implementation in that story's phase

3. **From Data Model**:
   - Map each entity to the user story(ies) that need it
   - If entity serves multiple stories: Put in earliest story or Setup phase
   - Relationships → service layer tasks in appropriate story phase

4. **From Setup/Infrastructure**:
   - Shared infrastructure → Setup phase (Phase 1)
   - Foundational/blocking tasks → Foundational phase (Phase 2)
   - Story-specific setup → within that story's phase

### Phase Structure

- **Phase 1**: Setup (project initialization)
- **Phase 2**: Foundational (blocking prerequisites - MUST complete before user stories)
- **Phase 3+**: User Stories in priority order (P1, P2, P3...)
  - Within each story: Tests (if requested) → Models → Services → Endpoints → Integration
  - Each phase should be a complete, independently testable increment
- **Final Phase**: Polish & Cross-Cutting Concerns

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
     - Read `.specify/templates/phr-template.prompt.md` (or `templates/...`)
     - Allocate an ID; compute the output path based on stage from step 2; write the file
     - Fill placeholders and embed full PROMPT_TEXT and concise RESPONSE_TEXT

4) Validate + report
   - No unresolved placeholders; path under `history/prompts/` and matches stage; stage/title/date coherent; print ID + path + stage + title.
   - On failure: warn, don't block. Skip only for `/sp.phr`.

## Response snapshot

Based on the provided context and rules, I generated a detailed `tasks.md` file for the 'Module 1 — The Robotic Nervous System (ROS 2)' feature.

The process involved:
1.  Interpreting the detailed plan from the prompt as the primary source for tasks.
2.  Mapping the prompt's phases (Research, Synthesis, Outlining, etc.) to the standard `tasks.md` structure (Setup, Foundational, User Stories, Polish).
3.  Converting each item into the strict checklist format (`- [ ] TXXX [USX] ...`), assigning sequential IDs, and including output file paths.
4.  Writing the final content to `specs/001-ros2-nervous-system/tasks.md`.

The resulting file contains 37 tasks, organized into 7 phases, with clear checkpoints and dependencies, ready for execution.

## Outcome

- ✅ Impact: Successfully generated a detailed and actionable tasks.md file according to the specified format and logic.
- 🧪 Tests: No tests were run as part of this task generation.
- 📁 Files: Created `specs/001-ros2-nervous-system/tasks.md`.
- 🔁 Next prompts: {{NEXT_PROMPTS}}
- 🧠 Reflection: {{REFLECTION_NOTE}}

## Evaluation notes (flywheel)

- Failure modes observed: {{FAILURE_MODES}}
- Graders run and results (PASS/FAIL): {{GRADER_RESULTS}}
- Prompt variant (if applicable): {{PROMPT_VARIANT_ID}}
- Next experiment (smallest change to try): {{NEXT_EXPERIMENT}}

