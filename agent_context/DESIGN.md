# SkillPolaris — Design Brief

> Semi-stable design context transferred from ideation notes.
> Complements `PROJECT.md` (vision) and GitHub `awnt9/skillpolaris` (implementation truth).
> Update when design decisions, constraints, or open questions change — not for routine progress (use `STATUS.md`).
>
> This file is **harness memory**, not thesis prose. Academic chapters are written only via `/write`.

## Intended stack

| Layer | Choice |
|-------|--------|
| Language | Python |
| Orchestration | Prefect |
| Relational store | PostgreSQL |
| LLM / agents | Pydantic AI |
| Vector store | Qdrant |

Implementation details and current code live in GitHub `awnt9/skillpolaris`; this table records the **intended** thesis stack.

## Scope constraints (simplification)

- Prefer **open-data / public APIs** where possible: fewer legal risks, cleaner data, stable IDs.
- Market scope is **programmers** in the current framing (`PROJECT.md`); final acquisition filters may still refine how “programmer market” is operationalized (see Open questions).
- **Document length:** final thesis PDF must be **20–25 pages** (master’s programme directors). Budget sections accordingly; see `PROJECT.md` § Formal constraints.

## Layer challenges

### Acquisition (scraper / extractor)

Hard problems: bound search parameters, handle heterogeneous sources, guarantee idempotency.

**Target properties:**

| Property | Intent |
|----------|--------|
| Idempotency | Each job offer lands in the database once |
| Observability | Developer can see what the pipeline is doing |
| Extraction speed | High throughput |
| Low cost | Prefer free / open sources |
| Block management | Avoid IP blocks and legal exposure |
| Cleanliness | Offers arrive in a standardized format |
| Scalability | Easy to add new sources |
| Representativeness | Corpus should represent the target labor market |

**Candidate acquisition strategies (under consideration):**

| Approach | Recall | Adaptability | Cost | Complexity | Brief description |
|----------|--------|--------------|------|------------|-------------------|
| ESCO keywords | Low | None | Free | Medium | Search by ESCO/ISCO occupation codes |
| Manual list (skills + roles) | Medium | None (manual) | Free | Low | Developer-defined keywords for API queries |
| Pull-all feeds | High (unfiltered feeds) | High | High | Low | Ingest full feeds; classify afterwards |
| Sector codes | Medium–high | Low (stable) | Free | Medium | Filter by sector (NACE, SOC, ROME, …) |
| **Emergent taxonomy** | **High** | **High (automatic)** | **Free** | **High** | Cluster real titles; feed clusters back into search |
| ATS coverage (tech firms) | High in tech | Medium | Free | Medium | Ingest Greenhouse / Lever / Ashby boards |
| Stratified sampling | Controlled | Medium | Free | Medium | Sweep geo × seniority × modality × keywords without exhausting quotas |

**Candidate sources (human-in-the-loop shortlist; not an approved final set):**

RemoteOK, Remotive, Arbeitnow, Himalayas, Jobicy, Landing.jobs, Greenhouse, Lever, Ashby, USAJOBS, France Travail, Adzuna, Bundesagentur, EURES, InfoJobs, Jooble, Reed, The Muse, CareerOneStop, Find a Job UK.

### Transformer

Two outputs per offer (both required for the guidance model):

| Output | Role |
|--------|------|
| **Recruiter-oriented metadata** | Fields used later in aggregations (standardized title/role, stack, years of experience, languages, …). |
| **Ideal candidate** | Structured representation of the person the offer seeks; embedded and indexed so a user profile can be compared in the same space. |

Job-title / role-name normalization is critical: rankings of standardized titles in a cohort are a primary user-facing signal.

### Application (guidance / metrics)

**Query path (settled intent):**

1. User profile → embedding (same space as ideal candidates).
2. Retrieve top-*k* nearest ideal candidates (e.g. order of hundreds; exact *k* is a Method parameter).
3. Aggregate **metadata** of that cohort (not return the vacancies as recommendations).
4. Frontend shows inspectable metrics, e.g. most frequent standardized titles, stack-fit % per title, mean experience required, language requirement rates.

Framing: **profile-conditioned aggregation** / retrieval-conditioned statistics. Embeddings = cohort filter; answers = deterministic aggregates. Information system, not recommender, not RAG.

**Observability:** Langfuse (or equivalent) for tracing transform LLM calls; useful for monitoring and for LLM-as-judge evaluation of transform outputs.

## Evaluation plan (thesis-measurable)

Proximal product vision (“better career decisions / long-term goals”) is **not** the primary experimental target — see `PROJECT.md` § Success Criteria.

| Instrument | What it evaluates | Notes |
|------------|-------------------|--------|
| **Golden dataset** | Transform quality vs author-defined labels/criteria on a curated offer sample | Primary human ground truth |
| **LLM-as-judge** | Quality of model-generated transform fields (metadata / ideal candidate) | Auxiliary; rubric + monitoring (e.g. Langfuse); not the sole success metric |
| **Aggregation checks** | Backend metrics match independent recomputation on the same *k* neighbors | Deterministic; no LLM |
| **Pipeline / *k*-sensitivity** | Feasibility, coverage, stability of rankings/% when *k* changes | Reproducibility of the cohort slice |
| **Longitudinal user outcomes** | Employment / long-term goals | **Out of scope** as evaluable experiment; keep as proximal vision only |

## Decision log (settled for harness)

1. **Statistics, not RAG** as the user-facing paradigm — see `PROJECT.md`.
2. **Programmer market first** — specialization over breadth.
3. **Pipeline + metrics app** as the solution shape.
4. **Transform = metadata + ideal candidate**; guidance = top-*k* proximity then **aggregate metadata** (not rank jobs).
5. **Success:** proximal vision vs evaluable metrics split as above; LLM-as-judge only on transform quality (auxiliary).
6. **Other markets** → twin extractors / separate indexes later; not one shared Qdrant corpus.
7. **RAG roadmap** → out of scope for this thesis.

## Open questions

- Exact operational definition of the “programmer market” filter (depends on the final acquisition strategy).
- Which acquisition strategy (or hybrid) becomes the thesis Method baseline.
- Which subset of candidate sources is implemented and evaluated.
- Exact *k*, distance metric, and embedding model version (document for reproducibility).
- Operational definition of stack-fit and title standardization.
- Which metric set is “valuable” enough for the Experiments / Results chapters.
- Alternatives to compare later if needed: occupation/cluster stats without kNN; global aggregates as baseline.

## Mapping to thesis chapters (guidance only)

| Design material | Likely chapter |
|-----------------|----------------|
| Motivation, scope, non-goals, high-level solution | §1 Introduction |
| Related systems, ESCO/taxonomies, job-mining vs recommenders | §2 State of the Art |
| NFRs, sources, strategy trade-offs, observability (Langfuse) | §3 Requirements and System Design |
| Pipeline, transform schema, embedding space, *k*, aggregation formulas | §4 Method |
| Golden set, LLM-as-judge protocol, aggregation/*k* checks, coverage | §5–6 Experiments / Results |
| Twin markets, RAG roadmap, longitudinal outcomes | §7 Conclusions / future work |
