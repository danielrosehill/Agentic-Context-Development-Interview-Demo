# Contributing to Agentic Context Development Interview Demo

Thank you for your interest in contributing to this project! This guide will help you get started.

## Development Setup

### Prerequisites

- Python 3.8 or higher
- Git
- OpenAI API key (for testing)

### Local Development

1. Fork and clone the repository:
   ```bash
   git clone https://github.com/danielrosehill/Agentic-Context-Development-Interview-Demo.git
   cd Agentic-Context-Development-Interview-Demo
   ```

2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your environment variables:
   ```bash
   cp .env.example .env  # If example exists
   # Add your OpenAI API key to .env
   ```

5. Run the application:
   ```bash
   streamlit run app.py
   ```

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue with:
- A clear, descriptive title
- Steps to reproduce the issue
- Expected behavior
- Actual behavior
- Your environment (OS, Python version, etc.)
- Screenshots if applicable

### Suggesting Enhancements

Enhancement suggestions are welcome! Please open an issue with:
- A clear description of the enhancement
- Use cases and benefits
- Any implementation ideas you have

### Pull Requests

1. Fork the repository
2. Create a new branch for your feature (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test your changes thoroughly
5. Commit your changes (`git commit -m 'Add some amazing feature'`)
6. Push to your branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Pull Request Guidelines

- Keep changes focused and atomic
- Update documentation as needed
- Follow existing code style and conventions
- Test your changes with different scenarios
- Include clear commit messages

## Code Style

- Follow PEP 8 style guide for Python code
- Use meaningful variable and function names
- Add comments for complex logic
- Keep functions focused and single-purpose

## Testing

Before submitting a pull request:
- Test the application end-to-end
- Verify interview flow works correctly
- Ensure context extraction produces valid markdown
- Test with different interview topics and response lengths
- Check error handling (invalid API keys, network issues, etc.)

## Areas for Contribution

Here are some areas where contributions would be particularly valuable:

### High Priority
- Support for additional LLM providers (Anthropic Claude, local models)
- Enhanced error handling and user feedback
- Interview template customization
- Multi-language support

### Medium Priority
- Direct vector database integration
- Enhanced context extraction algorithms
- Batch interview processing
- Export format options (JSON, YAML, etc.)

### Documentation
- Tutorial videos or guides
- Example use cases and workflows
- Integration examples with popular RAG frameworks
- API documentation

## Architecture Notes

### Key Components

**app.py**: Main Streamlit application
- Session state management for interview persistence
- OpenAI API integration for conversation and context extraction
- Markdown generation and export functionality

**Interview Flow**:
1. User inputs area of focus
2. OpenAI generates contextual questions
3. User responses are stored in session state
4. Follow-up questions adapt based on responses
5. Context extraction processes full conversation
6. Markdown output is generated for download

**Data Format**:
- Output is markdown for maximum compatibility
- Designed for vector database ingestion
- Platform-agnostic storage format

## Questions?

If you have questions about contributing, feel free to:
- Open an issue for discussion
- Contact Daniel Rosehill via [danielrosehill.com](https://danielrosehill.com)
- Check the [README.md](README.md) and [CLAUDE.md](CLAUDE.md) for project details

## License

By contributing, you agree that your contributions will be licensed under the same MIT License that covers this project.

## Acknowledgments

This project was developed through collaboration between Daniel Rosehill and Claude (Anthropic). All contributions help advance this demonstration of human-AI collaboration in building practical AI tools.
