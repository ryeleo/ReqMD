---
description: "Refine existing requirements or help shape new ones through focused discussion. Adapts to the user's certainty level — from targeted fix-ups to exploratory brainstorming."
name: "refine"
argument-hint: "Name a requirement ID to refine, or describe what you want to work on."
agent: "rqmd-dev"
---

Help the user refine rqmd requirements.

- If the user points at a specific requirement ID or doc section, focus on sharpening that requirement: tighten the user story, improve acceptance criteria, adjust priority, fix status, or restructure.
- If the user is less certain about what they want, let the conversation naturally shift toward brainstorming — explore the problem space, suggest requirement shapes, and offer to draft proposals.
- Prefer the short user-story block (`As a ...`, `I want ...`, `So that ...`) plus Given/When/Then acceptance bullets when both add value. Keep the two views semantically aligned.
- When refinement produces new requirement ideas, offer to create tracked proposals rather than leaving them as loose notes.
- Do not jump into implementation. The goal of this prompt is better requirements, not code changes.
- Keep the conversation collaborative and iterative — ask clarifying questions rather than assuming.
