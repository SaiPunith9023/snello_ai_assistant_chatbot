from langchain_core.tools import tool
from data_manager import todo_items, save_all_persistent_data

# --- To-Do List Core Functions ---
# These functions directly modify/read the 'todo_items' list.

def add_todo_item(task: str) -> str:
    """Adds a task to the user's to-do list."""
    # todo_items is a mutable list, so appending modifies the global object directly.
    todo_items.append(task)
    save_all_persistent_data() # Save immediately after modification
    return f"Got it! I've added '{task}' to your to-do list."

def get_todo_list() -> str:
    """Retrieves and displays the user's current to-do list."""
    if not todo_items:
        return "Your to-do list is currently empty."
    
    numbered_list = "\n".join([f"{i+1}. {item}" for i, item in enumerate(todo_items)])
    return f"Here's your current to-do list:\n{numbered_list}"

def remove_todo_item(task: str) -> str:
    """
    Removes a specified task from the to-do list.
    The task must match exactly (case-insensitive for better UX).
    """
    # Declare todo_items as global *before* any usage within this function
    # because we are reassigning the list itself (todo_items = [...])
    global todo_items 
    
    original_length = len(todo_items)
    
    # Create a new list excluding the task to be removed (case-insensitive comparison)
    # Reassigning todo_items to this new list updates the global reference.
    todo_items = [item for item in todo_items if item.lower() != task.lower()] 
    
    if len(todo_items) < original_length:
        save_all_persistent_data() # Save immediately after modification
        return f"Great! I've removed '{task}' from your list."
    else:
        return f"Couldn't find '{task}' in your to-do list. Please make sure the task matches exactly."

# --- LangChain Tools ---
# These functions wrap the core logic and expose them as tools for the LLM.
# The @tool decorator and docstrings are crucial for the LLM's understanding.

@tool
def add_todo_tool(task: str) -> str:
    """Adds a task to the user's to-do list.
    Args:
        task (str): The description of the task to add.
    """
    return add_todo_item(task)

@tool
def list_todos_tool() -> str:
    """Retrieves and displays the user's current to-do list.
    Args:
        None
    """
    return get_todo_list()

@tool
def remove_todo_tool(task: str) -> str:
    """Removes a specified task from the to-do list. The task must match exactly.
    Args:
        task (str): The description of the task to remove.
    """
    return remove_todo_item(task)

# List of all tools to be exposed to the LangChain agent
all_tools = [add_todo_tool, list_todos_tool, remove_todo_tool]
