# Complete Action

Use this action only after the implementation has passed `/feature review` and
`/feature test`, or after explicitly recording why no additional unit tests were
warranted.

1. Read `@context/current-feature.md` and the selected feature file. Confirm:
   - the active feature is marked `Completed`,
   - the review verdict is `Ready to complete`,
   - tests pass or the test action documented that no meaningful tests apply.
2. Identify the current feature branch and confirm the working tree contains
   only the intended feature changes. Do not stage or discard unrelated user
   changes.
3. Verify the commit identity with `git config user.name`. Use the configured
   `user.name` for every commit; do not override it with `--author`, environment
   variables, or repository-local changes unless the user explicitly requests
   that change.
4. Stage the feature changes and commit them with a Conventional Commit message
   in the format `type(scope): description`.
   - Example: `feat(ui): add dark mode toggle switch`
   - Example: `fix(api): prevent timeout on heavy report generation`
   - Choose the type and scope that accurately describe the feature.
5. Switch to `main` and verify it is up to date with the intended merge base.
6. Merge the feature branch into `main` without pushing yet.
   - If the merge has conflicts, stop and report them. Do not delete the branch
     or reset `current-feature.md` until the conflicts are resolved.
7. Delete the local feature branch after the merge succeeds.
8. Reset `current-feature.md`:
   - change the H1 back to `# Current Feature`,
   - reset Status to `Not Started`,
   - clear Goals and Notes while keeping their placeholder comments,
   - append a concise summary of the completed feature to the end of History.
9. Commit the reset on `main` with the Conventional Commit message:
   `chore(feature): reset current-feature after completing [feature]`
10. Push `main` to `origin` once, after both commits and the merge are complete.
11. If the feature branch was previously pushed, delete that remote branch only
    after the `main` push succeeds.

## Completion Result

Report:

- feature branch merged into `main`,
- local branch deleted,
- whether the remote branch was deleted,
- `current-feature.md` reset and history updated,
- commits created,
- final push result.