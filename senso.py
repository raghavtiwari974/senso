from openai import OpenAI
import gradio as gr
key ="your_api_key"

gemini_model = OpenAI(
    api_key=key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# myprompt = input("enter your prompte here: ")
def lovegurullm(myprompt):
    mymsg = [
    {"role": "system", "content": "I am your Friend!!" },
    {"role": "user", "content": myprompt }
    ]

    response = gemini_model.chat.completions.create(model="gemini-2.5-flash", messages = mymsg)

    return(response.choices[0].message.content)
myadvice = lovegurullm("i am not feeling good")

myadvice

CUSTOM_CSS = """
body {background:#fff0f5;}
.gr-button-primary,
button.gr-button-primary {background:#ff69b4;border-color:#ff69b4;}
.gr-chatbot .message.user   {background:#ffe4e6;}
.gr-chatbot .message.bot    {background:#fff;}
"""

def user_submit(user_msg, chat_hist):
    chat_hist = chat_hist or []
    chat_hist.append((user_msg, None))
    return "", chat_hist

def bot_reply(chat_hist):
    user_msg = chat_hist[-1][0]
    answer   = lovegurullm(user_msg)           # <— your LLM function
    chat_hist[-1] = (user_msg, answer)
    return chat_hist

with gr.Blocks(theme=gr.themes.Soft(), css=CUSTOM_CSS) as demo:
    gr.Markdown(
        "<h1 style='text-align:center;'>How are You Dear 😊!!</h1>"
        "<p style='text-align:center;'>Share your feelings — with Senso..❤️</p>"
    )

    chatbox = gr.Chatbot(height=450)
    msg     = gr.Textbox(
        placeholder="How's your Mood Today?",
        show_label=False,
        container=False
    )
    with gr.Row():
        send_btn  = gr.Button("Send 💬", variant="primary")
        clear_btn = gr.Button("🗑️ Clear")

    # interactions
    msg.submit(user_submit,  [msg, chatbox], [msg, chatbox], queue=False) \
       .then(bot_reply, chatbox, chatbox)
    send_btn.click(user_submit,  [msg, chatbox], [msg, chatbox], queue=False) \
            .then(bot_reply, chatbox, chatbox)
    clear_btn.click(lambda: [], None, chatbox, queue=False)

    gr.Markdown(
        "<div style='text-align:center;font-size:0.9em;'>@Made with Senso❤️</div>"
    )

demo.launch()

