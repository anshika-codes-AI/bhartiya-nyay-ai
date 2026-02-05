# START — Getting Started with Bhartiya Nyay AI

This file is a **quick-start guide** for developers who want to run the MVP locally and understand the workflow in under 15 minutes.

> If you want the *why* and architecture, read **README.md**.
> This file is only about **how to start**.

---

## 0️⃣ Prerequisites

Make sure you have:

* Python **3.10+**
* Git
* pip (comes with Python)

Optional but recommended:

* VS Code
* GitHub Copilot enabled

---

## 1️⃣ Clone the Repository

```bash
git clone <your-repo-url>
cd bhartiya_nyay_ai
```

---

## 2️⃣ Create & Activate Virtual Environment

```bash
python -m venv venv
```

### Activate

**Windows**

```bash
venv\Scripts\activate
```

**macOS / Linux**

```bash
source venv/bin/activate
```

You should now see `(venv)` in your terminal.

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` is not present yet, install manually:

```bash
pip install django djangorestframework python-dotenv python-docx
```

---

## 4️⃣ Environment Setup

Create a `.env` file in the project root:

```env
DJANGO_ENV=development
SECRET_KEY=dev-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

⚠️ Never commit `.env` to GitHub.

---

## 5️⃣ Run Database Migrations

```bash
python manage.py migrate
```

(Optional) Create superuser:

```bash
python manage.py createsuperuser
```

---

## 6️⃣ Start the Development Server

```bash
python manage.py runserver
```

Open browser:

```
http://127.0.0.1:8000/
```

Admin panel:

```
http://127.0.0.1:8000/admin/
```

---

## 7️⃣ Seed Minimal Data (Required Once)

### Draft Types

Add via Django admin or shell:

```bash
python manage.py shell
```

```python
from drafting.models import DraftType

DraftType.objects.get_or_create(
    code="BAIL_BNSS",
    name="Regular Bail Application (BNSS)",
)
```

### Legal Mapping (Example)

```python
from transition_engine.models import LegalSection, SectionMapping

ipc_420 = LegalSection.objects.create(
    act="IPC",
    section_number="420",
    title="Cheating"
)

bns_318 = LegalSection.objects.create(
    act="BNS",
    section_number="318",
    title="Cheating"
)

SectionMapping.objects.create(
    ipc_section=ipc_420,
    bns_section=bns_318,
    intent="Cheating / dishonest inducement",
    drafting_note="Focus on mens rea and inducement"
)
```

Exit shell:

```python
exit()
```

---

## 8️⃣ Core API Flow (Happy Path)

Follow this order **exactly**:

### 1. Create Draft

```
POST /api/drafts/create/
```

### 2. Submit Facts

```
POST /api/drafts/{id}/facts/
```

### 3. Map Law (IPC → BNS)

```
POST /api/drafts/{id}/map-law/
```

### 4. Generate Draft Blueprint

```
POST /api/drafts/{id}/generate/
```

### 5. AI Drafting (Controlled)

```
POST /api/drafts/{id}/ai-draft/
```

### 6. Export DOCX

```
POST /api/drafts/{id}/export/
```

If you skip a step → API will reject it. This is intentional.

---

## 9️⃣ Important Rules (Read This)

* ❌ Do NOT call AI before `DRAFT_GENERATED`
* ❌ Do NOT send free-text facts
* ❌ Do NOT bypass workflow status
* ✅ Always use service functions for transitions

This is **not a CRUD app**.

---

## 🔎 RAG Status

RAG (case-law retrieval) is **partially implemented**:

* ✅ Judgment models
* ✅ Chunk schema
* ⏳ Ingestion pipeline (next)
* ⏳ Retrieval + citation injection

Do not attempt open-ended search yet.

---

## 🆘 Common Issues

### Server won’t start

* Check `.env`
* Ensure virtual environment is active

### Migration errors

* Run `python manage.py makemigrations`
* Commit migrations before pushing

### API returns workflow error

* You are skipping a step (by design)

---

## ✅ You’re Ready

If you reached here:

* Backend is running
* Workflow is enforced
* Drafts can be generated & exported

You now understand **how to run Bhartiya Nyay AI locally**.

---

➡️ Next steps:

* Implement RAG ingestion
* Add frontend
* Deploy to production

Happy building 🚀
