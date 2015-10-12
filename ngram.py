#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, print_function, absolute_import,
                        unicode_literals)

import sys
import tweepy
import string
import numpy as np
import configparser as ConfigParser
import pickle
from datetime import datetime
from collections import defaultdict

alpha = 0.9
START = "<S>"
STOP = "</S>"


print(datetime.now())


def build_sentence(words):
    s = " "
    for w in words:
        if w == "$":
            continue
        if not len(w.strip(string.punctuation)):
            if w in ["(", "{", "\{", "[", "`", "``"]:
                s += w
            else:
                s = s[:-1]+w+" "
        else:
            s += w+" "
    s = s.strip()
    s = s[0].upper() + s[1:]
    return s


if "--build" in sys.argv:
    titles = [[START, START] + t.strip().split() + [STOP, STOP]
              for t in open("titles.txt").readlines()]

    bigrams = defaultdict(lambda: defaultdict(int))
    trigrams = defaultdict(lambda: defaultdict(int))

    print("Building ngrams...")
    for title in titles:
        for i in range(2, len(title)):
            bigrams[title[i-1]][title[i]] += 1
            trigrams[title[i-2]+" "+title[i-1]][title[i]] += 1
    pickle.dump((dict(bigrams), dict(trigrams)), open("ngrams.pkl", "wb"), -1)

else:
    print("Loading ngrams...")
    bigrams, trigrams = pickle.load(open("ngrams.pkl", "rb"))

print("Generating title...")
title = [START, START]
while True:
    b_prob = bigrams[title[-1]]
    t_prob = trigrams[title[-2]+" "+title[-1]]

    b_norm = sum(b_prob.values())
    t_norm = sum(t_prob.values())

    words, probs = [], []
    for w in set(b_prob.keys()) | set(t_prob.keys()):
        words.append(w)
        probs.append(alpha * t_prob.get(w, 0.0)/t_norm
                     + (1-alpha) * b_prob.get(w, 0.0)/b_norm)

    word = np.random.choice(words, p=probs)
    if word == STOP:
        if len(title) < 5:
            print("Too short")
            title = [START, START]
            continue
        else:
            break
    title.append(word)
    sent = build_sentence(title[2:])
    if len(sent) > 140:
        print("Too long")
        title = [START, START]

print("Title: \"{0}\"".format(sent))

if "--tweet" in sys.argv:
    config = ConfigParser.ConfigParser()
    config.read("local.cfg")
    sect = "twitter"

    print("Posting to twitter...")
    auth = tweepy.OAuthHandler(config.get(sect, "consumer_key"),
                               config.get(sect, "consumer_secret"))
    auth.set_access_token(config.get(sect, "user_key"),
                          config.get(sect, "user_secret"))
    api = tweepy.API(auth)
    api.update_status(status=sent)
