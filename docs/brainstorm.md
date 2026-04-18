# Brainstorm

Active ideas and untracked nuggets. Items move out once 
promoted to `docs/requirements/` or shipped.

## rqmd should have configuration to know whether to do pushes automatically or give the user git push commands instead

- Right now, rqmd agents love pushing things immediately! I love this a lot for a lot of my work as a single developer.... and it might be good for XP too even... BUT, my current workplace is definitely more 

## Multiuser support

- Most cross-device sync services also store a copy of the
data on a server, which provides a convenient off-site backup
for the data. These solutions work quite well as long as each
file is only edited by one person at a time. If several people
edit the same file at the same time, conflicts may arise, which
we discuss in Section 2.4 from https://dl.acm.org/doi/pdf/10.1145/3359591.3359737
- Moreover, we expect that local-first apps can support various workflows for collaboration. Besides having several
people edit the same document in real-time, it is sometimes
useful for one person to tentatively propose changes that
can be reviewed and selectively applied by someone else.
Google Docs supports this workflow with its suggesting
mode (Figure 5, [69]), and pull requests serve this purpose
in Git (Figure 6, [61]).

## Inbox

- next_id should return 1 if there is no existing objects. (bugs, reqs)
- /cathcup command should mostly repeat prior message but,  with added context of the discussion that lead to that prior message!

## Catchup should also check remotes

When doing a /catchup, it is prudent to make sure to run a "git fetch" and make sure that your local branches are up to date with their remote counterparts or upstream branches.


## TODO

I LOVE EDGE CASES that you provided! OMG! That is genius that generative AI would be amazing at imagining edge cases that I'm too lazy to think up!!!

Unfortunately, I should probably stop, since I am now totally vibe coding unfortunately. Reminder that tomorrow we should make sure to prioritize the concept of detecting and advising when the primary user (myself) is vibe coding 


## Requirement Polishing

/reqs-polish: Polish requirements so that they are properly formatted, well organized into correct repo/domain/subdomain, and easy for both humans and AI to navigate and understand!

## New Prompt

/refine-or-go: Could be a nice shortcut to either refine a requirement or proceed to implementation based on its current state.

> /refine "agent shaping" one more time if needed. o/w, gimme a "/go"!


## A key insight: Heirarchy

Remember that the human developer's brain is small, much smaller than the AI.

So the whole requirements system should be heirarchical in many regards:
- requirement domains and subdomains
- requirement relationships (parent/child, related, etc.)
- Make sure AI can step deeper into topics and remember how to step back up to the higher-level topic that drove them there. Remember the very begining, but also try to make a model of the path that got us there, so that it is easy to turn that path into a tree that can easily be navigated around with the developer as they refine requirements.

So, we should leverage 

## Requriements should be links to the docs  [→ promoted: RQMD-EXT-066–068]

Ideally in preview mode even, so that the user can immediately click on the "REQUIREMENT-XXX-NNN" and it will be a hyperlink to the actual requirement in the markdown docs already rendered into preview mode and scrolled to the right requirement/bug.

**Tracked:** DocumentLinkProvider (EXT-066), agent emits linked IDs in chat (EXT-067), stable anchor IDs on headings (EXT-068).

## GitHub / Copilot First Class


### Pull Request / Chat Agent

Make it possible to use `rqmd` within GitHub App. Right now, my only choice of "agents" in my GitHub Account is "copilot".

### Template Repo

Make a template repo for rqmd projects to easily copy from!


## Coach and Train the Developer to be a better dev with RQMD  [→ promoted: RQMD-EXT-061–065]

I do need to get back in the habit of actually doing specification/requriemtns driven development -- doing 'prompt development' has been very vibe-codey for us recently, which has resulted in some good iterations, but we really do need to get back to making sure we know what we are building it, why we are building it, and HOW we are building it (Requirements Driven Development via`rqmd` is the HOW that we need to make sure is coming  across).

**Tracked:** nudge on `/go` (EXT-061), brainstorm promotion status (EXT-062), `/refine` pre-fill (EXT-063), `/retro` prompt (EXT-064), session-start orientation (EXT-065).

### Requirements coverage report  [raw idea]

Like test coverage but for changes: "This commit touched 5 files. 3 changes map to tracked requirements. 2 are untracked." Could be a `rqmd --coverage` flag that cross-references `git diff` with requirement references in commit messages or changelogs. Larger effort — needs git integration.

### `/what` and `/why` clarity-test prompts  [raw idea]

Before `/go`, two quick prompts: `/what RQMD-XXX-NNN` drafts a one-paragraph "what are we building?" summary; `/why RQMD-XXX-NNN` drafts who benefits and what problem it solves. If the requirement is too vague to answer either, that's the signal to refine first. Lightweight alternative to full `/refine` when you just want a sanity check.

### Auto-capture turning-point insights to `docs/insights/`  [raw idea]

When the agent and user hit a turning point — a correction, a "wait actually...", a user story that reframes a requirement — the agent captures the moment as a small `docs/insights/<slug>.md` file. Each file records: date, model, what triggered the shift, what changed, linked requirement IDs, and a short transcript excerpt.

Cost: near-zero to scan — even 50 files is ~25KB, and agents only need `ls docs/insights/` + read by title. The insight IS the audit trail for why a requirement is shaped the way it is.

Related: could power `/retro` reviews ("these changes were motivated by these insights — did the build honor them?") and long-term pattern recognition ("most insights come from user stories, not from reading code").

### User-story-driven `/refine`, `/retro`, and `/brainstorm`  [raw idea]

The best requirement shaping happens when the developer tells a **first-person narrative** — "here's what happens to me when I try to do X." Every turning point in this session was triggered by the user describing actual friction, not by reading specs.

Idea: `/refine`, `/retro`, and `/brainstorm` should all **actively invite** first-person stories: "Walk me through what happens to you right now when you try to do X." Make the narrative the shaping tool, not a side effect.

Applies to bugs too: "Tell me what happened" > "Describe the expected behavior."

### Developer wellness nudges  [raw idea]

If the system clock says it's 2am and the developer is still in a `/go` loop... maybe gently suggest they get some sleep? Half-joke, half-serious. Rested developers write better requirements. Could be a light preference in agent instructions: "After midnight local time, the agent may gently note that rest improves both code quality and requirement clarity."

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
| Developer coaching | RQMD-EXT-061–065 |
| Clickable requirement IDs | RQMD-EXT-066–068 |
| Retro, catchup, session tree | RQMD-EXT-071–075 |\n| Domain term convention | RQMD-EXT-076 |\n| Inbox capture | RQMD-EXT-077, RQMD-EXT-078, RQMD-CORE-044 |
| Self-healing bootstrap | RQMD-EXT-056–060 |
| Performance | RQMD-CORE-037–040, RQMD-AUTOMATION-038 |
| Bug tracking | RQMD-CORE-041–043, RQMD-AUTOMATION-039, RQMD-AI-059–060 |
| Agent workflow | RQMD-AI-039, 041, 042, 053–058 |
| Feedback/telemetry | RQMD-AI-053–055, RQMD-TELEMETRY-015 |
