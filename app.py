import os
import streamlit as st
import tempfile
import re
import time
from pathlib import Path
from utils.pdf_processor import PDFProcessor
from utils.vector_db import VectorDBManager
from utils.openai_manager import OpenAIModelManager
from utils.database import register_user, authenticate_user
from qdrant_client import QdrantClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Function to validate email
def is_valid_email(email):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email) is not None

# Function to delete a Qdrant collection
def delete_collection(collection_name, qdrant_url=None):
    if not qdrant_url:
        qdrant_url = os.environ.get("QDRANT_URL", "http://localhost:6333")
    
    try:
        client = QdrantClient(url=qdrant_url)
        client.delete_collection(collection_name=collection_name)
        return True, f"Collection '{collection_name}' deleted successfully"
    except Exception as e:
        return False, f"Error deleting collection: {str(e)}"

# Set page configuration
st.set_page_config(
    page_title="RAG Chatbot",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = []

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

if "chain" not in st.session_state:
    st.session_state.chain = None

if "collection_name" not in st.session_state:
    st.session_state.collection_name = "pdf_collection"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_email" not in st.session_state:
    st.session_state.user_email = ""

if "page" not in st.session_state:
    st.session_state.page = "login"

if "openai_manager" not in st.session_state:
    st.session_state.openai_manager = None

if "detected_language" not in st.session_state:
    st.session_state.detected_language = None

# Function to handle login
def login():
    st.title("Login")
    
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if not email or not password:
            st.error("Please fill in all fields")
            return
        
        # Authenticate user with database
        success, message = authenticate_user(email, password)
        if success:
            st.session_state.logged_in = True
            st.session_state.user_email = email
            st.session_state.page = "main"
            
            # Initialize OpenAI manager if not already initialized
            if not st.session_state.openai_manager and os.getenv("OPENAI_API_KEY"):
                try:
                    st.session_state.openai_manager = OpenAIModelManager()
                except ValueError as e:
                    st.error(f"Error initializing OpenAI manager: {str(e)}")
                    st.warning("Please check your OpenAI API key in the .env file.")
                
            st.success("Login successful!")
            st.rerun()
        else:
            st.error(message)
    
    st.write("Don't have an account?")
    if st.button("Register"):
        st.session_state.page = "register"
        st.rerun()

# Function to handle registration
def register():
    st.title("Registration")
    
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    
    if st.button("Register"):
        if not email or not password or not confirm_password:
            st.error("Please fill in all fields")
            return
        
        if not is_valid_email(email):
            st.error("Please enter a valid email")
            return
        
        if password != confirm_password:
            st.error("Passwords do not match")
            return
        
        # Register user in database
        success, message = register_user(email, password)
        if success:
            st.success("Registration successful! Please login.")
            st.session_state.page = "login"
            st.rerun()
        else:
            st.error(message)
    
    st.write("Already have an account?")
    if st.button("Login"):
        st.session_state.page = "login"
        st.rerun()

# Function to handle logout
def logout():
    st.session_state.logged_in = False
    st.session_state.user_email = ""
    st.session_state.page = "login"
    st.rerun()

# Main app function
def main_app():
    # App title and description
    st.title("📚 RAG Chatbot")
    st.markdown("""
    Upload a PDF document, and chat with an AI assistant that can answer questions based on the document content.
    This application uses:
    - Qdrant as the vector database
    - Advanced hierarchical chunking for better context retention
    """)

    # Add logout button in the sidebar
    with st.sidebar:
        st.write(f"Logged in as: {st.session_state.user_email}")
        if st.button("Logout"):
            logout()
    
    # Sidebar for configuration
    with st.sidebar:
        
        # Check if OpenAI API key is available
        openai_key = os.getenv("OPENAI_API_KEY")

        
        # PDF upload section
        st.header("Upload PDF")
        uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
        
        if uploaded_file is not None and openai_key:
            # Save the uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                pdf_path = tmp_file.name
            
            if st.button("Process PDF"):
                with st.spinner("Processing PDF..."):
                    try:
                        # Initialize PDF processor
                        pdf_processor = PDFProcessor()
                        
                        # Process PDF
                        chunks, detected_language = pdf_processor.process_pdf(pdf_path)
                        st.session_state.chunks = chunks
                        st.session_state.detected_language = detected_language
                        
                        # Check if OCR was used for processing
                        ocr_used = any(chunk.metadata.get("ocr_processed", False) for chunk in chunks if len(chunks) > 0)
                        st.session_state.ocr_used = ocr_used
                        
                        # Display detected language
                        st.success(f"PDF processed successfully! Created {len(chunks)} chunks.")
                        
                        # Show chunking stats
                        parent_chunks = [c for c in chunks if c.metadata.get("chunk_type") == "parent"]
                        child_chunks = [c for c in chunks if c.metadata.get("chunk_type") == "child"]
                        st.info(f"Created {len(parent_chunks)} parent chunks and {len(child_chunks)} child chunks")
                        
                        # Display language information
                        st.info(f"Detected language: {detected_language}")
                        
                        # Display OCR information if used
                        if ocr_used:
                            st.info("OCR processing was used for non-English text extraction")
                        
                        # Initialize vector database
                        try:
                            vector_db_manager = VectorDBManager()
                            
                            # Create vector store
                            st.session_state.vector_store = vector_db_manager.get_or_create_vector_store(
                                documents=chunks,
                                collection_name=st.session_state.collection_name
                            )
                            
                            # Initialize OpenAI manager if not already initialized
                            if not st.session_state.openai_manager:
                                try:
                                    st.session_state.openai_manager = OpenAIModelManager()
                                except ValueError as e:
                                    st.error(f"Error initializing OpenAI manager: {str(e)}")
                                    st.warning("Please check your OpenAI API key in the .env file.")
                                    return
                            
                            # Create retrieval chain
                            st.session_state.chain = st.session_state.openai_manager.create_retrieval_chain(
                                vector_store=st.session_state.vector_store
                            )
                            
                            st.success("Vector store and retrieval chain created successfully!")
                        
                        except Exception as e:
                            st.error(f"Error creating vector store: {str(e)}")
                    
                    except Exception as e:
                        st.error(f"Error processing PDF: {str(e)}")
                    finally:
                        # Clean up the temporary file
                        if os.path.exists(pdf_path):
                            os.unlink(pdf_path)
        else:
            if uploaded_file is not None and not openai_key:
                st.error("OpenAI API key is missing. Please add it to your .env file.")
                st.info("You need to set the OPENAI_API_KEY in your environment variables to process PDFs.")

    # Main chat interface
    st.header("Chat")
    
    # Display detected language if available
    if st.session_state.detected_language:
        language_info = f"Document language: {st.session_state.detected_language}"
        st.info(language_info)
        
        # Display OCR information if available and used
        if hasattr(st.session_state, 'ocr_used') and st.session_state.ocr_used:
            st.info("OCR processing was used for text extraction due to non-English content")
    
    # Display chunking information
    if hasattr(st.session_state, 'chunks') and st.session_state.chunks:
        parent_chunks = [c for c in st.session_state.chunks if c.metadata.get("chunk_type") == "parent"]
        child_chunks = [c for c in st.session_state.chunks if c.metadata.get("chunk_type") == "child"]
        st.info(f"Using hierarchical chunking with {len(parent_chunks)} parent chunks and {len(child_chunks)} child chunks")
    
    # Check if OpenAI API key is provided
    if not os.getenv("OPENAI_API_KEY") and not st.session_state.openai_manager:
        st.warning("⚠️ OpenAI API key is required. Please add it to your .env file.")
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
            
            # Display source documents for AI messages
            if message["role"] == "assistant" and "source_docs" in message:
                with st.expander("View Sources"):
                    for i, doc in enumerate(message["source_docs"]):
                        st.markdown(f"**Source {i+1}:**")
                        chunk_type = doc.metadata.get('chunk_type', 'standard')
                        parent_id = doc.metadata.get('parent_id', 'N/A')
                        
                        if chunk_type == "child":
                            st.markdown(f"*Child Chunk (Parent ID: {parent_id}) - Page {doc.metadata.get('page', 'N/A')}*")
                        else:
                            st.markdown(f"*Page {doc.metadata.get('page', 'N/A')}*")
                            
                        st.markdown(doc.page_content)

    # Chat input
    chat_disabled = not (st.session_state.chain is not None and st.session_state.openai_manager is not None)
    
    if chat_disabled:
        st.info("Please upload and process a PDF document and ensure OpenAI API key is provided in the .env file to start chatting.")
    
    if prompt := st.chat_input("Ask a question about your document", disabled=chat_disabled):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.write(prompt)
            
        # Generate and display AI response
        if st.session_state.chain:
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        # Call the chain to get a response
                        response = st.session_state.openai_manager.generate_response(
                            chain=st.session_state.chain,
                            query=prompt
                        )
                        
                        # Extract answer and source documents
                        answer = response.get("answer", "I couldn't find an answer to that question.")
                        source_docs = response.get("source_documents", [])
                        
                        # Display the answer
                        st.write(answer)
                        
                        # Display source documents
                        if source_docs:
                            with st.expander("View Sources"):
                                for i, doc in enumerate(source_docs):
                                    st.markdown(f"**Source {i+1}:**")
                                    chunk_type = doc.metadata.get('chunk_type', 'standard')
                                    parent_id = doc.metadata.get('parent_id', 'N/A')
                                    
                                    if chunk_type == "child":
                                        st.markdown(f"*Child Chunk (Parent ID: {parent_id}) - Page {doc.metadata.get('page', 'N/A')}*")
                                    else:
                                        st.markdown(f"*Page {doc.metadata.get('page', 'N/A')}*")
                                        
                                    st.markdown(doc.page_content)
                        
                        # Add to chat history
                        st.session_state.messages.append({
                            "role": "assistant", 
                            "content": answer,
                            "source_docs": source_docs
                        })
                    except Exception as e:
                        error_msg = f"Error generating response: {str(e)}"
                        st.error(error_msg)
                        st.session_state.messages.append({
                            "role": "assistant", 
                            "content": error_msg
                        })
        else:
            with st.chat_message("assistant"):
                error_msg = "Please upload and process a document first."
                st.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": error_msg
                })
    
# Run the appropriate page
if __name__ == "__main__":
    if st.session_state.page == "login" and not st.session_state.logged_in:
        login()
    elif st.session_state.page == "register" and not st.session_state.logged_in:
        register()
    else:
        main_app()
