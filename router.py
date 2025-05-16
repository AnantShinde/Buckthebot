from modules.rag_module import handle_rag_query
from modules.form_manager import handle_structured_intent
from modules.validators import is_structured_request, is_out_of_domain

def route_message(user_input, history):
    if is_out_of_domain(user_input):
        return "I'm here to help with The Hartford insurance questions. Could you ask something insurance-related?"

    if is_structured_request(user_input):
        return handle_structured_intent(user_input, history)

    return handle_rag_query(user_input)
