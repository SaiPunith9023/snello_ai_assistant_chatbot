# ✨ Snello AI Assistant: Your Smart To-Do Companion ✨

Welcome to Snello, your personal AI assistant designed to make managing your daily tasks a breeze while engaging in natural conversation! Snello leverages the power of Google's Gemini AI and LangChain to understand your requests, keep track of your to-do list, and remember your conversations.

<img width="972" height="798" alt="Screenshot 2025-07-14 001345" src="https://github.com/user-attachments/assets/7afbece3-779b-42b6-bb79-169eb3975489" />

**Note:** The "Clear Chat" option here is to delete the entire conversation.

## 🌟 Features at a Glance

* **Intelligent Conversation:** Chat naturally with Snello, ask questions, and get helpful responses.

* **Personal To-Do List Management:**

  * **Add Tasks**

  * **View Tasks**

  * **Remove Tasks**

* **Persistent Memory:** Snello remembers your name and your entire conversation history, as well as your to-do list, even after you close the application.

* **Modular & Clean Architecture:** Built with a clear, organized codebase for easy understanding and future expansion.

* **Google Gemini Integration:** Powered by Google's advanced `gemini-2.0-flash` model for intelligent responses.

* **User-Friendly Web Interface (Gradio):** Interact with Snello through a clean and intuitive web-based chat interface with custom avatars.

## 🧠 How It Works: The Brains Behind Snello

Snello is built on a robust **agentic architecture** using the **LangChain** framework. This design allows Snello to not just chat, but also to intelligently decide when to use specific "tools" to perform actions, like managing your to-do list.

### Architecture Flow Description

Imagine Snello's brain as a sophisticated decision-maker:

1.  **User Input:** You type a message into the Gradio web interface.

2.  **Agent Executor (The Orchestrator):** Your message, along with the current conversation history (from Snello's memory), is sent to the `AgentExecutor`. This is the central component that orchestrates the entire process.

3.  **Large Language Model (LLM - The Brain):** The `AgentExecutor` consults the `ChatGoogleGenerativeAI` (powered by `gemini-2.0-flash`). The LLM analyzes your input and the conversation history.

4.  **Tool Selection (Decision Making):** Based on your message, the LLM decides:

    * "Does the user want to chat normally?" (e.g., "How are you?")

    * "Does the user want to perform an action with the to-do list?" (e.g., "Add 'buy milk'"). If an action is needed, it identifies the correct "tool" (e.g., `add_todo_tool`).

5.  **Tool Invocation:** If a tool is selected, the `AgentExecutor` calls that specific tool with the necessary arguments (e.g., `add_todo_tool(task="buy milk")`).

6.  **Tool Execution:** The tool performs its action (e.g., adds "buy milk" to the internal to-do list and saves it to JSON).

7.  **Observation:** The result of the tool's action (e.g., "OK, I've added 'buy milk' to your list.") is sent back to the `AgentExecutor`.

8.  **Final Response Generation:** The `AgentExecutor` feeds the tool's observation (or just the context if no tool was used) back to the LLM. The LLM then formulates a natural, human-friendly response based on the action taken (or the conversation).

9.  **Response to User:** The final response is sent back to the Gradio UI and displayed in the chat.

10. **Memory Update:** Throughout this process, Snello's memory is continuously updated to remember the latest conversation turn and the state of the to-do list.

### How Memory is Stored and Retrieved

Snello uses a custom memory solution to ensure all your interactions and to-do items are saved and loaded persistently:

* **`data_manager.py`:** This file acts as the primary interface for reading from and writing to local JSON files. It contains functions like `load_json_data` and `save_json_data`.

* **`config.py`:** Defines the specific file paths: `data/conversation_history.json` (for chat history) and `data/todo_list.json` (for to-do items). The `data/` directory is automatically created if it doesn't exist.

* **`custom_memory.py`:** This is where the magic happens for conversation history.

    * It defines `CustomJsonConversationMemory`, which inherits from LangChain's `ConversationBufferMemory`.

    * When the application starts, `CustomJsonConversationMemory` calls `load_memory_from_json()`, which in turn uses `data_manager` to load messages from `conversation_history.json` into LangChain's internal memory structure.

    * After every user interaction, the `chatbot_response` function in `gradio_app.py` explicitly calls `memory.save_memory_to_json()`, ensuring the latest conversation is written back to `conversation_history.json`.

* **To-Do List Memory:** The `todo_items` list in `data_manager.py` directly stores the to-do items. Any changes made by the to-do tools (e.g., `add_todo_item`, `remove_todo_item`) trigger `save_all_persistent_data()` in `data_manager.py`, which saves the `todo_items` list to `todo_list.json`.

* **Gradio UI State:** For the Gradio web interface, a `gr.State` component (`chatbot_history_state`) is used to manage the *display* of the chat history, ensuring a smooth, continuous conversation flow in the browser. This state is initialized from the loaded persistent memory.

### How Each Tool Call is Defined and Registered with the LLM

The "tools" are the specific actions Snello can perform. They are defined in `todo_tools.py`:

* **Tool Definition (`todo_tools.py`):**

    * Functions like `add_todo_tool`, `list_todos_tool`, and `remove_todo_tool` are defined.

    * Each function is decorated with `@tool` from `langchain_core.tools`. This decorator automatically converts a Python function into a format that LangChain's LLM can understand and use.

    * Crucially, the **docstring** of each `@tool` function is vital. It acts as the "description" that the LLM reads to understand what the tool does, its arguments, and when to use it. For example, `add_todo_tool`'s docstring tells the LLM it "Adds a task to the user's to-do list" and expects a `task` argument.

* **Tool Registration (`agent_setup.py`):**

    * In `agent_setup.py`, after creating an instance of `UserTodoTools` (which encapsulates the to-do logic), the `tools_from_object()` function from `langchain.tools` is used.

    * `all_tools = tools_from_object(user_todo_tools_instance)` collects all methods decorated with `@tool` from that instance into a list.

    * This `all_tools` list is then passed to `create_tool_calling_agent` and `AgentExecutor`, making these tools available for the LLM to invoke during a conversation.

### Code Structure: A Modular Approach

The project is thoughtfully organized into several Python files, each with a specific role:

* `gradio_app.py`: This is the main entry point for the web interface. It sets up the Gradio UI, manages the chat display, and connects user input to the core chatbot logic.

* `agent_setup.py`: Configures the core LangChain components: the Gemini LLM, the conversation prompt, the agent executor, and the custom memory. This is where Snello's "brain" and "memory" are wired up.

* `todo_tools.py`: Defines the specific Python functions (tools) that allow Snello to manage your to-do list.

* `custom_memory.py`: Implements Snello's custom memory system, ensuring conversation history is loaded from and saved to a JSON file.

* `data_manager.py`: Handles the low-level details of loading and saving data to JSON files, providing persistence for both conversation history and to-do items.

* `config.py`: Stores global configuration variables, primarily the file paths for data storage.

* `.env`: A hidden file that securely stores your Google API key, keeping it out of your main code.

* `requirements.txt`: Lists all the Python libraries needed to run Snello.

## 🚀 Getting Started: Your Snello Journey

Follow these simple steps to get Snello up and running on your local machine!

### Prerequisites

* **Python 3.10 or higher:** Download and install from [python.org](https://www.python.org/).

* **`pip`:** Python's package installer (usually comes with Python).

* **Git:** For cloning the repository. Download from [git-scm.com](https://git-scm.com/downloads).

### Step 1: Get Your Google AI Studio (Gemini) API Key

Snello needs an API key to talk to Google's Gemini models.

1.  Go to <https://aistudio.google.com/>.

2.  Sign in with your Google account.

3.  Generate a new API key.

4.  **Copy this key immediately!** You'll need it in the next step.

### Step 2: Set Up Your Project

1.  **Clone the Repository:**

    ```bash
    git clone [https://github.com/SaiPunith9023/snello_ai_assistant_chatbot.git](https://github.com/SaiPunith9023/snello_ai_assistant_chatbot.git)
    cd snello_ai_assistant_chatbot
    ```

2.  **Create Your `.env` File (Crucial for Security!):**

    * In the root of your `snello_ai_assistant_chatbot` directory, create a new file named `.env` (note the leading dot).

    * Open this `.env` file and add your API key like this, replacing `"your_copied_api_key_here"` with your actual key:

        ```
        GOOGLE_API_KEY="your_copied_api_key_here"
        ```

    * **Save and close** the `.env` file.

    * **Important:** The `.gitignore` file is configured to prevent `.env` from being committed to GitHub, keeping your key secure.

3.  **Install Dependencies:**

    * Open your terminal or VS Code Bash (make sure you're in the `snello_ai_assistant_chatbot` directory).

    * Install all the necessary Python libraries:

        ```bash
        pip install -r requirements.txt
        ```

### Step 3: Run Snello!

Once all dependencies are installed, you can launch Snello's web interface:

1.  In your terminal (still in `snello_ai_assistant_chatbot` directory), run:

    ```bash
    python gradio_app.py
    ```

2.  Gradio will start a local server. You'll see a URL in the terminal output, typically `http://127.0.0.1:7860`.
3.  Open your web browser and navigate to that URL.

You should now see the Snello AI Assistant chat interface with user and AI avatars!

### Quick Start Examples

Try these prompts in the chat:

* `Hi, my name is Alice`

* `Add "buy groceries" to my list.`

* `What's on my to-do list?`

* `Please add "call mom" to my tasks.`

* `Remove "buy groceries" from my list.`

* `How are you?`

* `Do you remember my name?`

**To test persistence:**

1.  Add a few items to your list.

2.  Type `Ctrl+C` in your terminal to stop the `gradio_app.py` server.

3.  Run `python gradio_app.py` again.

4.  Ask `What's on my to-do list?` – Snello should remember your tasks!

## 🚧 Limitations & Future Enhancements

While Snello is quite capable, here are some areas for future growth and potential improvements:

### Current Limitations

* **Single-User Focus:** Currently, Snello is designed for one user at a time. All data (conversation and to-do list) is stored locally in JSON files for that single user.

* **Simple Name Memory Heuristic:** Snello remembers your name based on a simple "my name is" phrase and only stores the first word. It doesn't use more advanced techniques for name entity recognition or dedicated memory slots for user profiles.

* **Basic Error Handling:** While it catches general errors during chat processing, more specific and user-friendly error messages could be added for various tool or API call failures.

* **To-Do Item Nuance:** It treats to-do items as simple strings. It doesn't inherently understand or manage due dates, priorities, recurring tasks, or complex task relationships (e.g., "remind me to call mom tomorrow at 3 PM").

### Ideas for Future Enhancements

* **Full Multi-User Support:** Implement a proper user authentication system and store data in a scalable database (like Firestore, SQLite, or PostgreSQL) to support multiple distinct users with their own private data.

* **Advanced To-Do Features:** Add capabilities for setting due dates, priorities, recurring tasks, or sub-tasks. This would require extending the `todo_tools.py` and potentially the data storage schema.

* **More Tools:** Integrate with external APIs for weather forecasts, calendar events, setting reminders, sending emails, or providing general knowledge answers beyond the scope of the to-do list.

* **Improved Natural Language Understanding:** Enhance the agent's ability to extract entities (dates, times, locations, specific names) from user requests more robustly.

* **Tool Error Feedback:** Provide more specific and helpful responses to the user when a tool fails (e.g., "I couldn't find that task to remove" instead of a generic error).
  
Thank you for exploring the Snello AI Assistant!
