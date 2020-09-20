#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import feedparser

import language.filters as lf
import language.words as w

SPON_RSS = 'https://www.spiegel.de/schlagzeilen/index.rss'

MAX_DYNAMIC_SIZE_GAIN = 22
MIN_SIZE = 10
def format_as_html(words, old_words):
    buf = ['<h3><a href="https://www.spiegel.de" target="_blank">spiegel.de</a></h3>']

    min_count = words[-1].usage_count if len(words) else 0
    max_count = words[0].usage_count if len(words) else 0
    buf.append(f'<p>{max_count} to {min_count} occurrences</p>')
    buf.append('<p>')
    last_font_size = -1
    for word in words:
        font_scale = (word.usage_count - min_count) / float(max_count - min_count)
        font_size = int(font_scale * MAX_DYNAMIC_SIZE_GAIN + MIN_SIZE)
        if last_font_size == -1:
            last_font_size = font_size
        elif last_font_size > font_size:
            last_font_size = font_size
            buf.append('<br>')
        color = 'blue'
        if word.is_new():
            color = 'green'
        buf.append(f'<span style="font-size:{font_size}pt;padding:2pt"><a href="news_links.html#{word.word}" style="color:{color}">{word.word}</a></span>')
    buf.append('</p>')
    if len(old_words):
        buf.append('<p style="font-size:12pt;color:red;">')
        buf.append(' '.join([w.word for w in old_words]))
        buf.append('</p>')
    return '\n'.join(buf)

def format_as_html_links_list(words):
    buf = ['<h1>News Links</h1>']
    buf.append('<a href="index.html">back</a>')
    for word in words:
        w = word.word
        buf.append('<p>')
        buf.append(f'<h3><a name="{w}">{w}</a></h3>')
        buf.append('<ul>')
        for link in word.links:
            buf.append(f'<li><a href="{link}" target="_blank">{link}</a></li>')
        buf.append('</ul>')
        buf.append('</p>')
    return '\n'.join(buf)


DE_WORDDB = 'de.json'
def main():
    spon = feedparser.parse(SPON_RSS)
    worddb = w.worddb_from_file(DE_WORDDB)
    for item in spon['items']:
        link = item['link']
        if not link.startswith('https://www.spiegel.de/international/'): # don't mix DE and EN, focus on just DE for now
            worddb.add_words(item['title'], link)
            worddb.add_words(item['summary'], link)

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
