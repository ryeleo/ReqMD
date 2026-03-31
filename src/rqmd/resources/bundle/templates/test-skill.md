---
name: test
description: Repository-specific automated test, check, and validation commands for this project.
argument-hint: Describe whether you need the primary test command, integration coverage, or lint/check guidance for this repository.
user-invocable: true
metadata:
  guide:
    summary: Use the repository's canonical validation commands instead of guessing test workflows.
    workflow:
      - Start with the primary automated test command.
      - Use any dedicated integration or lint/check commands when the task calls for them.
      - Update this generated skill if the repository's real validation workflow differs from the scaffold.
    examples:
      - Ask for the canonical test command for this repository.
      - Ask for integration or lint commands before finishing a change.
---

Use this skill when work needs the repository's actual automated validation commands.

Detected sources:
{{DETECTED_SOURCES}}

Primary automated test commands:
{{PRIMARY_TEST_COMMANDS}}

Integration or end-to-end test commands:
{{INTEGRATION_TEST_COMMANDS}}

Lint and check commands:
{{LINT_AND_CHECK_COMMANDS}}

Notes:
{{NOTES}}

Constraints:
- Prefer these repository-specific validation commands over generic guesses.
- Review and edit this generated skill after bootstrap if the detected commands are incomplete or stale.