import re

import language.words as w

def test_read_worddb_from_file():
    db = w.worddb_from_file('test/example_worddb.json')
    assert db.words.keys() == set({'auto', 'welt', 'zeit'})
    assert db.words['zeit'].links == []
    assert db.words['zeit'].usage_count == 0
    assert db.words['zeit'].first == '2020-08-24'
    assert db.words['zeit'].last == '2020-09-01'

def test_word_as_json_snippet():
    word = w.Word('zeit', None, 3, '2020-08-15', '2020-09-01')
    assert word._as_json_snippet() == '"zeit": {"first": "2020-08-15", "last": "2020-09-01"},'

def test_word_relevant_for_days():
    word = w.Word('zeit', None, 3, '2020-08-15', '2020-09-01')
    assert word.relevant_for_days() == 17

def test_word_as_empty_json_snippet_if_it_is_on_filter_list():
    word = w.Word('a', None, 1, '2020-08-15', '2020-09-01')
    assert word._as_json_snippet() == ''

def test_word_as_empty_json_if_obsolete():
    word = w.Word('a', None, 1, '2020-01-01', '2020-02-01')
    assert word._as_json_snippet() == ''

def test_worddb_as_json():
    worddb = w.WordDB()
    worddb.add_words('Brown wolf jumps. Brown wolf jumps.')
    assert re.match(r'''{
"brown": {"first": "\d{4}-\d{2}-\d{2}", "last": "\d{4}-\d{2}-\d{2}"},
"jumps": {"first": "\d{4}-\d{2}-\d{2}", "last": "\d{4}-\d{2}-\d{2}"},
"wolf": {"first": "\d{4}-\d{2}-\d{2}", "last": "\d{4}-\d{2}-\d{2}"}
}
''', worddb.as_json())

def test_worddb_should_retain_insertion_order():
    '''As of Python 3.6 dict retaining insertion order is an implementation detail of CPython
    With Python 3.7 it will be a language standard, see: https://github.com/naftaliharris/tauthon/issues/86
    WordDB retaining insertion order (as opposed to lexicographic order) is useful to see word contexts in
    the word cloud.
    '''
    worddb = w.WordDB()
    worddb.add_words('Alle satten Entchen. Alle satten Entchen.')
    worddb.add_words('Der Schwan sammelte alle satten Entchen.')

    by_usage = [word.word for word in worddb.words_by_usage()]
    assert by_usage == ['alle', 'satten', 'entchen', 'schwan', 'sammelte']

def test_merge_worddb():
    worddb = w.WordDB()
    worddb.add_words('Alle satten Entchen. Alle satten Entchen im Auto.')
    worddb_from_file = w.worddb_from_file('test/example_worddb.json')

    worddb.merge(worddb_from_file)

    by_usage = [word.word for word in worddb.words_by_usage()]
    assert by_usage == ['alle', 'satten', 'entchen', 'auto', 'welt', 'zeit']

def test_merge_word():
    #self, word, link=None, usage_count=1, first=None, last=None
    aword = w.Word('zeit', 'https://example.com', 3, '2020-05-15', '2020-05-15')
    other = w.Word('zeit', 'https://example.com/other', 1, '2020-01-15', '2020-03-15')

    aword = aword.merge(other)

    assert aword.word == 'zeit'
    assert aword.links == ['https://example.com']
    assert aword.usage_count == 4
    assert aword.first == '2020-01-15'
    assert aword.last == '2020-05-15'

def test_now():
    date = w._now_date()
    assert re.match(r'\d{4}-\d{2}-\d{2}', date)
