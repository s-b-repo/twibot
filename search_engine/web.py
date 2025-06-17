from flask import Flask, request, render_template_string
from .indexer import Indexer

app = Flask(__name__)
indexer = Indexer()

template = """
<!doctype html>
<title>Simple Search Engine</title>
<h1>Search</h1>
<form action="/search" method="get">
  <input type="text" name="q" placeholder="Enter search query">
  <input type="submit" value="Search">
</form>
{% if results is not none %}
  <h2>Results</h2>
  <ul>
  {% for doc_id, score in results %}
    <li>{{ doc_id }} (score: {{ score }})</li>
  {% endfor %}
  </ul>
{% endif %}
"""

@app.route('/')
def home():
    return render_template_string(template, results=None)

@app.route('/search')
def search():
    query = request.args.get('q', '')
    results = indexer.search(query) if query else []
    return render_template_string(template, results=results)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Simple search engine web interface')
    parser.add_argument('directory', help='Directory of text files to index')
    parser.add_argument('--host', default='0.0.0.0')
    parser.add_argument('--port', type=int, default=5000)
    args = parser.parse_args()
    indexer.index_directory(args.directory)
    app.run(host=args.host, port=args.port)
