import language.filters as f

def test_normalize():
    assert f.normalize('Zeit-geist?') == 'zeitgeist'