import flair
from textblob import TextBlob
from nltk.sentiment.vader import SentimentIntensityAnalyzer


def textblob_score(res):
    if -0.2 < res < 0.2:
        return "NEUTRAL"
    elif res < -0.2:
        return "NEGATIVE"
    else:
        return "POSITIVE"


def flair_score(res):
    return res.value


def nltk_score(res):
    if res == 'neg':
        return 'NEGATIVE'
    elif res == 'pos':
        return 'POSITIVE'
    else:
        return 'NEUTRAL'


def get_sentiment(model_name, sentence):
    if model_name.lower() == 'flair':
        tmp_sentence = flair.data.Sentence(sentence)
        flair_model = flair.models.TextClassifier.load('en-sentiment')
        flair_model.predict(tmp_sentence)
        total_sentiments = tmp_sentence.labels
        try:
            total_sentiments[0]
        except:
            return "NEUTRAL"
        return total_sentiments[0].value
    
    elif model_name.lower() == 'textblob':
        res = TextBlob(sentence).sentiment
        return textblob_score(res.polarity)
    
    elif model_name.lower() == 'nltk':
        res = SentimentIntensityAnalyzer().polarity_scores(sentence)
        return nltk_score(max(res, key=res.get))
