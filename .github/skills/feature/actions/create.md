# Create Action

Use this action when the user provides either:

- an epic or phase specification, or
- a build plan with a specific phase selected, and asks for individual implementation feature files.

The skill supports two modes:

1. Epic/spec mode: break a spec into feature sections.
2. Build-plan phase mode: break the selected phase into work items, where each work item becomes a feature file.

## 1. Validate the argument

- Read the text after `create` as a file path.
- If no path is provided, stop with:
  `"create" requires a filename and, for build plans, a phase selector such as "phase 1" (e.g., /feature create <build-plan.md> phase 1)`.
- Resolve relative paths from the repository root.
- Confirm the file exists and is Markdown before parsing it.
- Read the complete file. Do not infer features from only the first section.

## 2. Determine the mode

- If the user provides a phase selector such as `phase 1`, `Phase 1`, or `phase-1`, treat the input as a build-plan phase decomposition.
- Otherwise treat the document as a spec/epic document and apply the feature-section logic in Section 4.

## 3. Build-plan phase mode

### 3.1 Parse the selected phase

- Find a heading matching the requested phase, such as:
  - `## Phase 1: Local Runtime Foundation`
  - `### Phase 1: Local Runtime Foundation`
  - `Phase 1`
- Normalize the phase label for naming by lowercasing it and replacing spaces and punctuation with hyphens.
- Within the selected phase section, look for a subsection named `### Work items` or a numbered list of work items.
- If no work items are found, stop and report that no work items were found for that phase.

### 3.2 Identify each work item as a feature

Each work item must be converted into a feature file in this order:

- `1. Create the application directories`
- `2. Initialize the frontend`
- `3. Initialize the backend`
- etc.

For each work item:

- Extract the work item number and title.
- Use the title as the feature name.
- Build a short filename from the phase and work item number, for example:
  - `phase1-feature1-repo-structure.md`
  - `phase1-feature2-initialize-frontend.md`
- Use the same naming pattern for all files:
  `context/features/<phase>-feature<item-number>-<short-description>.md`
- Keep the short description lowercase kebab-case and specific to the work item title.

### 3.3 Repository path rules for build-plan features

- Create each file under `context/features/`.
- If the exact file already exists, skip it and report that it was already present.
- Never overwrite an existing feature file.

### 3.4 Build-plan feature file template

Each generated build-plan feature file must contain this structure:

```markdown
# Feature: <Feature Name>

- **Phase:** <original phase label>
- **Feature ID:** <phase label>-feature<work-item-number>
- **Status:** Not Started
- **Source plan:** <repository-relative plan path>

## Goal

<One plain-language paragraph describing the outcome of this specific work item.>

## Non-Goals

- <What this feature explicitly does not include>
- <Related work reserved for later phases or sibling features>

## Why This Matters

<Short explanation of why this work item exists and how it enables the MVP outcome.>

## Prerequisites

- <Dependencies and setup required before starting this work item>

## Technical Solution

<Describe the implementation pattern, architecture, files, modules, and boundaries for this feature.>

## Implementation Steps
### Below is the sample steps to be used in implementation, and not rigid steps

### Step 1: <small outcome>

- **What to do:** <specific action>
- **Where:** `<expected path/module>`
- **How:** <concrete implementation instruction>
- **Done when:** <observable result>

### Step 2: <small outcome>

...

## Interface and Data Contracts

- <Routes, schemas, models, config values, or module boundaries>

## Verification

1. <Exact command or manual check>
2. <Focused behavior check>
3. <Expected result>

## Acceptance Criteria

- [ ] <Feature-specific acceptance criterion>

## Out of Scope

- <Work explicitly excluded from this feature>

## Notes

<Technical context, risks, dependencies, or implementation decisions.>
```

Generation rules for build-plan features:

- Convert the work item into a concrete feature that is independently implementable.
- Include explicit `Goal`, `Non-Goals`, and `Technical Solution` sections.
- Turn each subtask or implementation note from the work item into ordered steps.
- Preserve privacy, safety, approval, and provider-scoping constraints from the build plan and PRD.
- Keep the feature focused on the work item, not the whole phase.
- If the work item is a setup step, keep the technical solution around repo structure, local runtime, environment setup, and configuration boundaries.
- If the work item is a domain or workflow task, keep the technical solution around models, repositories, services, and APIs.

## 4. Epic/spec mode

Use this mode when no `phase` selector is given.

### 4.1 Identify every feature

Process all feature sections in document order. A feature section is a
heading that matches one of these forms, case-insensitively:

- `Feature #1: Name`
- `Feature 1: Name`
- `Feature FEAT-01: Name`
- `## Feature 1 - Name`

The heading starts a feature and the feature continues until the next feature
heading of the same or higher level, or until the end of the document.

For each feature:

- Extract the feature number exactly as written, then normalize it for the
  filename: `1` becomes `01`, `FEAT-01` remains `FEAT-01`.
- Use the heading text as the feature name.
- Extract the feature's `Scope`, `Tasks`, requirements, acceptance criteria,
  and feature-specific dependencies from its section.
- If the document has no matching feature headings, stop and report that no
  features were found. Do not create one generic feature file.
- Do not treat the epic's general goals, non-goals, or dependencies as separate
  features.

### 4.2 Derive the filename

Create exactly one file per feature using:

```text
context/features/<EPIC_ID>-<FEATURE_ID>-<short-description>.md
```

Rules for `<short-description>`:

- Derive it from the feature heading, not from arbitrary task text.
- Convert to lowercase kebab-case.
- Remove punctuation and filler words where possible.
- Keep it short and specific, normally two to five words.
- Example: `Feature #1: Repository and local runtime setup` becomes
  `context/features/EPIC01-01-repository-local-runtime-setup.md`.
- Before creating a file, check whether the exact path already exists. Never
  overwrite an existing feature file; report it as skipped and explain why.

### 4.3 Generate a junior-friendly feature file

Each generated file must contain this structure:

```markdown
# Feature: <Feature Name>

- **EPIC:** <original epic ID>
- **Feature ID:** <feature ID>
- **Status:** Not Started
- **Source spec:** <repository-relative spec path>

## Goal

<One plain-language paragraph describing the outcome.>

## Why This Matters

<Short explanation of how this feature supports the epic and later work.>

## Prerequisites

- <Dependencies and setup required before starting>

## Implementation Steps

### Step 1: <small outcome>

- **What to do:** <specific action>
- **Where:** `<expected path/module>`
- **How:** <concrete implementation instruction>
- **Done when:** <observable result>

### Step 2: <small outcome>

...

## Interface and Data Contracts

- <Routes, schemas, models, environment variables, or module boundaries>

## Verification

1. <Exact command or manual check>
2. <Focused behavior check>
3. <Expected result>

## Acceptance Criteria

- [ ] <Feature-specific acceptance criterion>

## Out of Scope

- <Related work that must not be implemented in this feature>

## Notes

<Technical context, risks, or implementation decisions.>
```

Generation rules:

- Turn each source task into one or more ordered implementation steps. Do not
  merely copy the task list into `Notes`.
- Order steps from setup, to implementation, to integration, to tests.
- Each step must identify where the work belongs, what the junior engineer
  should do, and an observable definition of done.
- Use plain language and explain unfamiliar terms on first use.
- Include concrete paths and names only when supported by the source spec or
  repository conventions. Otherwise mark the path as a proposed location.
- Convert feature-specific acceptance criteria into checkboxes.
- Add verification commands only when they are known from the repository; if
  not known, provide a manual verification procedure and mark the command as
  `TBD` rather than inventing one.
- Preserve security, approval, privacy, and non-goal constraints from the
  source spec in the generated file.
- Keep each feature independently implementable, but list dependencies on
  sibling features explicitly.

## 5. Confirm the result

After processing the complete input, report:

- The mode used: `build-plan phase` or `epic/spec`.
- The phase identifier used (if applicable).
- Every created file with its repository-relative path.
- Any existing files skipped without modification.
- Any ambiguity, missing feature sections, or assumptions.
- A short count such as `Created 6 feature files; skipped 0`.

## 6. Examples

### Example A: build-plan phase mode

Input:

```text
/feature create docs/mvp-build-plan.md phase 1
```

Behavior:

- Read `Phase 1: Local Runtime Foundation`.
- Extract each work item.
- Create files such as:
  - `context/features/phase1-feature1-repo-structure.md`
  - `context/features/phase1-feature2-initialize-frontend.md`
  - `context/features/phase1-feature3-initialize-backend.md`

Each feature file includes:

- Goal
- Non-Goals
- Why This Matters
- Technical Solution
- Implementation Steps
- Verification
- Acceptance Criteria

### Example B: epic/spec mode

Input:

```text
/feature create context/features/phase1-spec.md
```

Behavior:

- Read the feature sections in order.
- Create one file per feature using the `EPIC01-xx-name.md` naming convention.
