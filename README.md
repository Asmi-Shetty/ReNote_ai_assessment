Adaptive RAG is an intelligent, end-to-end Retrieval-Augmented Generation (RAG) system powered by agentic AI architecture. It combines dynamic query routing, intelligent document retrieval, and advanced LLM capabilities to provide accurate, context-aware answers to user queries.

The system intelligently adapts its retrieval strategy based on query type, utilizing indexed documents, general knowledge, or real-time web search to generate comprehensive responses. Built with a modular architecture using LangGraph for workflow orchestration and multiple storage backends for scalability.

🎯 Key Features
🧠 Intelligent Query Routing
Adaptive Classification: Automatically routes queries to the most appropriate processing pipeline
Three Query Types:
Index: Queries answerable from uploaded documents
General: Queries answerable with general knowledge
Search: Queries requiring real-time web search
📚 Advanced RAG Pipeline
Document Processing: Intelligent chunking and embedding of documents
Vector Search: Fast similarity-based retrieval using Qdrant
Relevance Grading: Automatic evaluation of retrieved documents
Query Rewriting: Optimizes queries for better retrieval results
🤖 Agentic AI Architecture
Multi-Agent System: Specialized agents for different tasks
ReAct Framework: Reasoning and Acting pattern for intelligent decision-making
Tool Integration: Seamless integration with retrieval tools and web search
💾 State Management
MongoDB Backend: Persistent chat history and session management
Session Tracking: Individual conversation contexts per user
Memory Management: Full conversation context retention
🎨 User Interface
Streamlit Web App: Interactive chat interface with document upload
File Support: PDF and TXT document uploads
Real-time Feedback: Live chat with instant responses
⚡ API-First Architecture
FastAPI Backend: High-performance REST API
Async Operations: Non-blocking database and API calls
RESTful Endpoints: Well-defined API contracts
🏗️ Architecture
System Components
┌─────────────────────────────────────────────────────────────────┐
│                         User Interface                          │
│  ┌──────────────��───────────────────────────────────────��───┐  │
│  │  Streamlit Web Application                               │  │
│  │  • Chat Interface                                        │  │
│  │  • Document Upload (PDF, TXT)                            │  │
│  │  • Session Management                                    │  │
│  └──────────────────────────────────────────────────────────��  │
└───────────────────────────────────────────��─────────────────────┘
                            ↓
┌────────────────────────────────────────────────��────────────────┐
│                       FastAPI Backend                           │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  REST API Endpoints                                      │  │
│  │  • POST /rag/query                                       │  │
│  │  • POST /rag/documents/upload                            │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│                    LangGraph Orchestration                      │
│  ┌─────────┐  ┌──────────┐  ┌─────────┐  ┌──────────┐         │
│  │ Query   │→ │ Classify │→ │ Router  │→ │ Pipeline │         │
│  │ Analyze │  │ Query    │  │ Output  │  │ Exec     │         │
│  └─────────┘  └──────────┘  └───��─────┘  └──────────┘         │
└─────────────────────────────────────────────────────────────────┘
                            ↓
        ┌───────��──────────┬────────────────��─┬────────────────┐
        ↓                  ↓                  ↓                ↓
   ┌─────────┐       ┌──────────┐      ┌────────────┐   ┌──────────┐
   │ Retriever│      │ General  │      │ Web Search │   │ Response │
   │ (Index)  │      │ LLM      │      │ (Tavily)   │   │ Generator│
   └─────────┘       └──────────┘      └────────────┘   └──────────┘
        ↓                  ↓                  ↓                ↓
        └──────────────────┬──────────────────┬────────────────┘
                           ↓
            ┌─────────────────────────────────┐
            │   Response to User               │
            └─────────────────────────────────┘
Graph Nodes
query_analysis: Analyzes and classifies incoming queries
retriever: Retrieves relevant documents from vector store
grade: Evaluates relevance of retrieved documents
rewrite: Optimizes query for better retrieval results
generate: Generates final response from context
web_search: Performs real-time web search when needed
general_llm: Provides general knowledge answers




📖 Usage Guide
1. Prerequisites
# System Requirements
- Python 3.9 or higher
- MongoDB (local or cloud)
- Qdrant vector database
- OpenAI API key
- Tavily API key (for web search)
2. Installation
# Clone the repository
git clone https://github.com/dhruvsinghal09/Adaptive-Rag.git
cd AdaptiveRag

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
3. Environment Configuration
Create a .env file in the project root:

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Tavily Search Configuration
TAVILY_API_KEY=your_tavily_api_key_here

# Qdrant Configuration
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=your_qdrant_api_key
QDRANT_CODE_COLLECTION=code_documents
QDRANT_DOCS_COLLECTION=documents

# MongoDB Configuration
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB_NAME=adaptive_rag
4. Running the Application
Start FastAPI Backend:

# Terminal 1: Run FastAPI server
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
Start Streamlit Frontend:

# Terminal 2: Run Streamlit app
streamlit run streamlit_app/home.py
Access the Application:

Web Interface: http://localhost:8501
API Documentation: http://localhost:8000/docs
ReDoc Documentation: http://localhost:8000/redoc



📚 Technology Stack
Component	Technology	Version
LLM Framework	LangChain	~0.3.27
Workflow Orchestration	LangGraph	~0.5.4
Web Framework	FastAPI	Latest
ASGI Server	Uvicorn	Latest
UI Framework	Streamlit	Latest
Vector Database	Qdrant/FAISS	Latest
Chat Database	MongoDB/InMemory	Latest
Document Processing	LangChain Community	~0.3.27
LLM Provider	OpenAI	~0.3.28
Web Search	Tavily	Latest
Async DB	Motor	Latest
Data Validation	Pydantic	~2.11.7