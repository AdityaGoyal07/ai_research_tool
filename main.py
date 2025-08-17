import os,time
import streamlit as st
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
# Set the OpenAI API key
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

st.title("NEWS RESEARCH TOOL")
st.sidebar.title("NEWS Article URLs")

urls = []
for i in range(3):
    url = st.sidebar.text_input(f"URL {i+1}")
    urls.append(url)

process_url_clicked = st.sidebar.button("Process URLs")

main_placeholder = st.empty()
index_dir = "embeddings_folder" # faiss index folder

llm = OpenAI(temperature=0.9, max_tokens=500)

# Step 1: Process URLs -> Create embeddings & FAISS index
if process_url_clicked:
    #load the data from the URLs
    loader = UnstructuredURLLoader(urls=urls)
    main_placeholder.text("📥 Loading data from URLs...")
    data = loader.load()
    
    #split the data into manageable chunks
    text_splitter = RecursiveCharacterTextSplitter(
        separators=['\n\n','\n','.',','],
        chunk_size=1000, 
        #chunk_overlap=200
        )
    
    main_placeholder.text("✂️ Text Splitter ..... Started...")
    docs = text_splitter.split_documents(data)
    
    #create embeddings for the chunks and save them to Faiss index
    main_placeholder.text("🔎 Creating embedding vectors and faiss indexes started .....")
    embeddings = OpenAIEmbeddings()
    vectorstore_openai = FAISS.from_documents(docs, embeddings)
    time.sleep(2)
    
    # save the faiss index
    vectorstore_openai.save_local(index_dir)
    main_placeholder.text("✅ Embeddings created successfully!")

#Step 2 : Ask questions 
query = main_placeholder.text_input("❓Ask a Question : ")
if query:
    if os.path.exists(index_dir):
        # Recreate the embeddings obect
        embeddings = OpenAIEmbeddings()
        vectorstore = FAISS.load_local(index_dir, embeddings, allow_dangerous_deserialization=True)
        
        chain = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=vectorstore.as_retriever(),
            return_source_documents=True
        )
        
        result = chain({"query": query}, return_only_outputs=True)
        # result -> {"result" : "", "sources" : []}
        st.header("Answer:")
        st.subheader(result["result"])
        
        # Display sources if available
        sources = result.get("source_documents", [])
        if sources:
            st.subheader("Sources:")
            unique_urls = set()
            for source in sources:
                url = source.metadata.get("source", "Unknown Source")
                if url not in unique_urls:
                    st.write(url)
                    unique_urls.add(url)

    
    else:
        st.warning("⚠️ Please process URLs first to create embeddings before asking questions.")
