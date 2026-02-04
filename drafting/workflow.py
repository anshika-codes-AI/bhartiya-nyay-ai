# drafting/workflow.py

from enum import Enum


class DraftStatus(Enum):
    CREATED = "CREATED"
    FACTS_COLLECTED = "FACTS_COLLECTED"
    LEGAL_MAPPED = "LEGAL_MAPPED"
    DRAFT_GENERATED = "DRAFT_GENERATED"
    REVIEWED = "REVIEWED"
    EXPORTED = "EXPORTED"

   
ALLOWED_TRANSITIONS = {
    DraftStatus.CREATED: [DraftStatus.FACTS_COLLECTED],
    DraftStatus.FACTS_COLLECTED: [DraftStatus.LEGAL_MAPPED],
    DraftStatus.LEGAL_MAPPED: [DraftStatus.DRAFT_GENERATED],
    DraftStatus.DRAFT_GENERATED: [DraftStatus.REVIEWED],
    DraftStatus.REVIEWED: [DraftStatus.EXPORTED],
}

# drafting/workflow.py (continued)

def can_transition(current_status: DraftStatus, next_status: DraftStatus) -> bool:
    return next_status in ALLOWED_TRANSITIONS.get(current_status, [])