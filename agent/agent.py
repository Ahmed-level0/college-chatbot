from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import tool
import config
from rules_tool import search_rules
from schedules_tool import get_lectures, get_exams

# Tools
tools = [search_rules, get_lectures, get_exams]

# Gemini with tool calling
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=config.GOOGLE_API_KEY,
    temperature=0.1
)

# Bind tools to the model
llm_with_tools = llm.bind_tools(tools)

# Simple conversation memory (just a list)
conversation_history = []

SYSTEM_PROMPT = """You are a helpful university assistant. You answer questions about:
1. University rules and policies (use search_rules tool)
2. Class schedules, exams, and academic calendar (use get_schedule tool)

Be concise and accurate. Cite page numbers when referencing rules."""

def chat(message: str) -> str:
    # Build messages
    messages = [SystemMessage(content=SYSTEM_PROMPT)]
    messages.extend(conversation_history)
    messages.append(HumanMessage(content=message))
    
    # Get response from LLM (may include tool calls)
    response = llm_with_tools.invoke(messages)
    
    # Handle tool calls
    while response.tool_calls:
        # Add assistant's tool request to history
        messages.append(response)
        conversation_history.append(response)
        
        # Execute each tool
        for tool_call in response.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            
            print(f"  🔧 Calling tool: {tool_name}({tool_args})")
            
            # Find and execute the tool
            selected_tool = next(t for t in tools if t.name == tool_name)
            tool_result = selected_tool.invoke(tool_args)
            
            # Add tool result to messages
            from langchain_core.messages import ToolMessage
            messages.append(ToolMessage(
                content=tool_result,
                tool_call_id=tool_call["id"]
            ))
        
        # Get final response after tool results
        response = llm_with_tools.invoke(messages)
    
    # Add final response to history
    conversation_history.append(HumanMessage(content=message))
    conversation_history.append(response)
    
    # Keep history manageable (last 10 exchanges)
    if len(conversation_history) > 20:
        conversation_history[:] = conversation_history[-20:]
    
    return response.content

if __name__ == "__main__":
    print("🎓 University Chatbot")
    print("Type 'exit' to quit\n")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        
        response = chat(user_input)
        print(f"Bot: {response}\n")