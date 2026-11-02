# The harness, distilled

ECC is not a product and not a framework you call — it is a **configuration and workflow corpus** for
coding harnesses (Claude Code, Codex, OpenCode, Cursor, Gemini CLI). Nothing runs on its own: the harness
loads the markdown (skills / rules / agents) and the hooks, and the model does the work. Every claim about
"an AI team" reduces to three things: better prompts, phase discipline, and automated gates.

This document is the sixty-line version of that system, written after reading the upstream guides
(`the-shortform-guide.md`, `the-longform-guide.md`, `the-security-guide.md`), `AGENTS.md` and the skills
themselves. Everything below is upstream's thinking, compressed.

## Five layers, in the order they matter

| Layer | What it is | Why it exists |
|---|---|---|
| **Skills** (`skills/<name>/SKILL.md`) | canonical workflow/domain knowledge, loaded on demand | the durable unit; carries checklists, scripts, references |
| **Agents** (`agents/<name>.md`) | a scoped persona plus tool permissions handed to a subagent | saves orchestrator context; one job per agent |
| **Commands** (`commands/<name>.md`) | slash-entry shims that invoke a skill | legacy compatibility; the logic lives in the skill |
| **Rules** (`rules/common/*.md`, per-language) | always-on constraints (immutability, 80% coverage, no secrets) | guardrails that must not depend on recall |
| **Hooks** (`hooks/`) | event automations: PreToolUse, PostToolUse, UserPromptSubmit, Stop, PreCompact, SessionStart | deterministic gates the model cannot skip |

Plus **memory**: a session file that records *worked / failed / not attempted*, persisted by PreCompact and
Stop hooks, reloaded at SessionStart, and a continuous-learning skill that appends any non-trivial discovery
to a skill so it is not re-derived next session.

## The five operating principles

1. **Agent-first** — delegate to a specialist instead of doing everything in the main thread.
2. **Test-driven** — failing test first, then minimal green, then refactor; 80% coverage is the floor.
3. **Security-first** — secrets never in code, inputs validated at boundaries, parameterized SQL, no error leakage.
4. **Immutability** — return new objects instead of mutating; makes diffs and rollbacks cheap.
5. **Plan before execute** — complex features get a written plan before any edit.

## The phase pipeline (the real "team" effect)

```
research → plan → implement (TDD) → review → verify → commit
```

Rules that make it work, and that a single agent usually violates:

- each phase has ONE input and ONE output, written to a file (`research-summary.md`, `plan.md`, …);
- the output of phase N is the input of phase N+1 — never skip a phase, never merge two;
- clear context between phases so exploration tokens do not survive into implementation;
- the reviewer is a *different* pass than the writer, with a checklist, not a vibe;
- verification loops back to implement, not to plan, unless the plan itself was wrong.

**Subagent discipline** (`The Sub-Agent Context Problem`): a subagent sees the literal query, not the purpose.
Pass objective context, ask follow-ups on the returned summary, and cap the negotiate loop at **three cycles**
before accepting or escalating.

## Context economics (the part most people skip)

- Keep 20–30 MCP servers configured but **fewer than 10 enabled and fewer than 80 tools active**; a 200k
  window collapses to roughly 70k when every tool is loaded.
- Prefer a CLI wrapped in a skill over an always-on MCP (GitHub → `gh` in a command, Supabase → its CLI).
  Same capability, no tool-schema tax.
- Avoid the **last 20%** of the context window for multi-file work; simple edits tolerate more.
- Modular files (200–400 lines, 800 max) are a token optimisation, not just taste: the model re-reads less.
- Route by cost: a cheap model for search / simple edits / docs, mid for multi-file implementation and review,
  the top model for architecture, security analysis and gnarly debugging. Default mid; escalate on first
  failure, on 5+ files, or on security-critical code.

## Evals

- **Checkpoint evals** — explicit criteria per phase, fix before moving on.
- **Continuous evals** — full suite plus lint after every N changes or a major edit.
- `pass@k` (at least one of k attempts works): 70% → 91% (k=3) → 97% (k=5).
- `pass^k` (all k attempts must work): 70% → 34% (k=3) → 17% (k=5).

Use `pass@k` for "can it do this at all"; use `pass^k` where consistency *is* the product (cron jobs,
publishing pipelines).

## Self-evaluation, five axes

Accuracy, completeness, clarity, actionability, conciseness — the `agent-self-evaluation` skill scores
finished work on those before calling it done; `agent-architecture-audit` and the silent-failure hunters
audit swallowed errors. This is the antidote to "it returned 200, so it worked".

## Parallelism

Minimum viable parallelism, not an arbitrary terminal count. Overlapping code changes need git worktrees;
questions about the codebase go to a fork so they do not pollute the implementation thread; focus 3–4 tasks
at a time (cascade: new tasks to the right, sweep left to right, oldest first).

## Two rules worth adopting verbatim

- **A gate that cannot run must be named manual.** Reporting "all checks passed" while five items were
  human-only is worse than a shorter checklist.
- **A non-trivial discovery goes into the skill that failed**, immediately — not into the next session's
  memory, where it will be lost.

## What this collection keeps, and what it drops

Kept: the gates that stop fake completion (TDD, verification loop, security review), the context and memory
discipline, the orchestration pipeline, and real per-stack checklists.

Dropped: domain skills that only matter to one project (healthcare EDI, x402 payments, HarmonyOS, network
config templates) and the 250-odd language variants. They stay upstream — see
[github.com/affaan-m/ECC](https://github.com/affaan-m/ECC) — and can be copied in one command with
`tools/install-skill.sh` when a project actually needs one.
