import pandas as pd

columns = ['R_D_NAI', 'D_D_NAI', 'D_INSC', 'D_URGENCE', 'DCEC', 'DPROBNP', 'DCREAT', 'DBILI', 'D_PREL']
df = pd.read_excel("Cas-tests-V1.xlsx", sheet_name='Cas_Coeur', parse_dates=columns)
data = df.to_dict(orient='index')
sample1 = data[3]
