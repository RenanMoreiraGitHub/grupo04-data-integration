import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, r2_score

df_temperatura = pd.read_csv('temperature_brazil.csv', decimal=',')
df_precipitacao = pd.read_csv('dataset_precipitation_soybean.csv', decimal=',')
df_preco_soja = pd.read_csv('Dataset_prices_soybean.csv', decimal=',')

df_merged = pd.merge(df_preco_soja, df_temperatura, on='date', how='inner')
df_merged = pd.merge(df_merged, df_precipitacao, on='date', how='inner')

df_merged['data_futura'] = pd.to_datetime(df_merged['date']) + pd.to_timedelta(2110, 'D')

X = df_merged[['TempBulboSeco', 'TempBulboUmido', 'TempMaxima', 'TempMinima', 'UmidadeRelativa', 'precipitation']]
y = df_merged['real']

model = sm.OLS(y, X).fit()

y_pred = model.predict(X)
rmse = mean_squared_error(y, y_pred, squared=False)
r2 = r2_score(y, y_pred)

print('RMSE:', rmse)
print('R²:', r2)

plt.plot(df_merged['data_futura'], y, color='blue', label='Previsão futura', alpha=0.5)
plt.title('Previsão de preço da soja desde o último dia de coleta do dataset (2017-11-30) até o mês atual')
plt.xlabel('Data')
plt.ylabel('Preço (R$/Sacas de 30kg)')
plt.legend()
historic_data = '2017-11-30'
plt.axvline(x=pd.to_datetime(historic_data), color='black', linestyle=':')
plt.show()
