def build_draft_blueprint(draft):
    """
    Returns a structured blueprint for drafting.
    NO AI. NO TEXT GENERATION.
    """

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

    blueprint = {
        "draft_type": draft.draft_type.code,
        "title": draft.title,
        "facts": facts,
        "legal_basis": legal_basis,
        "sections": {
            "cause_title": True,
            "facts_section": True,
            "grounds_section": True,
            "prayer_section": True,
        }
    }

    return blueprint