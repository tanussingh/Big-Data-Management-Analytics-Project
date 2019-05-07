from articlesToPandas import getDF
import pandas

df = getDF()
for index, row in df.iterrows():
    text1 = row['url']
    print(text1)
