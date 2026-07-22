# SkillPolaris — Project Context

> Stable project vision. Update only when objectives, success criteria, or core approach change — not when implementation details evolve.
>
> For design decisions, constraints, challenges, and open questions, see `DESIGN.md`.
> For code and runtime architecture, see GitHub `awnt9/skillpolaris`.

## Motivation

Career uncertainty is rising as people migrate across professions and sectors into a labor market that is both complex and difficult:

- **Complex** — many occupation labels, and job offers for the same role ask for very different skills.
- **Difficult** — especially for newcomers entering software, amid the conjuncture of programming agents and shifting skill expectations.

Despite that difficulty, people keep entering programming. The working intuition is a medium-term paradox: most knowledge work trends toward software-related paths, while long-horizon automation may eventually reach further. SkillPolaris addresses the near-term information gap: grounding career decisions in labor-market evidence rather than generic advice.

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

The project succeeds when users make better career decisions and, ultimately, find employment as a result of the strategic guidance the application provides — guided by **objective, reproducible statistics** from which users draw their own conclusions.

## Core Approach

**Proposed solution:** an offline **pipeline (extractor + transformer)** plus an application that surfaces **aggregated metrics**.

Collect and analyze large volumes of job offers automatically. Use LLMs and vector databases during **offline processing** to enrich and index the corpus. Present users with **deterministic, reproducible statistics** derived from that corpus — not LLM-generated advice about their profile.

### Design Principle: Statistical Truth, Not RAG

The LLM enriches the data pipeline; the user-facing layer answers with calculated facts:

- Affinity scores (e.g. "80% match with this occupation").
- Skill demand frequencies (e.g. "technology X appears in 40% of offers for this role").

This is not a conversational career chatbot. Insights must be traceable to the underlying dataset.

**Why not RAG as the core:**

- The hard problem is extraction + transformation; a production-grade RAG product on top would be another thesis, starting from the dataset this work can produce.
- Value lies in the dataset and derived metrics, not in a chatbot layered on top.
- Naive RAG over Qdrant does not repay its cost for the key market questions; those are answered better by aggregations than by retrieval + LLM.
- The product intent is objective statistics so the user can form their own conclusions.

## System Concept

Three conceptual layers:

1. **Acquisition** — automated collection of job offers from multiple sources.
2. **Processing** — transform raw offers into structured, searchable representations (including an "ideal candidate" view per offer).
3. **Guidance** — match the user profile against the corpus and surface statistical career intelligence through the application UX.

## Thesis Framing

A labor-market intelligence system for early-career professionals (initially programmers) that separates intelligent offline enrichment from a deterministic statistical insight layer — oriented toward career strategy, not job recommendation or conversational HR assistance.

## Future Work (not this thesis)

- **Other markets** (engineering, law, marketing, …): likely **twin extractors** with a different LLM filter — **not** the same Qdrant collection (embeddings and offer formats do not extrapolate cleanly).
- **RAG / conversational guidance:** roadmap item; treat as a separate thesis-scale effort on top of the dataset and metrics foundation.
