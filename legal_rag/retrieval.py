# legal_rag/retrieval.py

from legal_rag.models import JudgmentChunk


def retrieve_relevant_chunks(
    *,
    sections,
    intent,
    limit=5
):
    """
    sections: list like ["BNS 318"]
    intent: string describing legal intent
    """

    # Fetch all chunks (safe for SQLite)
    queryset = JudgmentChunk.objects.all()

    matched_chunks = []

    # 1. HARD FILTER — section match (legal gate)
    for chunk in queryset:
        normalized_chunk_sections = [
            s.strip().lower() for s in chunk.relevant_sections
        ]

        normalized_query_sections = [
            s.strip().lower() for s in sections
        ]

        if any(sec in normalized_chunk_sections for sec in normalized_query_sections):
            matched_chunks.append(chunk)

    # 2. RANKING — intent is a booster, not a gate
    scored_chunks = []

    for chunk in matched_chunks:
        score = 1  # section match guarantees base relevance

        if intent and intent.lower() in chunk.legal_issue.lower():
            score += 2

        scored_chunks.append((score, chunk))

    # 3. Sort by relevance score (highest first)
    scored_chunks.sort(key=lambda x: x[0], reverse=True)

    # 4. Return top N chunks only
    return [chunk for _, chunk in scored_chunks[:limit]]


def build_citations(chunks):
    citations = []

    for chunk in chunks:
        judgment = chunk.judgment

        citations.append(
            {
                "case_title": judgment.case_title,
                "court": judgment.court,
                "citation": judgment.citation,
                "holding": chunk.text,
                "relevance": chunk.legal_issue,
            }
        )

    return citations
