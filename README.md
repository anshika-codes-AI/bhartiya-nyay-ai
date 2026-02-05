# Bhartiya Nyay AI

> **A workflow-first, BNS/BNSS-native Legal Drafting Assistant for Indian Advocates**  
> Built to solve the post-IPC “Year Zero” transition with trust, structure, and auditability.

---

## 🚀 Getting Started

New here?  
👉 Start with [START.md](START.md)

---

## 📌 Project Philosophy

Bhartiya Nyay AI is **not a chatbot**.

It is a **law-governed drafting system** that mirrors how real advocates think and work:

- Facts before drafting  
- Statutory grounding before AI  
- Judicial support before arguments  
- Mandatory human review  
- Court-ready output, not chat text  

Every design decision in this codebase prioritizes:

- ❌ Zero tolerance for hallucinated law  
- 📜 Auditability and traceability  
- ⚖️ Legal discipline over AI creativity  

---

## 🧠 High-Level Architecture
```
User
↓
Draft Creation
↓
Structured Fact Intake (Validated)
↓
IPC → BNS Legal Mapping (Intent-based)
↓
Draft Blueprint Generation (Deterministic)
↓
RAG-Based Judicial Retrieval
↓
Citation-Locked AI Drafting
↓
Mandatory Advocate Review
↓
DOCX Export (Court-Ready)
```

AI is never allowed to operate on raw data or free text.  
All reasoning flows through controlled layers.

---

## 🏗️ Tech Stack

- **Backend:** Django + Django REST Framework  
- **Architecture:** Workflow-gated services (not prompt-first)  
- **AI Layer:** Controlled, LLM-agnostic (OpenAI / Gemini pluggable)  
- **RAG:** Section-scoped, intent-aware retrieval  
- **Docs Export:** `python-docx`  
- **Database:** SQLite (development) → PostgreSQL (production-ready)  

---

## 📂 Project Structure
```
bhartiya_nyay_ai/
├── users/ # Advocate identity (custom user model)
├── drafting/ # Core drafting workflow
│ ├── models.py
│ ├── workflow.py
│ ├── services.py
│ ├── fact_definitions.py
│ ├── draft_blueprint.py
│ ├── ai_prompts.py
│ ├── ai_drafting.py
│ ├── docx_export.py
│ ├── views.py
│ └── urls.py
├── transition_engine/ # IPC → BNS / BNSS mapping logic
│ ├── models.py
│ └── services.py
├── legal_rag/ # Judicial RAG system
│ ├── models.py
│ ├── ingestion.py
│ ├── retrieval.py
│ └── admin.py
├── manage.py
└── README.md
```

---

## 🔐 Core Design Principles

### 1. Workflow First (Not Chat First)

No legal step can be skipped.

Draft lifecycle is strictly enforced:
```
CREATED
→ FACTS_COLLECTED
→ LEGAL_MAPPED
→ DRAFT_GENERATED
→ REVIEWED
→ EXPORTED
```

All transitions are validated centrally.

---

### 2. Structured Fact Intake (Anti-Hallucination Layer)

Facts are **schema-driven**, not free text.

Each draft type defines:
- Allowed fact keys  
- Required vs optional fields  
- Expected data types  

Example (BNSS Bail):
- FIR_NUMBER (string)  
- DATE_OF_ARREST (date)  
- CUSTODY_DURATION_DAYS (number)  
- SECTIONS_INVOKED (list)  

Invalid or missing facts block progression.

---

### 3. Legal Mapping Engine (IPC → BNS)

Mapping is not numeric substitution.

Each mapping stores:
- IPC Section  
- Corresponding BNS Section  
- Legal intent  
- Drafting notes  

Mapped law becomes the **immutable legal basis** for drafting.

---

### 4. Draft Blueprint (AI-Free Core)

Before AI is ever invoked, the system builds a deterministic **Draft Blueprint**:

```json
{
  "draft_type": "BAIL_BNSS",
  "facts": {...},
  "legal_basis": [...],
  "citations": [...],
  "sections": {
    "facts": true,
    "grounds": true,
    "prayer": true
  }
}
```

This blueprint is:

* Predictable

* Auditable

* Reusable

AI never accesses raw database records.
---
### 5. RAG (Retrieval-Augmented Generation)

Judicial precedents are retrieved using a law-scoped RAG system:

* Judgments are ingested and chunked

* Each chunk carries section + intent metadata

* Retrieval is scoped by mapped BNS sections

* Ranking is intent-aware

If no relevant precedent exists, the system explicitly records this.
---

### 6. Citation-Locked AI Drafting (Human-in-the-Loop)

AI behaves like a junior drafting clerk, not an authority.

Strict rules enforced:

* Use only provided facts

* Use only mapped law

* Cite only retrieved judgments

* Never invent or recall case law

If citations are empty, AI must clearly state so.

AI output:

* Is versioned

* Is never auto-finalized

* Always requires advocate review
---

### 7. Draft Versioning & Audit Trail

Every AI-generated draft is stored as a version:

* v1, v2, v3…

* No overwriting

* Full history preserved

This enables auditability and court defensibility.
---

### 8. DOCX Export (Lawyer Reality)

Final drafts are exported as court-ready DOCX files:

* Times New Roman

* 12 pt font

* 1.5 line spacing

* Fully editable

Export is allowed only after review.
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
## 🚀 Current MVP Capabilities

* ✔ Workflow-enforced legal drafting
* ✔ BNS/BNSS-native statutory reasoning
* ✔ Anti-hallucination fact intake
* ✔ Intent-based IPC → BNS mapping
* ✔ RAG-backed judicial citations
* ✔ Citation-locked AI drafting
* ✔ Versioned drafts
* ✔ Court-ready DOCX export

## 🧭 Roadmap

* 🎨 Frontend (Stitch AI)

* ☁️ Production deployment (PostgreSQL + cloud)

* 🔐 OTP-based advocate authentication

* 📚 Expanded judgment corpus

* 🧩 Court-specific drafting templates

## 🧑‍⚖️ Final Note

Bhartiya Nyay AI is built on one principle:

> **Legal AI must behave like law, not like chat.**

This repository represents a **court-defensible MVP foundation**, not a demo.

This README will continue to evolve as frontend and deployment layers are added.