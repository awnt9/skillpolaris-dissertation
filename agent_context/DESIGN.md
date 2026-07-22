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

- Select metadata through a **recruiter-oriented** view of each offer.
- Job-title / role-name metadata is a critical field for clustering, affinity, and metrics.

### Application (guidance / metrics)

- Select **valuable statistical metrics** (aggregations), not LLM answers.
- Product is an information and metrics source, not a recommender chatbot.

## Decision log (settled for harness)

1. **Statistics, not RAG** as the user-facing paradigm — see `PROJECT.md`.
2. **Programmer market first** — specialization over breadth.
3. **Pipeline + metrics app** as the solution shape.
4. **Other markets** → twin extractors / separate indexes later; not one shared Qdrant corpus.
5. **RAG roadmap** → out of scope for this thesis.

## Open questions

- Exact operational definition of the “programmer market” filter (depends on the final acquisition strategy).
- Which acquisition strategy (or hybrid) becomes the thesis Method baseline.
- Which subset of candidate sources is implemented and evaluated.
- Which metric set is “valuable” enough for the Experiments / Results chapters.

## Mapping to thesis chapters (guidance only)

| Design material | Likely chapter |
|-----------------|----------------|
| Motivation, scope, non-goals | §1 Introduction |
| Related systems, ESCO/taxonomies, job-mining literature | §2 State of the Art |
| NFRs, sources, strategy trade-offs | §3 Requirements and System Design |
| Pipeline, transformer schema, aggregations | §4 Method |
| Corpus coverage, metrics validation | §5–6 Experiments / Results |
| Twin markets, RAG roadmap | §7 Conclusions / future work |
