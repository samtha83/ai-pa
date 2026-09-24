# Test Action

Use this action after the feature has been implemented and `/feature review` has
confirmed that the implementation is ready for focused test verification.

1. Read `@context/current-feature.md` and the selected feature `.md` file to understand:
   - the feature goals,
   - acceptance criteria,
   - intended behavior and error handling.
2. Identify new or modified logic that is appropriate for unit tests, prioritizing:
   - server actions,
   - services,
   - domain logic,
   - validation and parsing utilities,
   - data-access helpers with deterministic behavior.
3. Check existing tests before adding anything. Extend an existing test file or
   follow the repository's established test location and framework.
4. Add tests only where they provide meaningful protection for feature behavior:
   - cover important happy paths,
   - cover relevant invalid-input and error paths,
   - verify observable results and side effects,
   - avoid tests that merely duplicate implementation details,
   - do not add tests solely to increase line or branch coverage.
5. Do not create unit tests for presentational components unless the feature
   explicitly requires testable component behavior. Do not add tests for trivial
   pass-through code, configuration-only changes, or code with no meaningful
   deterministic behavior.
6. If no meaningful unit-test target exists, do not create placeholder tests.
   Report that no additional unit tests were warranted and explain why.
7. Run the repository's established focused test command for the affected code.
   If no focused command exists, run the project's standard test command. Do not
   invent a test command; inspect package scripts, project configuration, or the
   README first.
8. Report the result with:
   - tests added or updated,
   - the functionality and scenarios each test covers,
   - the test command and result,
   - any meaningful gaps or risks.

## Output Format

## Tests Added or Updated

**path/to/test-file**
Describe the feature behavior covered, including happy-path and error scenarios.

## Verification

`<test command>`

Passed / Failed

## Coverage of Feature Behavior

Explain which goals or acceptance criteria are protected by tests. Do not report
raw coverage percentages unless the user explicitly asks for coverage metrics.

## Test Gaps

List only meaningful untested behavior, or state that no additional unit tests
were warranted.