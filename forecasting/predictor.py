from forecasting.model import SalesModel
from forecasting.utils import date_to_day

class SalesPredictor:
    def __init__(self):
        self.model = SalesModel()

    def forecast(self, date_str):
        day = date_to_day(date_str)
        return self.model.predict(day)
