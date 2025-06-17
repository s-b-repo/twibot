# Simple Search Engine

This repository provides a lightweight search engine that indexes text files and offers a small web interface to query them.  The indexer uses a TF–IDF ranking scheme for more relevant results and the web page displays snippets from the matched documents.

## Usage

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Index a directory and start the web interface:
   ```bash
   python -m search_engine.web /path/to/text/files
   ```

3. Open your browser to `http://localhost:5000` and perform searches.  Results include snippets and links to the indexed files.

## Testing

Run tests with:
```bash
python -m pytest
```
