# SkillPolaris — Project Context

> Stable project vision. Update only when objectives, success criteria, or core approach change — not when implementation details evolve.

## Motivation

Career uncertainty is a major challenge for young professionals, especially recent graduates facing many possible paths with little data-driven guidance. SkillPolaris exists to reduce that uncertainty by grounding career decisions in real labor-market evidence rather than generic advice.

## Objective

Enable users to understand what the labor market demands from them and from people in their field, so they can:

1. Identify occupations where they have the highest aptitude.
2. Decide where to invest their learning time for the best return.
3. Build a sound professional strategy.

## Success Criteria

The project succeeds when users make better career decisions and, ultimately, find employment as a result of the strategic guidance the application provides.

## Core Approach

Collect and analyze large volumes of job offers automatically. Use LLMs and vector databases during **offline processing** to enrich and index the corpus. Present users with **deterministic, reproducible statistics** derived from that corpus — not LLM-generated advice about their profile.

### Design Principle: Statistical Truth, Not RAG

The LLM enriches the data pipeline; the user-facing layer answers with calculated facts:

- Affinity scores (e.g. "80% match with this occupation").
- Skill demand frequencies (e.g. "technology X appears in 40% of offers for this role").

This is not a conversational career chatbot. Insights must be traceable to the underlying dataset.

### System Concept

Three conceptual layers:

1. **Acquisition** — automated collection of job offers from multiple sources.
2. **Processing** — transform raw offers into structured, searchable representations (including an "ideal candidate" view per offer).
3. **Guidance** — match the user profile against the corpus and surface statistical career intelligence through the application UX.

## Thesis Framing

A labor-market intelligence system for early-career professionals that separates intelligent offline enrichment from a deterministic statistical insight layer — oriented toward career strategy, not job recommendation or conversational HR assistance.
