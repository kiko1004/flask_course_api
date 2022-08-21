import yfinance as yf


class Recommender:
    def __init__(self, ticker):
        self.ticker = ticker

    def get_recomendation(self):
        res = (
            yf.Ticker(self.ticker)
            .recommendations.drop(columns=["From Grade", "Action"])
            .iloc[-1:]
            .reset_index()
            .astype("str")
            .to_dict("r")[0]
        )
        res["recommendation"] = res.pop("To Grade")
        self.res = res

    def get_balancesheet(self):
        df = yf.Ticker(self.ticker).balancesheet.reset_index()
        df.columns = [str(i) for i in df.columns]
        self.res = df.astype("str").to_dict("r")

    def get_analysis(self):
        self.res = (
            yf.Ticker(self.ticker).analysis.reset_index().astype("str").to_dict("r")
        )
