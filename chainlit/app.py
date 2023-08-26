import os

from langchain import LLMChain
import chainlit as cl
from langchain.chat_models import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage


system_message = ""
init_messages = [
    SystemMessage(
        content=system_message
    ),
]

cache = dict()

@cl.on_chat_start
def main():
    # Instantiate the chain for that user session
    chat = ChatOpenAI(temperature=0,
                      openai_api_key=os.environ.get('OPENAI_API_KEY'),
                      model='gpt-3.5-turbo'
                     )

    # Store the chain in the user session
    cl.user_session.set("chat", chat)


@cl.on_message
async def main(message: str):
    # Retrieve chain and session id from user_session
    llm_chain = cl.user_session.get("chat")  # type: LLMChain
    session_id = cl.user_session.get("id")
    
    # Initialize the cache
    messages = cache.get(session_id, init_messages)

    human_message = HumanMessage(content=message)
    messages.append(human_message)

    # update cache everytime messages get updated.
    cache[session_id] = messages

    # Call the chain asynchronously
    res = llm_chain(messages, callbacks=[cl.AsyncLangchainCallbackHandler()])  # comment for testing.
    # res = AIMessage(content='hello, this is a dummy reply. I am not hooked up to a LLM yet.')  # uncomment for testing.
    messages.append(res)

    # update cache everytime messages get updated.
    cache[session_id] = messages

    # Do any post processing here
    # TODO - Save chat to DB.

    # Send the response
    await cl.Message(content=res.content).send()  # comment for testing.
    # await cl.Message(content=res).send()  # uncomment for testing.
