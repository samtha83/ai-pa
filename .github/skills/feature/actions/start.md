# Start Action

Use this action when a feature file has been created from either:

- an epic/spec feature, or
- a build-plan phase work item.

## Required behavior

1. Read the selected `<feature>.md` file.
2. Verify that the file contains the required sections for the generated feature format:
   - `## Goal`
   - `## Non-Goals`
   - `## Technical Solution`
   - `## Implementation Steps`
3. If any of these are missing or empty, stop with:
   `Run /feature create <spec-or-plan-file> [phase <n>] first`
4. Load the selected feature into `@context/current-feature.md` and update it as the active work record:
   - set the H1 heading to `# Current Feature: <Feature Name>`
   - set `## Status` to `Not Started`
   - write the feature goals as bullet points under `## Goals`
   - include relevant notes and implementation context under `## Notes`
   - preserve or append the feature history under `## History`
5. Set the feature status to `In Progress`.
6. Create and checkout a feature branch based on the feature title in the H1 heading.
   - Example: `# Feature: Initialize the frontend` -> `feature-initialize-the-frontend`
7. Summarize the feature plan in plain language:
   - goal,
   - non-goals,
   - technical solution,
   - implementation steps.
8. Implement the feature step-by-step in order.
9. After each step, validate the expected result before moving to the next.
10. When the feature is fully complete, set status to `Completed`.

## Notes for build-plan phase items

- The generated work-item feature files are intentionally small and implementable.
- They may follow names such as:
  - `phase1-feature1-repo-structure.md`
  - `phase1-feature2-initialize-frontend.md`
- Each file should be treated as one independent feature, even though it belongs to a larger phase.
- Do not treat the entire phase as one task. Work on the selected feature file only.

## Branch naming

- Derive the branch from the H1 heading, normalized to lowercase kebab-case.
- Remove punctuation and filler words where appropriate.
- Example:
  - `# Feature: Initialize the frontend` -> `feature-initialize-the-frontend`
  - `# Feature: Create the application directories` -> `feature-create-the-application-directories`

## Commands / workflow

1. Open the selected feature file.
2. Confirm required sections are populated.
3. Load the selected feature into `@context/current-feature.md`.
4. Set `## Status` to `In Progress` in the working file.
5. Create the branch.
6. Execute the implementation steps in order.
7. Verify each outcome before continuing.
8. Mark the feature complete when the acceptance criteria are satisfied.

## Error handling

- If the file is missing, return: `Feature file not found.`
- If the file is empty or incomplete, return: `Run /feature create <spec-or-plan-file> [phase <n>] first`
- If the repo is not ready for branching, stop and report the issue clearly.
