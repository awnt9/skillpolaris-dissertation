# Agent Workflow

> How the thesis agent reads instructions and modifies files across the human-in-the-loop pipeline.

## Prompt stack (top to bottom)

The agent does not follow a single prompt. Instructions are layered and combined on every turn.

```
┌─────────────────────────────────────────────────────────┐
│  Layer 0 — Cursor (always active)                       │
│  System prompt + user rules                             │
└──────────────────────────┬──────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────┐
│  Layer 1 — .cursorrules (workspace)                     │
│  Academic role, slash commands, workflow rules          │
└──────────────────────────┬──────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────┐
│  Layer 2 — agent_context/ (read each session)           │
│  STATUS · STRUCTURE · WORKFLOW · PROJECT · DESIGN ·     │
│  OUTLINE                                                │
└──────────────────────────┬──────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────┐
│  Layer 3 — On demand                                    │
│  GitHub skillpolaris · fetch_papers.py · output/*.tex   │
└─────────────────────────────────────────────────────────┘
```

| Layer | Source | When read | Modified by agent? |
|-------|--------|-----------|-------------------|
| 0 | Cursor (system + user rules) | Always | No |
| 1 | `.cursorrules` | Always (workspace-injected) | Only when improving the harness |
| 2 | `agent_context/*` | Session start; required in `/research` and `/write` | `STATUS.md` **always auto-updated** after `/research`, `/write`, and other progress-changing turns; `OUTLINE.md` when the index is approved/revised; `PROJECT.md` / `DESIGN.md` when vision or design changes (user-approved) |
| 3 | Code, papers, LaTeX | Per command or need | See read/write tables below |

## Expected flow

```
  ┌──────────────┐
  │ Normal chat  │  idea, question, feedback (no file writes)
  └──────┬───────┘
         │ need evidence
         ▼
  ┌──────────────┐
  │  /research   │  fetch_papers → discuss → auto-update STATUS.md
  └──────┬───────┘
         │
         ▼
  ┌──────────────┐
  │   Iterate    │  refine with user (repeat /research as needed)
  └──────┬───────┘
         │ content agreed
         ▼
  ┌──────────────┐
  │   /write     │  LaTeX + bibliography + compile → auto-update STATUS.md
  └──────┬───────┘
         │
         └──────────► next session
```

| Phase | Command | Writes files? | Output |
|-------|---------|---------------|--------|
| Ideate | *(none)* | No (unless user explicitly requests an edit) | Chat only |
| Research | `/research [topic]` | `STATUS.md` only (plus `OUTLINE.md` if approved) | Chat + paper summaries + proposed BibTeX |
| Iterate | *(none)* | No | Chat only |
| Write | `/write [section]` | Yes (`.tex`, `.bib`, PDF) + `STATUS.md` | Compiled thesis + refreshed status |

There is **no** `/update_status` command. Progress tracking is automatic.

## Read / write matrix

### Read (context — do not modify unless instructed)

| File | Purpose |
|------|---------|
| `.cursorrules` | Commands and constraints |
| `agent_context/PROJECT.md` | Stable vision |
| `agent_context/DESIGN.md` | Design decisions, constraints, challenges |
| `agent_context/STRUCTURE.md` | Repo layout |
| `agent_context/WORKFLOW.md` | This file |
| `agent_context/STATUS.md` | Current progress |
| `agent_context/OUTLINE.md` | Thesis index |
| `template/MasterThesis.tex` | IEEE skeleton (reference) |
| GitHub `awnt9/skillpolaris` | Technical implementation |
| `output/**` | Current thesis state |

### `/research` — chat + status only

| Action | Target |
|--------|--------|
| Read | `PROJECT.md`, `DESIGN.md`, `OUTLINE.md` |
| Run | `uv run tools/fetch_papers.py` (**always with full network** — OpenAlex fails in the default sandbox with ProxyError/403; use Shell `required_permissions: ["full_network"]`) |
| Output | Chat (proposed BibTeX, outline ideas) |
| Write | `STATUS.md` (always); `OUTLINE.md` only if user approved index changes |

### `/write` — writes

| File | Action |
|------|--------|
| `output/chapters/*.tex` | Create or edit chapter content |
| `output/MasterThesis.tex` | Title, abstract, `\input` wiring |
| `bibliography.bib` | Append cited references only |
| `output/TFM_Final.pdf` | Generated by `./compile.sh` |
| `output/*.log`, `output/*.aux` | LaTeX build artifacts (read to fix errors) |
| `agent_context/STATUS.md` | Auto-refresh at end of turn |
| `agent_context/OUTLINE.md` | If the thesis index changed |

`/write` should also **read** `DESIGN.md` for requirements, method, and design rationale.

### Auto-status (built-in, not a command)

| File | When |
|------|------|
| `agent_context/STATUS.md` | End of every `/research` and `/write`; also after user-requested harness/thesis edits that change progress |
| `agent_context/OUTLINE.md` | When the thesis index was approved or revised in that turn |

### Never touch

| Path | Reason |
|------|--------|
| `template/**` | Read-only IEEE skeleton |

### Rare (harness improvements only)

| File | When changed |
|------|--------------|
| `.cursorrules` | Workflow or command rules change |
| `agent_context/PROJECT.md` | Vision, objectives, scope, or approach change |
| `agent_context/DESIGN.md` | Design decisions, constraints, challenges, or open questions change |
| `agent_context/STRUCTURE.md` | Repo layout changes |
| `agent_context/WORKFLOW.md` | Agent behavior model changes |
| `tools/fetch_papers.py` | Search tool changes |

## Decision hierarchy

When multiple instructions could conflict, the agent applies this order:

1. **Is there a slash command?**
   - Yes → apply the matching skill in `.cursorrules` (`/research`, `/write`)
   - No → normal conversation (no tools or file writes unless the user explicitly requests an edit, or auto-status applies after such an edit)

2. **Inside `/research` or `/write`:**
   - `PROJECT.md` → *what* and *why* (stable vision)
   - `DESIGN.md` → *how we intend to solve it* (decisions, constraints, open questions)
   - `OUTLINE.md` → *where* in the thesis (evolves)
   - `STATUS.md` → *current progress* (most mutable; always refreshed at end of turn)

3. **Technical system detail:**
   - GitHub `awnt9/skillpolaris` — implementation truth (not `PROJECT.md` / not speculative DESIGN notes)

4. **Citations and prose:**
   - Only in `/write` → `bibliography.bib` + `.tex` files

## File roles (quick reference)

| File | Mutability | Owner of truth |
|------|------------|----------------|
| `PROJECT.md` | Stable — vision, objectives, scope, success criteria | User approves changes |
| `DESIGN.md` | Semi-stable — decisions, NFRs, strategy options, open questions | User approves changes |
| `OUTLINE.md` | Evolves — high-level index, detail added gradually | User approves; agent persists when approved |
| `STATUS.md` | Highly mutable — session-to-session progress | Agent, **automatically** after progress-changing turns |
| `bibliography.bib` | Grows during writing | Agent via `/write` (cited refs only) |
| `output/chapters/*.tex` | Grows during writing | Agent via `/write` |
| SkillPolaris repo | Independent codebase | Implementation truth for Method/Experiments |

## Outline evolution model

`OUTLINE.md` currently holds top-level chapters only, with subsections under §1 Introduction.

- Subsections for §2–§7 are **proposed in `/research` chat** first.
- They are **written to `OUTLINE.md` only after user approval** (in the same turn, with auto-status).
- This keeps the harness coarse early and precise only when needed.
