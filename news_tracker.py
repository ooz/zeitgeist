#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import feedparser

import language.filters as lf

SPON_RSS = 'https://www.spiegel.de/schlagzeilen/index.rss'

class Word(object):
    def __init__(self, word, link):
        self.word = word
        self.usage_count = 1
        self.links = [link]
    def add_occurrence(self, link):
        self.usage_count += 1
        if link not in self.links:
            self.links.append(link)
    def __str__(self):
        return f'({self.word}, {self.usage_count})'
    def __repr__(self):
        return str(self)


class WordDB(object):
    def __init__(self):
        self.words={}
    def add_words(self, text, link):
        words = text.split(' ')
        for word in words:
            w = lf.normalize(word)
            if len(w):
                if w in self.words.keys():
                    self.words[w].add_occurrence(link)
                else:
                    self.words[w] = Word(w, link)
    def words_by_usage(self):
        words = self.words.values()
        words = sorted(words, reverse=True, key=lambda w: w.usage_count)
        return list(words)

MAX_DYNAMIC_SIZE_GAIN = 22
MIN_SIZE = 10
def format_as_html(words):
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
        buf.append(f'<span style="font-size:{font_size}pt;padding:2pt"><a href="news_links.html#{word.word}">{word.word}</a></span>')
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


def main():
    spon = feedparser.parse(SPON_RSS)
    word_db = WordDB()
    for item in spon['items']:
        link = item['link']
        if not link.startswith('https://www.spiegel.de/international/'): # don't mix DE and EN, focus on just DE for now
            word_db.add_words(item['title'], link)
            word_db.add_words(item['summary'], link)

    occured_at_least_twice = [w for w in word_db.words_by_usage() if w.usage_count > 1]

    with open('news.html', 'w') as f:
        formatted = format_as_html(occured_at_least_twice) + '\n'
        f.write(formatted)

    with open('news_links.html', 'w') as f:
        formatted = format_as_html_links_list(occured_at_least_twice) + '\n'
        f.write(formatted)

if __name__ == '__main__':
    main()
