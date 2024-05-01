import datetime
import os

import streamlit as st
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_anthropic import ChatAnthropic
from langchain_community.chat_message_histories import \
    StreamlitChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
from pages import (PrintRetrievalHandler, RetrieveDocuments, StreamHandler,
                   footer, save_conversation_history, set_bg_local, set_llm)

# Initialize LangSmith tracing
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "FreeStream-v4.0.0"
os.environ["LANGCHAIN_ENDPOINT"] = st.secrets.LANGCHAIN.LANGCHAIN_ENDPOINT
os.environ["LANGCHAIN_API_KEY"] = st.secrets.LANGCHAIN.LANGCHAIN_API_KEY

# Set up page config
st.set_page_config(page_title="FreeStream: Chatbot", page_icon="💬")
st.title("💬Chatbot")
st.header(":green[_General Use Chatbot_]", divider="red")
# Show footer
st.markdown(footer, unsafe_allow_html=True)

# Add sidebar
st.sidebar.subheader("__User Panel__")

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
    value=0.4,
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

# Create a dictionary with keys to chat model classes
model_names = {
    "GPT-3.5 Turbo": ChatOpenAI(  # Define a dictionary entry for the "ChatOpenAI GPT-3.5 Turbo" model
        model="gpt-3.5-turbo-0125",  # Set the OpenAI model name
        openai_api_key=st.secrets.OPENAI.openai_api_key,  # Set the OpenAI API key from the Streamlit secrets manager
        temperature=temperature_slider,  # Set the temperature for the model's responses using the sidebar slider
        streaming=True,  # Enable streaming responses for the model
        max_tokens=4096,  # Set the maximum number of tokens for the model's responses
        max_retries=1,  # Set the maximum number of retries for the model
    ),
    "GPT-4 Turbo": ChatOpenAI(
       model="gpt-4-0125-preview",
       openai_api_key=st.secrets.OPENAI.openai_api_key,
       temperature=temperature_slider,
       streaming=True,
       max_tokens=4096,
       max_retries=1,
    ),
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

# Define the prompt template
prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a friendly AI chatbot designed to assist users in comprehending reality, exploring their curiosity, and practicing critical thinking skills. Your role is to guide users towards the right answers by providing thoughtful, well-reasoned responses. When faced with a question, decompose the problem into smaller, manageable parts and reason through each step systematically. This approach will help you provide comprehensive and accurate answers. Remember, your goal is to enhance learning and understanding, so only provide direct advice when explicitly asked to do so. Always strive to provide responses that are relevant, accurate, and contextually appropriate.""",
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{question}"),
    ]
)

# Create a chain that ties everything together
chain = prompt_template | llm
chain_with_history = RunnableWithMessageHistory(
    runnable=chain,
    get_session_history=lambda session_id: msgs,
    input_messages_key="question",
    history_messages_key="chat_history",
)

# Display coversation history window
avatars = {"human": "user", "ai": "assistant"}
for msg in msgs.messages:
    st.chat_message(avatars[msg.type]).write(msg.content)

# Display user input field and enter button
if user_query := st.chat_input(placeholder="What's on your mind?"):
    st.chat_message("user").write(user_query)

    # Display assistant response
    # Using a `with` block instantly displays the response without having to `st.write` it
    with st.chat_message("assistant"):
        stream_handler = StreamHandler(st.empty())
        response = chain_with_history.invoke(
            {"question": user_query},
            config={
                "configurable": {"session_id": "any"},
                "callbacks": [stream_handler],
            },
        )

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