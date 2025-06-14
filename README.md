# Oman-low-chatbot

## 🤖 RAG Chatbot with PDF Processing

A sophisticated Retrieval-Augmented Generation (RAG) chatbot that allows users to upload PDF documents and chat with an AI assistant that can answer questions based on the document content. The system features advanced hierarchical chunking, multi-language support, OCR capabilities, and user authentication.

## 🚀 Features

### Core Functionality
- **PDF Processing**: Upload and process PDF documents with automatic text extraction
- **Advanced Chunking**: Hierarchical chunking strategy with parent and child chunks for better context retention
- **Multi-language Support**: Automatic language detection and appropriate processing
- **OCR Integration**: Azure Computer Vision OCR for complex document processing
- **Vector Database**: Qdrant for efficient similarity search and retrieval
- **OpenAI Integration**: GPT models for intelligent question answering

### User Experience
- **User Authentication**: Secure login and registration system
- **Chat Interface**: Intuitive chat interface with source document references
- **Real-time Processing**: Live feedback during PDF processing and chat interactions
- **Source Citations**: View exact document sources for AI responses

### Technical Features
- **Docker Support**: Containerized deployment with Docker Compose
- **Database Integration**: PostgreSQL for user management
- **Environment Configuration**: Flexible configuration through environment variables
- **Health Checks**: Built-in health monitoring for containerized deployment

## 🏗️ Architecture

### System Components
1. **Frontend**: Streamlit web application
2. **Backend**: Python-based processing engine
3. **Vector Database**: Qdrant for document embeddings
4. **Relational Database**: PostgreSQL for user data
5. **AI Services**: OpenAI GPT models and Azure Computer Vision

### Key Technologies
- **Web Framework**: Streamlit
- **Vector Database**: Qdrant
- **Database**: PostgreSQL
- **AI/ML**: OpenAI GPT, LangChain, Azure Computer Vision
- **PDF Processing**: PyPDF, pdf2image, OCR
- **Containerization**: Docker & Docker Compose

## 📦 Installation

### Prerequisites
- Docker and Docker Compose
- OpenAI API key
- Azure Computer Vision API key (optional, for OCR)

### Quick Start with Docker

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Oman-low-chatbot
   ```

2. **Create environment file**
   ```bash
   cp .env.sample .env
   ```

3. **Configure environment variables**
   Edit `.env` file with your API keys:
   ```bash
   OPENAI_API_KEY=your_openai_api_key
   AZURE_COMPUTER_VISION_KEY=your_azure_key
   AZURE_COMPUTER_VISION_ENDPOINT=your_azure_endpoint
   ```

4. **Start the application**
   ```bash
   docker-compose up -d
   ```

5. **Access the application**
   Open your browser and navigate to `http://localhost:8501`

### Manual Installation

1. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up databases**
   - Install and run PostgreSQL
   - Install and run Qdrant
   - Update database URLs in `.env`

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following variables:

```bash
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key

# Azure Computer Vision (Optional)
AZURE_COMPUTER_VISION_KEY=your_azure_key
AZURE_COMPUTER_VISION_ENDPOINT=your_azure_endpoint

# Database Configuration
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/ragchatbot
QDRANT_URL=http://localhost:6333

# Security
STORE_PLAIN_PASSWORDS=false
```

### Docker Compose Services

The application runs the following services:

- **app**: Main Streamlit application (port 8501)
- **qdrant**: Vector database (ports 6333, 6334)
- **postgres**: User database (port 5432)

## 🛠️ Usage

### Getting Started

1. **Register/Login**: Create an account or log in with existing credentials
2. **Upload PDF**: Use the sidebar to upload a PDF document
3. **Process Document**: Click "Process PDF" to extract and index content
4. **Start Chatting**: Ask questions about your document in the chat interface

### Features in Detail

#### PDF Processing
- Supports various PDF formats
- Automatic language detection
- OCR for complex documents
- Hierarchical chunking for better context

#### Chat Interface
- Natural language questions
- Source document references
- Context-aware responses
- Chat history preservation

#### Advanced Features
- Multi-language document support
- Parent-child chunk relationships
- Detailed processing statistics
- Error handling and user feedback

## 📚 API Reference

### Core Modules

The application is structured around several utility modules:

- **pdf_processor**: Handles PDF parsing, text extraction, and chunking
- **vector_db**: Manages Qdrant vector database operations
- **openai_manager**: Interfaces with OpenAI APIs
- **database**: Handles user authentication and data persistence

### Key Functions

#### PDF Processing
- Text extraction from PDFs
- Language detection
- Hierarchical chunking
- OCR integration

#### Vector Operations
- Document embedding
- Similarity search
- Collection management

#### AI Integration
- Question answering
- Context retrieval
- Response generation

## 🔒 Security

### Authentication
- User registration and login
- Password hashing (configurable)
- Session management

### Data Protection
- Environment variable configuration
- Database connection security
- API key management

## 🚀 Deployment

### Docker Deployment
```bash
docker-compose up -d
```

### Production Considerations
- Use strong database passwords
- Enable HTTPS in production
- Configure proper firewall rules
- Set up monitoring and logging
- Use environment-specific configurations

## 🐛 Troubleshooting

### Common Issues

1. **OpenAI API Key Missing**
   - Ensure `OPENAI_API_KEY` is set in `.env`
   - Verify API key validity

2. **Database Connection Issues**
   - Check PostgreSQL is running
   - Verify database URL configuration
   - Ensure database exists

3. **PDF Processing Errors**
   - Check file format compatibility
   - Verify OCR API keys if needed
   - Check disk space for temporary files

4. **Vector Database Issues**
   - Ensure Qdrant is running
   - Check Qdrant URL configuration
   - Verify network connectivity

## 📊 Performance

### Optimization Tips
- Use appropriate chunk sizes for your documents
- Monitor vector database performance
- Implement caching for frequently accessed data
- Consider GPU acceleration for large-scale deployments

### Monitoring
- Built-in health checks
- Docker container monitoring
- Database performance metrics
- API usage tracking

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue on GitHub
- Check the troubleshooting section
- Review the configuration guide

## 🔄 Updates

### Planned Features
- Support for more document formats
- Enhanced multi-language support
- Advanced analytics dashboard
- API endpoints for external integration
- Batch document processing

---

**Note**: This application requires valid API keys for OpenAI and optionally Azure Computer Vision services. Make sure to secure your API keys and never commit them to version control.
