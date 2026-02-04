from drafting.workflow import DraftStatus
from drafting.services import transition_draft
from drafting.draft_blueprint import build_draft_blueprint


class DraftGenerationError(Exception):
    pass


def generate_draft_blueprint(draft):
    if draft.status != DraftStatus.LEGAL_MAPPED.value:
        raise DraftGenerationError(
            "Draft is not ready for generation"
        )

    blueprint = build_draft_blueprint(draft)

    # IMPORTANT: no AI call here yet

    transition_draft(draft, DraftStatus.DRAFT_GENERATED)

    return blueprint