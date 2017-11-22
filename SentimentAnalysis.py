from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

def sentiment_analysis(text):
    blob = TextBlob(text
                , analyzer=NaiveBayesAnalyzer())
    return blob.sentiment[0]