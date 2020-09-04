from kafka import KafkaConsumer
from pymongo import MongoClient
from json import loads
from time import sleep
import model


client = MongoClient(port = 27017)
db = client.kafka_trump
table_raw = db.raw_data
table_processed = db.processed_data

consumer = KafkaConsumer(
    'trump_data',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group',
    value_deserializer=lambda x: loads(x.decode('utf-8'))
)
counter = 0
for message in consumer:
    message = message.value
    try: 
        message['text']
    except:
        message['text'] = ''

    _id = table_raw.insert_one(message).inserted_id
    table_processed.insert_one({
        'id': counter,
        'message': message['text'],
        'flair_sentiment': model.get_sentiment('flair', message['text']),
        'textblob_sentiment': model.get_sentiment('textblob', message['text']),
        'nltk_sentiment': model.get_sentiment('nltk', message['text'])
    })

    counter += 1
    print('Processed {}'.format(_id))