import pandas as pd

df = pd.read_excel("CCas-tests-V1.xlsx", sheet_name='Cas_Coeur')
data = df.to_dict(orient='index')
print(data[0]['SexR'])