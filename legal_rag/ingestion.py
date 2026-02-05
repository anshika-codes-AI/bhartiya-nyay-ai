from legal_rag.models import Judgment, JudgmentChunk


def ingest_judgment(
    *,
    court,
    case_title,
    citation,
    judgment_date,
    acts,
    sections,
    chunks,
    source_url=None,
):
    """
    chunks: list of dicts
    [
        {
            "text": "...",
            "relevant_sections": ["BNS 318"],
            "legal_issue": "Bail in cheating cases"
        }
    ]
    """

    judgment, created = Judgment.objects.get_or_create(
        citation=citation,
        defaults={
            "court": court,
            "case_title": case_title,
            "judgment_date": judgment_date,
            "acts": acts,
            "sections": sections,
            "source_url": source_url or "",
        },
    )

    if not created:
        raise ValueError("Judgment already exists")

    for chunk in chunks:
        JudgmentChunk.objects.create(
            judgment=judgment,
            text=chunk["text"],
            relevant_sections=chunk["relevant_sections"],
            legal_issue=chunk["legal_issue"],
        )

    return judgment
