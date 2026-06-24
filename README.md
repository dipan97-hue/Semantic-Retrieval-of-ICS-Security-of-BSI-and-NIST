# OT Cybersecurity RAG Pipeline

An advanced Retrieval-Augmented Generation (RAG) system designed for querying and analyzing OT (Operational Technology) cybersecurity standards. This project integrates multiple security frameworks (BSI and NIST) with Large Language Models (LLMs) to provide intelligent responses to cybersecurity questions.

## Overview

This thesis project implements a comprehensive RAG pipeline that:

- **Extracts and processes** security standards from BSI and NIST PDF documents
- **Embeds** security requirements using sentence transformers
- **Retrieves** relevant context from a vector database (Supabase)
- **Generates** contextual answers using multiple LLM providers
- **Evaluates** response quality with an LLM-based judge
- **Maps** requirements across different security frameworks
- **Provides an interactive UI** via Streamlit for easy querying

## Key Features

### 1. **Multi-Standard Support**
   - **BSI Standard 2001**: German IT security standard for operational technology
   - **NIST SP 800-82 Rev 3**: NIST cybersecurity framework for industrial control systems

### 2. **Multiple LLM Integration**
   - OpenAI (GPT models)
   - Google Gemini
   - Anthropic Claude
   - Mistral
   - Support for local models via Ollama
   - Intelligent LLM routing based on query complexity

### 3. **Semantic Search & Retrieval**
   - Vector embeddings using sentence-transformers (all-MiniLM-L6-v2)
   - K-nearest neighbor retrieval from Supabase vector database
   - Query expansion for improved retrieval accuracy
   - Re-ranking of results for relevance optimization

### 4. **Requirement Mapping**
   - Automatic mapping between BSI and NIST requirements
   - Lifecycle phase tracking (Planning, Implementation, Monitoring, Optimization)
   - Normative type classification

### 5. **Response Evaluation**
   - LLM-based quality assessment of generated answers
   - Relevance scoring of retrieved context
   - Automated evaluation metrics

## Project Structure

```
├── app.py                          # Streamlit web application
├── requirements.txt                # Python dependencies
├── config/                         # Configuration files
│   └── config.py                  # API keys and environment setup
├── etl/                           # Extract-Transform-Load pipeline
│   ├── bsi_extract.py            # BSI standard extraction
│   ├── nist_extract.py           # NIST standard extraction
│   ├── chunking.py               # Document chunking strategy
│   ├── cleaning.py               # Data cleaning utilities
│   ├── lifecycle_bsi.py          # BSI lifecycle mapping
│   ├── lifecycle_nist.py         # NIST lifecycle mapping
│   ├── combined_dataset.py       # Dataset merging
│   └── pipeline.py               # Main ETL orchestration
├── embeddings/                    # Embedding models
│   ├── embedding_model.py        # Embedding model initialization
│   ├── embeddings.py             # Embedding generation
│   └── requirement_mapping.py    # Mapping utilities
├── rag/                          # RAG pipeline
│   └── rag_pipeline.py           # Main RAG orchestration
├── retrieval/                    # Retrieval components
│   ├── retrieve.py               # Vector retrieval
│   ├── query_expansion.py        # Query enhancement
│   ├── reranker.py               # Result re-ranking
│   ├── mappings.py               # Cross-standard mappings
│   └── context_building.py       # Context preparation
├── llm/                          # LLM integrations
│   ├── gpt_llm.py                # OpenAI integration
│   ├── gemini_llm.py             # Google Gemini integration
│   ├── anthropic_llm.py          # Anthropic Claude integration
│   ├── mistral_llm.py            # Mistral integration
│   ├── llm_router.py             # Intelligent LLM selection
│   ├── llm_judge.py              # Response evaluation
│   └── role_generator.py         # Role-based prompt generation
├── prompts/                      # Prompt templates
│   └── prompt_builder.py         # Dynamic prompt construction
├── storage/                      # Database integrations
│   ├── supabase_bsi.py           # BSI data storage
│   ├── supabase_nist.py          # NIST data storage
│   ├── supabase_combined.py      # Combined dataset storage
│   └── supabase_mapping.py       # Mapping storage
├── Runs/                         # Execution management
│   ├── run_etl.py                # ETL pipeline execution
│   └── run_db.py                 # Database operations
├── evaluation/                   # Evaluation utilities
│   └── ares.py                   # ARES evaluation framework
└── Json Files/                   # Processed data
    ├── bsi_standard.json
    ├── nist_standard.json
    └── combined_dataset.json
```

## Installation

### Prerequisites
- Python 3.8+
- Supabase account for vector database
- API keys for LLM providers (OpenAI, Gemini, Anthropic, Mistral)

### Setup

1. **Clone the repository** (or navigate to project directory)

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   Create a `.env` file in the root directory:
   ```
   SUPABASE_URL=your_supabase_url
   SUPABASE_KEY=your_supabase_key
   OPENAI_API_KEY=your_openai_key
   GEMINI_API_KEY=your_gemini_key
   ANTHROPIC_API_KEY=your_anthropic_key
   MISTRAL_API_KEY=your_mistral_key
   ```

## Usage

### Running the Streamlit App

```bash
streamlit run app.py
```

The web interface provides:
- Query input field
- Model selection dropdown
- Interactive retrieval and generation
- Result display with mappings and lifecycle information
- Quality evaluation metrics

### Running the ETL Pipeline

To extract and process security standards:

```bash
python Runs/run_etl.py
```

This will:
1. Extract chunks from BSI PDF
2. Extract chunks from NIST PDF
3. Generate embeddings
4. Store data in Supabase vector database

### Testing

Run the test notebooks:
- `test_ollama.ipynb` - Test local LLM integration
- `bsi_to_json.ipynb` - Test BSI extraction
- `nsit_to_json.ipynb` - Test NIST extraction
- `unified.ipynb` - Test complete pipeline

## How It Works

### Query Processing Pipeline

1. **Embedding**: User query is converted to vector embedding
2. **Retrieval**: Top-k relevant chunks retrieved from vector database
3. **Enrichment**: Retrieved chunks enriched with requirement mappings
4. **Context Building**: Retrieved context formatted for LLM
5. **Generation**: LLM generates answer based on context
6. **Evaluation**: Response evaluated for quality and relevance

### LLM Routing

The system intelligently selects the best LLM based on:
- Query complexity
- Required expertise
- Available API keys
- Fallback mechanisms for redundancy

## Dependencies

Key libraries:
- **streamlit**: Web UI framework
- **sentence-transformers**: Semantic embedding models
- **supabase-py**: Vector database client
- **openai**: OpenAI API
- **google-generativeai**: Google Gemini API
- **anthropic**: Claude API
- **mistralai**: Mistral API
- **pymupdf**: PDF processing
- **pandas**: Data manipulation
- **scikit-learn**: ML utilities
- **nltk**: NLP processing

## Configuration

The system is configured via:
- `config/config.py`: API keys and endpoints
- `.env` file: Environment variables
- Streamlit session state: Runtime parameters


## Link to the app --- https://semantic-retrieval-of-ics-security.streamlit.app/

## License

This project is for research and educational purposes.
