#Import Files
import os
os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.0.2 pyspark-shell'
from pyspark import SparkContext, SparkConf
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

if __name__ == "__main__":
    sc = SparkContext(appName="PythonStreamingRecieverKafkaWordCount")
    sc.setLogLevel("WARM")
    ssc = StreamingContext(sc, 60) # Batch duration set to 60secs

    #Get topic name and broker information from user
    topic = 'SpanishArticles'
    kvs = KafkaUtils.createDirectStream(ssc, ['SpanishArticles'], {'metadata.broker.list':'localhost:9092'})
    lines = kvs.map(lambda x: x[1])
    ##Manipulate the data however

    ssc.start()
    ssc.awaitTermination()
