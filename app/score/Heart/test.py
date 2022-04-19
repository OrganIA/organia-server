from datetime import datetime
import pandas as pd

df = pd.read_excel("Cas-tests-V1.xlsx", sheet_name='Cas_Coeur', dtype={
    'D_D_NAI': datetime, 
    'D_INSC': datetime, 
    'D_URGENCE': datetime, 
    'DPROBNP': datetime, 
    'DPROBNB': datetime,
    'D_CREATE': datetime, 
    'D_BILI': datetime,
    'D_D_NAI': datetime,
    })
data = df.to_dict(orient='index')
sample1 = data[0]
print(sample1)