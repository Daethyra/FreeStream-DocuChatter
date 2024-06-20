import datetime
import os

import streamlit as st
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_anthropic import ChatAnthropic
from langchain_community.chat_message_histories import \
    StreamlitChatMessageHistory
from langchain_openai import ChatOpenAI
from pages import (PrintRetrievalHandler, RetrieveDocuments, StreamHandler,
                   footer, save_conversation_history, set_bg_local, set_llm)

# Initialize LangSmith tracing
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "FreeStream-v4.0.0"
os.environ["LANGCHAIN_ENDPOINT"] = st.secrets.LANGCHAIN.LANGCHAIN_ENDPOINT
os.environ["LANGCHAIN_API_KEY"] = st.secrets.LANGCHAIN.LANGCHAIN_API_KEY

# Set up page config
st.set_page_config(page_title="FreeStream: RAGbot", page_icon="🤖")
st.title("🤖RAGbot")
st.header(":green[_Retrieval Augmented Generation Chatbot_]", divider="red")
st.caption(":violet[_Ask Your Documents Questions_]")
# Show footer
st.markdown(footer, unsafe_allow_html=True)

# Add sidebar
st.sidebar.subheader("__User Panel__")

# Get an OpenAI API Key before continuing
if "openai_api_key" in st.secrets.OPENAI:
    openai_api_key = st.secrets.OPENAI.openai_api_key
else:
    openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")

# Get an Anthropic API Key before continuing
if "anthropic_api_key" in st.secrets.ANTHROPIC:
    anthropic_api_key = st.secrets.ANTHROPIC.anthropic_api_key
else:
    anthropic_api_key = st.sidebar.text_input("Anthropic API Key", type="password")

# Ensure at least one model is accessible
if not "openai_api_key" in st.secrets and not "openai_api_key" in st.secrets.OPENAI and not "anthropic_api_key" in st.secrets and not "anthropic_api_key" in st.secrets.ANTHROPIC:
    st.error(
        body="""You must set at least one API key before you may continue.""",
        icon="🚨",
    )

# Add file-upload button
uploaded_files = st.sidebar.file_uploader(
    label="Upload a PDF or text file",
    type=["pdf", "doc", "docx", "txt"],
    help="Types supported: pdf, doc, docx, txt \n\nConsider the size of your files before you upload. Processing speed varies by server load.",
    accept_multiple_files=True,
)
if not uploaded_files:
    st.info("Please upload documents to continue.")
    st.stop()

retriever = RetrieveDocuments().configure_retriever(uploaded_files)

# Add temperature header
temperature_header = st.sidebar.markdown(
    """
    ## Temperature Slider
    """
)
# Add the sidebar temperature slider
temperature_slider = st.sidebar.slider(
    label=""":orange[Set LLM Temperature]. The :blue[lower] the temperature, the :blue[less] random the model will be. The :blue[higher] the temperature, the :blue[more] random the model will be.""",
    min_value=0.0,
    max_value=1.0,
    value=0.0,
    step=0.05,
    key="llm_temperature",
)

# Setup memory for contextual conversation
msgs = StreamlitChatMessageHistory()
memory = ConversationBufferMemory(
    memory_key="chat_history", chat_memory=msgs, return_messages=True
)

# Button to clear conversation history
if st.sidebar.button("Clear message history", use_container_width=True):
    msgs.clear()

# Create dictionaries with keys to chat model classes
openai_models = {
    "GPT-3.5 Turbo": ChatOpenAI(  # Define a dictionary entry for the "ChatOpenAI GPT-3.5 Turbo" model
        model="gpt-3.5-turbo",  # Set the OpenAI model name
        openai_api_key=st.secrets.OPENAI.openai_api_key,  # Set the OpenAI API key from the Streamlit secrets manager
        temperature=temperature_slider,  # Set the temperature for the model's responses using the sidebar slider
        streaming=True,  # Enable streaming responses for the model
        max_tokens=4096,  # Set the maximum number of tokens for the model's responses
        max_retries=1,  # Set the maximum number of retries for the model
    ),
    "GPT-4o": ChatOpenAI(
       model="gpt-4o",
       openai_api_key=st.secrets.OPENAI.openai_api_key,
       temperature=temperature_slider,
       streaming=True,
       max_tokens=4096,
       max_retries=1,
    )
}

anthropic_models = {
    "Claude: Haiku": ChatAnthropic(
        model="claude-3-haiku-20240307",
        anthropic_api_key=st.secrets.ANTHROPIC.anthropic_api_key,
        temperature=temperature_slider,
        streaming=True,
        max_tokens=4096,
    ),
    "Claude: Sonnet": ChatAnthropic(
        model="claude-3-sonnet-20240229",
        anthropic_api_key=st.secrets.ANTHROPIC.anthropic_api_key,
        temperature=temperature_slider,
        streaming=True,
        max_tokens=4096,
    ),
    "Claude: Opus": ChatAnthropic(
        model="claude-3-opus-20240229",
        anthropic_api_key=st.secrets.ANTHROPIC.anthropic_api_key,
        temperature=temperature_slider,
        streaming=True,
        max_tokens=4096,
    ),
}

# Master dictionary
model_names = {}

# Update model master dictionary based on present API keys
if "openai_api_key" in st.secrets or "openai_api_key" in st.secrets.OPENAI:
    model_names.update(openai_models)
if "anthropic_api_key" in st.secrets or "anthropic_api_key" in st.secrets.ANTHROPIC:
    model_names.update(anthropic_models)

# Create a dropdown menu for selecting a chat model
selected_model = st.selectbox(
    label="Choose your chat model:",  # Set the label for the dropdown menu
    options=list(model_names.keys()),  # Set the available model options
    key="model_selector",  # Set a unique key for the dropdown menu
    on_change=lambda: set_llm(
        st.session_state.model_selector, model_names
    ),  # Set the callback function
)

# Load the selected model dynamically
llm = model_names[
    selected_model
]  # Get the selected model from the `model_names` dictionary

# Create a chain that ties everything together
qa_chain = ConversationalRetrievalChain.from_llm(
    llm, retriever=retriever, memory=memory, verbose=True
)

# Display coversation history window
avatars = {"human": "user", "ai": "assistant"}
for msg in msgs.messages:
    st.chat_message(avatars[msg.type]).write(msg.content)

# Save the formatted conversation history to a variable
formatted_history = save_conversation_history(msgs.messages)
current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
# Create a sidebar button to download the conversation history
st.sidebar.download_button(
    label="Download conversation history",
    data=formatted_history,
    file_name=f"conversation_history {current_time}.txt",
    mime="text/plain",
    key="download_conversation_history_button",
    help="Download the conversation history as a text file with some formatting.",
    use_container_width=True,   
)

## Create an on/off switch for the GIF background
st.sidebar.divider()
# Define a GIF toggle
gif_bg = st.sidebar.toggle(
    label="Rain Background",
    value=False,
    key="gif_background",
    help="Turn on an experimental background.",
)
if gif_bg:
    set_bg_local("assets/62.gif")

# Display user input field and enter button
if user_query := st.chat_input(placeholder="Ask me about your documents!"):
    st.chat_message("user").write(user_query)

    # Display assistant response
    with st.chat_message("assistant"):
        retrieval_handler = PrintRetrievalHandler(st.container())
        stream_handler = StreamHandler(st.empty())
        response = qa_chain.run(
            user_query, callbacks=[retrieval_handler, stream_handler]
        )

