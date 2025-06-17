# Simple Search Engine

This repository provides a minimal search engine that indexes text files and provides a web interface for searching.

## Usage

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Index a directory and start the web interface:
   ```bash
   python -m search_engine.web /path/to/text/files
   ```

3. Open your browser to `http://localhost:5000` and perform searches.

## Testing

Run tests with:
```bash
python -m pytest
```
