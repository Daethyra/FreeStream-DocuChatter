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
    
    Curie is great for reflective critical thinking and programming code. It's also great for context-stuffing, which is when you just copy/paste whatever context you want the AI to consider. Context-stuffing is particularily useful when you want the AI to generate a response based on the entirety of your context, rather than just retrieving semantically-similar snippets of your context, which is what RAGbot does.
    """
)

with st.expander(label=":violet[System Prompt:]", expanded=False):
    st.markdown(
        """
        *You are a chatbot primarily designed to assist users in learning, programming, and project management; help the user learn, and provide actionable code when asked. When faced with a question that does not have a clear answer, verify step by step to decompose the problem into smaller, manageable parts and reason through each step systematically.*
        """
    )
st.write(
    """
    ### :blue[RAGbot]:
    
    :orange[*Vector Store Based Chatbot*]
    
    RAGbot searches files you upload for answers to your questions. It first rephrases the user's query and then retrieves specific snippets of your uploaded documents that are semantically relevant to your question. 
    
    It's great at finding specific answers from long documents and synthesizing knowledge from across uploaded documents. You may to upload however many PDFs, Word documents, or plain text files you'd like.
    """
)

with st.expander(label=":violet[RAGbot workflow:]", expanded=False):
    st.markdown(
        """
        1. Upload Documents:  Upload your documents to RAGbot.
        
        2. Document Splitting:  RAGbot splits your documents into chunks for further processing.
        
        3. Embedding Generation:  The chunks of text are turned into vector embeddings, which basically means the data is standardized into numerical representations.
        
        4. Retriever Creation and Indexing:  The vector embeddings are sorted into a vector database using Facebook AI Similarity Search (FAISS).
        
        5. Context Retrieval: Upon being asked a question, the chatbot rephrases the user's query to optimize retrieved results, and then retrieves relevant context from the vector database.
        
        6. Context Relevance Validation:  To safeguard against errors, the system will claim ignorance if the retrieved context is impertinent to the query and the chatbot doesn't have training knowledge to sufficiently answer the query.
        
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
