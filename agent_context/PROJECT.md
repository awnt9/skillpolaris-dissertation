# SkillPolaris — Project Context

> Stable project vision. Update only when objectives, success criteria, or core approach change — not when implementation details evolve.
>
> For design decisions, constraints, challenges, and open questions, see `DESIGN.md`.
> For code and runtime architecture, see GitHub `awnt9/skillpolaris`.

## Naming (thesis vs product)

| Name | Role |
|------|------|
| **SkillPolaris** | Repository / software product only (`awnt9/skillpolaris`). Valid in harness, chats about code, Method/Experiments when referring to the implementation. |
| **Thesis title** | Independent of the product name. Still TBD. |

**Hard rule for academic prose:** never write “SkillPolaris” in thesis chapters, abstract, title, or keywords. Prefer “this work”, “the proposed system”, “the pipeline”, or the eventual thesis title once set.

## Formal constraints (master’s programme)

| Constraint | Requirement | Source |
|------------|-------------|--------|
| **Length** | **20–25 pages** (final compiled PDF) | Master’s programme directors |

Writing and outline decisions must keep the full thesis inside this band: dense enough to cover Motivation → Conclusions, without padding. Prefer depth on Method / Experiments over verbose restatements. Target the IEEE one-column layout used in `output/MasterThesis.tex`.

## Motivation

Career uncertainty is rising as people migrate across professions and sectors into a labor market that is both complex and difficult:

- **Complex** — many occupation labels, and job offers for the same role ask for very different skills.
- **Difficult** — especially for newcomers entering software, amid the conjuncture of programming agents and shifting skill expectations.

Despite that difficulty, people keep entering programming. The working intuition is a medium-term paradox: most knowledge work trends toward software-related paths, while long-horizon automation may eventually reach further. The thesis system addresses the near-term information gap: grounding career decisions in labor-market evidence rather than generic advice.

## Objective

Enable users to understand what the labor market demands from them and from people in their field, so they can:

1. Identify occupations where they have the highest aptitude.
2. Decide where to invest their learning time for the best return.
3. Build a sound professional strategy.

## Scope

**In scope for this thesis:** the **programmer / software labor market**, not the general labor market.

Rationale:

- Job offers in this market are relatively homogeneous in structure (title + stack + salary-like signals), which makes extraction, enrichment, and statistical aggregation tractable.
- Embedding-based differentiation works better inside a specialized corpus than across heterogeneous occupations.
- Scope aligns with the motivation (migrations into programming, market complexity, agent conjuncture).
- Broad coverage (“everything”) would dilute quality; specialization is preferred.

**Out of scope (explicit non-goals):**

- A conversational RAG career chatbot as the primary product surface.
- A general job-recommendation engine.
- Multi-market corpora in the **same** vector index (see Future work).

## Success Criteria

Two levels (do not conflate in Experiments):

| Level | Criterion | Role in thesis |
|-------|-----------|----------------|
| **Proximal (product vision)** | The user can make sound career decisions from the information the app provides; in the long run those decisions support professional goals. | Framing only — not the primary experimental metric |
| **Evaluable (thesis)** | Pipeline and metrics are feasible, faithful to the corpus, and inspectable: transform quality, aggregation correctness/stability, coverage of the target market. | What §5–§6 measure |

Guidance for users remains **objective, reproducible statistics** from which they draw their own conclusions — not LLM advice and not a ranked list of job openings.

Detail of evaluation instruments (golden set, LLM-as-judge on transform, aggregation checks, *k*-sensitivity) lives in `DESIGN.md`.

## Core Approach

**Proposed solution:** an offline **pipeline (extractor + transformer)** plus an application that surfaces **profile-conditioned aggregated metrics**.

Collect and analyze large volumes of job offers automatically. Use LLMs and vector databases during **offline processing** to enrich and index the corpus. At query time, retrieve a cohort of nearby **ideal-candidate** representations for the user profile, then return **deterministic statistics over that cohort’s metadata** — not LLM-generated advice and not a ranked list of vacancies.

### Design Principle: Statistical Truth, Not RAG

The LLM enriches the data pipeline; the user-facing layer answers with calculated facts. Embeddings support **cohort selection** (proximity); they are not the answer surface.

Examples of user-facing outputs:

- Most frequent standardized role titles in the retrieved cohort.
- Stack-fit percentages per standardized role relative to the user profile.
- Mean years of experience required, language requirements, etc., aggregated over the cohort.

This is a labor-market **information** system (profile-conditioned aggregation), not a job recommender and not a conversational career chatbot. Insights must be traceable to the underlying vacancy metadata.

**Why not RAG as the core:**

- The hard problem is extraction + transformation; a production-grade RAG product on top would be another thesis, starting from the dataset this work can produce.
- Value lies in the dataset and derived metrics, not in a chatbot layered on top.
- Naive RAG over Qdrant does not repay its cost for the key market questions; those are answered better by aggregations than by retrieval + LLM.
- The product intent is objective statistics so the user can form their own conclusions.

**Why not a job recommender:**

- Recommenders optimize item ranking (vacancies ↔ candidates). This work returns **distributions over a proximity cohort**, not “apply to these N jobs”.

## System Concept

Three conceptual layers:

1. **Acquisition** — automated collection of job offers from multiple sources.
2. **Processing** — transform each offer into (a) recruiter-oriented **metadata** and (b) an **ideal candidate** representation for embedding/indexing.
3. **Guidance** — embed the user profile, retrieve the top-*k* nearest ideal candidates, **aggregate their metadata**, and surface inspectable career metrics in the application UX.

## Thesis Framing

A labor-market intelligence system for early-career professionals (initially programmers) that separates intelligent offline enrichment from a deterministic statistical insight layer — oriented toward career strategy, not job recommendation or conversational HR assistance.

## Future Work (not this thesis)

- **Other markets** (engineering, law, marketing, …): likely **twin extractors** with a different LLM filter — **not** the same Qdrant collection (embeddings and offer formats do not extrapolate cleanly).
- **RAG / conversational guidance:** roadmap item; treat as a separate thesis-scale effort on top of the dataset and metrics foundation.
