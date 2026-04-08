---
description: "Commit the current work with a clear, human-narrative git commit message that distinguishes human decisions from AI-driven implementation."
name: "commit"
argument-hint: "Optionally describe the focus of this commit, or leave blank to auto-summarize."
agent: "rqmd-dev"
---

Create a clean git commit for the current working-tree changes.

Commit message conventions:
- The subject line should be a concise summary of the change driven by the human decision or request, not a list of files touched.
- The body should clearly reflect the human inputs and decisions that motivated the change.
- Include a separate section under a `# AI Development` heading that summarizes what the AI agent did to implement the request (files changed, tests added, docs updated, etc.).
- At the end of the commit message body, include a line like `AI agent: Claude Opus 4.6` (or whatever model and version you are) so the commit history tracks which AI contributed.
- Follow the same human-first, AI-acknowledged narrative used by the rqmd-changelog skill: human-driven decisions and key functional changes are the headline; AI implementation details are supporting context.

Workflow:
- Review the current `git diff --staged` and `git diff` to understand what changed.
- If nothing is staged, stage all changes that form a coherent unit of work. If the changes span unrelated concerns, ask the user which subset to commit.
- Do not amend or force-push existing commits.
- Do not sweep unrelated changes into the commit without asking.
- After committing, report the commit hash and a brief summary.
