CMU ARK Twitter Part-of-Speech Tagger [v0.3](http://www.cs.cmu.edu/~ark/TweetNLP/owoputi+etal.naacl13.pdf) Many thanks to [this python port](https://github.com/ljm233/ark_tweet_nlp_python/blob/master/twokeniser.py)

PLUS

MPQA lexicon entry for [subjectivity polarity](http://people.cs.pitt.edu/~wiebe/pubs/papers/emnlp05polarity.pdf)

Usage:
```
import sentiment_twokeniser

S = Sentiment()
output = S.get_overall_sentiment('i absolutely abhor your bonus')
print(output)
```
