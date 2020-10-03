import language.filters as f

def test_normalize():
    assert f.normalize('Zeit-geist?') == 'zeitgeist'

def test_normalize_linebreak():
    assert f.normalize('Zeit\ngeist?') == 'zeitgeist'
