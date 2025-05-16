import gradio as gr
from modules.form_manager import handle_form
from modules.intent_guide import detect_intent

session_id = "demo"

def chatbot(user_input):
    intent = detect_intent(user_input)
    if intent == "unknown":
        return "Can you clarify what you'd like help with?"
    elif intent == "out_of_scope":
        return "I'm here to help with The Hartford's auto insurance. Would you like to ask about coverage, purchase a policy, or file a claim?"
    return handle_form(session_id, intent, user_input)

iface = gr.ChatInterface(fn=chatbot, title="Buck - Auto Insurance Assistant")
iface.launch()
