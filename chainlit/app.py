import os

from datetime import datetime
from langchain import PromptTemplate, OpenAI, LLMChain
import chainlit as cl
from langchain.chat_models import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage


system_message = ""
messages = [
    SystemMessage(
        content=system_message
    ),
]

@cl.on_chat_start
def main():
    # Instantiate the chain for that user session
    chat = ChatOpenAI(temperature=0,
                      openai_api_key=os.environ.get('OPENAI_API_KEY'),
                      model='gpt-3.5-turbo'
                     )
    
    # Session ID
    session_id = datetime.now().strftime('%H%M%S%f')

    # Store the chain in the user session
    cl.user_session.set('session_id', session_id)
    cl.user_session.set("chat", chat)


@cl.on_message
async def main(message: str):
    # Retrieve the chain from the user session
    llm_chain = cl.user_session.get("chat")  # type: LLMChain

    human_message = HumanMessage(content=message)
    messages.append(human_message)

    # Call the chain asynchronously
    res = llm_chain(messages, callbacks=[cl.AsyncLangchainCallbackHandler()])
    messages.append(res)

    # Do any post processing here
    # TODO - Save chat to DB.
    session_id = cl.user_session.get("session_id")

    # Send the response
    await cl.Message(content=res.content).send()
