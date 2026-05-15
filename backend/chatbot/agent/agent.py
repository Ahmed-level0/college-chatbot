from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import ToolMessage
from langchain_core.tools import tool
from .tools.schedules_tool import get_lectures, get_exams
from .tools.rules_tool import search_rules
from .tools import config

tools = [search_rules, get_lectures, get_exams]

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=config.GOOGLE_API_KEY,
    temperature=0.1
)

llm_with_tools = llm.bind_tools(tools)

conversation_history = []

SYSTEM_PROMPT = """You are a helpful university assistant. You answer questions about:
1. University rules and policies (use search_rules tool)
2. Class schedules, exams, and academic calendar (use get_schedule tool)

Be concise and accurate. Cite page numbers when referencing rules."""

def chat(prompt: str) -> str:
    human_message = HumanMessage(content=prompt)

    messages = [SystemMessage(content=SYSTEM_PROMPT)]
    messages.extend(conversation_history)
    messages.append(human_message)

    # save user message immediately
    conversation_history.append(human_message)

    response = llm_with_tools.invoke(messages)

    while response.tool_calls:
        messages.append(response)
        conversation_history.append(response)

        for tool_call in response.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]

            print(f"🔧 Calling tool: {tool_name}({tool_args})")

            selected_tool = next(t for t in tools if t.name == tool_name)

            tool_result = selected_tool.invoke(tool_args)

            tool_message = ToolMessage(
                content=str(tool_result),
                tool_call_id=tool_call["id"]
            )

            messages.append(tool_message)
            conversation_history.append(tool_message)

        response = llm_with_tools.invoke(messages)

    conversation_history.append(response)

    if len(conversation_history) > 20:
        conversation_history[:] = conversation_history[-20:]
    response = response.content
    if response[0]['text']:
            return response[0]['text']
    else:    
        return response

if __name__ == "__main__":
    print("🎓 University Chatbot")
    print("Type 'exit' to quit\n")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        
        response = chat(user_input)

        if response[0]['text']:
            print(response[0]['text'])
        else:    
            print(f"Bot: {response}\n")