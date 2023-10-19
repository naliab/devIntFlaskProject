import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.model_selection import train_test_split
from models import TrainData
from app import db

ml_model = LinearRegression()

DEGREE = 3


def train_model():
    data = TrainData.query.all()
    df = pd.DataFrame([{'id': d.id, 'age': d.age, 'sex': d.sex, 'bmi': d.bmi, 'children': d.children,
                        'smoker': d.smoker, 'charges': d.charges} for d in data])
    # print(df)

    X = df.drop(columns=['id', 'charges'])
    y = df['charges']

    # polynomial
    poly = PolynomialFeatures(degree=DEGREE)
    X_poly = poly.fit_transform(X)

    # score
    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=777)
    # X_train = poly.fit_transform(X_train)
    # X_test = poly.fit_transform(X_test)
    # lin = LinearRegression()
    # lin.fit(X_train, y_train)
    # y_pred = lin.predict(X_test)

    # print("R2 score", r2_score(y_test, y_pred))
    # print("MSE", np.sqrt(mean_squared_error(y_test, y_pred)))

    ml_model.fit(X_poly, y)


def predict_model(age, sex, bmi, children, smoker):
    X = [[age, sex, bmi, children, smoker]]

    poly = PolynomialFeatures(degree=DEGREE)
    X_poly = poly.fit_transform(X)

    print(ml_model.predict(X_poly)[0])

    return ml_model.predict(X_poly)[0]
