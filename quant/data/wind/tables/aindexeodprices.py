from ....common.db.sql import VARCHAR as VARCHAR2, Numeric as NUMBER, DateTime, Column, BaseModel


class AIndexEODPrices(BaseModel):
    """
    中国A股指数日行情

    Attributes
    ----------
    object_id: VARCHAR2(100)
        对象ID   
    s_info_windcode: VARCHAR2(40)
        Wind代码   
    trade_dt: VARCHAR2(8)
        交易日期   
    crncy_code: VARCHAR2(10)
        货币代码   
    s_dq_preclose: NUMBER(20,4)
        昨收盘价(点)   
    s_dq_open: NUMBER(20,4)
        开盘价(点)   
    s_dq_high: NUMBER(20,4)
        最高价(点)   
    s_dq_low: NUMBER(20,4)
        最低价(点)   
    s_dq_close: NUMBER(20,4)
        收盘价(点)   

    """
    object_id = Column(VARCHAR2(100))
    s_info_windcode = Column(VARCHAR2(40))
    trade_dt = Column(VARCHAR2(8))
    crncy_code = Column(VARCHAR2(10))
    s_dq_preclose = Column(NUMBER(20,4))
    s_dq_open = Column(NUMBER(20,4))
    s_dq_high = Column(NUMBER(20,4))
    s_dq_low = Column(NUMBER(20,4))
    s_dq_close = Column(NUMBER(20,4))
    