import json
import os
from config import CONVERSATION_HISTORY_FILE, TODO_LIST_FILE

# Global variables to hold the in-memory state
conversation_history_data = []
todo_items = []

def load_json_data(filepath, default_value):
    """
    Loads data from a JSON file.
    Returns default_value if the file doesn't exist, is empty, or invalid JSON.
    """
    if not os.path.exists(filepath) or os.path.getsize(filepath) == 0:
        return default_value
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Warning: Could not decode JSON from {filepath}. Returning default value.")
        return default_value
    except Exception as e:
        print(f"An unexpected error occurred while loading {filepath}: {e}")
        return default_value

def save_json_data(filepath, data):
    """Saves data to a JSON file."""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        # print(f"Data saved to {filepath}.") # Uncomment for verbose saving
    except Exception as e:
        print(f"Error saving data to {filepath}: {e}")

def load_all_persistent_data():
    """Loads all persistent data from files into global variables."""
    global conversation_history_data, todo_items
    conversation_history_data = load_json_data(CONVERSATION_HISTORY_FILE, [])
    todo_items = load_json_data(TODO_LIST_FILE, [])
    print("Persistent data loaded.")

def save_all_persistent_data():
    """Saves all current global data to files."""
    save_json_data(CONVERSATION_HISTORY_FILE, conversation_history_data)
    save_json_data(TODO_LIST_FILE, todo_items)
    print("Persistent data saved.")

# Load data immediately when this module is imported
load_all_persistent_data()
