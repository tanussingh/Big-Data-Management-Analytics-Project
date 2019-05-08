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

collection_ud = dbArticles['udpipe_parse']

if (collection_d2v.count()) > 0:
    cursor = collection_d2v.find({"d2v_dup_count": {"$gt": 0}})
    df_d2v = pandas.DataFrame(list(cursor))

if collection_ud.count() > 0:
    cursor = collection_ud.find()
    df_ud = pandas.DataFrame(list(cursor))

#Get full list of spanish articles as pandas dataframe
print(df_d2v.head(20))
df_full = df_ud
print(df_full)
df_out = pandas.DataFrame(columns = ['url', 'SimilarityList', 'TotalNumDups'])
df_DeDup = pandas.DataFrame(columns = ['url', 'SimilarUrls', 'TotalNum'])

for index, row in df_d2v.iterrows():
    url1 = row['url']
    #text1 = df_full[df_full['url'] == url1].iloc[0]['text']
    match1= df_full[df_full['url'] == url1]
    if len(match1) == 0 or 'text' not in match1.columns or match1.iloc[0]['text'] is None:
        continue
    text1 = match1.iloc[0]['text']
    parse_pos = df_full[df_full['url'] == url1].iloc[0]['udpipe']
    parse_pos = json.loads(parse_pos)
    simList = {}
    simUrls = []
    for url2 in json.loads(row['d2v_sim']):
        #text2 = df_full[df_full['url'] == url2].iloc[0]['text']
        match2 = df_full[df_full['url'] == url2]
        if len(match2) == 0 or 'text' not in match2.columns or match2.iloc[0]['text'] is None:
            continue
        text2 = match2.iloc[0]['text']
        parse_pos2 = df_full[df_full['url'] == url2].iloc[0]['udpipe']
        parse_pos2 = json.loads(parse_pos2)
        s1 = set(parse_pos['AUX']) | set(parse_pos['NUM']) | set(parse_pos['VERB']) | set(parse_pos['NOUN']) | set(parse_pos['PROPN'])
        s2 = set(parse_pos2['AUX']) | set(parse_pos2['NUM']) | set(parse_pos2['VERB']) | set(parse_pos2['NOUN']) | set(parse_pos2['PROPN'])
        valuejacc = jacc_sim(s1, s2)
        if (valuejacc > .1):
            simUrls.append(url2)
            print("FOUND SIMILAR MATCH FOR ", url1, " WITH SIMILARITY RATE OF ", valuejacc)
        simList[url2] = valuejacc
    row = {'url': url1, 'SimilarityList': json.dumps(simList), 'TotalNumDups': len(simList)}
    df_out = df_out.append(row, ignore_index=True)
    if (len(simUrls) != 0) :
        row2 = {'url': url1, 'SimilarUrls': json.dumps(simUrls), 'TotalNum': len(simUrls)}
        df_DeDup = df_DeDup.append(row2,ignore_index=True)
    print("------------------- " ,url1, " DONE ------------------------")

dbCol = dbArticles['jacc_sim_calculated']
dbCol.insert_many(df_out.to_dict(orient='records'))

dbDeDup = dbArticles['dedup_calculated']
dbDeDup.insert_many(df_DeDup.to_dict(orient='records'))
