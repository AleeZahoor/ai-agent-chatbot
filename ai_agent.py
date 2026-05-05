from dotenv import load_dotenv
load_dotenv()

import os
from langchain_groq import ChatGroq

from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

def get_response_from_ai_agent(llm_id, query, allow_search, system_prompt, provider):
    """
    Get response from AI agent with search capability
    """
    try:
        # Initialize LLM based on provider
        if provider == "Groq":
            llm = ChatGroq(model=llm_id, temperature=0.7)
       # elif provider == "OpenAI":
           # llm = ChatOpenAI(model=llm_id, temperature=0.7)
        else:
            return f"Error: Unknown provider '{provider}'"

        # Setup search tool if allowed
        tools = []
        if allow_search:
            tools = [TavilySearchResults(max_results=2)]

        # Create messages
        messages = []
        if system_prompt:
            messages.append(SystemMessage(content=system_prompt))
        
        # Add user query
        if isinstance(query, list):
            messages.extend(query)
        else:
            messages.append(HumanMessage(content=query))

        # Create and run agent
        agent = create_react_agent(
            model=llm,
            tools=tools
        )
        
        # Invoke agent
        response = agent.invoke({"messages": messages})
        
        # Extract AI response
        for msg in reversed(response["messages"]):
            if isinstance(msg, AIMessage) and msg.content:
                return msg.content
        
        return "Sorry, I couldn't generate a response."
    
    except Exception as e:
        return f"Error: {str(e)}"
