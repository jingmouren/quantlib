from ....common.db.sql import VARCHAR, Numeric as NUMBER, DateTime as DATETIME, Column, BaseModel, CLOB, DATE
VARCHAR2 = VARCHAR


class ChinaOptionValuation(BaseModel):
    """
    4.196 中国期权衍生指标

    Attributes
    ----------
    object_id: VARCHAR2(100)
        对象ID   
    s_info_windcode: VARCHAR2(40)
        Wind代码   
    trade_dt: VARCHAR2(8)
        交易日期   
    w_anal_underlyingimpliedvol: NUMBER(24,8)
        隐含波动率(%)   
    w_anal_delta: NUMBER(24,8)
        Delta   
    w_anal_theta: NUMBER(24,8)
        Theta   
    w_anal_gamma: NUMBER(24,8)
        Gamma   
    w_anal_vega: NUMBER(24,8)
        Vega   
    w_anal_rho: NUMBER(24,8)
        Rho   
    opdate: DATETIME
        opdate   
    opmode: VARCHAR(1)
        opmode   

    """
    __tablename__ = "ChinaOptionValuation"
    object_id = Column(VARCHAR2(100), primary_key=True)
    s_info_windcode = Column(VARCHAR2(40))
    trade_dt = Column(VARCHAR2(8))
    w_anal_underlyingimpliedvol = Column(NUMBER(24,8))
    w_anal_delta = Column(NUMBER(24,8))
    w_anal_theta = Column(NUMBER(24,8))
    w_anal_gamma = Column(NUMBER(24,8))
    w_anal_vega = Column(NUMBER(24,8))
    w_anal_rho = Column(NUMBER(24,8))
    opdate = Column(DATETIME)
    opmode = Column(VARCHAR(1))
    
