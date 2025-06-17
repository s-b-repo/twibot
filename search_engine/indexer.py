import os
import re
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict, List, Tuple

@dataclass
class Document:
    doc_id: str
    text: str

@dataclass
class Indexer:
    documents: Dict[str, Document] = field(default_factory=dict)
    inverted_index: Dict[str, Dict[str, List[int]]] = field(default_factory=lambda: defaultdict(lambda: defaultdict(list)))

    token_pattern = re.compile(r"\w+")

    def index_directory(self, directory: str) -> None:
        """Index all .txt files in a directory recursively."""
        for root, _, files in os.walk(directory):
            for name in files:
                if name.lower().endswith('.txt'):
                    path = os.path.join(root, name)
                    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                        text = f.read()
                    doc_id = os.path.relpath(path, directory)
                    self.add_document(doc_id, text)

    def add_document(self, doc_id: str, text: str) -> None:
        self.documents[doc_id] = Document(doc_id, text)
        tokens = self.tokenize(text)
        for position, token in enumerate(tokens):
            self.inverted_index[token][doc_id].append(position)

    def tokenize(self, text: str) -> List[str]:
        return [t.lower() for t in self.token_pattern.findall(text)]

    def search(self, query: str) -> List[Tuple[str, int]]:
        tokens = self.tokenize(query)
        if not tokens:
            return []
        doc_scores: Dict[str, int] = defaultdict(int)
        for token in tokens:
            postings = self.inverted_index.get(token, {})
            for doc_id, positions in postings.items():
                doc_scores[doc_id] += len(positions)
        return sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)
