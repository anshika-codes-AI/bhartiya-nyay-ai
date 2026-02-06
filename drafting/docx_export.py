from docx import Document
from pathlib import Path
from drafting.workflow import DraftStatus
from drafting.services import transition_draft


class DocxExportError(Exception):
    pass


def export_draft_to_docx(draft, draft_text):
    if draft.status != DraftStatus.REVIEWED.value:
        raise DocxExportError("Draft not ready for export")

    BASE_DIR = Path(__file__).resolve().parent.parent.parent

    template_path = BASE_DIR / "bhartiya_nyay_ai" / "drafting" / "templates" / "bail_template.docx"

    if not template_path.exists():
        raise DocxExportError(f"Template not found at {template_path}")

    document = Document(template_path)

    for paragraph in document.paragraphs:
        if "{{CONTENT}}" in paragraph.text:
            paragraph.text = paragraph.text.replace("{{CONTENT}}", draft_text)

    export_dir = BASE_DIR / "bhartiya_nyay_ai" / "drafting" / "exports"
    export_dir.mkdir(exist_ok=True)

    output_path = export_dir / f"draft_{draft.id}.docx"
    document.save(output_path)

    transition_draft(draft, DraftStatus.EXPORTED)

    return output_path
