#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import feedparser

import block_words

SPON_RSS = 'https://www.spiegel.de/schlagzeilen/index.rss'

class Word(object):
    def __init__(self, word, link):
        self.word = word
        self.usage_count = 1
        self.links = [link]
    def add_occurrence(self, link):
        self.usage_count += 1
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
            w = word.lower().replace(':', '').replace('.', '').replace(',', '').replace('"', '').replace('-', '')
            if len(w) and w not in block_words.DE:
                if w in self.words.keys():
                    self.words[w].add_occurrence(link)
                else:
                    self.words[w] = Word(w, link)
    def words_by_usage(self):
        words = self.words.values()
        words = sorted(words, reverse=True, key=lambda w: w.usage_count)
        return list(words)

def main():
    spon = feedparser.parse(SPON_RSS)
    word_db = WordDB()
    for item in spon['items']:
        link = item['link']
        word_db.add_words(item['title'], link)
        word_db.add_words(item['summary'], link)
        #print(item['title'])
        #print(' ' + item['summary'])
        #print(' ' + link)
    occured_at_least_twice = [w for w in word_db.words_by_usage() if w.usage_count > 1]
    print(occured_at_least_twice)


if __name__ == '__main__':
    main()
