from search_engine.indexer import Indexer


def test_index_and_search(tmp_path):
    # create sample files
    file1 = tmp_path / "doc1.txt"
    file1.write_text("hello world")
    file2 = tmp_path / "doc2.txt"
    file2.write_text("hello python world")

    indexer = Indexer()
    indexer.index_directory(tmp_path)

    results = indexer.search("python")
    assert results[0][0] == "doc2.txt"
    assert results[0][1] > 0
