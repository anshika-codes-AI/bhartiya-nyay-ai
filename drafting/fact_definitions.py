DRAFT_TYPES = {
    "BAIL_BNSS": "Regular Bail Application (BNSS)",
    "NI_138_NOTICE": "Legal Notice under Section 138 NI Act",
}


BAIL_BNSS_FACTS = [
    {
        "key": "FIR_NUMBER",
        "label": "FIR Number",
        "type": "string",
        "required": True,
        "example": "123/2024",
    },
    {
        "key": "POLICE_STATION",
        "label": "Police Station",
        "type": "string",
        "required": True,
        "example": "Kotwali Police Station, Indore",
    },
    {
        "key": "SECTIONS_INVOKED",
        "label": "Sections Invoked (IPC/BNS)",
        "type": "list",
        "required": True,
        "example": ["BNS 318", "BNS 103"],
    },
    {
        "key": "DATE_OF_ARREST",
        "label": "Date of Arrest",
        "type": "date",
        "required": True,
        "example": "2024-11-12",
    },
    {
        "key": "CUSTODY_DURATION_DAYS",
        "label": "Custody Duration (in days)",
        "type": "number",
        "required": True,
        "example": 14,
    },
    {
        "key": "GROUNDS_FOR_BAIL",
        "label": "Grounds for Bail",
        "type": "text",
        "required": True,
        "example": "Investigation complete, no criminal antecedents",
    },
    {
        "key": "CHARGESHEET_FILED",
        "label": "Has chargesheet been filed?",
        "type": "boolean",
        "required": False,
        "example": True,
    },
]

NI_138_FACTS = [
    {
        "key": "CHEQUE_NUMBER",
        "label": "Cheque Number",
        "type": "string",
        "required": True,
        "example": "987654",
    },
    {
        "key": "CHEQUE_AMOUNT",
        "label": "Cheque Amount (INR)",
        "type": "number",
        "required": True,
        "example": 250000,
    },
    {
        "key": "CHEQUE_DATE",
        "label": "Cheque Date",
        "type": "date",
        "required": True,
        "example": "2024-10-01",
    },
    {
        "key": "RETURN_REASON",
        "label": "Reason for Dishonour",
        "type": "string",
        "required": True,
        "example": "Insufficient Funds",
    },
    {
        "key": "NOTICE_DATE",
        "label": "Date of Legal Notice",
        "type": "date",
        "required": True,
        "example": "2024-10-20",
    },
    {
        "key": "DRAWEE_BANK",
        "label": "Drawee Bank",
        "type": "string",
        "required": True,
        "example": "State Bank of India",
    },
]

FACT_SCHEMAS = {
    "BAIL_BNSS": BAIL_BNSS_FACTS,
    "NI_138_NOTICE": NI_138_FACTS,
}