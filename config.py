import os

# Define file paths for persistent storage
CONVERSATION_HISTORY_FILE = 'data/conversation_history.json'
TODO_LIST_FILE = 'data/todo_list.json'

# Ensure the 'data' directory exists when config is loaded
os.makedirs('data', exist_ok=True)
