import os
import streamlit as st
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_openai import OpenAI
from dotenv import load_dotenv
import random

load_dotenv()
# Set the OpenAI API key
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# Page configuration
st.set_page_config(
    page_title="AI Research Tool",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .question-card {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin: 0.5rem 0;
    }
    
    .analysis-container {
        background: #1e1e2f;
        color: #fff;           /* white text */
        border: 1px solid #333;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 6px rgba(0,0,0,0.4);
    }
    
    .ai-analysis p {           /* nicer body copy */
    line-height: 1.6;
    margin: 0.5rem 0 1rem;
    }

    .ai-analysis h4 {          /* question header */
        margin-bottom: 0.75rem;
    }
    
    .source-link {
        background: #2a2a3d;   /* dark card background */
        color: #e0e0e0;
        border: 1px solid #444;
        border-radius: 8px;
        padding: 0.75rem;
        margin: 0.5rem 0;
    }
    
    .success-message {
        background: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
    }
    
    .info-box {
        background: #1e1e2f;
        color: #fff;
        border: 1px solid #333;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown("""
<div class="main-header">
    <h1>🔬 AI Research Tool</h1>
    <p>Intelligent Content Analysis & Question Generation</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if 'suggested_questions' not in st.session_state:
    st.session_state.suggested_questions = []
if 'chunks_processed' not in st.session_state:
    st.session_state.chunks_processed = False
if 'processed_content' not in st.session_state:
    st.session_state.processed_content = ""
if 'selected_question' not in st.session_state:
    st.session_state.selected_question = None
if 'show_analysis' not in st.session_state:
    st.session_state.show_analysis = False

# Collapsible documentation section
with st.expander("📚 How to Use This Tool", expanded=False):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 🚀 Getting Started
        1. **Add URLs**: Enter up to 3 article URLs in the input section
        2. **Process Content**: Click the "Analyze Content" button
        3. **Explore Questions**: Review AI-generated questions
        4. **Get Insights**: Click on any question to see detailed analysis
        """)
    
    with col2:
        st.markdown("""
        ### ✨ Features
        - **Smart Analysis**: AI understands your content automatically
        - **Relevant Questions**: Generated based on actual article content
        - **Source Tracking**: See which articles support each answer
        - **Custom Queries**: Ask your own questions anytime
        """)
    
    with col3:
        st.markdown("""
        ### 💡 Tips
        - Use high-quality news sources for best results
        - Try both suggested and custom questions
        - Check the debug mode to verify content extraction
        - Questions adapt to any topic (news, business, policy, etc.)
        """)

# Main content area with tabs
tab1, tab2, tab3 = st.tabs(["📝 Content Input", "🧠 AI Analysis", "❓ Custom Questions"])

llm = OpenAI(temperature=0.8, max_tokens=600)
index_dir = "embeddings_folder"

def generate_suggested_questions(docs, sample_size=8):
    """
    Generate suggested questions based on processed document chunks.
    Improved version with better content validation and general topic focus.
    """
    if not docs:
        return []
    
    try:
        # Use more documents for better content coverage
        sample_docs = random.sample(docs, min(sample_size, len(docs)))
        
        # Combine sample documents with longer text for better context
        combined_text = "\n\n".join([doc.page_content[:800] for doc in sample_docs])
        
        # Store processed content for debugging
        st.session_state.processed_content = combined_text[:1500]
        
        # Improved general-purpose question generation prompt
        question_prompt = f"""
        Based on the following news content, generate 10 specific, insightful questions that would be valuable for understanding and analyzing the topics discussed. Focus on questions about:
        - Key events and developments mentioned
        - Policy implications and impacts
        - Economic and business implications
        - Stakeholder perspectives and reactions
        - Future outlook and predictions
        - Cause-and-effect relationships
        - Comparative analysis with similar situations
        
        Content to analyze:
        {combined_text}
        
        Requirements:
        - Generate exactly 10 questions, each on a new line starting with "Q:"
        - Make questions specific to the actual content provided
        - Focus on the main topics, companies, countries, policies, or events mentioned in the text
        - Avoid generic questions - be specific to what's actually discussed
        - Questions should help readers gain deeper insights into the topics covered
        """
        
        # Generate questions using the existing LLM
        response = llm.invoke(question_prompt)
        
        # Parse questions from response
        questions = []
        lines = response.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('Q:'):
                question = line[2:].strip()
                if question and len(question) > 15:
                    questions.append(question)
        
        # Ensure we have exactly 6 questions
        if len(questions) < 10:
            content_lower = combined_text.lower()
            default_questions = []
            
            if 'trade' in content_lower or 'tariff' in content_lower:
                default_questions.extend([
                    "What are the main trade issues discussed in the articles?",
                    "How might these trade developments affect the economies involved?"
                ])
            if 'policy' in content_lower or 'government' in content_lower:
                default_questions.extend([
                    "What policy changes or decisions are highlighted?",
                    "What are the potential impacts of these policy decisions?"
                ])
            if 'company' in content_lower or 'business' in content_lower:
                default_questions.extend([
                    "Which companies or sectors are most affected by these developments?",
                    "What are the business implications of the events discussed?"
                ])
            
            if not default_questions:
                default_questions = [
                    "What are the key developments discussed in these articles?",
                    "Who are the main stakeholders affected by these events?",
                    "What are the potential future implications of these developments?",
                    "How do these events compare to similar situations in the past?",
                    "What are the different perspectives on these issues?",
                    "What challenges and opportunities are identified in the content?"
                ]
            
            questions.extend(default_questions[:10-len(questions)])
        
        return questions[:10]
    
    except Exception as e:
        st.error(f"Error generating questions: {str(e)}")
        return [
            "What are the main topics and events discussed in the articles?",
            "Who are the key stakeholders or entities mentioned?",
            "What are the potential implications of the developments discussed?",
            "What challenges or issues are highlighted in the content?",
            "How might these events affect different sectors or regions?",
            "What are the different viewpoints or reactions mentioned in the articles?"
        ]

# Run custom query analysis
def run_question_analysis(question):
    """
    Run a question through the QA chain and return results.
    """
    if os.path.exists(index_dir):
        embeddings = OpenAIEmbeddings()
        vectorstore = FAISS.load_local(index_dir, embeddings, allow_dangerous_deserialization=True)
        
        chain = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=vectorstore.as_retriever(),
            return_source_documents=True
        )
        
        result = chain({"query": question}, return_only_outputs=True)
        return result
    return None

# Tab 1: Content Input
with tab1:
    st.markdown("### 📰 Enter Article URLs")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        urls = []
        for i in range(3):
            url = st.text_input(f"URL {i+1}", placeholder=f"https://example.com/article-{i+1}")
            urls.append(url)
    
    with col2:
        st.markdown("### 🎛️ Options")
        show_debug = st.checkbox("🔍 Debug Mode", help="Show content preview for verification")
        
        if st.button("🚀 Analyze Content", type="primary", use_container_width=True):
            if not any(url.strip() for url in urls):
                st.warning("⚠️ Please enter at least one URL before processing.")
            else:
                try:
                    valid_urls = [url.strip() for url in urls if url.strip()]
                    
                    with st.spinner("📥 Loading content from URLs..."):
                        loader = UnstructuredURLLoader(urls=valid_urls)
                        data = loader.load()
                    
                    if not data:
                        st.error("❌ No content could be loaded from the provided URLs. Please check if the URLs are accessible.")
                    else:
                        with st.spinner("✂️ Processing and analyzing content..."):
                            text_splitter = RecursiveCharacterTextSplitter(
                                separators=['\n\n', '\n', '.', '!', '?', ','],
                                chunk_size=1000,
                                chunk_overlap=250
                            )
                            
                            docs = text_splitter.split_documents(data)
                            
                            if not docs:
                                st.error("❌ No content chunks could be created. Please check the URL content.")
                            else:
                                embeddings = OpenAIEmbeddings()
                                vectorstore_openai = FAISS.from_documents(docs, embeddings)
                                vectorstore_openai.save_local(index_dir)
                                
                                suggested_questions = generate_suggested_questions(docs)
                                
                                st.session_state.suggested_questions = suggested_questions
                                st.session_state.chunks_processed = True
                        
                        st.markdown("""
                        <div class="success-message">
                            ✅ Content analysis complete! Check the "AI Analysis" tab to explore suggested questions.
                        </div>
                        """, unsafe_allow_html=True)
                        
                except Exception as e:
                    st.error(f"❌ Error processing URLs: {str(e)}")
    
    # Debug content preview
    if show_debug and st.session_state.processed_content:
        with st.expander("🔍 Content Preview (Debug)", expanded=False):
            st.text_area("Processed Content Sample:", 
                        value=st.session_state.processed_content, 
                        height=200, 
                        disabled=True)

# Tab 2: AI Analysis
with tab2:
    if st.session_state.chunks_processed and st.session_state.suggested_questions:
        st.markdown("### 💡 AI-Generated Questions")
        st.markdown("Click on any question below to get detailed analysis:")
        
        # Create two columns for questions and analysis
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("#### 📋 Suggested Questions")
            for i, question in enumerate(st.session_state.suggested_questions):
                with st.container():
                    st.markdown(f"""
                    <div class="question-card">
                        <strong>{i+1}.</strong> {question}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button(f"🔍 Analyze", key=f"analyze_btn_{i}", help=f"Get detailed analysis for: {question}"):
                        st.session_state.selected_question = question
                        st.session_state.show_analysis = True
        
        with col2:
            st.markdown("#### 📊 Analysis Results")
            if st.session_state.show_analysis and st.session_state.selected_question:
                with st.container():
                    st.markdown(f"""
                    <div class="analysis-container ai-analysis">
                        <h4>🎯 Question: {st.session_state.selected_question}</h4>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    with st.spinner("🤖 Generating analysis..."):
                        result = run_question_analysis(st.session_state.selected_question)
                        
                        if result:
                            st.markdown("**🤖 AI Analysis:**")
                            st.write(result["result"])
                            
                            sources = result.get("source_documents", [])
                            if sources:
                                st.markdown("**📚 Sources:**")
                                unique_urls = set()
                                for source in sources:
                                    url = source.metadata.get("source", "Unknown Source")
                                    if url not in unique_urls:
                                        st.markdown(f"""
                                        <div class="source-link">
                                            📄 <a href="{url}" target="_blank">{url}</a>
                                        </div>
                                        """, unsafe_allow_html=True)
                                        unique_urls.add(url)
                        else:
                            st.error("❌ Unable to analyze question. Please ensure content has been processed.")
            else:
                st.markdown("""
                <div class="info-box">
                    <h4>👈 Select a Question</h4>
                    <p>Click on any "Analyze" button from the suggested questions to see detailed AI analysis and source citations here.</p>
                </div>
                """, unsafe_allow_html=True)
    
    else:
        st.markdown("""
        <div class="info-box">
            <h4>🚀 Get Started</h4>
            <p>Go to the <strong>"Content Input"</strong> tab, enter your article URLs, and click <strong>"Analyze Content"</strong> to generate AI-powered questions and insights.</p>
        </div>
        """, unsafe_allow_html=True)

# Tab 3: Custom Questions
with tab3:
    st.markdown("### ❓ Ask Your Own Questions")
    
    if st.session_state.chunks_processed:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            custom_query = st.text_input("💬 Enter your question about the content:", 
                                       placeholder="What specific aspect would you like to explore?")
        
        with col2:
            ask_custom = st.button("🎯 Get Answer", type="primary", use_container_width=True)
        
        if custom_query and ask_custom:
            st.markdown("---")
            with st.spinner("🤖 Processing your question..."):
                result = run_question_analysis(custom_query)
                
                if result:
                    st.markdown(f"""
                    <div class="analysis-container">
                        <h4>🎯 Your Question: {custom_query}</h4>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("**🤖 AI Analysis:**")
                    st.write(result["result"])
                    
                    sources = result.get("source_documents", [])
                    if sources:
                        st.markdown("**📚 Sources:**")
                        unique_urls = set()
                        for source in sources:
                            url = source.metadata.get("source", "Unknown Source")
                            if url not in unique_urls:
                                st.markdown(f"""
                                <div class="source-link">
                                    📄 <a href="{url}" target="_blank">{url}</a>
                                </div>
                                """, unsafe_allow_html=True)
                                unique_urls.add(url)
                else:
                    st.error("❌ Unable to process your question. Please ensure content has been analyzed first.")
    
    else:
        st.markdown("""
        <div class="info-box">
            <h4>⚠️ Content Required</h4>
            <p>Please process some article URLs in the <strong>"Content Input"</strong> tab before asking custom questions.</p>
        </div>
        """, unsafe_allow_html=True)

# Sidebar for additional tools
with st.sidebar:
    st.markdown("### ⚙️ Tools & Settings")
    
    if st.button("🔄 Clear Analysis", help="Reset all processed data"):
        st.session_state.suggested_questions = []
        st.session_state.chunks_processed = False
        st.session_state.processed_content = ""
        st.session_state.selected_question = None
        st.session_state.show_analysis = False
        if os.path.exists(index_dir):
            import shutil
            shutil.rmtree(index_dir)
        st.success("✅ Analysis cleared!")
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 📊 Status")
    if st.session_state.chunks_processed:
        st.success("✅ Content Processed")
        st.info(f"📝 {len(st.session_state.suggested_questions)} questions generated")
    else:
        st.warning("⏳ No content processed")
    
    st.markdown("---")
    st.markdown("""
    ### 🔗 About
    **AI Research Tool** uses advanced LangChain and OpenAI technologies to analyze news content and generate intelligent questions for deeper insights.
    
    Built with:
    - 🦜 LangChain
    - 🤖 OpenAI GPT
    - 📊 FAISS Vector DB
    - 🎨 Streamlit
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <p>🔬 <strong>AI Research Tool</strong> - Powered by LangChain & OpenAI</p>
    <p><em>Intelligent content analysis for better insights</em></p>
</div>
""", unsafe_allow_html=True)
