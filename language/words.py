#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

import language.filters as lf

class Word(object):
    def __init__(self, word, link=None, usage_count=1, first='', last=''):
        self.word = word
        self.usage_count = usage_count
        self.links = [link] if link else []
        self.first = first
        self.last = last
    def add_occurrence(self, link):
        self.usage_count += 1
        if link not in self.links:
            self.links.append(link)
    def __str__(self):
        return f'({self.word}, {self.usage_count})'
    def __repr__(self):
        return str(self)

class WordDB(object):
    def __init__(self, words_json=None):
        self.words = words_json or {}
        for word in self.words.keys():
            w = self.words[word]
            self.words[word] = Word(word, None, 0, w['first'], w['last'])
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

def worddb_from_file(filename):
    with open(filename) as f:
        data = json.load(f)
        print(data)
        return WordDB(data)
    return dict()
