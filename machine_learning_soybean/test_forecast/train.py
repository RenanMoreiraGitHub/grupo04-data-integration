import numpy as np
import pandas as pd
from skopt import BayesSearchCV
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split

df = pd.read_parquet('df_test.parquet') 
df['data_int'] = df['data'].astype('int64') // 10**9
df = df.ffill()

lower_limit = 0  # Defina o limite inferior
upper_limit = 20  # Defina o limite superior

df_no_outliers = df[(df['preciptacao'] >= lower_limit) & (df['preciptacao'] <= upper_limit)]


X = df_no_outliers[['pressao_atm','pressao_atm_max','pressao_atm_min','temperatura','temperatura_orvalho',
                    'temperatura_max','temperatura_min','temperatura_orvalho_max','temperatura_orvalho_min',
                    'umidade_rel_ar_max','umidade_rel_ar_min','umidade_rel_ar',
                    'velocidade_vento', 'data_int', 'percentage']]


y = df_no_outliers['preciptacao']  # Corrigi a seleção da coluna de destino

# Divida os dados em treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

# Espaço de busca
param_space = {
    'n_estimators': (50, 150),  # Ajuste conforme necessário
    'learning_rate': (0.01, 1.0, 'log-uniform'),
    'max_depth': (1, 20),
}

# Modelo XGBoost
xgb = XGBRegressor(objective='reg:squarederror')

# Otimização Bayesiana
opt = BayesSearchCV(xgb, param_space, n_iter=50, cv=5, n_jobs=-1)
opt.fit(X_train, y_train)

# Melhores hiperparâmetros
best_params = opt.best_params_
print("Melhores Hiperparâmetros:", best_params)

