
from langchain.agents import AgentExecutor, create_react_agent
from langchain import hub
import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain.tools import Tool
from langchain.chains.conversation.memory import ConversationBufferWindowMemory

load_dotenv()

llm = ChatOpenAI(
    openai_api_key=input("Enter API Key: "),
    model="gpt-3.5-turbo",
)

tools = [
    Tool.from_function(
        name="General Chat",
        description="For general chat not covered by other tools",
        func=llm.invoke,
        return_direct=True
    )
]



memory = ConversationBufferWindowMemory(
    memory_key='chat_history',
    k=5,
    return_messages=True,
)

agent_prompt = hub.pull("hwchase17/react-chat")
agent = create_react_agent(llm, tools, agent_prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    memory=memory,
    verbose=True
)

def generate_response(prompt):
    """
    Create a handler that calls the Conversational agent
    and returns a response to be rendered in the UI
    """

    response = agent_executor.invoke({"input": prompt})

    return response['output']

generate_response(input("Write: "))