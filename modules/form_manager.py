from modules.sql_agent import run_sql_action
from modules.validators import extract_info, get_required_fields

conversation_state = {
    'policy_lookup': {
        'required': ['name', 'dob', 'email', 'address'],
        'optional': ['policy_number'],
        'collected': {}
    }
}

def handle_structured_intent(user_input, history):
    state = conversation_state['policy_lookup']
    extracted = extract_info(user_input)
    state['collected'].update(extracted)

    missing = [field for field in state['required'] if field not in state['collected']]

    if missing:
        return f"I need a bit more info: please provide your {', '.join(missing)}."

    return run_sql_action(state['collected'])
