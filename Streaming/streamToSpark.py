#Import Files
import os
os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.0.2 pyspark-shell'
from pyspark.sql import SparkSession
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

spark = SparkSession \
         .builder \
         .appName('PythonStreamingRecieverKafkaWordCount') \
         .getOrCreate()

def do_something(rdd):
    json_rdd = rdd.map(lambda x: x[1])
    df = spark.read.json(json_rdd)
    df.show()

if __name__ == "__main__":
    sc = spark.sparkContext
    sc.setLogLevel("WARN")
    ssc = StreamingContext(sc, 10)  # Batch duration set to 60secs

    #Get topic name and broker information from user
    topic = 'SpanishArticles'
    kvs = KafkaUtils.createDirectStream(ssc, ['SpanishArticles'], {'metadata.broker.list':'localhost:9092'})
    # lines = kvs.map(lambda x: x[1])
    kvs.foreachRDD(do_something)
    ##Manipulate the data however

    ssc.start()
    ssc.awaitTermination()
