from twokeniser import Twagger

import nltk
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords

import sqlite3
from sqlite3 import Error

class Sentiment:
    def __init__(self):
        self.tagger = Twagger('ark-tweet-nlp-0.3.2.jar')

        self.english_stopwords = set(stopwords.words('english'))
        self.tweet_tokenizer = TweetTokenizer()

        self.adj_array = ['A']
        self.adverb_array = ['R']
        self.noun_array = ['N', '^', 'M']
        self.verb_array = ['T']

        subjectivitydb = 'subjectivity.db'
        self.conn = self.create_connection(subjectivitydb)

    def create_connection(self, db_file):
        conn = None
        try:
            conn = sqlite3.connect(db_file, check_same_thread=False)
        except Error as e:
            print(e)
        return conn

    def match_tag_to_sentiment_postag(self, tag):
        if tag in self.adj_array:
            return 'adj'
        elif tag in self.adverb_array:
            return 'adverb'
        elif tag in self.noun_array:
            return 'noun'
        elif tag in self.verb_array:
            return 'verb'
        else:
            return 'anypos'

    def select_task(self, word, pos):
        cur = self.conn.cursor()
        cur.execute("SELECT priorpolarity FROM clues WHERE word=? AND pos=?", (word, pos))
        rows = cur.fetchall()

        sentiment = ''

        if len(rows) > 0:
            sentiment = rows[0][0]
        
        return sentiment

    def sentiment_to_int(self, sentiment):
        if sentiment == 'negative':
            return -1
        elif sentiment == 'positive':
            return 1
        elif sentiment == 'neutral':
            return 0
        elif sentiment == 'both':
            return 0
        elif sentiment == 'weakneg':
            return -0.5

    def get_overall_sentiment(self, text):
        text_tokens = self.tweet_tokenizer.tokenize(text)
        text_filtered_array = [w for w in text_tokens if not w in self.english_stopwords]
        text_filtered_string = ' '.join(text_filtered_array)

        twitter_tagger_output = self.tagger.tag(text_filtered_string)

        overall_polarity = 0

        for tag in twitter_tagger_output:
            word, pos_tag, accuracy = tag
            sentiment_postag = self.match_tag_to_sentiment_postag(pos_tag)

            polarity = self.select_task(word, sentiment_postag)
            if polarity is not '':
                polarity_int = self.sentiment_to_int(polarity)
                overall_polarity = overall_polarity + polarity_int

        return overall_polarity


if __name__ == '__main__':
    S = Sentiment()
    output = S.get_overall_sentiment('i absolutely abhor your bonus')
    print(output)