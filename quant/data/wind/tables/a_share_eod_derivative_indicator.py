from ....common.db.sql import BaseModel, Column, VARCHAR, Numeric, DateTime


class AShareEODDerivativeIndicator(BaseModel):
    __tablename__ = "AShareEODDerivativeIndicator".upper()
    OBJECT_ID = Column(VARCHAR(100), primary_key=True)
    s_info_windcode = Column(VARCHAR(40))
    trade_dt = Column(VARCHAR(8))
    crncy_code = Column(VARCHAR(10))
    s_val_mv = Column(Numeric(20, 4, asdecimal=False))
    s_dq_mv = Column(Numeric(20, 4, asdecimal=False))
    s_pq_high_52w_ = Column(Numeric(20, 4, asdecimal=False))
    s_pq_low_52w_ = Column(Numeric(20, 4))
    s_val_pe = Column(Numeric(20, 4, asdecimal=False))
    s_val_pb_new = Column(Numeric(20, 4, asdecimal=False))
    s_val_pe_ttm = Column(Numeric(20, 4, asdecimal=False))
    s_val_pcf_ocf = Column(Numeric(20, 4, asdecimal=False))
    s_val_pcf_ocfttm = Column(Numeric(20, 4, asdecimal=False))
    s_val_pcf_ncf = Column(Numeric(20, 4, asdecimal=False))
    s_val_pcf_ncfttm = Column(Numeric(20, 4, asdecimal=False))
    s_val_ps = Column(Numeric(20, 4, asdecimal=False))
    s_val_ps_ttm = Column(Numeric(20, 4, asdecimal=False))
    s_dq_turn = Column(Numeric(20, 4, asdecimal=False))
    s_dq_freeturnover = Column(Numeric(20, 4, asdecimal=False))
    tot_shr_today = Column(Numeric(20, 4, asdecimal=False))
    float_a_shr_today = Column(Numeric(20, 4, asdecimal=False))
    s_dq_close_today = Column(Numeric(20, 4, asdecimal=False))
    s_price_div_dps = Column(Numeric(20, 4, asdecimal=False))
    s_pq_adjhigh_52w = Column(Numeric(20, 4, asdecimal=False))
    s_pq_adjlow_52w = Column(Numeric(20, 4, asdecimal=False))
    free_shares_today = Column(Numeric(20, 4, asdecimal=False))
    net_profit_parent_comp_ttm = Column(Numeric(20, 4, asdecimal=False))
    net_profit_parent_comp_lyr = Column(Numeric(20, 4, asdecimal=False))
    net_assets_today = Column(Numeric(20, 4, asdecimal=False))
    net_cash_flows_oper_act_ttm = Column(Numeric(20, 4, asdecimal=False))
    net_cash_flows_oper_act_lyr = Column(Numeric(20, 4, asdecimal=False))
    oper_rev_ttm = Column(Numeric(20, 4, asdecimal=False))
    oper_rev_lyr = Column(Numeric(20, 4, asdecimal=False))
    net_incr_cash_cash_equ_ttm = Column(Numeric(20, 4, asdecimal=False))
    net_incr_cash_cash_equ_lyr = Column(Numeric(20, 4, asdecimal=False))
    up_down_limit_status = Column(Numeric(2, 0, asdecimal=False))
    lowest_highest_status = Column(Numeric(2, 0, asdecimal=False))
    opdate = Column(DateTime)
    opmode = Column(VARCHAR(1))
