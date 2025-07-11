import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from todo_tools import all_tools # Import the list of tools
from custom_memory import CustomJsonConversationMemory # Import your custom memory class

# Load environment variables (ensures GOOGLE_API_KEY is available)
load_dotenv()

# Check if the Google API key is set
if "GOOGLE_API_KEY" not in os.environ:
    raise ValueError(
        "GOOGLE_API_KEY environment variable not set. "
        "Please set it as described in the instructions (Step 1) "
        "or ensure your .env file is correctly configured (Step 4)."
    )

# 1. Initialize the LLM (Gemini-Pro model)
# IMPORTANT CHANGE: Updated model name to 'gemini-2.0-flash' based on your guide's curl command.
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.7) # Changed model name

# 2. Initialize the custom memory, linking it to the "chat_history" input key for the agent
memory = CustomJsonConversationMemory(memory_key="chat_history")

# 3. Create the Prompt Template for the Agent
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI assistant named Snello. You remember the user's name and previous conversations. You can help manage a personal to-do list using the provided tools. If the user mentions their name, try to remember it for future interactions. Always be polite and concise."),
    MessagesPlaceholder(variable_name="chat_history"), # Existing chat history
    ("human", "{input}"),                             # Current user input
    MessagesPlaceholder(variable_name="agent_scratchpad"), # Agent's internal thought process and tool outputs
])

# 4. Create the Agent
agent = create_tool_calling_agent(llm, all_tools, prompt)

# 5. Create the Agent Executor
agent_executor = AgentExecutor(agent=agent, tools=all_tools, memory=memory, verbose=True)

# You can now import 'agent_executor' and 'memory' from this file in app.py
