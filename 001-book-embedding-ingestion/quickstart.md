# Quickstart: Book Embedding Ingestion Pipeline

## Prerequisites
- Python 3.11 or higher
- pip package manager
- Git for version control
- Cohere API key
- Qdrant Cloud account and API key

## Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Create Backend Directory
```bash
mkdir backend
cd backend
```

### 3. Set up Python Environment
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install uv (if not already installed)
pip install uv
```

### 4. Create Project Structure
```bash
mkdir -p src/ingestion src/embeddings src/storage tests/unit tests/integration
```

### 5. Create Requirements File
Create `backend/requirements.txt`:
```
requests>=2.31.0
beautifulsoup4>=4.12.2
cohere>=4.0.0
qdrant-client>=1.9.0
python-dotenv>=1.0.0
pytest>=7.4.0
```

### 6. Create Configuration File
Create `backend/.env.example`:
```
COHERE_API_KEY=your_cohere_api_key_here
QDRANT_URL=your_qdrant_cluster_url
QDRANT_API_KEY=your_qdrant_api_key
QDRANT_COLLECTION_NAME=docs_embeddings
DOCUMENTATION_URLS=https://example-docusaurus-site.com
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
EMBEDDING_MODEL=embed-english-v3.0
```

## Installation

### 1. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your actual API keys and URLs
# (edit the .env file with your preferred editor)
```

## Usage

### 1. Run the Ingestion Pipeline
The main pipeline is executed through the `main.py` file:

```bash
cd backend
python -m src.ingestion.main
```

### 2. Pipeline Steps
The ingestion pipeline performs the following steps:
1. Crawls specified Docusaurus URLs
2. Extracts clean text content from HTML
3. Chunks the text into appropriate segments
4. Generates embeddings using Cohere
5. Stores embeddings in Qdrant vector database

### 3. Custom Configuration
You can customize the pipeline behavior by modifying environment variables:
- `DOCUMENTATION_URLS`: Comma-separated list of URLs to crawl
- `CHUNK_SIZE`: Size of text chunks in characters (default: 1000)
- `CHUNK_OVERLAP`: Overlap between chunks in characters (default: 200)
- `EMBEDDING_MODEL`: Cohere model to use for embeddings (default: embed-english-v3.0)

## Testing

### Run Unit Tests
```bash
cd backend
pytest tests/unit/
```

### Run Integration Tests
```bash
cd backend
pytest tests/integration/
```

## Development

### Project Structure
```
backend/
├── src/
│   ├── ingestion/
│   │   ├── __init__.py
│   │   ├── crawler.py
│   │   ├── cleaner.py
│   │   ├── chunker.py
│   │   └── main.py
│   ├── embeddings/
│   │   ├── __init__.py
│   │   └── generator.py
│   └── storage/
│       ├── __init__.py
│       └── qdrant_client.py
├── tests/
│   ├── unit/
│   └── integration/
├── requirements.txt
├── .env
└── .env.example
```

### Adding New Documentation Sources
To add new documentation sources:
1. Update the `DOCUMENTATION_URLS` environment variable
2. Ensure the site follows Docusaurus patterns for proper content extraction
3. Test the crawling process to verify content extraction quality