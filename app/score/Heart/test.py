from cmath import isnan
from datetime import datetime
from attr import NOTHING
import pandas as pd
from sqlalchemy import null

df = pd.read_excel("CCas-tests-V1.xlsx", sheet_name='Cas_Coeur', dtype={
    'D_D_NAI': datetime, 
    'D_INSC': datetime, 
    'D_URGENCE': datetime, 
    'DPROBNP': datetime, 
    'D_CREATE': datetime, 
    'D_BILI': datetime,
    'D_D_NAI': datetime,
    })
data = df.to_dict(orient='index')
sample1 = data[0]
print(type(sample1["CREAT"]))