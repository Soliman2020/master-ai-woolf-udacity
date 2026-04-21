# NASA Mission Intelligence: RAG-Based Chat System

A Retrieval-Augmented Generation (RAG) system for querying NASA space mission documents with real-time RAGAS evaluation.

***

## Project Overview

This project implements a RAG-based chat system that allows users to ask questions about NASA space missions (Apollo 11, Apollo 13, Challenger). It uses ChromaDB for vector storage, OpenAI embeddings for semantic search, and RAGAS metrics for real-time response quality evaluation.

***

## Prerequisites

- Python 3.8 or higher
- OpenAI API key (or Vocareum API key)

***

## Installation

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs all required packages including:

- `chromadb` - Vector database
- `openai` - OpenAI API client
- `langchain-openai` - LangChain OpenAI integration
- `ragas` - RAG evaluation metrics
- `streamlit` - Web interface
- `nest-asyncio` - Async support for Streamlit

***

## Usage

### Step 2: Activate the Embedding Pipeline

Create embeddings from NASA mission documents:

```bash
python embedding_pipeline.py --data-path data_text --stats-only --openai-key "YOUR-OPENAI/VOC-KEY"
```

**Options:**

- `--data-path` - Directory containing mission data folders (default: `.`)
- `--chroma-dir` - ChromaDB persist directory (default: `./chroma_db_openai`)
- `--collection-name` - Collection name (default: `nasa_space_missions_text`)
- `--chunk-size` - Text chunk size (default: 500)
- `--chunk-overlap` - Chunk overlap size (default: 100)
- `--update-mode` - How to handle existing documents: `skip`, `update`, or `replace`
- `--stats-only` - Show collection statistics only (no processing)

**Example - Full processing:**

```bash
python embedding_pipeline.py --data-path data_text --update-mode skip
```

**Example - Replace all documents:**

```bash
python embedding_pipeline.py --data-path data_text --update-mode replace
```

***

### Step 3: Run the Chat Application

Launch the Streamlit web interface:

```bash
streamlit run chat.py
```

The application will:

1. Display available ChromaDB backends
2. Allow you to select a document collection
3. Provide a chat interface for asking questions
4. Show real-time RAGAS evaluation metrics

***

### Step 4: Run Batch Evaluation (Optional)

Evaluate the system against a test question set:

```bash
python run_evaluation.py --openai-key "YOUR_OPENAI_KEY" --chroma-dir chroma_db_openai --collection nasa_space_missions_text --test-questions test_questions.json --output evaluation_results.json
```

**Arguments:**

- `--openai-key` - Your OpenAI API key (required)
- `--chroma-dir` - ChromaDB directory (default: `./chroma_db_openai`)
- `--collection` - Collection name (default: `nasa_space_missions_text`)
- `--test-questions` - Test questions JSON file (default: `test_questions.json`)
- `--output` - Output file for results (default: `evaluation_results.json`)

***

## Project Structure

```
nasa/
├── embedding_pipeline.py    # ChromaDB embedding creation
├── rag_client.py            # Document retrieval functions
├── llm_client.py            # LLM response generation
├── ragas_evaluator.py       # RAGAS evaluation metrics
├── chat.py                  # Streamlit chat interface
├── run_evaluation.py        # Batch evaluation script
├── test_questions.json      # Test question set
├── requirements.txt         # Python dependencies
├── data_text/               # NASA mission documents
│   ├── apollo11/
│   ├── apollo13/
│   └── challenger/
└── chroma_db_openai/        # ChromaDB vector store
```

***

## Key Files

| File                    | Purpose                                                             |
| ----------------------- | ------------------------------------------------------------------- |
| `embedding_pipeline.py` | Creates ChromaDB collection with OpenAI embeddings                  |
| `rag_client.py`         | Handles ChromaDB connection, document retrieval, context formatting |
| `llm_client.py`         | Generates LLM responses with context grounding                      |
| `ragas_evaluator.py`    | Evaluates response quality using RAGAS metrics                      |
| `chat.py`               | Streamlit web interface for interactive chat                        |
| `run_evaluation.py`     | Batch evaluation on test questions                                  |

***

## Features

- **Semantic Search**: Retrieves relevant documents using OpenAI embeddings
- **Mission Filtering**: Filter results by Apollo 11, Apollo 13, or Challenger
- **Context Grounding**: LLM responses cite specific sources from retrieved documents
- **Real-time Evaluation**: RAGAS metrics (Faithfulness, Response Relevancy, BLEU, ROUGE)
- **Conversation History**: Maintains chat context across multiple turns
- **Batch Evaluation**: Evaluate system performance on test question sets

***

## RAGAS Metrics

The system evaluates responses using:

| Metric                 | Description                                          |
| ---------------------- | ---------------------------------------------------- |
| **Faithfulness**       | How well the answer is grounded in retrieved context |
| **Response Relevancy** | How relevant the answer is to the question           |
| **BLEU Score**         | N-gram overlap metric                                |
| **ROUGE Score**        | Recall-oriented metric                               |
| **Context Precision**  | Quality of retrieved context                         |

***

## Configuration

### Environment Variables

```bash
export OPENAI_API_KEY="your-api-key-here"
```

Or enter the API key directly in the Streamlit interface.

***

## Troubleshooting

### No ChromaDB backends found

Run the embedding pipeline first:

```bash
python embedding_pipeline.py --data-path data_text
```

### RAGAS metrics showing 0.00

Ensure you have a valid OpenAI API key and the RAGAS package is installed correctly.

### Import errors

Reinstall dependencies:

```bash
pip install -r requirements.txt --upgrade
```

***

## License

This project is for educational purposes as part of the Udacity Generative AI Nanodegree.
