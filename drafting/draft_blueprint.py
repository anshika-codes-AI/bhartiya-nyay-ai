from legal_rag.retrieval import retrieve_relevant_chunks, build_citations

def build_draft_blueprint(draft):
    facts = {f.key: f.value for f in draft.facts.all()}

    legal_basis = [
        {
            "ipc": str(m.ipc_section),
            "bns": str(m.bns_section),
            "intent": m.intent,
            "drafting_note": m.drafting_note,
        }
        for m in draft.legal_mappings.all()
    ]

    # 🔎 RAG: retrieve citations per mapped section
    all_sections = [
        str(m.bns_section) for m in draft.legal_mappings.all()
    ]

    intent = (
        draft.legal_mappings.first().intent
        if draft.legal_mappings.exists()
        else ""
    )

    chunks = retrieve_relevant_chunks(
        sections=all_sections,
        intent=intent,
    )

    citations = build_citations(chunks)

    blueprint = {
        "draft_type": draft.draft_type.code,
        "title": draft.title,
        "facts": facts,
        "legal_basis": legal_basis,
        "citations": citations,   # 👈 RAG injected here
        "sections": {
            "cause_title": True,
            "facts_section": True,
            "grounds_section": True,
            "prayer_section": True,
        },
    }

    return blueprint
