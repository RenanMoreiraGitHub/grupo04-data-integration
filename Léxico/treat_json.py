import json
import pandas as pd
from dotenv import load_dotenv
from os import getenv
from datetime import datetime
from tokeniza_words import get_felling
from mysql_connection import MysqlConnection

load_dotenv()

with open('./scrapper_soybean_twitter.json', encoding='utf-8') as fh:
    data = json.load(fh)

df = pd.DataFrame()
for search in data:
    for idx, line in enumerate(data[search]):
        tweet_text = data[search][idx]

        # Realize a análise léxica do tweet_text utilizando a função get_feling do seu analisador léxico
        sentiment = get_felling(tweet_text)

        dict_sentiment = {
            'search': search,
            'date': datetime.now(),
            'sentiment': sentiment
        }

        df_dict = pd.DataFrame([dict_sentiment])
        df = pd.concat([df, df_dict], ignore_index=True)

print(df)
df.to_csv('resultados.csv', index=False)

mysql = MysqlConnection(user=getenv('BD_USER'), 
                            passwd=getenv('BD_PASS'),
                            host=getenv('BD_HOST'))
mysql.connect()
mysql.insert_dataframe(df, 'sentiment', 'twitter')
mysql.disconnect()