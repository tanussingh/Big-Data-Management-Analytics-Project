#Import Files
from udpipe_parse import udpipe_parse, udpipe_pos
import os
os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.0.2 pyspark-shell --py-files udpipe_parse.py streamToSpark.py'
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.types import ArrayType, StringType
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

spark = SparkSession \
         .builder \
         .appName('PythonStreamingRecieverKafkaWordCount') \
         .getOrCreate()
sc = spark.sparkContext


def do_something(rdd):
    json_rdd = rdd.map(lambda x: x[1])
    df = spark.read.json(json_rdd)
    udparse = udf(udpipe_parse, StringType())
    udparse_pos = udf(udpipe_pos, StringType())
    print(df.columns)
    new_df = df.withColumn('udpipe_raw', udparse(df.text))
    new_df = new_df.withColumn('udpipe', udparse_pos(new_df.udpipe_raw))
    new_df.select('udpipe_raw', 'udpipe').show()


if __name__ == "__main__":
    sc.setLogLevel("WARN")
    ssc = StreamingContext(sc, 3)  # Batch duration set to 60secs

    #Get topic name and broker information from user
    topic = 'SpanishArticles'
    kvs = KafkaUtils.createDirectStream(ssc, ['SpanishArticles'], {'metadata.broker.list':'localhost:9092'})
    # lines = kvs.map(lambda x: x[1])
    kvs.foreachRDD(do_something)
    ##Manipulate the data however

    ssc.start()
    ssc.awaitTermination()
