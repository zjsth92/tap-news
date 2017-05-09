# -*- coding: utf-8 -*-
import os
import json
import collections
import pandas as pd
import tensorflow as tf
# build word context for each class
TRAINING_DATA = "../labeled_news.csv"
TRAINING_DATA_NAMES = ["class", "title", "discription", "source"]

SELECTED_SOURCE = "bloomberg"
# Step 1: read all news for specific source, loaded as words
df = pd.read_csv(os.path.join(os.path.dirname(__file__), TRAINING_DATA), header=None, names=TRAINING_DATA_NAMES)

# train = df[df['source'] == SELECTED_SOURCE]
train = df

words = tf.compat.as_str(train["title"].to_string()).split()
words = words + tf.compat.as_str(train["discription"].to_string()).split()
print len(words)

# Step 2: Build the dictionary and replace rare words with UNK(unknow) token.
vocabulary_size = 10


def build_dataset(words, vocabulary_size):
  count = [['UNK', -1]]
  count.extend(collections.Counter(words).most_common(vocabulary_size - 1))
  dictionary = dict()
  for word, _ in count:
    dictionary[word] = len(dictionary)
  data = list()
  unk_count = 0
  for word in words:
    if word in dictionary:
      index = dictionary[word]
    else:
      index = 0  # dictionary['UNK']
      unk_count += 1
    data.append(index)
  count[0][1] = unk_count
  reverse_dictionary = dict(zip(dictionary.values(), dictionary.keys()))
  return data, count, dictionary, reverse_dictionary

data, count, dictionary, reverse_dictionary = build_dataset(words, vocabulary_size)
# del words  # Hint to reduce memory.
print('Most common words (+UNK)', count[:10])