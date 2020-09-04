import tweepy
from tweepy import Stream
from tweepy.streaming import StreamListener
import keys
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: x.encode('utf-8')
)

auth = tweepy.OAuthHandler(keys.API_KEY, keys.API_SECRET_KEY)
auth.set_access_token(keys.ACCESS_TOKEN, keys.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)


class Producer(StreamListener):
    def __init__(self, producer):
        self.producer = producer

    def on_data(self, data):
        self.producer.send('trump_data', value=data)
        return True

    def on_error(self, error):
        print(error)


twitter_stream = Stream(auth, Producer(producer))
twitter_stream.filter(track=["trump"])
