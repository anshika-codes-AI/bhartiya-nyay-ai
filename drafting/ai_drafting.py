
from drafting.workflow import DraftStatus
from drafting.services import transition_draft
from drafting.ai_prompts import DRAFTING_SYSTEM_PROMPT



def build_ai_prompt(blueprint):
    citations = blueprint.get("citations", [])

    user_prompt = f"""
DRAFT TYPE:
{blueprint["draft_type"]}

FACTS:
{blueprint["facts"]}

LEGAL BASIS:
{blueprint["legal_basis"]}

CITATIONS (USE ONLY THESE):
{citations}

INSTRUCTIONS:
- Draft the document sections requested.
- Follow the STRICT RULES.
"""

    return [
        {"role": "system", "content": DRAFTING_SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]

def assert_citation_safety(blueprint):
    if not blueprint.get("citations"):
        return "NO_CITATIONS"
    return "CITATIONS_AVAILABLE"

# placeholder LLM call (we'll plug real one later)
def call_llm(system_prompt, user_payload):
    """
    TEMPORARY MOCK.
    Replace with OpenAI / Gemini later.
    """
    return f"""
CAUSE TITLE:
In the matter of bail application...

FACTS:
1. FIR No: {user_payload['facts'].get('FIR_NUMBER', '[Not Provided]')}

GROUNDS:
The applicant submits that...

PRAYER:
It is therefore prayed that...
"""


class AIDraftingError(Exception):
    pass


def generate_ai_draft(draft, blueprint):
    if draft.status != DraftStatus.DRAFT_GENERATED.value:
        raise AIDraftingError("Draft not ready for AI drafting")

    ai_output = call_llm(
        system_prompt=DRAFTING_SYSTEM_PROMPT,
        user_payload=blueprint
    )

    # IMPORTANT: we do NOT auto-accept AI output
    transition_draft(draft, DraftStatus.REVIEWED)

    return ai_output