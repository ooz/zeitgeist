#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import language.filters as lf

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
