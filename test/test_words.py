import language.words as w

def test_read_worddb_from_file():
    db = w.worddb_from_file('test/example_worddb.json')
    assert db.words.keys() == set({'auto', 'welt', 'zeit'})
    assert db.words['zeit'].links == []
    assert db.words['zeit'].usage_count == 0
    assert db.words['zeit'].first == '2020-08-24'
    assert db.words['zeit'].last == '2020-09-01'