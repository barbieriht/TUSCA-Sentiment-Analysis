import pandas as pd
import numpy as np
from cmath import isnan

tweets_df = pd.read_csv('all_tweets.csv', header=0, index_col=0)

for i in range(0, len(tweets_df)):
    successful = False
    quit = False
    try:
        if np.isnan(tweets_df.loc[tweets_df.index[i], 'rating']):
            while(not successful):
                value = input('Qual sentimento tem no tweet a seguir?\n' + tweets_df.loc[tweets_df.index[i], 'text'] + '\n(\'Negativo\':{1, 2}, \'Neutro\':{3}, \'Positivo\':{4,5}): ')
                try:
                    if(int(value) > 0 and int(value) <= 5 and value != ''):
                        tweets_df.loc[tweets_df.index[i], 'rating'] = value
                        successful = True
                    else:
                        print('Insira uma resposta de formato int\n')
                        i = i - 1
                except:
                    if(value == 'q'):
                        successful = True
                        quit = True
                        break
        if quit:
            break
    except:
        pass
