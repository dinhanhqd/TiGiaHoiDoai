from langchain_community.llms import CTransformers
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain_community.vectorstores import FAISS

# Cấu hình
model_file = "models/vinallama-7b-chat_q5_0.gguf"
vector_db_path = "vectorstores/db_faiss"

# Load LLM
def load_llm(model_file):
    llm = CTransformers(
        model=model_file,
        model_type="llama",
        max_new_tokens=512,
        temperature=0.3,
        context_length=1024
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
        retriever=db.as_retriever(search_kwargs={"k": 4},
                                  max_tokens_limit=512),
        return_source_documents= False,
        chain_type_kwargs={'prompt': prompt}
    )
    return llm_chain

# Đọc từ VectorDB
def read_vectors_db():
    # Embedding
    embedding_model = GPT4AllEmbeddings(model_file="models/all-MiniLM-L6-v2-f16.gguf")
    db = FAISS.load_local(vector_db_path, embedding_model, allow_dangerous_deserialization=True)
    return db

# Bắt đầu thử nghiệm
db = read_vectors_db()
llm = load_llm(model_file)

# Tạo Prompt
template = """system\nSử dụng thông tin sau đây để trả lời câu hỏi. Nếu bạn không biết câu trả lời, hãy nói không biết, đừng cố tạo ra câu trả lời\n
    {context}\nuser\n{question}\nassistant"""
prompt = create_prompt(template)

llm_chain = create_qa_chain(prompt, llm, db)


# Chạy chain
question = "tổng cầu là gì"
response = llm_chain.invoke({"query": question})
print(response)
