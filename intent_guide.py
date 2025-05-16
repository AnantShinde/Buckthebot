
# intent_guide.py

AUTO_INSURANCE_INTENTS = {
    "inquire": {
        "keywords": ["coverage", "deductible", "comprehensive", "liability", "premium"],
        "type": "rag",
        "response": "Let me check that for you..."
    },
    "purchase": {
        "keywords": ["buy", "quote", "new policy", "start coverage", "get insured"],
        "type": "structured",
        "required_fields": ["name", "dob", "address", "vehicle_make", "vehicle_model", "vehicle_year"],
        "optional_fields": ["email", "phone"]
    },
    "update_info": {
        "keywords": ["change address", "update email", "new phone", "correct my info"],
        "type": "structured",
        "required_fields": ["name", "dob", "email", "field_to_update"],
    },
    "file_claim": {
        "keywords": ["accident", "file claim", "report damage", "submit claim"],
        "type": "structured",
        "required_fields": ["name", "dob", "email", "phone", "vehicle", "date", "location"],
        "optional_fields": ["policy_number", "police_report"]
    }
}

OUT_OF_SCOPE_KEYWORDS = ["adhd", "depression", "therapy", "mental health", "anxiety", "medication"]

def detect_intent(user_input):
    lower_input = user_input.lower()
    for intent, config in AUTO_INSURANCE_INTENTS.items():
        for keyword in config.get("keywords", []):
            if keyword in lower_input:
                return intent
    if any(word in lower_input for word in OUT_OF_SCOPE_KEYWORDS):
        return "out_of_scope"
    return "unknown"

def get_required_fields(intent):
    return AUTO_INSURANCE_INTENTS.get(intent, {}).get("required_fields", [])

def get_optional_fields(intent):
    return AUTO_INSURANCE_INTENTS.get(intent, {}).get("optional_fields", [])

def is_supported_intent(intent):
    return intent in AUTO_INSURANCE_INTENTS
