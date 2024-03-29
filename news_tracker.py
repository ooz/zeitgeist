#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import feedparser

import language.filters as lf
import language.words as w

SPON_RSS = 'https://www.spiegel.de/schlagzeilen/index.rss'

MAX_DYNAMIC_SIZE_GAIN = 20
MIN_SIZE = 12
def format_as_html(words, old_words):
    min_count = words[-1].usage_count if len(words) else 0
    max_count = words[0].usage_count if len(words) else 0

    buf = [f'<h3><a href="https://www.spiegel.de" target="_blank">spiegel.de</a> (German, {max_count} to {min_count} occurrences)</h3>']
    buf.append('<p style="font-family:monospace">')
    last_font_size = -1
    for word in words:
        font_scale = (word.usage_count - min_count) / float(max_count - min_count)
        font_size = int(font_scale * MAX_DYNAMIC_SIZE_GAIN + MIN_SIZE)
        if last_font_size == -1:
            last_font_size = font_size
        elif last_font_size > font_size:
            last_font_size = font_size
            buf.append('<br>')
        color = 'current'
        if word.is_new():
            color = 'new'
        buf.append(f'<span style="font-size:{font_size}pt"><a href="news_links.html#{word.word}" class="{color}">{word.word}</a></span>')
    buf.append('</p>')
    if len(old_words):
        buf.append('<details>')
        buf.append('<summary>Stopped using...</summary>')
        buf.append('<p class="former" style="font-size:12pt">')
        buf.append(' '.join([f'{w.word}({w.relevant_for_days()})' for w in old_words if w.relevant_for_days() >= 5]))
        buf.append('</p>')
        buf.append('</details>')
    buf.append('''<p>Legend:
<ul>
<li><span class="new">new</span>, first seen within the last 10 days</li>
<li><span class="current">current</span>, regular topical words used in the news, not "new", not "former"</li>
<li><span class="former">former(days span relevant)</span>, not used in the last 30 days, but still re-occurring enough to not get deleted</li>
<li>Only words which occurred at least twice in the RSS feed are tracked. <a href="language/filters.py">Some common words are blocked</a></li>
<li>Words not used for more than 90 days get deleted from the database, but may re-enter as "new" words when used again</li>
</ul>
</p>''')
    return '\n'.join(buf)

def format_as_markdown_links_list(words):
    buf = ['---']
    buf.append('tags: __no_header__')
    buf.append('---')
    buf.append('')
    buf.append('# [Zeitgeist News Links](index.html)')
    buf.append('')
    for word in words:
        w = word.word
        buf.append(f'### {w}')
        buf.append('')
        for link in word.links:
            #                      v-- removes the trailing '#ref=rss' and hash
            buf.append(f'''* [{link[:-47]}]({link})''')
    buf.append('')
    return '\n'.join(buf)


DE_WORDDB = 'de.json'
def main():
    spon = feedparser.parse(SPON_RSS)
    worddb = w.WordDB()
    for item in spon['items']:
        link = item['link']
        if not link.startswith('https://www.spiegel.de/international/'): # don't mix DE and EN, focus on just DE for now
            worddb.add_words(item['title'], link)
            summary = item.get('summary', None)
            if summary:
                worddb.add_words(summary, link)

    worddb_from_file = w.worddb_from_file(DE_WORDDB)
    worddb = worddb.merge(worddb_from_file)

    occured_at_least_twice = [w for w in worddb.words_by_usage() if w.usage_count > 1]
    old_words = worddb.old_words()

    with open('news.html', 'w') as f:
        formatted = format_as_html(occured_at_least_twice, old_words) + '\n'
        f.write(formatted)

    with open('news_links.md', 'w') as f:
        formatted = format_as_markdown_links_list(occured_at_least_twice) + '\n'
        f.write(formatted)

    with open(DE_WORDDB, 'w') as f:
        f.write(worddb.as_json())

if __name__ == '__main__':
    main()
