import gradio as gr
from router import route_message

chat_history = []

with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    msg = gr.Textbox(label="Ask Buck a question about your insurance")

    def respond(user_input):
        global chat_history
        response = route_message(user_input, chat_history)
        chat_history.append((user_input, response))
        return chat_history

    msg.submit(respond, inputs=msg, outputs=chatbot)

demo.launch()
