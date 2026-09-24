# Review Action

Use this action after a feature has been implemented.

This action combines the old "explain" and "review" steps into one final verification pass.

1. Read `@context/current-feature.md` to understand the feature goals and active scope.
2. Read the feature spec file (the generated feature `.md` file) to confirm the intended implementation and acceptance criteria.
3. Run `git diff main --name-only` to get the list of files changed for this feature.
4. For each changed file, provide a brief summary:
   - file path
   - whether it was new or modified
   - what changed and why
   - any key functions, components, or patterns introduced
5. Explain how the implemented pieces fit together in plain language.
6. Review the implementation against the feature goals and acceptance criteria:
   - ✅ Goals met
   - ❌ Goals missing or incomplete
   - ⚠️ Code quality issues or bugs
   - 🚫 Scope creep beyond the feature definition
7. Final verdict: `Ready to complete` or `Needs changes`.

## Output Format

## Implementation Summary

**path/to/file.ts** (new)
Brief explanation of what this file does and why it was added.

**path/to/other.ts** (modified)
What changed and why.

## How It All Connects

Brief summary of the data flow or control flow between the changed files and how the feature works together.

## Goal Verification

- Goal 1: Met / Missing / Partially met
- Goal 2: Met / Missing / Partially met
- Additional notes on quality, risk, or open issues

## Final Verdict

Ready to complete

or

Needs changes