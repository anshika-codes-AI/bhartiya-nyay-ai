# Bhartiya Nyay AI

> **A workflow-first, BNS/BNSS-native Legal Drafting Assistant for Indian Advocates**
> Built to solve the post-IPC “Year Zero” transition with trust, structure, and auditability.

---
## 🚀 Getting Started

New here?  
👉 Start with [START.md](START.md)

## 📌 Project Philosophy

Bhartiya Nyay AI is **not a chatbot**.

It is a **legal workflow engine** that mirrors how real advocates work:

* Facts first
* Law mapping second
* Drafting only after legal grounding
* Mandatory human review
* File-ready court documents

Every design decision in this codebase prioritizes:

* ❌ Zero hallucination tolerance
* 📜 Auditability (court-defensible)
* ⚖️ Legal discipline over AI freedom

---

## 🧠 High-Level Architecture

```
User
 ↓
Draft Creation
 ↓
Guided Fact Intake (Validated)
 ↓
IPC → BNS Legal Mapping (Intent-based)
 ↓
Draft Blueprint Generation (No AI)
 ↓
Controlled AI Drafting (Review Mandatory)
 ↓
DOCX Export (Court-Ready)
```

> **RAG (case-law retrieval)** will be inserted **after Legal Mapping** and before Draft Generation.

---

## 🏗️ Tech Stack

* **Backend:** Django + Django REST Framework
* **Architecture:** Workflow-gated services (not prompt-based)
* **AI (current):** Mocked / controlled (LLM pluggable later)
* **Docs Export:** `python-docx`
* **Database:** SQLite (dev) → PostgreSQL (prod-ready)

---

## 📂 Project Structure

```
bhartiya_nyay_ai/
├── users/                 # Advocate identity (minimal, OTP-ready)
├── drafting/              # Core drafting workflow
│   ├── models.py
│   ├── workflow.py
│   ├── services.py
│   ├── fact_definitions.py
│   ├── draft_blueprint.py
│   ├── ai_prompts.py
│   ├── ai_drafting.py
│   ├── docx_export.py
│   ├── views.py
│   └── urls.py
├── transition_engine/     # IPC → BNS / BNSS logic
│   ├── models.py
│   └── services.py
├── legal_rag/             # RAG foundation (judgments + chunks)
│   ├── models.py
│   └── admin.py
├── manage.py
└── README.md
```

---

## 🔐 Core Design Principles

### 1. Workflow First (Not Chat First)

No step can be skipped.

Draft lifecycle:

```
CREATED
 → FACTS_COLLECTED
 → LEGAL_MAPPED
 → DRAFT_GENERATED
 → REVIEWED
 → EXPORTED
```

All transitions are enforced centrally.

---

### 2. Structured Fact Intake (Anti-Hallucination Layer)

Facts are **not free text**.

Each draft type has a **fact schema** defining:

* Allowed keys
* Required vs optional facts
* Expected data types

Example (BNSS Bail):

* FIR_NUMBER (string)
* DATE_OF_ARREST (date)
* CUSTODY_DURATION_DAYS (number)
* SECTIONS_INVOKED (list)

❌ Unknown facts are rejected
❌ Missing required facts are blocked
❌ Wrong data types are rejected

---

### 3. Legal Mapping Engine (IPC → BNS)

Instead of mapping section numbers blindly, Bhartiya Nyay AI maps:

* **IPC Section → BNS Section**
* **Legal intent**
* **Drafting notes**

This solves the post-IPC transition problem at the **reasoning level**, not just numerically.

Mapped law is:

* Persisted per draft
* Immutable once saved
* Used as the legal basis for drafting

---

### 4. Draft Blueprint (AI-Free Core)

Before AI is ever called, the system generates a **Draft Blueprint**:

```json
{
  "draft_type": "BAIL_BNSS",
  "facts": {...},
  "legal_basis": [...],
  "sections": {
    "facts": true,
    "grounds": true,
    "prayer": true
  }
}
```

This blueprint is:

* Deterministic
* Auditable
* Reusable

AI never sees raw DB data — only this blueprint.

---

### 5. Controlled AI Drafting (Human-in-the-Loop)

AI is treated as a **junior drafting clerk**:

Rules enforced via prompt + code:

* Use only provided facts
* Use only provided law
* No invented citations
* Neutral placeholders if data is insufficient

AI output:

* Is **never auto-finalized**
* Always moves draft to `REVIEWED`

---

### 6. Draft Versioning & Audit Trail

Every AI draft is stored as a **versioned DraftContent**:

* v1, v2, v3...
* No overwrites
* Full history preserved

This allows:

* Re-exporting
* Comparison
* Court defensibility

---

### 7. DOCX Export (Lawyer Reality)

Drafts are exported as **court-ready DOCX files**:

* Times New Roman
* 12 pt
* 1.5 spacing
* Editable in MS Word

Export is allowed **only after review**.

---

## 🔌 API Workflow Summary

1. **Create Draft**

   * `POST /api/drafts/create/`

2. **Submit Facts**

   * `POST /api/drafts/{id}/facts/`

3. **Map Law (IPC → BNS)**

   * `POST /api/drafts/{id}/map-law/`

4. **Generate Draft Blueprint**

   * `POST /api/drafts/{id}/generate/`

5. **AI Drafting**

   * `POST /api/drafts/{id}/ai-draft/`

6. **Export DOCX**

   * `POST /api/drafts/{id}/export/`

---

## 📚 RAG (Retrieval-Augmented Generation) — Status

### ✅ Completed

* Judgment model
* JudgmentChunk model
* Section-aware metadata

### 🔜 Upcoming

* Judgment ingestion (PDF/text → chunks)
* Embeddings + vector search
* Section-scoped retrieval
* Citation injection into blueprint

RAG will:

* Retrieve **only relevant case law**
* Be scoped by **mapped BNS sections + intent**
* Never allow AI to invent citations

---

## 🚀 Current MVP Capabilities

✔ Workflow-enforced legal drafting
✔ BNS/BNSS-native reasoning
✔ Anti-hallucination fact intake
✔ Intent-based law mapping
✔ Versioned AI drafts
✔ Court-ready DOCX export

---

## 🧭 Roadmap (Next Extensions)

* 🔎 Full RAG integration (case-law citations)
* 🔐 OTP-based advocate authentication
* 🧩 Court-specific templates
* 🌐 Frontend (Stitch AI)
* ☁️ Production deployment (Postgres + cloud)

---

## 🧑‍⚖️ Final Note

Bhartiya Nyay AI is built with a simple belief:

> **Legal AI must behave like law, not like chat.**

This repository represents a **court-defensible foundation**, not a demo.

---

*This README will be extended as RAG and frontend layers are implemented.*
