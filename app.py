from agent_setup import agent_executor, memory # Import the agent and memory
from data_manager import save_all_persistent_data # Import save function for robustness
# IMPORTANT: Add imports for HumanMessage and AIMessage
from langchain_core.messages import HumanMessage, AIMessage

# --- Main Chat Loop (Command Line Interface) ---
def chat_loop():
    """
    Main loop for the command-line interface of the chatbot.
    Handles user input, agent invocation, and persistence.
    """
    print("Welcome to the Snello Chatbot! Type 'exit' to quit.")
    
    # Attempt to remember user's name from previous conversation history
    user_name = None 
    # The memory has already been loaded from JSON upon initialization in custom_memory.py
    for msg in memory.chat_memory.messages:
        # Now HumanMessage is defined because it's imported
        if isinstance(msg, HumanMessage) and "my name is" in msg.content.lower():
            parts = msg.content.lower().split("my name is", 1)
            if len(parts) > 1:
                name_candidate = parts[1].strip().split(' ')[0].replace('.', '').replace('!', '')
                if name_candidate:
                    user_name = name_candidate.capitalize()
                    print(f"Remembered user name from history: {user_name}")
                    break 

    # Greet the user, using their remembered name if available
    if user_name:
        print(f"Hello, {user_name}! What can I help you with today?")
    else:
        print("What can I help you with today?")

    # Start the continuous chat loop
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            # Save all data before exiting to ensure persistence
            save_all_persistent_data() # Saves todo_items
            memory.save_memory_to_json() # Saves conversation_history
            print("Goodbye!")
            break

        # Simple name recognition for the current session if name wasn't found in history
        if not user_name and "my name is" in user_input.lower():
            parts = user_input.lower().split("my name is", 1)
            if len(parts) > 1:
                name_candidate = parts[1].strip().split(' ')[0].replace('.', '').replace('!', '')
                if name_candidate:
                    user_name = name_candidate.capitalize()
                    print(f"Acknowledged your name: {user_name}")

        try:
            # Invoke the agent executor with the user's input.
            # The agent_executor automatically manages memory updates internally,
            # and tool calls will trigger saving of the todo list.
            response = agent_executor.invoke({"input": user_input})
            agent_response_content = response['output']
            
            print(f"Agent: {agent_response_content}")
            
        except Exception as e:
            print(f"An error occurred: {e}")
            print("Please try again.")

# Entry point for the script
if __name__ == "__main__":
    chat_loop()