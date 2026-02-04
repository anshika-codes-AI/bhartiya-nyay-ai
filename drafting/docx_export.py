from docx import Document
from drafting.workflow import DraftStatus
from drafting.services import transition_draft
import os


class DocxExportError(Exception):
    pass


def export_draft_to_docx(draft, draft_text):
    if draft.status != DraftStatus.REVIEWED.value:
        raise DocxExportError("Draft not ready for export")

    template_path = "drafting/templates/bail_template.docx"

    if not os.path.exists(template_path):
        raise DocxExportError("DOCX template not found")

    document = Document(template_path)

    for paragraph in document.paragraphs:
        if "{{CONTENT}}" in paragraph.text:
            paragraph.text = paragraph.text.replace(
                "{{CONTENT}}", draft_text
            )

    output_path = f"drafting/exports/draft_{draft.id}.docx"
    os.makedirs("drafting/exports", exist_ok=True)
    document.save(output_path)

    transition_draft(draft, DraftStatus.EXPORTED)

    return output_path