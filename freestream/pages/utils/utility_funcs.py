import base64
import datetime
import logging
import os
import sys
import tempfile
from typing import Any, List

import streamlit as st
import torch
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.chat_message_histories import \
    StreamlitChatMessageHistory
from langchain_community.document_loaders import UnstructuredFileLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.callbacks.base import BaseCallbackHandler
from langchain_core.documents import Document
from PIL import Image

# Set up logging
logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)


class RetrieveDocuments:
    """
    A class for retrieving and managing documents for processing.

    This class is responsible for loading documents from uploaded files, splitting them into chunks,
    generating embeddings for these chunks, and configuring a retriever for efficient document retrieval.

    Attributes:
        uploaded_files (list): A list of uploaded files to be processed.
        docs (list): A list of documents loaded from the uploaded files.
        temp_dir (TemporaryDirectory): A temporary directory for storing uploaded files.
        text_splitter (RecursiveCharacterTextSplitter): An instance of a text splitter for dividing documents into chunks.
        vectordb (FAISS): A vector database for storing embeddings and facilitating document retrieval.
        retriever (Retriever): A configured retriever for retrieving documents based on embeddings.
        embeddings (HuggingFaceEmbeddings): An instance for generating embeddings for document chunks.
    """

    def __init__(self):
        """
        Initialize the RetrieveDocuments class with a list of uploaded files.

        Args:
            uploaded_files (list): A list of uploaded files to be processed.
        """
        self.docs = []
        self.temp_dir = tempfile.TemporaryDirectory()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2500, chunk_overlap=50
        )
        self.embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2",
            model_kwargs={"device": "cuda" if torch.cuda.is_available() else "cpu"},
        )

    @st.cache_resource(ttl="1h")
    def configure_retriever(_self, uploaded_files: List[Document]):
        """
        Configure the retriever by creating a vector database from the provided chunks and embeddings.

        This method first splits the loaded documents into chunks using the text splitter.
        It then generates embeddings for these chunks and creates a vector database (FAISS)
        from these chunks and embeddings.
        Finally, it configures a retriever using the vector database and returns the
        configured retriever.

        Returns:
            Retriever: A configured retriever for retrieving documents based on embeddings.
        """

        # Read documents
        docs = _self.docs
        temp_dir = _self.temp_dir
        for file in uploaded_files:
            temp_filepath = os.path.join(temp_dir.name, file.name)
            with open(temp_filepath, "wb") as f:
                f.write(file.getvalue())
            loader = UnstructuredFileLoader(temp_filepath)
            docs.extend(loader.load())
            logger.info("Loaded document: %s", file.name)

        # Split documents
        text_splitter = _self.text_splitter
        chunks = text_splitter.split_documents(docs)

        vectordb = FAISS.from_documents(chunks, _self.embeddings)

        # Define retriever
        retriever = vectordb.as_retriever(
            search_type="mmr", search_kwargs={"k": 5, "fetch_k": 13, "lambda_mult": 0.5}
        )

        return retriever


# Define a callback function for selecting a model
def set_llm(selected_model: str, model_names: dict):
    """
    Sets the large language model (LLM) in the session state based on the user's selection.
    Also, displays an alert based on the selected model.
    """
    try:
        # Set the model in session state
        st.session_state.llm = model_names[selected_model]

        # Show an alert based on what model was selected
        st.success(body=f"Switched to {selected_model}!", icon="✅")

    except Exception as e:
        # Log the detailed error message
        logging.error(
            f"An unsupported model name was selected or injected. Error changing model: {e}\n{selected_model}"
        )
        # Display a more informative error message to the user
        st.error(f"Failed to change model! Error: {e}\n{selected_model}")


# # Define a dictionary for Real-ESRGAN's model weights
# upscale_model_weights = {
#     2: "weights/RealESRGAN_x2plus.pth",
#     4: "weights/RealESRGAN_x4plus.pth",
#     # 8: "weights/RealESRGAN_x8plus.pth",
# }


# # Define a function to upscale images using Real-ESRGAN
# def image_upscaler(image: str, scale: int) -> Image:
#     """
#     Upscales the input image using the specified model and returns the upscaled image.

#     Parameters:
#     image (str): The file path of the input image.

#     Returns:
#     Image: The upscaled image.
#     """

#     # Assign the image to a variable
#     img = Image.open(image).convert("RGB")

#     # Initialize the upscaler
#     upscaler = RealESRGAN(
#         device="cuda" if torch.cuda.is_available() else "cpu", scale=scale
#     )

#     # Load the corresponding model weight
#     if scale in upscale_model_weights:
#         upscaler.load_weights(
#             upscale_model_weights[scale],
#             # Download the model weight if it doesn't exist
#             download=True,
#         )
#     else:
#         logger.error("Scale factor not in supported model weights.")

#     try:
#         # Capture start time
#         start_time = datetime.datetime.now()

#         with st.spinner(
#             f"Began upscaling: {datetime.datetime.now().strftime('%H:%M:%S')}..."
#         ):
#             # Upscale the image
#             upscaled_img = upscaler.predict(img)

#         # Capture end time
#         end_time = datetime.datetime.now()

#         # Calculate  and log the process duration
#         process_duration = end_time - start_time
#         logger.info(f"Upscale process took {process_duration.total_seconds()} seconds.")

#         # Notify the user
#         st.toast(
#             f"Success! Upscaling took {process_duration.total_seconds()} seconds.",
#             icon="😄",
#         )

#     except Exception as e:
#         logger.error(f"Failed to upscale image. Error: {e}")
#         st.error(f"Failed to upscale image! Please try again.")

#     return upscaled_img


# Define a function to change the background to an image via URL
# https://discuss.streamlit.io/t/how-do-i-use-a-background-image-on-streamlit/5067/19?u=daethyra
def set_bg_url():
    """
    A function to unpack an image from url and set as bg.
    Returns
    -------
    The background.
    """

    st.markdown(
        f"""
         <style>
         .stApp {{
             background: url("https://cdn.pixabay.com/photo/2020/06/19/22/33/wormhole-5319067_960_720.jpg");
             background-size: cover
         }}
         </style>
         """,
        unsafe_allow_html=True,
    )


# Define a function to change the background to a local image
# https://discuss.streamlit.io/t/how-do-i-use-a-background-image-on-streamlit/5067/16?u=daethyra
def set_bg_local(main_bg):
    """
    A function to unpack an image from root folder and set as bg.

    Returns
    -------
    The background.
    """
    # set bg name
    main_bg_ext = "png"

    st.markdown(
        f"""
         <style>
         .stApp {{
             background: url(data:image/{main_bg_ext};base64,{base64.b64encode(open(main_bg, "rb").read()).decode()});
             background-size: cover
         }}
         </style>
         """,
        unsafe_allow_html=True,
    )

# Create a function to save the conversation history to a file
def save_conversation_history(conversation_history: List[Any]) -> str:
    """
    Utility function to format and prepare the conversation history for download.

    Parameters:
    conversation_history (List[Any]): List of objects containing the conversation history.

    Returns:
    str: Formatted conversation history ready for download.
    """
    formatted_history = ""
    for msg in conversation_history:
        if msg.type == 'human':
            formatted_history += f"Human: {msg.content}\n\n"
        elif msg.type == 'ai':
            formatted_history += f"Assistant: {msg.content}\n\n"

    return formatted_history

################################
### CUSTOM CALLBACK HANDLERS ###
class StreamHandler(BaseCallbackHandler):
    """
    A callback handler for streaming the model's output to the user interface.

    This handler updates the user interface with the model's token by token. It also ignores the rephrased question    as output by using a run ID.

    Attributes:
        container (DeltaGenerator): The delta generator object for updating the user interface.
        text (str): The text that has been generated by the model.
        run_id_ignore_token (str): The run ID for ignoring the rephrased question as output.
    """

    def __init__(
        self, container: st.delta_generator.DeltaGenerator, initial_text: str = ""
    ):
        """
        Initialize the StreamHandler object.

        Args:
            container (DeltaGenerator): The delta generator object for updating the user interface.
            initial_text (str): The initial text for the user interface.
        """
        self.container = container
        self.text = initial_text
        self.run_id_ignore_token = None

    def on_llm_start(self, serialized: dict, prompts: list, **kwargs):
        """
        Called when the language model starts generating a response.

        This method sets the run ID for ignoring the rephrased question as output.

        Args:
            serialized (dict): The serialized data for the language model.
            prompts (list): The list of prompts for the language model.
            kwargs: Additional keyword arguments.
        """
        # Workaround to prevent showing the rephrased question as output
        if prompts[0].startswith("Human"):
            self.run_id_ignore_token = kwargs.get("run_id")

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        """
        Called when the language model generates a new token.

        This method updates the user interface with the new token and appends it to the text.

        Args:
            token (str): The new token generated by the language model.
            kwargs: Additional keyword arguments.
        """
        if self.run_id_ignore_token == kwargs.get("run_id", False):
            return
        self.text += token
        self.container.markdown(self.text)


class PrintRetrievalHandler(BaseCallbackHandler):
    """
    A callback handler for printing the context retrieval status.

    This handler updates the status of the retrieval process, including the question, document sources,
    and page contents. It also changes the status label and state according to the retrieval process.

    Attributes:
        container (Container): The container object that contains the status object.
        status (Status): The status object for updating the retrieval process status.
    """

    def __init__(self, container):
        """
        Initialize the PrintRetrievalHandler object.

        Args:
            container (Container): The container object that contains the status object.
        """
        self.status = container.status("**Context Retrieval**")

    def on_retriever_start(self, serialized: dict, query: str, **kwargs):
        """
        Called when the retriever starts the retrieval process.

        This method writes the question to the status and updates the label of the status.

        Args:
            serialized (dict): The serialized data for the retrieval process.
            query (str): The question for which the context is being retrieved.
            kwargs: Additional keyword arguments.
        """
        self.status.write(f"**Question:** {query}")
        self.status.update(label=f"**Context Retrieval:** {query}")

    def on_retriever_end(self, documents, **kwargs):
        """
        Called when the retriever finishes the retrieval process.

        This method prints the document sources and page contents to the status and updates the state of the status.

        Args:
            documents (list): The list of documents retrieved for the question.
            kwargs: Additional keyword arguments.
        """
        for idx, doc in enumerate(documents):
            source = os.path.basename(doc.metadata["source"])
            self.status.write(f"**Document {idx} from {source}**")
            self.status.markdown(doc.page_content)
        self.status.update(state="complete")
