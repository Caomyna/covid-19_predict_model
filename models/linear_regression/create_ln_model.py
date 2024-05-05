import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
import pickle

# Đọc dữ liệu
covid =  pd.read_csv('../../covid_19/data_world/covid_19_clean_complete.csv')

#Tiền xử lý dữ liệu
datewise = covid.groupby(["Date"]).agg({"Confirmed":"sum","Recovered":"sum","Deaths":"sum"})
datewise["Days Since"]=datewise.index-datewise.index[0]
datewise["Days Since"] = datewise["Days Since"].dt.days
train_ml = datewise.iloc[:int(datewise.shape[0]*0.95)]
valid_ml = datewise.iloc[:int(datewise.shape[0]*0.95):]

# Huấn luyện mô hình Linear Regression
lin_reg = LinearRegression()
scaler = StandardScaler()
X_train = np.array(train_ml["Days Since"]).reshape(-1, 1)
y_train = np.array(train_ml["Confirmed"]).reshape(-1, 1)
lin_reg.fit(X_train, y_train)

# Lưu mô hình vào file .plk
with open('linear_regression_model.plk', 'wb') as f:
    pickle.dump(lin_reg, f)

