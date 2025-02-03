# Context Extraction Demo

[![Made with Streamlit](https://img.shields.io/badge/Made%20with-Streamlit-FF4B4B.svg)](https://www.streamlit.io)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Hugging Face Space](https://img.shields.io/badge/🤗%20Hugging%20Face-Space-blue)](https://huggingface.co/spaces/danielrosehill/AI-Context-Generation-Interviews)

This project demonstrates an innovative approach to enhancing personalized Large Language Model (LLM) experiences through agentic workflow-based context extraction. The system showcases how AI agents can proactively generate and collect contextual data to improve the quality and relevance of LLM interactions.

## Purpose

The primary goal of this project is to illustrate how an agent-driven workflow can:
- Proactively identify and extract relevant contextual information
- Generate meaningful data that enhances LLM understanding
- Create more personalized and context-aware AI interactions
- Demonstrate practical implementation of agentic workflows in LLM systems

## Screenshots

### Step 1: AI agent asks you questions according to your preferred area of focus

![alt text](screenshots/2/1.png)

### Step 2: Sit back and talk about yourself for a while

The bot asked me if I could wake up with one magic power in the morning what would it be? This is the SFW version:

![alt text](screenshots/2/2.png)

### When you're done, click on 'End Interview' and your interview with the bot is done:

![alt text](screenshots/2/3.png)

### The chat transcript is then parsed, mined for contextual data, and reformatted for ingress to a RAG pipeline / vector DB

(Behind the scenes)

### You get your context data out the other end!

![alt text](screenshots/2/4.png)

### Download and load into an agent for personalised LLM!

The reformatted contextual data snippets from the interviews are provided as downloadable markdown files. Markdown was chosen for its compact nature, its versatility, and its ubiquitous presence in the world of large language models. 

![alt text](screenshots/2/5.png)

These marked on files can then be aggregated, uploaded, or added to a RAG pipeline and added to an agent for personalized large language model (LLM) experiences. 

An iterative workflow is envisioned whereby the user engages in a few interviews at a time, feeding these into vector database storage and progressively increasing the pool of personal context data available to the tools being worked with. 
 
## About

This project was developed through collaboration between [Daniel Rosehill](https://danielrosehill.com) and Claude (Anthropic). It serves as a practical demonstration of how AI systems can be designed to actively participate in context generation and enhancement, leading to more effective and personalized LLM experiences.

## Implementation

The system implements an agentic workflow that enables:
- Automated context extraction from user interactions
- Proactive generation of contextual metadata
- Integration of extracted context into LLM inference processes
- Enhanced personalization through accumulated contextual understanding

## Attribution

Development: Claude (Anthropic)
Project Direction and Implementation: Daniel Rosehill
