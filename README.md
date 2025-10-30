# Context Extraction Demo

[![Made with Streamlit](https://img.shields.io/badge/Made%20with-Streamlit-FF4B4B.svg)](https://www.streamlit.io)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Hugging Face Space](https://img.shields.io/badge/🤗%20Hugging%20Face-Space-blue)](https://huggingface.co/spaces/danielrosehill/AI-Context-Generation-Interviews)

This project demonstrates a workflow pattern for building personalized LLM context through conversational data extraction. The system uses an AI agent to conduct interviews, extract contextual information, and format it for use in RAG pipelines.

## Purpose

This project models a workflow where an AI agent conducts structured interviews to build a personal context repository. The implementation:
- Extracts contextual information through conversational interviews
- Outputs structured markdown files suitable for vector database ingestion
- Maintains platform-agnostic data storage for use across different LLM systems
- Provides a reference implementation of agent-driven context collection

## Use Cases

### Primary Use Case: Personal RAG Pipeline
- Iteratively build a personal context collection through structured interviews
- Store context in portable markdown format for integration with any vector database
- Compatible with local RAG systems (LlamaIndex, ChromaDB) or cloud platforms (Pinecone, Weaviate)
- Expand context repository through repeated interview sessions

### Additional Use Cases
- Training data for personal AI assistants
- Structured documentation of domain expertise
- Team knowledge capture and onboarding materials
- Interview data collection for research purposes

### Integration Examples
- Vector databases: Pinecone, ChromaDB, Weaviate, Qdrant
- RAG frameworks: LangChain, LlamaIndex
- Custom retrieval pipelines
- Fine-tuning datasets

## Screenshots

### Step 1: AI agent asks you questions according to your preferred area of focus

 ![alt text](screenshots/v2/1.png)

### Step 2: Interview conversation flow

The agent generates contextually relevant questions based on responses:

 ![alt text](screenshots/v2/2.png)

### Step 3: Complete the interview session

 ![alt text](screenshots/v2/3.png)

### Step 4: Context extraction and formatting

The system parses interview transcripts and extracts structured context data suitable for vector database ingestion.

### Step 5: Export formatted context data

Context is exported as downloadable markdown files:

![alt text](screenshots/2/5.png)

The markdown format provides a compact, portable structure compatible with most LLM and vector database systems.

### Workflow Pattern

The intended workflow involves conducting multiple interview sessions over time, with each session adding to the personal context repository. This incremental approach builds a comprehensive context dataset for RAG-enhanced LLM interactions. 
 
## About

This project was developed through collaboration between [Daniel Rosehill](https://danielrosehill.com) and Claude (Anthropic). It demonstrates a workflow pattern for agent-driven context collection and RAG pipeline data preparation.

## Implementation

Built with Streamlit and OpenAI API, implementing an agent-driven interview workflow:

### Core Features
- **Interview System**: Conversational interface for conducting structured interviews via OpenAI API
- **Question Generation**: Context-aware follow-up questions based on prior responses
- **API Key Management**: Local storage and configuration for OpenAI credentials
- **Session Management**: State preservation across interview sessions
- **Context Extraction**: LLM-based processing to extract structured context from interview transcripts

### Technical Components
- **Frontend**: Streamlit interface
- **Backend Processing**:
  - OpenAI API integration for conversation and context extraction
  - Local file system for configuration and session data
  - Markdown generation pipeline
- **Data Export**: Markdown file generation for extracted context
- **Configuration**: Local storage for API keys and settings

### User Interface
- Chat interface with conversation history
- Session progress tracking
- Markdown file download
- API key configuration
- Error handling

### Integration Architecture
- Context output formatted for vector database ingestion
- Platform-agnostic markdown storage
- Compatible with RAG frameworks (LangChain, LlamaIndex)
- Suitable for training data or fine-tuning datasets

## Attribution

Development: Claude (Anthropic)
Project Direction and Implementation: Daniel Rosehill
