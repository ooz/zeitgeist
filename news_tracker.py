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

    buf = [f'<h3><a href="https://www.spiegel.de" target="_blank">spiegel.de</a> ({max_count} to {min_count} occurrences)</h3>']
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
    buf.append('<p>Legend: <span class="new">new</span>, <span class="current">current</span>, <span class="former">former(days relevant)</span></p>')
    return '\n'.join(buf)

def format_as_html_links_list(words):
    buf = ['<!DOCTYPE html>']
    buf.append('<html><head>')
    buf.append('<link rel="stylesheet" type="text/css" href="static/oz.css" />')
    buf.append('<link rel="stylesheet" type="text/css" href="static/zeitgeist.css" />')
    buf.append('<script src="static/oz-dark-mode.js"></script>')
    buf.append('</head><body onload="initTheme()">')
    buf.append('<header><a href="index.html"><h1>News Links</h1></a></header>')
    buf.append('<section>')
    for word in words:
        w = word.word
        buf.append('<p>')
        buf.append(f'<a name="{w}"></a><h3>{w}</h3>')
        buf.append('<ul>')
        for link in word.links:
            buf.append(f'''<li><a href="{link.replace('#ref=rss', '')}" target="_blank" class="current">{link}</a></li>''')
        buf.append('</ul>')
        buf.append('</p>')
    buf.append('</section>')
    buf.append('<footer><a href="index.html" class="nav">back</a><a href="javascript:toggleTheme()" class="nav">🌓</a></footer>')
    buf.append('</body></html>')
    return '\n'.join(buf)


DE_WORDDB = 'de.json'
def main():
    spon = feedparser.parse(SPON_RSS)
    worddb = w.WordDB()
    for item in spon['items']:
        link = item['link']
        if not link.startswith('https://www.spiegel.de/international/'): # don't mix DE and EN, focus on just DE for now
            worddb.add_words(item['title'], link)
            worddb.add_words(item['summary'], link)

    worddb_from_file = w.worddb_from_file(DE_WORDDB)
    worddb = worddb.merge(worddb_from_file)

    occured_at_least_twice = [w for w in worddb.words_by_usage() if w.usage_count > 1]
    old_words = worddb.old_words()

    with open('news.html', 'w') as f:
        formatted = format_as_html(occured_at_least_twice, old_words) + '\n'
        f.write(formatted)

    with open('news_links.html', 'w') as f:
        formatted = format_as_html_links_list(occured_at_least_twice) + '\n'
        f.write(formatted)

    with open(DE_WORDDB, 'w') as f:
        f.write(worddb.as_json())

if __name__ == '__main__':
    main()
