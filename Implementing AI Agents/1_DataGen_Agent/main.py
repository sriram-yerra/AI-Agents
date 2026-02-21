from typing import List
from dotenv import load_dotenv
import os

from langchain_google_vertexai import ChatVertexAI
from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langgraph.prebuilt import create_react_agent

load_dotenv("../.env")

# -------------------------
# TOOLS
# -------------------------
from tools import (
    write_json,
    read_json,
    generate_sample_users,
    show_users_table,
    update_user_by_name
)

TOOLS = [
    write_json,
    read_json,
    generate_sample_users,
    show_users_table,
    update_user_by_name
]

# -------------------------
# GEMINI LLM
# -------------------------
llm = ChatVertexAI(
    model_name=os.getenv("GEMINI_MODEL"),
    project=os.getenv("GOOGLE_CLOUD_PROJECT"),
    location=os.getenv("GOOGLE_CLOUD_REGION"),
    temperature=float(os.getenv("TEMPERATURE")),
    max_output_tokens=int(os.getenv("MAX_OUTPUT_TOKENS")),
)

# -------------------------
# SYSTEM PROMPT
# -------------------------
SYSTEM_MESSAGE = (
    "You are DataGen, an autonomous data generation and management agent.\n\n"

    "Your responsibilities include:\n"
    "1. Generating realistic sample user data\n"
    "2. Saving user data to JSON files\n"
    "3. Displaying user data in table format\n"
    "4. Updating user records\n\n"

    "-----------------------------\n"
    "USER GENERATION RULES:\n"
    "-----------------------------\n"
    "To generate users you need:\n"
    "- first_names (list)\n"
    "- last_names (list)\n"
    "- domains (list)\n"
    "- min_age (int)\n"
    "- max_age (int)\n\n"

    "STRICT RULES:\n"
    "1. NEVER ask the user for these values\n"
    "2. ALWAYS create reasonable defaults yourself\n"
    "3. ALWAYS call the tool `generate_sample_users`\n"
    "4. If user says 'save', call `write_json` immediately after generating users\n"
    "5. If user input is vague like 'hi', 'hello', or 'generate users', still generate users\n\n"

    "-----------------------------\n"
    "TABLE DISPLAY RULES:\n"
    "-----------------------------\n"
    "If the user asks to:\n"
    "- 'show users'\n"
    "- 'display table'\n"
    "- 'view users'\n"
    "Then call the tool `show_users_table` with the file path.\n\n"
    '''If the user says "show", "display", or "list users", 
    you MUST call show_table tool.

    Do NOT ask for file path.
    Always use default users.json file.

    If file is empty, suggest generating users.'''

    "-----------------------------\n"
    "UPDATE USER RULES:\n"
    "-----------------------------\n"
    "If the user asks to update user data:\n"
    "1. Ask for the FULL NAME of the user\n"
    "2. Ask which field to update (age, email, domain, etc)\n"
    "3. Ask the new value\n"
    "4. Then call `update_user_by_name`\n\n"

    "-----------------------------\n"
    "GENERAL BEHAVIOR:\n"
    "-----------------------------\n"
    "- Be proactive\n"
    "- Do NOT ask unnecessary questions\n"
    "- Always prefer tool usage over plain text\n"
    "- Always return clean, structured responses\n"
)

# -------------------------
# AGENT
# -------------------------
agent = create_react_agent(llm, TOOLS, prompt=SYSTEM_MESSAGE)

# -------------------------
# RUNNER
# -------------------------
def run_agent(user_input: str, history: List[BaseMessage]) -> AIMessage:
    try:
        result = agent.invoke(
            {"messages": history + [HumanMessage(content=user_input)]},
            config={"recursion_limit": 50}
        )
        return result["messages"][-1]

    except Exception as e:
        return AIMessage(
            content=f"Error: {str(e)}\n\nPlease try rephrasing your request."
        )

# -------------------------
# CLI LOOP
# -------------------------
if __name__ == "__main__":
    print("=" * 60)
    print("DataGen Agent - Sample Data Generator (Gemini Vertex AI)")
    print("=" * 60)

    history: List[BaseMessage] = []

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in ['quit', 'exit', 'q', ""]:
            print("Goodbye!")
            break

        print("Agent: ", end="", flush=True)
        response = run_agent(user_input, history)

        print(response.content)
        print()

        history += [HumanMessage(content=user_input), response]
