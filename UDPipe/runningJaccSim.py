#Import libraries
from articlesToPandas import getDF
from udpipe_parse import jacc_sim, udpipe_parse, udpipe_pos
import sys, json

#Get spanish articles as a pandas dataframe
df = getDF()
print(df.head(10))

#Increment through the pandas dataframe
for index, row in df.iterrows():
    text1 = row['text']
    if(text1 is not None):
        parse_pos = udpipe_pos(udpipe_parse(text1))
        parse_pos = json.loads(parse_pos)
        simList = {}
        #For each row of the dataframe compare with everything that follows
        for index2, row2 in df.iterrows():
            if ((index < index2) and (row2['text'] is not None)) :
                text2 = row2['text']
                parse_pos2 = udpipe_pos(udpipe_parse(text2))
                parse_pos2 = json.loads(parse_pos2)
                valuejacc = jacc_sim(parse_pos['PROPN'], parse_pos2['PROPN'])
                simList[row2['url']] = valuejacc
                print(index2 , "HIII")
        print(simList)
