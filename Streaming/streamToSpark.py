#Import Files
from udpipe_parse import udpipe_parse, udpipe_pos
import os
import json
os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.0.2,org.mongodb.spark:mongo-spark-connector_2.11:2.4.0 pyspark-shell \
    --py-files udpipe_parse.py streamToSpark.py \
    --conf "spark.mongodb.input.uri=mongodb://127.0.0.1/big_data.udpipe_parse" \
    --conf "spark.mongodb.output.uri=mongodb://127.0.0.1/big_data.udpipe_parse"'

from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.types import ArrayType, StringType
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
import pymongo

spark = SparkSession \
         .builder \
         .appName('PythonStreamingRecieverKafkaWordCount') \
         .getOrCreate()

sc = spark.sparkContext

# try:
#     conn = MongoClient()
#     print('connected successfully!')
# except:
#     print('could not connect to mongo :(')
#
# db = conn.big_data
# collection = db.udpipe_parse

def do_something(rdd):
    if rdd.count() == 0:
        print('No data received from stream')
        return
    json_rdd = rdd.map(lambda x: x[1])
    df = spark.read.json(json_rdd)
    udparse = udf(udpipe_parse, StringType())
    udparse_pos = udf(udpipe_pos, StringType())
    new_df = df.withColumn('udpipe_raw', udparse(df.text))
    new_df = new_df.withColumn('udpipe', udparse_pos(new_df.udpipe_raw))

    getpropn = udf(lambda x: json.loads(x)['PROPN'], ArrayType(StringType()))
    getnoun = udf(lambda x: json.loads(x)['NOUN'], ArrayType(StringType()))
    getverb = udf(lambda x: json.loads(x)['VERB'], ArrayType(StringType()))
    pos = new_df.select('_id', 'udpipe')
    pos = pos.withColumn('propn', getpropn(pos.udpipe))
    pos = pos.withColumn('noun', getnoun(pos.udpipe))
    pos = pos.withColumn('verb', getverb(pos.udpipe))

    new_df.write.format('com.mongodb.spark.sql.DefaultSource') \
        .mode('append') \
        .option('spark.mongodb.output.uri', 'mongodb://127.0.0.1:27017/big_data.udpipe_parse') \
        .option('database', 'big_data') \
        .option('collection', 'udpipe_parse') \
        .save()
    pos.show()





if __name__ == "__main__":
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
