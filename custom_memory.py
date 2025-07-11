from langchain.memory import ConversationBufferMemory
from langchain_core.messages import HumanMessage, AIMessage
from data_manager import conversation_history_data, save_json_data
from config import CONVERSATION_HISTORY_FILE # This is already imported and available

class CustomJsonConversationMemory(ConversationBufferMemory):
    """
    Custom memory class that loads and saves conversation history from/to a JSON file.
    This ensures chat history persists across sessions.
    """
    def __init__(self, **kwargs):
        # Initialize the base ConversationBufferMemory with return_messages=True
        super().__init__(return_messages=True, **kwargs)
        # Removed: self.json_filepath = CONVERSATION_HISTORY_FILE
        # We will directly use CONVERSATION_HISTORY_FILE imported from config.py
        self.load_memory_from_json() # Load history when memory is initialized

    def load_memory_from_json(self):
        """
        Loads messages from the global conversation_history_data (which is loaded from JSON)
        into the LangChain memory.
        """
        # conversation_history_data is a global list updated by data_manager.py
        # no need to pass CONVERSATION_HISTORY_FILE here, it's handled by data_manager
        
        # Convert stored dictionary representations to LangChain message objects
        loaded_messages = []
        for msg in conversation_history_data:
            if msg.get("role") == "user":
                loaded_messages.append(HumanMessage(content=msg.get("content")))
            elif msg.get("role") == "assistant":
                loaded_messages.append(AIMessage(content=msg.get("content")))
        
        # Set the messages in the underlying chat memory
        self.chat_memory.messages = loaded_messages
        print(f"Loaded {len(loaded_messages)} messages from JSON history into memory.")

    def save_memory_to_json(self):
        """Saves current memory messages from LangChain to the JSON file."""
        global conversation_history_data
        conversation_history_data = [] # Clear current in-memory data before populating
        
        # Convert LangChain message objects back to dictionary representations for JSON
        for msg in self.chat_memory.messages:
            if isinstance(msg, HumanMessage):
                conversation_history_data.append({"role": "user", "content": msg.content})
            elif isinstance(msg, AIMessage):
                conversation_history_data.append({"role": "assistant", "content": msg.content})
        
        # Use CONVERSATION_HISTORY_FILE directly from config.py
        save_json_data(CONVERSATION_HISTORY_FILE, conversation_history_data)
        print("Saved current conversation history from memory to JSON.")

    def clear(self):
        """Clears memory and also the JSON file for conversation history."""
        super().clear() # Clear LangChain's internal memory
        global conversation_history_data
        conversation_history_data = [] # Clear global variable
        # Use CONVERSATION_HISTORY_FILE directly from config.py
        save_json_data(CONVERSATION_HISTORY_FILE, []) # Clear the file
        print("Conversation history cleared from memory and JSON.")
