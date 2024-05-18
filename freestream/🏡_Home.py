import streamlit as st

from freestream import footer

st.set_page_config(
    page_title="FreeStream: Chatbots for specific use-cases", page_icon="🏡"
)

st.title("FreeStream")
st.header(":green[_Chatbots, tuned for specific use-cases_]", divider="red")
# Project Overview
st.subheader(":blue[What is FreeStream?]")
# Show footer
st.markdown(footer, unsafe_allow_html=True)

### Body content ###
st.write(
    """
    FreeStream is a collection of chatbots that are tuned for specific use-cases.
    """
)
st.divider()
st.subheader("What tools are currently available?")
st.write(
    """
    ### :blue[Curie]:
    
    :orange[*General Purpose Chatbot*]
    
    Curie is great for constructive feedback and programming code. Plus you don't have to upload any files. It's great for stuffing context into your questions when you use the Claude Haiku model. Personally, I like GPT-4o for coding the most.
    """
)

with st.expander(label=":violet[System Prompt:]", expanded=False):
    st.markdown(
        """
        *You are a friendly AI chatbot designed to assist users in learning, programming, and project management. Your role is to guide users towards the right answers by providing thoughtful, well-reasoned responses. When faced with a question, decompose the problem into smaller, manageable parts and reason through each step systematically. Verify step by step to provide comprehensive, truthful answers. Your main goals are to help the user learn, and provide actionable code when asked.*
        """
    )
st.write(
    """
    ### :blue[RAGbot]:
    
    :orange[*Vector Store Based Chatbot*]
    
    The first chatbot made for FreeStream was RAGbot. RAGbot searches files you upload for answers to your questions. It's great for asking specific questions about long policy documents, summarizing the contents of an article, or synthesizing knowledge from multiple sources, such as legal or scientific documents. You may to upload however many PDFs, Word documents, or plain text files you'd like. You can then pose specific questions directly related to the content of your documents.
    """
)

with st.expander(label=":violet[RAGbot workflow:]", expanded=False):
    st.markdown(
        """
        1. Upload Documents:  Upload your documents to RAGbot.
        
        2. Document Splitting:  RAGbot splits your documents into chunks for further processing.
        
        3. Embedding Generation:  The chunks of text are turned into vector embeddings, which basically means the data is standardized into numerical representations.
        
        4. Retriever Creation and Indexing:  The vector embeddings are sorted into a vector database using FAISS.
        
        5. Context Retrieval: Upon being asked a question, the retriever returns the relevant context from the vector database.
        
        6. Context Relevance Validation:  To safeguard against errors, the system only generates a response if the retrieved context is sufficiently relevant to aide the AI's response.
        
        7. Question Answering:  The system meticulously answers your question, drawing knowledge exclusively from the retrieved content.
        """
    )
st.divider()
st.markdown(
    """
    #### References
    
    * **[Run This App On Your Own Computer](https://github.com/Daethyra/FreeStream/blob/streamlit/README.md#installation)**
    * **[LLM Service Provider Privacy Policies](https://github.com/Daethyra/FreeStream/blob/streamlit/README.md#privacy-policy)**
    * **[FreeStream's GitHub Repository](https://github.com/Daethyra/FreeStream)**    
    """
)
st.divider()
