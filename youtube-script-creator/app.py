import os
from pathlib import Path
from typing import Literal

import streamlit as st
from langchain import PromptTemplate
from langchain.chains import LLMChain
from langchain.llms import GPT4All, OpenAIChat
from langchain.llms.base import BaseLLM
from langchain.memory import ConversationBufferMemory
from langchain.utilities import WikipediaAPIWrapper


def pick_model(model_name: Literal["gpt-3.5-turbo", "gpt4all"]) -> BaseLLM:
    """Pick an LLM.

    Note:
        temperature: the higher value, the more random and less deterministic output
    """

    if model_name == "gpt-3.5-turbo":
        api_key = os.environ["OPENAI_API_KEY"]  # you need this for OpenAI
        return OpenAIChat(
            model_name="gpt-3.5-turbo",
            openai_api_key=api_key,
            temperature=0.9,
        )
    if model_name == "gpt4all":
        repo_root = Path(__file__).parent.parent
        models = repo_root / Path("models")
        gpt4all_models = models.glob("*gpt4all*.bin")
        gpt4all_model = next(gpt4all_models)
        return GPT4All(
            model=str(gpt4all_model),
            temp=0.9,
        )

    raise NotImplementedError(f"Model {model_name} not implemented")


llm = pick_model(model_name="gpt-3.5-turbo")

# Streamlit
st.title("YouTube script creator")
st.write(f"Using LLM: {llm.__class__.__name__}")
prompt = st.text_input("Enter a topic for the YouTube video:")


# Prompts
title_template = PromptTemplate(
    input_variables=["topic"],
    template="Write me a YouTube video title about {topic}",
)
script_template = PromptTemplate(
    input_variables=["title", "wikipedia_research"],
    template=(
        "Write me a YouTube video script based on this title: {title} "
        "while leveraging this wikipedia research: {wikipedia_research}"
    ),
)

# Memory
title_memory = ConversationBufferMemory(input_key="topic", memory_key="chat_history")
script_memory = ConversationBufferMemory(input_key="title", memory_key="chat_history")


# Chains
title_chain = LLMChain(
    llm=llm,
    prompt=title_template,
    output_key="title",
    memory=title_memory,
    verbose=True,
)
script_chain = LLMChain(
    llm=llm,
    prompt=script_template,
    output_key="script",
    memory=script_memory,
    verbose=True,
)

# Utilities
wikipedia = WikipediaAPIWrapper()

# Run/display
if prompt:
    title = title_chain.run(prompt)
    wikipedia_research = wikipedia.run(prompt)
    script = script_chain.run(title=title, wikipedia_research=wikipedia_research)

    st.header("Title")
    st.write(title)
    st.header("Script")
    st.write(script)

    st.header("Memory")

    with st.expander("YouTube video title"):
        st.info(title_memory.buffer)

    with st.expander("YouTube video script"):
        st.info(script_memory.buffer)

    with st.expander("Wikipedia reasearch"):
        st.info(wikipedia_research)
