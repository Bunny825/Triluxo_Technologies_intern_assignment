from flask import Flask, request, jsonify
from langchain_community.document_loaders import WebBaseLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_huggingface import HuggingFaceEndpoint
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

os.environ["USER_AGENT"]="Brainlox_chatbot/1.0"
#user agent also should be set in the environment

HUGGINGFACEHUB_API_TOKEN=os.getenv("HUGGINGFACEHUB_API_TOKEN") 
#token should be set in environment variables

if not HUGGINGFACEHUB_API_TOKEN:
    raise ValueError("HUGGINGFACEHUB_API_TOKEN is not set in environment variables.")

#step 1:Load text from website
url="https://brainlox.com/courses/category/technical"
loader=WebBaseLoader(url)
docs=loader.load()

#step 2:Split text into chunks
splitter=RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=100)
docs=splitter.split_documents(docs)

#step 3:Create embeddings and FAISS vector store
embedding_model=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vector_store=FAISS.from_documents(docs,embedding_model)

# step 4:Save FAISS index
vector_store.save_local("faiss_web")

#step 5:Load FAISS index
web_saved=FAISS.load_local("faiss_web",embedding_model,allow_dangerous_deserialization=True)

retriever=web_saved.as_retriever(search_kwargs={"k":3})

#step 6:Initialize Hugging Face LLM
llm=HuggingFaceEndpoint(repo_id="tiiuae/falcon-7b-instruct",temperature=0.5)


#step 7:Create RetrievalQA chain
qa=RetrievalQA.from_chain_type(llm=llm,chain_type="stuff",retriever=retriever)

#Flask API
app=Flask(__name__)

@app.route("/ask", methods=["POST"])
def ask():
    data=request.json
    query=data.get("query", "")
    if not query:
        return jsonify({"error":"Query is required"}),400

    response=qa.invoke(query)
    return jsonify({"result":response["result"]})

if __name__=="__main__":
    app.run(debug=True)

