# drafting/services.py

from drafting.workflow import DraftStatus, can_transition


class DraftWorkflowError(Exception):
    pass


def transition_draft(draft, next_status: DraftStatus):
    current_status = DraftStatus(draft.status)

    if not can_transition(current_status, next_status):
        raise DraftWorkflowError(
            f"Illegal transition: {current_status.value} → {next_status.value}"
        )

    draft.status = next_status.value
    draft.save()