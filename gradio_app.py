import gradio as gr
import os
from dotenv import load_dotenv

# Import your modular files
from data_manager import load_all_persistent_data, save_all_persistent_data, conversation_history_data
from agent_setup import agent_executor, memory
from langchain_core.messages import HumanMessage, AIMessage

# Load environment variables (ensures GOOGLE_API_KEY is available)
load_dotenv()

# --- Initial Setup for the Gradio App (Single User) ---
load_all_persistent_data()

WEB_USER_NAME = None
for msg_dict in conversation_history_data:
    if msg_dict.get("role") == "user" and "my name is" in msg_dict.get("content", "").lower():
        parts = msg_dict["content"].lower().split("my name is", 1)
        if len(parts) > 1:
            name_candidate = parts[1].strip().split(' ')[0].replace('.', '').replace('!', '')
            if name_candidate:
                WEB_USER_NAME = name_candidate.capitalize()
                print(f"Gradio App: Remembered user name from history: {WEB_USER_NAME}")
                break

# Define the custom introduction message for the chatbot
CHAT_INTRO_MESSAGE = """
Hello there! I'm Snello, your personal AI assistant designed to help you manage your daily tasks and have a friendly chat.

**What I can do:**
* **Remember our conversations:** I'll recall what we've talked about, including your name!
* **Manage your to-do list:** Just tell me to add, list, or remove tasks.

Give it a try! You can start by telling me your name, asking me how I am, or diving straight into your to-do list.
"""

# Prepare initial messages for the Gradio Chatbot component.
initial_messages_for_display = []

if not memory.chat_memory.messages:
    initial_messages_for_display.append({"role": "assistant", "content": CHAT_INTRO_MESSAGE})
else:
    for msg in memory.chat_memory.messages:
        if isinstance(msg, HumanMessage):
            initial_messages_for_display.append({"role": "user", "content": msg.content})
        elif isinstance(msg, AIMessage):
            initial_messages_for_display.append({"role": "assistant", "content": msg.content})


# --- Chatbot Logic for Gradio ---
def chatbot_response(message: str, history_state: list) -> tuple:
    """
    Processes a user message and returns the chatbot's response, updating the history state.
    """
    global WEB_USER_NAME

    print(f"User message: {message}")

    if not WEB_USER_NAME and "my name is" in message.lower():
        parts = message.lower().split("my name is", 1)
        if len(parts) > 1:
            name_candidate = parts[1].strip().split(' ')[0].replace('.', '').replace('!', '')
            if name_candidate:
                WEB_USER_NAME = name_candidate.capitalize()
                print(f"Gradio App: Acknowledged user name: {WEB_USER_NAME}")

    try:
        response_dict = agent_executor.invoke({"input": message})
        agent_response_content = response_dict['output']
        
        save_all_persistent_data()
        memory.save_memory_to_json()

        print(f"Agent response: {agent_response_content}")
        
        current_history = history_state
        current_history.append({"role": "user", "content": message})
        current_history.append({"role": "assistant", "content": agent_response_content})
        
        return current_history, current_history, "" 

    except Exception as e:
        print(f"Error during chat processing: {e}")
        error_message = f"Oops! An error occurred: {e}. Please try again."
        
        current_history = history_state
        current_history.append({"role": "user", "content": message})
        current_history.append({"role": "assistant", "content": error_message})
        
        return current_history, current_history, ""

# --- Gradio Interface Setup ---
# Custom CSS to hide the unwanted elements
custom_css = """
/* Hide the default clear button (dustbin icon) in the chatbot header */
.gradio-container .gr-chatbot .clear-button {
    display: none !important;
}
/* Hide the "Built with Gradio" footer */
.gradio-container footer {
    display: none !important;
}
/* Hide the "Use via API" link/button and any other header buttons (like settings/share) */
.gradio-container .gr-header-buttons,
.gradio-container .gr-button.gr-button-sm { /* Target small buttons which might be API/Share */
    display: none !important;
}
"""

with gr.Blocks(theme="soft", title="Snello AI Assistant", css=custom_css) as demo:
    # Main headings at the top, outside the chat area
    gr.Markdown("# ✨ Snello AI Assistant ✨")
    gr.Markdown("Your personal chatbot for conversations and managing your to-do list.")

    chatbot_history_state = gr.State(value=initial_messages_for_display)

    user_avatar = "https://placehold.co/100x100/ADD8E6/000000?text=User"
    agent_avatar = "https://placehold.co/100x100/90EE90/000000?text=AI"

    # The actual chatbot display component, with no separate label (as the main heading is above)
    chatbot = gr.Chatbot(
        height=400,
        show_label=False, # Hides the default label area where the icon might be
        type='messages',
        value=initial_messages_for_display,
        avatar_images=(user_avatar, agent_avatar),
        show_copy_button=False # Keeps individual message icons off
    )

    # Use a gr.Row to neatly arrange the input textbox and send button
    with gr.Row():
        msg = gr.Textbox(placeholder="Type your message here...", container=False, scale=7)
        send_btn = gr.Button("Send", scale=1)

    # Clear Chat button below the input row
    def clear_chat_interface():
        memory.clear()
        cleared_display = [{"role": "assistant", "content": CHAT_INTRO_MESSAGE}]
        return cleared_display, cleared_display, "" 

    clear_btn = gr.Button("Clear Chat")
    clear_btn.click(clear_chat_interface, outputs=[chatbot, chatbot_history_state, msg])

    # Define the interaction flow
    msg.submit(chatbot_response, inputs=[msg, chatbot_history_state], outputs=[chatbot, chatbot_history_state, msg])
    send_btn.click(chatbot_response, inputs=[msg, chatbot_history_state], outputs=[chatbot, chatbot_history_state, msg])


if __name__ == '__main__':
    # Removed show_api, show_share_button, show_footer as they cause TypeError
    # Relying on CSS for hiding these elements.
    demo.launch(share=False, debug=True)
