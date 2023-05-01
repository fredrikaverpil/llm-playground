import os
from pathlib import Path

import streamlit as st
from langchain import PromptTemplate
from langchain.chains import LLMChain
from langchain.llms import GPT4All, OpenAIChat
from langchain.memory import ConversationBufferMemory
from langchain.utilities import WikipediaAPIWrapper

# Streamlit
st.title("YouTube script creator")
prompt = st.text_input("Enter a prompt")

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

# LLM
# temperature: the higher value, the more random and less deterministic output
gpt4all_models = Path(".").glob("*gpt4all*.bin")
if gpt4all_models:
    gpt4all_model = next(gpt4all_models)
    llm = GPT4All(model=str(gpt4all_model), temp=0.9)
else:
    api_key = os.environ["OPENAI_API_KEY"]  # you need this for OpenAI
    llm = OpenAIChat(model_name="gpt-3.5-turbo", temperature=0.9)

st.write(f"Using LLM: {llm.__class__.__name__}")

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

    st.write(title)
    st.write(script)

    with st.expander("YouTube video title"):
        st.info(title_memory.buffer)

    with st.expander("YouTube video script"):
        st.info(script_memory.buffer)

    with st.expander("Wikipedia reasearch"):
        st.info(wikipedia_research)
