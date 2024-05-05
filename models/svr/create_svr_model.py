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

# Huấn luyện mô hình SVR
svm = SVR(C=1, degree=5, kernel='poly', epsilon=0.001)
scaler = StandardScaler()
X_train = np.array(train_ml["Days Since"]).reshape(-1, 1)
y_train = np.array(train_ml["Confirmed"]).reshape(-1, 1)
X_train_scaled = scaler.fit_transform(X_train)
svm.fit(X_train_scaled, y_train)


with open('svm_model.plk', 'wb') as f:
    pickle.dump(svm, f)
