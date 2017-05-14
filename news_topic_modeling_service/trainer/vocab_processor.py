import string
import nltk
import tensorflow as tf

MAX_DOCUMENT_LENGTH = 100

replace_punctuation = string.maketrans(string.punctuation, ' '*len(string.punctuation))
porter = nltk.stem.porter.PorterStemmer()
stopwords = set(nltk.corpus.stopwords.words("english"))

learn = tf.contrib.learn

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

def get_processor(doc_len=MAX_DOCUMENT_LENGTH, fn=tokenize_and_stem):
    return learn.preprocessing.VocabularyProcessor(doc_len, tokenizer_fn=fn)
