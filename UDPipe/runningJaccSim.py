#Import libraries
import pandas
from udpipe_parse import jacc_sim, udpipe_parse, udpipe_pos
import sys, json
import pymongo
from pymongo import MongoClient
from articlesToPandas import getDF

#Get spanish articles as a pandas dataframe
df_d2v = pandas.DataFrame()

# Set up connection to Mongo Server
client = MongoClient("localhost", 27017)
dbArticles = client['big_data']

# Set connection to database
collection_d2v = dbArticles['d2v_calculated']
d2v_values = []

if (collection_d2v.count()) > 0:
    cursor = collection_d2v.find({"d2v_dup_count": {"$gt": 0}})
    df_d2v = pandas.DataFrame(list(cursor))

#Get full list of spanish articles as pandas dataframe
print(df_d2v.head(20))
df_full = getDF()
print(df_full)
df_out = pandas.DataFrame(columns = ['url', 'SimilarityList'])

for index, row in df_d2v.iterrows():
    url1 = row['url']
    text1 = df_full[df_full['url'] == url1].iloc[0]['text']
    parse_pos = udpipe_pos(udpipe_parse(text1))
    parse_pos = json.loads(parse_pos)
    simList = {}
    for url2 in json.loads(row['d2v_sim']):
        text2 = df_full[df_full['url'] == url2].iloc[0]['text']
        parse_pos2 = udpipe_pos(udpipe_parse(text2))
        parse_pos2 = json.loads(parse_pos2)
        s1 = set(parse_pos['AUX']) | set(parse_pos['NUM']) | set(parse_pos['VERB']) | set(parse_pos['NOUN']) | set(parse_pos['PROPN'])
        s2 = set(parse_pos2['AUX']) | set(parse_pos2['NUM']) | set(parse_pos2['VERB']) | set(parse_pos2['NOUN']) | set(parse_pos2['PROPN'])
        valuejacc = jacc_sim(s1, s2)
        simList[url2] = valuejacc
    row = {'url': url1, 'SimilarityList': json.dumps(simList), 'TotalNumDups': len(simList)}
    df_out = df_out.append(row, ignore_index=True)
    print("------------------- " ,url1)

dbCol = dbArticles['jacc_sim_calculated']
dbCol.insert_many(df_out.to_dict(orient='records'))
