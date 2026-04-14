# Brainstorm

Active ideas and untracked nuggets. Items move out once promoted to `docs/requirements/` or shipped.

## New Prompts

### /fix — Quick bug fix without ceremony

Right now: file bug → refine → propose `/go` → spawn implementation agent → fix.

Proposed: `/fix <description>` tries to fix immediately AND files a bug report to `bugs.md` for tracking. Quick path for frustrated devs, still leaves audit trail.

---

## Requirement Format


## Skills

### Systems Analysis

MTTF equations for estimating system availability from component failure rates. Learned in grad school — immensely powerful. Could be its own skill or tied into diagramming.

### Discovery vs Explore vs Solve modes

- **Explore:** open-ended, breadth-focused, no required outcome
- **Discover:** focused on finding info to drive decisions
- **Solve:** specific problem with a potential solution

Might inform how prompts/skills are categorized.

---

## CLI

### BrokenPipeError handling

AI loves `head`/`tail` but it breaks `--json` output. Add:
```python
except BrokenPipeError:
    pass  # normal when piping to head/tail/less
```

### 🤖 AI Verified status

Distinguish `✅ Verified (human)` from `🤖 Verified (AI)`. Pin model + version + date for audit trail. Lower confidence than human verification but still useful.

---

## Telemetry

### Skill trigger telemetry

Batch skill invocation events instead of per-invocation network calls.

### Local dev admin tools

Docker Compose for Adminer/pgAdmin autoconfigured to reach remote telemetry server via tunnel.

### Feedback loop automation

Weekly GitHub Action that reads telemetry, proposes improvements, opens PR automatically.

### Opt-out by default

Ship telemetry on, easy opt-out via `RQMD_TELEMETRY_DISABLED=1`.

---

## GitHub Integration

### CI/CD examples

Link requirements to GH issues. When issue closes, auto-PR a status update via `rqmd --update`.

---

## Still worth triaging

- Agent-opinionated interview hints (`render_as_checkbox_prompt`, etc.)
- Terminal markdown improvements beyond bold/headings
- Explicit `Ctrl+Z`/`Ctrl+Y` bindings
- README generation as "tool-owned index" policy
- Cross-root config discovery for `--docs-dir`

---

## Single Smart Agent Workflow (rqmd-vscode bundle)

> Context: The dumb-vs-smart cost split is irrelevant. Handoffs are always to a capable fork of the same smart agent. Refactor the whole bundle to reflect this.

### Collapse `rqmd-dev-easy` + `rqmd-dev-longrunning` into `/go` arguments

Two separate agent files exist entirely because users "picked the cheaper agent." With no cost concern, `/go easy-win` and `/go 10` already cover the UX. Delete the files; fold the unique behavior into the primary `rqmd` agent's `argument-hint`.

### Thin agent files — one shared contract in `copilot-instructions.md`

The AI output defaults block (15+ lines) and the full skill list are duplicated verbatim in `rqmd.agent.md`, `rqmd-dev-easy.agent.md`, and `rqmd-dev-longrunning.agent.md`. This duplication existed so each file was self-contained for a possibly-dumb receiver. Promote the shared contract to `copilot-instructions.md`; agent files become: name, description, tools, and the 1-2 lines unique to that agent.

### Skills as focus contracts, not instruction manuals

`rqmd-implement` opens with `Start: rqmd-ai --json --workflow-mode implement` — bootstrapping a cold agent. A smart fork already knows the domain. Skills → single-screen focus declaration: narrowed charter + done-when criteria + any non-obvious edge cases. Remove command rehearsals.

### "Complete and concise" as an explicit handoff standard

Define the quality indicator: **Complete** = receiver can make correct decisions without re-reading history. **Concise** = fits in a few lines, everything else omitted. Apply to `# Up next` and all skill handoff sections. Target: 3 bullets max, ID + one-line state + open question if any.

### Sub-agents as lenses, not dumb helpers

`rqmd-explore`, `rqmd-requirements`, `rqmd-docs` — reframe from "delegate to a simpler helper" to "invoke the same smart agent with a narrowed charter." Affects agent file language and handoff verbosity; not behavior.

### Init handoff: short brief instead of structured interview JSON

`rqmd-ai init --json` produces an elaborate interview protocol designed for a dumb receiver (see `RQMD-EXT-022`). With a smart fork: emit a short brief paragraph (repo context + 3-4 open questions). Preserve the schema for machine-readable validation, but shrink the prose payload by ~80%.

### Drop the "paste this into AI chat" init ceremony

The "print a prompt you paste into a new chat window" init gateway (`RQMD-EXT-014`/`015`) was designed for explicit session handoffs to a fresh/dumb agent. With smart forks: init continues in the same session. `rqmd init` → agent reads output → asks questions → writes files. No copy-paste checkpoint.

### Reconsider `RQMD-EXT-047` — brainstorm resisting implementation

"Brainstorm mode should resist code changes and defer to a cheaper implementation agent" encodes the dumb/smart split. Replace with: the agent self-disciplines within one session (tracks ideas → promotes to requirements → implements when ready), but no hard session boundary or deferral to a "cheaper" agent is assumed.

---

## Reference: Recently Tracked

Items promoted from this file — see `docs/requirements/` for details:

| Area | IDs |
|------|-----|
| @rqmd chat participant | RQMD-EXT-053, 054 |
| VS Code extension | RQMD-EXT-051, 052, 055 |
| Self-healing bootstrap | RQMD-EXT-056–060 |
| Performance | RQMD-CORE-037–040, RQMD-AUTOMATION-038 |
| Bug tracking | RQMD-CORE-041–043, RQMD-AUTOMATION-039, RQMD-AI-059–060 |
| Agent workflow | RQMD-AI-039, 041, 042, 053–058 |
| Feedback/telemetry | RQMD-AI-053–055, RQMD-TELEMETRY-015 |
