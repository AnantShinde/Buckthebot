
from intent_guide import get_required_fields, get_optional_fields
from sql_agent import run_sql_action

# Tracks user input during conversation
user_sessions = {}

def handle_form(session_id, intent, user_input):
    session = user_sessions.setdefault(session_id, {"intent": intent, "fields": {}})

    # Extract key-value from input (simulate NLP step)
    key, value = parse_field(user_input, intent)
    if key:
        session["fields"][key] = value

    required = get_required_fields(intent)
    missing = [field for field in required if field not in session["fields"]]

    if missing:
        return f"Please provide: {', '.join(missing)}"

    # Enough data, perform action
    result = run_sql_action(session["fields"], action_type=intent)
    user_sessions.pop(session_id, None)  # reset session
    return result

def parse_field(user_input, intent):
    user_input = user_input.lower()
    words = user_input.split()

    # Simple keyword-based field parser (extend with LLM/NLP later)
    for word in words:
        if "name" in user_input:
            return "name", user_input.split("is")[-1].strip().title()
        if "email" in user_input and "@" in user_input:
            return "email", user_input.split()[-1]
        if "address" in user_input:
            return "address", user_input.split("address")[-1].strip().strip(":")
        if "phone" in user_input or "number" in user_input:
            return "phone", "".join(filter(str.isdigit, user_input))
        if "dob" in user_input or "birth" in user_input:
            return "dob", user_input.split()[-1]
        if "vehicle" in user_input:
            return "vehicle", user_input.split("vehicle")[-1].strip()
        if "date" in user_input:
            return "date", user_input.split("on")[-1].strip()
        if "location" in user_input:
            return "location", user_input.split("in")[-1].strip()
        if "update" in user_input and ("address" in user_input or "phone" in user_input):
            return "field_to_update", "address" if "address" in user_input else "phone"
        if "new" in user_input:
            return "new_value", user_input.split("new")[-1].strip()

    return None, None
