# Inbox

- When providing a list of instructions, often times it is possible to embed a 'start page' hyperlink if the instructions start with "login here" or "go to this page" or "open this page" -- we can hyperlink the page in the instruction text.
  That way, when a user follows the instructions, the first instruction will have an actionable link that will get them started in the right place instead of having to figure out "where are the GitHub Actions for this repo..?"
- Is the fact that inbox.md is only temporarily holding items mean that it is gonna be an issue on multi-user repos where lots of people might churn through the inbox?
  As long as each item is a line item, git is quite good at merging line-item churn, so maybe not?
  Maybe we just need to make sure to keep items small and atomic so that they can be easily merged if multiple people are adding items at the same time?
- "Agent Context File" is a term maybe??
- Brainstorm.md, inbox.md, and any other md files we depend on should have some basic boilerplate/discussion of purpose at the top and instructions on how to use it as if it were just a MD doc (but also still nudge them towards using it as an agent context file)...
- When upgrading the rqmd VS Code extension, VS Code should try to install the newest version of rqmd CLI tool at the same time! OBVIOUS! Hopefully vscode extension marketplace supports this kind of paired release.
- Get rid of `reqmd` entirely -- we shouldn't have an extra name for our tool, just `rqmd`!
- I have a full telemetry server set up that we haven't even used yet to ingest feedback from! → already tracked: RQMD-TELEMETRY-010
- Add a custom icon for the rqmd VS Code extension (`package.json` top-level `icon` field, 128×128 PNG). Currently shows as generic in the chat mode picker. → already tracked: RQMD-VSCODE-011
- [tech-debt] RQMD-EXT-087 refinement: when `/tech-debt` encounters "implemented-but-unreferenced" reqs, recommend "annotate tests/source with `# RQMD-*` xref comments" as a batch action instead of "consider deprecating."
  Depends on RQMD-CORE-056 adding `"reason": "xref_gap"` to `--staleness --json`.
