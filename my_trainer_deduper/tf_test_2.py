# -*- coding: utf-8 -*-
news1 = """
Washington (CNN)The White House pushed back Sunday on questions about a signing statement President Donald Trump added to the latest government spending bill Friday that said his administration would treat minority spending programs -- including one to help historically black colleges pay for construction -- in a manner consistent with the Constitution.

The signing statement "simply indicates that the President will interpret those provisions consistent with the Constitution" and is not dissimilar to signing statements issued by past presidents, a White House official said Sunday.
"The important thing to realize is: The President was able to secure big wins for his top priorities in this spending bill, including more than $25 billion in additional funding for the military, $1.52 billion for border security, a permanent extension of health coverage for retired miners, and a three-year extension of the DC school choice program," the official said.
Trump signed the $1.1 trillion omnibus spending bill Friday, adding the statement: "My administration shall treat provisions that allocate benefits on the basis of race, ethnicity, and gender ... in a manner consistent with the requirement to afford equal protection of the laws under the Due Process Clause of the Constitution's Fifth Amendment."
Those programs included historically black college financing, Native American housing block grants and minority business development, the statement said.
Such statements are often used to flag provisions an administration might disregard.
The aim of the Historically Black College and University Capital Financing Program is provide low-cost capital to finance improvements to the infrastructure of the nation's historically black colleges and universities, including for the repair or construction of classrooms, libraries, dormitories and the like, according to the Department of Education.
"""
news2 = """
President Donald Trump on Friday signed the omnibus spending bill to fund the government through Sept. 30, a White House spokeswoman said.

The bipartisan, nearly $1.2 trillion measure comes after weeks of negotiations. The deal puts an additional $15 billion toward Trump's planned military buildup and $1.5 billion more for border security.

The president signed the bill Friday afternoon while at his golf club in New Jersey, White House deputy press secretary Sarah Huckabee Sanders told reporters.

Democrats talked up how the deal lacks funding for a wall on the border with Mexico, and pointed out that it does not include much of the massive cuts to domestic programs that Trump wanted. The president and House Speaker Paul Ryan both focused on defense and border security spending as Republican victories.

On Tuesday, Trump called the bill a "clear win for the American people," while Ryan said "this is what winning looks like."

Irked by Democrats such as Senate Minority Leader Chuck Schumer highlighting what they deemed victories in the spending bill, Trump lashed out in tweets Tuesday morning. He targeted Senate rules that require 60 votes to overcome a filibuster on spending bills, therefore requiring compromise between the majority and minority parties.

He wrote that the country "needs a good 'shutdown' in September," when the funding expires, to fix what he called a "mess."

Pressed to explain Trump's call for a shutdown Tuesday, Office of Management and Budget Director Mick Mulvaney said the president "is frustrated with the fact that he negotiated in good faith with Democrats, and they went out to try and spike the football and make him look bad."

Schumer chose not to counter Trump on the shutdown talk Tuesday.

"This is a good day, and it's a bipartisan day, so I'm not going to get into finger pointing," Schumer said. "It was a bipartisan negotiation as I said. The leaders — Democrat, Republican, House and Senate — work well together. And why ruin that?"
"""

import nltk
import string
from nltk import stem
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer

replace_punctuation = string.maketrans(string.punctuation, ' ' * len(string.punctuation))

porter = stem.porter.PorterStemmer()
stops = set(stopwords.words("english"))

'''
news1 = news1.lower()
news1 = news1.translate(replace_punctuation)
print news1


tokens = nltk.word_tokenize(news1)
print "##### TOKEN #####"
print tokens
print


stops = set(stopwords.words("english"))
filtered_words = [word for word in tokens if word not in stops]
print "##### FILTERED TOKEN #####"
print filtered_words
print

porter = stem.porter.PorterStemmer()
tokens_porter = [porter.stem(i) for i in filtered_words]
print "##### TOKEN After PORTER #####"
print tokens_porter
print


reduce_tokens_porter = list(set(tokens_porter))
print "##### Remove duplication #####"
print reduce_tokens_porter
print
'''
def translate_non_alphanumerics(unicode_text, replace_with=u' '):
    not_letters_or_digits = u'!"#%\'()*+,-./:;<=>?@[\]^_`{|}~'
    translate_table = dict((ord(char), replace_with) for char in not_letters_or_digits)
    return unicode_text.translate(translate_table)

def tokenize_and_stem(text):
    text = text.lower()
    text = translate_non_alphanumerics(unicode_text=text)
    tokens = nltk.word_tokenize(text)
    stem = [porter.stem(i) for i in tokens]
    print "####### STEM #######"
    print stem
    print
    return stem


tfidf = TfidfVectorizer(stop_words=stops, tokenizer=tokenize_and_stem)

documents = [news1, news2]
tfs = tfidf.fit_transform(documents)
pairwise_sim = tfs * tfs.T
print pairwise_sim.A

# print(tfidf.get_feature_names()) 

'''
Use nltk's stop word
'''
# download corpora/stopwords
# nltk.download()
# stop_words = nltk.corpus.stopwords.words('english')
# tfidf = TfidfVectorizer(stop_words=stop_words)

'''
tfidf_stopwords = TfidfVectorizer(stop_words='english')
tfs_stopwords = tfidf_stopwords.fit_transform(documents)
pairwise_sim_1 = tfs_stopwords * tfs_stopwords.T
# 0.19297724
print pairwise_sim_1.A
print(tfidf_stopwords.get_feature_names())  

tfidf = TfidfVectorizer()
tfs = tfidf.fit_transform(documents)
# 0.61512133
pairwise_sim_2 = tfs * tfs.T
print pairwise_sim_2.A

print(tfidf.get_feature_names())  
'''
