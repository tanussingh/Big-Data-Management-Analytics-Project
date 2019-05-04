import pymongo
from pymongo import MongoClient
from kafka import KafkaProducer
from time import sleep
import json, sys, requests, time

def publish_message(producer_instance, topic_name, value):
    try:
        key_bytes = bytes('foo', encoding='utf-8')
        value_bytes = bytes(value, encoding='utf-8')
        producer_instance.send(topic_name, key=key_bytes, value=value_bytes)
        producer_instance.flush()
        print('Message published successfully.')
    except Exception as ex:
        print('Exception in publishing message')
        print(str(ex))

def connect_kafka_producer():
    _producer = None
    try:
        #_producer = KafkaProducer(value_serializer=lambda v:json.dumps(v).encode('utf-8'),bootstrap_servers=['localhost:9092'], api_version=(0, 10),linger_ms=10)
         _producer = KafkaProducer(bootstrap_servers=['localhost:9092'], api_version=(0, 10),linger_ms=10)

    except Exception as ex:
        print('Exception while connecting Kafka')
        print(str(ex))
    finally:
        return _producer

if __name__== "__main__":
    # Set up connection to Mongo Server
    client = MongoClient("localhost", 27017)

    #Get user input on fileName
    if len(sys.argv) != 4:
        print ('Number of arguments is not correct')
        exit()

    #Read from mongo here
    #assume that start and end date is in order 'Y-M-D'
    fileName = sys.argv[1]
    start = sys.argv[2]
    end = sys.argv[3]
    dbArticles = client['big_data']

    # Set connection to database
    collection_Article = dbArticles['spanish_articles']

    #Write data onto Kafka
    if (collection_Article.count()) > 0:
        prod=connect_kafka_producer();
        for story in collection_Article.find():
            print(story)
            publish_message(prod, 'SpanishArticles', story)
            time.sleep(1)
        if prod is not None:
                prod.close()
