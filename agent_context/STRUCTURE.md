# Thesis Repository Layout

## Agent context (read before every session)

| File | Purpose |
|------|---------|
| `agent_context/STATUS.md` | Current progress, next steps, blockers (**auto-updated**; no `/update_status` command) |
| `agent_context/STRUCTURE.md` | This file — repo layout reference |
| `agent_context/WORKFLOW.md` | Agent prompt stack, flow, and read/write matrix |
| `agent_context/PROJECT.md` | Stable project vision — objectives, scope, success criteria, approach |
| `agent_context/DESIGN.md` | Design brief — decisions, constraints, challenges, open questions |
| `agent_context/OUTLINE.md` | Thesis index (draft → approved) |

See `agent_context/WORKFLOW.md` for the full human-in-the-loop pipeline and which files the agent reads or modifies per command.

## Read-only template

- `template/MasterThesis.tex` — IEEE skeleton. Do not edit.

## Working thesis (agent writes here)

- `output/MasterThesis.tex` — main document (title, abstract, `\input` wiring)
- `output/chapters/*.tex` — chapter and section content
- `output/TFM_Final.pdf` — compiled PDF (generated, not committed)

## Shared resources

- `bibliography.bib` — BibTeX references (populated by `/write`, not `/research`)
- `tools/fetch_papers.py` — academic paper search (OpenAlex)

## Build

- `./compile.sh` compiles `output/MasterThesis.tex` via Docker
