# Voices of Independence: An AI-Powered Time Travel Through 1776

An interactive experience exploring American Independence through historical documents using LLMs and semantic search.

## Project Overview

This project creates an AI-powered interactive experience where users can explore American Independence through historical archives. It combines:

- **Weaviate**: For vector search and semantic retrieval of historical documents
- **FriendliAI**: For LLM inference to generate human-like responses 
- **Comet Opik**: For observability and tracing of our RAG system

## Features

- **Semantic Search**: Find relevant historical documents based on natural language queries
- **Multiple Response Modes**: 
  - Expert Historian: Objective, factual responses
  - Benjamin Franklin: Responses in the persona of a founding father
  - Time-Traveling Guide: Modern perspective looking back at historical events
- **Document Timeline**: Visualize historical documents on an interactive timeline
- **System Evaluation**: Built-in metrics to evaluate retrieval and response quality

## Setup Instructions

### Prerequisites

You'll need accounts with:
- [Weaviate](https://weaviate.io/) - For vector search
- [FriendliAI](https://friendli.ai/) - For LLM inference
- [Comet](https://www.comet.com/) - For observability with Opik

### Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/voices-of-independence.git
   cd voices-of-independence
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Copy example environment file and add your API keys:
   ```
   cp .env.example .env
   # Edit .env with your API keys
   ```

4. Run the application:
   ```
   python main.py
   ```

## Usage

### Command Line Demo

```
python main.py --query "What were the key arguments for independence in 1776?" --mode historian
```

### Web Interface

Start the Gradio web interface:

```
python -m ui.gradio_app
```

Then open your browser to the URL displayed in the terminal (typically http://127.0.0.1:7860).

## Project Structure

- `data/`: Document sources and processing functions
- `database/`: Weaviate setup and operations
- `rag/`: RAG system components
- `ui/`: User interfaces (Gradio and React)
- `utils/`: Utility functions
- `main.py`: Application entry point

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Historical documents sourced from [The National Archives](https://www.archives.gov/), [Founders Online](https://founders.archives.gov/), and [Project Gutenberg](https://www.gutenberg.org/)
- Built with Weaviate, FriendliAI, and Comet Opik
