from flask import Flask, request, render_template_string, send_from_directory, abort
from .indexer import Indexer

app = Flask(__name__)
indexer = Indexer()

template = """
<!doctype html>
<title>Simple Search Engine</title>
<h1>Search</h1>
<form action="/search" method="get">
  <input type="text" name="q" value="{{ query or '' }}" placeholder="Enter search query">
  <input type="submit" value="Search">
</form>
{% if results is not none %}
  <h2>Results</h2>
  {% if results %}
  <ul>
  {% for doc_id, snippet, score in results %}
    <li><a href="/doc/{{ doc_id }}">{{ doc_id }}</a> (score: {{ "%.2f"|format(score) }})<br>{{ snippet }}</li>
  {% endfor %}
  </ul>
  {% else %}
  <p>No results</p>
  {% endif %}
{% endif %}
"""

@app.route('/')
def home():
    return render_template_string(template, results=None, query=None)

@app.route('/search')
def search():
    query = request.args.get('q', '')
    results = []
    if query:
        tokens = indexer.tokenize(query)
        for doc_id, score in indexer.search(query):
            doc = indexer.documents[doc_id]
            snippet = _make_snippet(doc.text, tokens)
            results.append((doc_id, snippet, score))
    return render_template_string(template, results=results, query=query)

def _make_snippet(text: str, tokens: list, length: int = 160) -> str:
    text_lower = text.lower()
    start = None
    for token in tokens:
        pos = text_lower.find(token)
        if pos != -1 and (start is None or pos < start):
            start = pos
    if start is None:
        start = 0
    start = max(0, start - length // 2)
    snippet = text[start:start + length].replace('\n', ' ')
    if start > 0:
        snippet = '...' + snippet
    if start + length < len(text):
        snippet += '...'
    return snippet

@app.route('/doc/<path:doc_id>')
def serve_doc(doc_id):
    if indexer.base_dir is None:
        abort(404)
    return send_from_directory(indexer.base_dir, doc_id)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Simple search engine web interface')
    parser.add_argument('directory', help='Directory of text files to index')
    parser.add_argument('--host', default='0.0.0.0')
    parser.add_argument('--port', type=int, default=5000)
    args = parser.parse_args()
    indexer.index_directory(args.directory)
    app.run(host=args.host, port=args.port)
