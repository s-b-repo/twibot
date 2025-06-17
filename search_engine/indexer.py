import os
import re
import math
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict, List, Tuple

@dataclass
class Document:
    doc_id: str
    text: str
    length: int

@dataclass
class Indexer:
    documents: Dict[str, Document] = field(default_factory=dict)
    inverted_index: Dict[str, Dict[str, int]] = field(default_factory=lambda: defaultdict(dict))
    doc_freq: Dict[str, int] = field(default_factory=lambda: defaultdict(int))
    total_docs: int = 0
    base_dir: str | None = None

    token_pattern = re.compile(r"\w+")

    def index_directory(self, directory: str) -> None:
        """Index all .txt files in a directory recursively."""
        self.base_dir = directory
        for root, _, files in os.walk(directory):
            for name in files:
                if name.lower().endswith('.txt'):
                    path = os.path.join(root, name)
                    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                        text = f.read()
                    doc_id = os.path.relpath(path, directory)
                    self.add_document(doc_id, text)

    def add_document(self, doc_id: str, text: str) -> None:
        tokens = self.tokenize(text)
        self.documents[doc_id] = Document(doc_id, text, len(tokens))
        token_counts: Dict[str, int] = defaultdict(int)
        for token in tokens:
            token_counts[token] += 1
        for token, count in token_counts.items():
            self.inverted_index[token][doc_id] = count
            self.doc_freq[token] += 1
        self.total_docs += 1

    def tokenize(self, text: str) -> List[str]:
        return [t.lower() for t in self.token_pattern.findall(text)]

    def search(self, query: str) -> List[Tuple[str, float]]:
        tokens = self.tokenize(query)
        if not tokens:
            return []
        doc_scores: Dict[str, float] = defaultdict(float)
        for token in tokens:
            postings = self.inverted_index.get(token, {})
            if not postings:
                continue
            df = self.doc_freq[token]
            idf = math.log((1 + self.total_docs) / (1 + df)) + 1
            for doc_id, tf in postings.items():
                tf_norm = tf / self.documents[doc_id].length
                doc_scores[doc_id] += tf_norm * idf
        return sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)
