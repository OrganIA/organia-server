import pandas as pd

columns = ['R_D_NAI', 'R_D_INSC', 'D_Reprise_ANC', 'D_DIAL', 'D_GRF (n-1)', 'D_ARF (n-1)', 'D_Ret_DIAL (n-1)',
           'D_D_NAI', 'D_D_PREL']
df = pd.read_excel("Cas-tests-V3.xlsx", sheet_name='Cas_Rein', parse_dates=columns)
data = df.to_dict(orient='index')
sample1 = data[4]
