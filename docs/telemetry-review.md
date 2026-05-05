# Running `/telemetry-review`

Turn recent agent friction into proposed requirements.
Do this whenever you want to see what's bothering the AI agents.

---

## Steps

**1. Open VS Code in this repo** — the tunnel task lives in `rqmd-cli`.

**2. Start the SSH tunnel** — open the Command Palette (`⌘⇧P`), run
`Tasks: Run Task`, pick **Tunnel to Az TeleVM**.
(You only need this once per session; it stays running in the background.)

**3. Run the prompt** — in the GitHub Copilot Chat panel, type:

```
/telemetry-review
```

Leave it blank for the default 14-day window, or pass a number:

```
/telemetry-review 30
```

**4. Review the output** — the agent will:
- Fetch events from the production gateway
- Print clusters of ≥ 2 similar events
- Flag any that look like duplicates of existing requirements
- Ask you to confirm before drafting each new one

**5. Commit** — once drafts land in `docs/requirements/`, commit normally.

---

## How often?

Weekly is plenty.
Any time you seed test events or deploy a new skill is a good trigger too.
