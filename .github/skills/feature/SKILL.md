---
name: feature
description: Manages feature lifecycle, parses epic specs into junior-friendly implementation files, and supports implementation tasks.
argument-hint: create|start|review|test|complete
---

# Feature Workflow

Manages the full lifecycle from an epic specification to individually
implementable feature files and then through implementation and review.

## Working File

@context/current-feature.md

### File Structure

current-feature.md has these sections:

- `# Current Feature` - H1 heading with feature name when active
- `## Status` - Not Started | In Progress | Completed
- `## Goals` - Bullet points of what success looks like
- `## Notes` - Additional context, constraints, or details from spec
- `## History` - Completed features (append only)

## Task

Execute the requested action: $ARGUMENTS

| Action | Description |
|--------|-------------|
| `create`| Parses every feature section in a spec and creates one detailed feature file per feature|
| `start` | Begin implementation, load the specified feature into current-feature and start implementation |
| `review` | Briefly summarize implementation and verify all feature goals are met |
| `test` | Add and run focused unit tests for meaningful feature behavior |
| `complete` | Commit, merge, delete branch, reset current feature, push |

See [actions/](actions/) for detailed instructions.

For `create`, follow [actions/create.md](actions/create.md) exactly. Generated
files must contain ordered implementation steps, file/module locations,
definitions of done, contracts, verification, acceptance criteria, and
out-of-scope notes. Never collapse an epic into one generic feature file.

If no action provided, explain the available options.