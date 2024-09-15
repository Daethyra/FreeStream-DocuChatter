import base64
from typing import Any, List

import streamlit as st

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