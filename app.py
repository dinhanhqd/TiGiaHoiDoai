import streamlit as st
from langchain_community.llms import CTransformers
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain_community.vectorstores import FAISS
import model  # Import the model.py module
import upload  # Import the upload.py module
import sentiment
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
# Cấu hình
model_file = "models/vinallama-7b-chat_q5_0.gguf"
vector_db_path = "vectorstores/db_faiss"

# Load LLM
def load_llm(model_file):
    llm = CTransformers(
        model=model_file,
        model_type="llama",
        config = {
            'temperature' : 0.5,
            'max_new_tokens' : 512,
            'context_length' : 1024
    }
    )
    return llm

# Tạo prompt template
def create_prompt(template):
    prompt = PromptTemplate(template=template, input_variables=["context", "question"])
    return prompt

# Tạo simple chain
def create_qa_chain(prompt, llm, db):
    llm_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=db.as_retriever(search_kwargs={"k": 2},
                                  max_tokens_limit=512),
        return_source_documents=False,
        chain_type_kwargs={'prompt': prompt}
    )
    return llm_chain

# Đọc từ VectorDB
def read_vectors_db():
    embedding_model = GPT4AllEmbeddings(model_file="models/all-MiniLM-L6-v2-f16.gguf")
    db = FAISS.load_local(vector_db_path, embedding_model, allow_dangerous_deserialization=True)
    return db

@st.cache_resource
def initialize():
    db = read_vectors_db()
    llm = load_llm(model_file)
    template = """system\nSử dụng thông tin sau đây để trả lời câu hỏi. Nếu bạn không biết câu trả lời, hãy nói không biết, đừng cố tạo ra câu trả lời\n
    {context}\nuser\n{question}\nassistant"""
    prompt = create_prompt(template)
    llm_chain = create_qa_chain(prompt, llm, db)
    return llm_chain

def chatbot_page():
    st.title("Chatbot Tư vấn")

    # Initialize the chat model and store it in session state
    if "llm_chain" not in st.session_state:
        st.session_state.llm_chain = initialize()

    # Initialize chat history if not already present in session state
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("Nhập câu hỏi của bạn:"):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Get response from the chat model
        response = st.session_state.llm_chain.invoke({"query": prompt})['result']

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

def main():
    st.set_page_config(layout="wide")  # Thiết lập trang Streamlit để có giao diện rộng

    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Chatbot","Sentiment nalysis", "Model Management", "File Upload"])

    if page == "Chatbot":
        chatbot_page()
    elif page == "Sentiment nalysis":
        sentiment.main()
    elif page == "Model Management":
        model.main()
    elif page == "File Upload":
        upload.main()

if __name__ == "__main__":
    main()
