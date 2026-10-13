# Project Roadmap — Daily Notes Calendar with AI Summarization

A Django web app where a user logs in, writes dated notes in a notepad UI, sees them laid out on a monthly calendar + 24-hour day view, and can ask an AI to summarize any day's notes. Built sequentially, snippet by snippet, with you approving each step.

**Framework decision:** Django (chosen 2026-10-12). Full-stack Django first; we can carve out a FastAPI microservice later for the AI summarizer if it adds value.

**Naming decision:** Product name **DailyDiary**. Django project module `dailydiary`. First app `notes`. (Python module names stay lowercase by convention; the product name is used in UI, README, and GitHub repo name.)

**Companion docs:**
- `PROGRESS_TRACKER.md` — live state + "you are here" flowchart
- `SYSTEM_DESIGN.md` — HLD / LLD decisions with interview framing
- `API_GUIDE.md` — HTTP, REST, auth, idempotency, CORS, DRF, security, observability

---

## How we work together (the process rule)

1. I propose the next small snippet (one concept at a time) with a plain-English explanation of what the code does and *why*.
2. You **accept / reject / modify**.
3. On accept: I write the file(s), you commit.
4. We update `PROGRESS_TRACKER.md` and move to the next item.
5. No bulk code dumps. If a step feels too big, we split it.

---

## Software Development Lifecycle (SDLC) phases we will touch

- [ ] **1. Requirements** — captured below in "Features"
- [ ] **2. Design** — data model, URL routes, UI wireframe, AI pipeline design
- [ ] **3. Environment setup** — Python venv, Django install, Git init, `.gitignore`, `.env`
- [ ] **4. Version control** — GitHub repo, branching (`main` + `feature/*`), PRs, commit hygiene
- [ ] **5. Implementation** — models → migrations → views → templates → static → AI layer
- [ ] **6. Testing** — Django `TestCase`, pytest, fixtures, AI output eval
- [ ] **7. Code quality** — `ruff`/`black`, pre-commit hooks, type hints
- [ ] **8. CI/CD** — GitHub Actions (lint + test on PR), deployment-ready config
- [ ] **9. Documentation** — README, docstrings, API docs for the AI endpoint
- [ ] **10. Observability** — logging, error tracking basics
- [ ] **11. Deployment** (stretch) — Docker + a free host (Fly.io / Render)

---

## Architecture at a glance

```
Browser (HTML/JS/CSS templates)
        │
        ▼
Django views  ──►  Django ORM  ──►  SQLite (dev) / Postgres (prod)
        │
        ├──► Auth (django.contrib.auth)
        │
        └──► AI summarizer service
                     │
                     ▼
             Anthropic Claude API
             (prompt + notes → summary)
```

- **Backend:** Django 5.x, Django ORM, Django auth.
- **Frontend:** Django templates + a sprinkle of vanilla JS for the calendar interactions. (We can swap to HTMX later for a nicer UX without a full SPA.)
- **Database:** SQLite for dev, Postgres-ready schema.
- **GitHub:** Repo, branches, PRs, Actions for CI.
- **AI layer:** Anthropic Claude API, called from a dedicated service module, prompt stored in a template file.

---

## AI Engineer skills we will deliberately practice

Because your goal is AI engineering roles, we fold these in on purpose:

- [ ] **Prompt engineering** — write and iterate on the summarization prompt as a versioned template.
- [ ] **Structured output** — have the model return JSON (title, bullet points, sentiment) and validate with Pydantic.
- [ ] **Context management** — chunking logic when a day has many long notes; token budgeting.
- [ ] **Evaluation** — small eval set of (notes → expected summary shape); automated check that output parses + hits required fields.
- [ ] **Observability for LLM calls** — log prompt, model id, latency, token counts, cost estimate.
- [ ] **Caching** — don't re-summarize unchanged note sets; hash inputs.
- [ ] **Safety** — PII redaction pass before sending to the API (configurable).
- [ ] **Model migration awareness** — read model id from config, document how to swap models.
- [ ] **Retrieval primer (stretch)** — add semantic search over past notes using embeddings.

---

## Features (what we're building)

### Phase 1 — Foundation
- [ ] 1.1 Create Django project + first app (`notes`)
- [ ] 1.2 Initialize Git repo + `.gitignore` + first commit
- [ ] 1.3 Create GitHub repo + push + protected `main` branch
- [ ] 1.4 Settings split (base / dev) + `.env` loading
- [ ] 1.5 Base template + static files setup

### Phase 2 — Auth & Profile
- [ ] 2.1 User registration view + form
- [ ] 2.2 Login / logout views
- [ ] 2.3 Password reset flow
- [ ] 2.4 `Profile` model (one-to-one with User) — display name, bio, timezone, avatar
- [ ] 2.5 Profile view + edit page
- [ ] 2.6 Access control: all notes/calendar pages require login

### Phase 3 — Notes CRUD
- [ ] 3.1 `Note` model — title, body, created_at, owner (FK), day (date, indexed)
- [ ] 3.2 "New note" page — notepad-style textarea + title input
- [ ] 3.3 On save: timestamp with user's current local time → persist
- [ ] 3.4 Note detail page — view / edit / delete
- [ ] 3.5 Permissions: user can only touch their own notes

### Phase 4 — Calendar views
- [ ] 4.1 Monthly calendar view (30-ish day grid) with per-day note counts
- [ ] 4.2 Day view — 24 one-hour rows, notes placed at their saved timestamp
- [ ] 4.3 Click a note block → opens the note detail page
- [ ] 4.4 Month navigation (prev/next, jump to today)
- [ ] 4.5 Timezone correctness (store UTC, render user tz)

### Phase 5 — AI Day Summarizer
- [ ] 5.1 `Summary` model — day (date), owner, created_at, model_id, prompt_version, body, input_hash
- [ ] 5.2 Service module `ai/summarizer.py` — pure function `summarize(notes) → Summary`
- [ ] 5.3 Prompt template file + versioning
- [ ] 5.4 Structured output (JSON) parsed with Pydantic
- [ ] 5.5 "Summarize this day" button on day view → async-ish request
- [ ] 5.6 Summaries listed at end of day page; multiple allowed per day
- [ ] 5.7 Summaries also visible as a distinct marker on the monthly calendar
- [ ] 5.8 Logging: tokens in/out, latency, cost estimate, cache hit/miss
- [ ] 5.9 Eval harness — tiny fixture set + a pytest that checks structure

### Phase 6 — Quality & Shipping
- [ ] 6.1 `ruff` + `black` + pre-commit
- [ ] 6.2 Pytest + Django test settings + a handful of real tests per app
- [ ] 6.3 GitHub Actions: lint + test on every PR
- [ ] 6.4 README with setup, env vars, screenshots
- [ ] 6.5 Dockerfile + `docker-compose.yml` (web + Postgres)
- [ ] 6.6 Deploy to **AWS** (chosen target): ECS Fargate + RDS Postgres + S3 + Secrets Manager + GitHub Actions → ECR → ECS pipeline. Terraform for infra-as-code (stretch).

### Phase 7 — Stretch / AI-engineer bonus
- [ ] 7.1 Embeddings over notes + semantic search bar
- [ ] 7.2 "Ask my notes" chat endpoint using retrieval
- [ ] 7.3 Weekly / monthly rollup summaries
- [ ] 7.4 Streaming responses for the summarizer

---

## GitHub workflow we will follow

- `main` is always deployable.
- Each feature from the list above → its own branch: `feature/2.1-user-registration`.
- Commits are small and in the imperative mood: `add Profile model and migration`.
- Open a PR per feature → self-review diff → merge → delete branch.
- CI must be green before merge once Actions is set up.

---

## Definition of done for a feature

A feature is "done" only when all are true:
- [ ] Code written and runs locally
- [ ] Migrations created and applied (if DB touched)
- [ ] At least one test (or an explicit note why skipped)
- [ ] Linter clean
- [ ] Committed on its own branch
- [ ] PR opened, merged, branch deleted
- [ ] `PROGRESS_TRACKER.md` updated
