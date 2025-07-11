# import gradio as gr
# import os
# from dotenv import load_dotenv

# # Import your modular files
# from data_manager import load_all_persistent_data, save_all_persistent_data, conversation_history_data
# from agent_setup import agent_executor, memory
# from langchain_core.messages import HumanMessage, AIMessage

# # Load environment variables (ensures GOOGLE_API_KEY is available)
# load_dotenv()

# # --- Initial Setup for the Gradio App (Single User) ---
# load_all_persistent_data()

# WEB_USER_NAME = None
# for msg_dict in conversation_history_data:
#     if msg_dict.get("role") == "user" and "my name is" in msg_dict.get("content", "").lower():
#         parts = msg_dict["content"].lower().split("my name is", 1)
#         if len(parts) > 1:
#             name_candidate = parts[1].strip().split(' ')[0].replace('.', '').replace('!', '')
#             if name_candidate:
#                 WEB_USER_NAME = name_candidate.capitalize()
#                 print(f"Gradio App: Remembered user name from history: {WEB_USER_NAME}")
#                 break

# # Prepare initial messages for the Gradio Chatbot component.
# initial_messages_for_display = []
# if memory.chat_memory.messages:
#     for msg in memory.chat_memory.messages:
#         if isinstance(msg, HumanMessage):
#             initial_messages_for_display.append({"role": "user", "content": msg.content})
#         elif isinstance(msg, AIMessage):
#             initial_messages_for_display.append({"role": "assistant", "content": msg.content})
# else:
#     initial_greeting_content = "Welcome to the Snello Chatbot! How can I help you today?"
#     if WEB_USER_NAME:
#         initial_greeting_content = f"Hello {WEB_USER_NAME}! How can I help you today?"
#     initial_messages_for_display.append({"role": "assistant", "content": initial_greeting_content})


# # --- Chatbot Logic for Gradio ---
# # The 'history' argument will now be a gr.State object
# def chatbot_response(message: str, history_state: list) -> tuple:
#     """
#     Processes a user message and returns the chatbot's response, updating the history state.
#     """
#     global WEB_USER_NAME

#     print(f"User message: {message}")

#     if not WEB_USER_NAME and "my name is" in message.lower():
#         parts = message.lower().split("my name is", 1)
#         if len(parts) > 1:
#             name_candidate = parts[1].strip().split(' ')[0].replace('.', '').replace('!', '')
#             if name_candidate:
#                 WEB_USER_NAME = name_candidate.capitalize()
#                 print(f"Gradio App: Acknowledged user name: {WEB_USER_NAME}")

#     try:
#         response_dict = agent_executor.invoke({"input": message})
#         agent_response_content = response_dict['output']
        
#         save_all_persistent_data()
#         memory.save_memory_to_json()

#         print(f"Agent response: {agent_response_content}")
        
#         current_history = history_state
#         current_history.append({"role": "user", "content": message})
#         current_history.append({"role": "assistant", "content": agent_response_content})
        
#         # IMPORTANT CHANGE: Return 3 values:
#         # 1. Updated history for the gr.Chatbot display component
#         # 2. Updated history for the gr.State component
#         # 3. Empty string to clear the gr.Textbox
#         return current_history, current_history, "" 

#     except Exception as e:
#         print(f"Error during chat processing: {e}")
#         error_message = f"Oops! An error occurred: {e}. Please try again."
        
#         current_history = history_state
#         current_history.append({"role": "user", "content": message}) # Add user message even on error
#         current_history.append({"role": "assistant", "content": error_message})
        
#         # IMPORTANT CHANGE: Return 3 values even on error
#         return current_history, current_history, ""

# # --- Gradio Interface Setup ---
# with gr.Blocks(theme="soft", title="Snello AI Assistant") as demo:
#     gr.Markdown("# Snello AI Assistant")
#     gr.Markdown("Your personal chatbot for conversations and managing your to-do list.")

#     chatbot_history_state = gr.State(value=initial_messages_for_display)

#     chatbot = gr.Chatbot(
#         height=400,
#         label="Snello Chatbot",
#         type='messages',
#         value=initial_messages_for_display
#     )

#     msg = gr.Textbox(placeholder="Type your message here...", container=False, scale=7)
#     send_btn = gr.Button("Send")

#     def clear_chat_interface():
#         memory.clear() # Clear LangChain's memory and JSON file
#         # Return empty list for chatbot, empty list for history state, and empty string for textbox
#         return [], [], "" 

#     clear_btn = gr.Button("Clear Chat")
#     # IMPORTANT CHANGE: Added msg as an output for clear_btn to clear the textbox
#     clear_btn.click(clear_chat_interface, outputs=[chatbot, chatbot_history_state, msg])


#     # Define the interaction flow
#     # When the send button is clicked or enter is pressed in the textbox:
#     # 1. Call chatbot_response with the message and the current history state.
#     # 2. Update the chatbot display and the history state.
#     # 3. Clear the message textbox.
#     msg.submit(chatbot_response, inputs=[msg, chatbot_history_state], outputs=[chatbot, chatbot_history_state, msg])
#     send_btn.click(chatbot_response, inputs=[msg, chatbot_history_state], outputs=[chatbot, chatbot_history_state, msg])


# if __name__ == '__main__':
#     demo.launch(share=False, debug=True)
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

# Prepare initial messages for the Gradio Chatbot component.
initial_messages_for_display = []
if memory.chat_memory.messages:
    for msg in memory.chat_memory.messages:
        if isinstance(msg, HumanMessage):
            initial_messages_for_display.append({"role": "user", "content": msg.content})
        elif isinstance(msg, AIMessage):
            initial_messages_for_display.append({"role": "assistant", "content": msg.content})
else:
    initial_greeting_content = "Welcome to the Snello Chatbot! How can I help you today?"
    if WEB_USER_NAME:
        initial_greeting_content = f"Hello {WEB_USER_NAME}! How can I help you today?"
    initial_messages_for_display.append({"role": "assistant", "content": initial_greeting_content})


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
# No custom CSS needed if show_label=False handles it
# custom_css = """
# .gradio-container .gr-chatbot .clear-button {
#     display: none !important;
# }
# """

with gr.Blocks(theme="soft", title="Snello AI Assistant") as demo: # Removed css=custom_css
    gr.Markdown("# Snello AI Assistant")
    gr.Markdown("Your personal chatbot for conversations and managing your to-do list.")

    chatbot_history_state = gr.State(value=initial_messages_for_display)

    user_avatar = "https://placehold.co/100x100/ADD8E6/000000?text=User"
    agent_avatar = "https://placehold.co/100x100/90EE90/000000?text=AI"

    gr.Markdown("### Snello Chatbot") # Manually add the label
    chatbot = gr.Chatbot(
        height=400,
        # IMPORTANT CHANGE: Set show_label=False to hide the default header and its clear icon
        show_label=False,
        type='messages',
        value=initial_messages_for_display,
        avatar_images=(user_avatar, agent_avatar),
        show_copy_button=False # Keeps individual message icons off
    )

    msg = gr.Textbox(placeholder="Type your message here...", container=False, scale=7)
    send_btn = gr.Button("Send")

    def clear_chat_interface():
        memory.clear()
        return [], [], "" 

    # Keep the explicit Clear Chat button
    clear_btn = gr.Button("Clear Chat")
    clear_btn.click(clear_chat_interface, outputs=[chatbot, chatbot_history_state, msg])


    msg.submit(chatbot_response, inputs=[msg, chatbot_history_state], outputs=[chatbot, chatbot_history_state, msg])
    send_btn.click(chatbot_response, inputs=[msg, chatbot_history_state], outputs=[chatbot, chatbot_history_state, msg])


if __name__ == '__main__':
    demo.launch(share=False, debug=True)
