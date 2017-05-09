import os
import yaml
import pickle
import shutil
import string
import nltk

import numpy as np
import pandas as pd
import tensorflow as tf

from sklearn import metrics

import news_cnn_model

with open(os.path.join(os.path.dirname(__file__), '../..', "config.yaml"), 'r') as config_file:
    config = yaml.load(config_file)
    model_config = config["news_topic_modeling_service"]

learn = tf.contrib.learn

REMOVE_PREVIOUS_MODEL = True
MODEL_OUTPUT_DIR = os.path.join(os.path.dirname(__file__), model_config["trainer"]["model_dir"])
DATA_SET_FILE = os.path.join(os.path.dirname(__file__), '..', 'labeled_news.csv')
VARS_FILE = os.path.join(os.path.dirname(__file__), model_config["trainer"]["vars_dir"])
VOCAB_PROCESSOR_SAVE_FILE =  os.path.join(os.path.dirname(__file__), model_config["trainer"]["vocab_procesor_save_file"])
MAX_DOCUMENT_LENGTH = 100
N_CLASSES = 17

# Training parms
STEPS = model_config["trainer"]["classifier_step"]

replace_punctuation = string.maketrans(string.punctuation, ' '*len(string.punctuation))
porter = nltk.stem.porter.PorterStemmer()
stopwords = set(nltk.corpus.stopwords.words("english"))

def tokenize_and_stem(iterator):
    result = []
    for text in iterator:
        if type(text) != str:
            print "UNKNOW text with type %s, Skip\n" % type(text)
            result.append([])
            continue
        # print "type: %s, text: %s" %(type(text), text)
        text = text.lower()
        text = text.translate(replace_punctuation)
        tokens = nltk.word_tokenize(text)
        filtered_token = [word for word in tokens if word not in stopwords]
        stem = [porter.stem(item) for item in filtered_token]
        # print "\n####### STEM #######"
        # print stem
        result.append(stem)

    return result

def main(unused_argv):
    if REMOVE_PREVIOUS_MODEL:
        # Remove old model
        shutil.rmtree(MODEL_OUTPUT_DIR)
        os.mkdir(MODEL_OUTPUT_DIR)

    # Prepare training and testing data
    # ["class", "title", "description", "source"]
    df = pd.read_csv(DATA_SET_FILE, header=None)
    train_df = df[0:500]
    test_df = df.drop(train_df.index)

    # x - news title, y - class
    x_train = train_df[2]
    y_train = train_df[0]
    x_test = test_df[2]
    y_test = test_df[0]

    # Process vocabulary
    vocab_processor = learn.preprocessing.VocabularyProcessor(MAX_DOCUMENT_LENGTH, tokenizer_fn=tokenize_and_stem)
    # vocab_processor = learn.preprocessing.VocabularyProcessor(MAX_DOCUMENT_LENGTH)
    print "#### TRAIN DATA ####"
    x_train = np.array(list(vocab_processor.fit_transform(x_train)))
    print "#### TEST DATA ####"
    x_test = np.array(list(vocab_processor.transform(x_test)))

    n_words = len(vocab_processor.vocabulary_)
    print('Total words: %d' % n_words)

    # Saving n_words and vocab_processor:
    with open(VARS_FILE, 'w') as f:
        pickle.dump(n_words, f)

    vocab_processor.save(VOCAB_PROCESSOR_SAVE_FILE)

    # Build model
    classifier = learn.Estimator(
        model_fn=news_cnn_model.generate_cnn_model(N_CLASSES, n_words),
        model_dir=MODEL_OUTPUT_DIR)

    # Train and predict
    classifier.fit(x_train, y_train, steps=STEPS)

    # Evaluate model
    y_predicted = [
        p['class'] for p in classifier.predict(x_test, as_iterable=True)
    ]

    score = metrics.accuracy_score(y_test, y_predicted)
    print('Accuracy: {0:f}'.format(score))

if __name__ == '__main__':
    tf.app.run(main=main)
