"""回测时使用的行情接口"""
from ...data import wind


class AShareMarket:
    """回测中的行情接口，用这个代替wind.get_wind_data，避免使用未来数据"""
    def __init__(self, strategy):
        self.strategy = strategy
        self.market_data = None
        self.trading_days = None
        self.today = None
        self.today_market = None
        self.open_prices = None
        self.close_prices = None
        self.preclose_prices = None

    def initalize_market(self, start_date, end_date):
        self.market_data = (wind.get_wind_data("AShareEODPrices", "s_dq_avgprice") * wind.get_wind_data("AShareEODPrices", "s_dq_adjfactor")) \
            .pct_change() \
            .fillna(0) \
            .truncate(start_date, end_date)
        self.market_data["CASH"] = 0
        self.open_prices = wind.get_wind_data("AShareEODPrices", "s_dq_adjopen")
        self.close_prices = wind.get_wind_data("AShareEODPrices", "s_dq_adjclose")
        self.preclose_prices = wind.get_wind_data("AShareEODPrices", "s_dq_adjpreclose")
        self.trading_days = self.market_data.index

    def on_newday(self, today):
        self.today = today
        self.today_market = self.market_data.loc[today][:-1]

    def get_wind_data(self, *args, **kwargs):
        """封装wind.get_wind_data,避免未来数据"""
        data = wind.get_wind_data(*args, **kwargs)
        return data.truncate(None, self.today)
