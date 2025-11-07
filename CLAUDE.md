# CLAUDE.md - Agentic Context Development Interview Demo

## Project Overview

This is a Streamlit-based application that demonstrates an AI agent-driven workflow for building personalized LLM context through conversational interviews. The system conducts structured interviews, extracts contextual information, and formats it as markdown files suitable for RAG (Retrieval-Augmented Generation) pipeline ingestion.

## Purpose

The application models a workflow where an AI agent conducts interviews to build a personal context repository. This context can be used with:
- Vector databases (Pinecone, ChromaDB, Weaviate, Qdrant)
- RAG frameworks (LangChain, LlamaIndex)
- Custom retrieval pipelines
- Fine-tuning datasets

## Technology Stack

- **Frontend**: Streamlit
- **AI Integration**: OpenAI API
- **Language**: Python 3.8+
- **Data Format**: Markdown (platform-agnostic for vector database ingestion)

## Key Features

1. **Interview System**: Conversational interface via OpenAI API
2. **Question Generation**: Context-aware follow-up questions based on responses
3. **API Key Management**: Local storage for OpenAI credentials
4. **Session Management**: State preservation across interview sessions
5. **Context Extraction**: LLM-based processing to extract structured context
6. **Data Export**: Markdown file generation for extracted context

## Project Structure

```
.
├── app.py                      # Main Streamlit application
├── app.spec                    # PyInstaller specification
├── requirements.txt            # Python dependencies
├── run.sh                      # Shell script to launch application
├── Streamlit-App.desktop       # Desktop launcher file
├── .env                        # Environment variables (gitignored)
├── .streamlit/                 # Streamlit configuration
├── example-output/             # Sample output files
├── screenshots/                # UI screenshots for documentation
└── .vscode/                    # VS Code configuration
```

## Setup and Usage

### Prerequisites

- Python 3.8 or higher
- OpenAI API key

### Installation

1. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Linux/Mac
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure OpenAI API key:
   - Option 1: Set in `.env` file
   - Option 2: Enter via application UI

### Running the Application

```bash
streamlit run app.py
```

Or use the provided shell script:
```bash
./run.sh
```

## Development Notes

### Environment Variables

The application uses a `.env` file for configuration. Ensure this file is never committed (it's in `.gitignore`).

### API Integration

- Uses OpenAI API for conversation and context extraction
- Requires valid API key with appropriate permissions
- API calls are made synchronously within the Streamlit session

### Data Storage

- Context data is exported as markdown files
- Format is designed for vector database ingestion
- File naming convention: `context_data_YYYYMMDD_HHMMSS.md`

## Workflow Pattern

1. User specifies area of focus for the interview
2. AI agent generates contextually relevant questions
3. User responds to questions in conversational format
4. Agent adapts follow-up questions based on responses
5. Upon completion, system extracts structured context
6. Context is formatted and exported as downloadable markdown

The intended use case involves conducting multiple interview sessions over time, incrementally building a comprehensive personal context repository for RAG-enhanced LLM interactions.

## Integration Examples

The markdown output can be integrated with:
- **Vector Databases**: Ingest into Pinecone, ChromaDB, Weaviate, Qdrant
- **RAG Frameworks**: Use with LangChain or LlamaIndex pipelines
- **Custom Systems**: Parse markdown for custom retrieval implementations
- **Training Data**: Format for fine-tuning or model training

## Attribution

- **Development**: Claude (Anthropic)
- **Project Direction and Implementation**: Daniel Rosehill
- **Collaboration**: This project demonstrates human-AI collaboration in building practical AI tools

## License

MIT License

## Additional Resources

- **Hugging Face Space**: [AI-Context-Generation-Interviews](https://huggingface.co/spaces/danielrosehill/AI-Context-Generation-Interviews)
- **Developer Website**: [danielrosehill.com](https://danielrosehill.com)

## Working on This Project

### For AI Assistants

When working on this codebase:
- The main application logic is in `app.py`
- Streamlit state management is used extensively for session persistence
- OpenAI API integration handles both interview questions and context extraction
- The output format (markdown) is critical for downstream RAG pipeline compatibility
- Error handling is important due to API dependencies

### Dependencies

See `requirements.txt` for the complete list. Key dependencies:
- streamlit
- openai
- python-dotenv (implied by .env usage)

### Desktop Integration

The project includes:
- `Streamlit-App.desktop`: Desktop launcher file for Linux environments
- `run.sh`: Shell script for easy application startup
- `app.spec`: PyInstaller specification for creating standalone executables

## Future Enhancements

Potential areas for expansion:
- Support for additional LLM providers (Anthropic, local models)
- Enhanced context extraction algorithms
- Direct vector database integration
- Multi-format export options
- Interview template customization
