import pandas as pd
from sklearn.linear_model import LinearRegression

class SalesModel:
    def __init__(self, data_path="data/sales.csv"):
        # Load dataset
        self.data = pd.read_csv(data_path, parse_dates=["date"])
        # Convert date to day of year
        self.data["day"] = self.data["date"].dt.dayofyear

        # Features and target
        X = self.data[["day"]]   # features
        y = self.data["sales"]   # target

        # Train model
        self.model = LinearRegression()
        self.model.fit(X, y)     # ✅ use X and y

    def predict(self, day):
        return self.model.predict([[day]])[0]
