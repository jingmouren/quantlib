"""quant.analysis"""
import numpy as np
import pandas as pd
import pandas.tseries.offsets
from ..data import wind


def cal_mdd(netvalue, compound=True):
    """
    计算最大回撤

    Parameters
    ----------
    netvalue: pd.Series
        净值序列
    compound: bool, optional
        是否为复利制，如果为真，回撤计算方法为$\frac{N_j}{N_i} - 1$ (j > i)；
                     如果为假，回撤计算方法为$N_j - N_i$ (j > i)

    Returns
    -------
    最大回撤值(正值)
    """
    cm = netvalue.cummax()
    if compound:
        dd = netvalue / cm - 1
    else:
        dd = netvalue - cm
    mdd = (-dd).max()
    return mdd


def get_ic(table1, table2):
    """
    求两组数据之间的IC score

    Parameters
    ----------
    table1, table2: pd.DataFrame
        要计算IC的两个数据框

    Returns
    -------
    pd.Series
        每期的相关系数，求平均可得IC分数。
    """
    common_index = sorted(set(table1.index) & set(table2.index))
    ic = pd.Series(np.empty(len(common_index)), index=common_index)
    for date_idx in common_index:
        rk1 = table1.loc[date_idx]
        rk2 = table2.loc[date_idx]
        corr = rk1.corr(rk2, method="spearman")
        ic[date_idx] = corr
    return ic.dropna()


def get_factor_exposure(position, factor_value, benchmark=None):
    """计算持仓的因子暴露

    Parameters
    ----------
    position: pd.DataFrame
        每期的持仓
    factor_value: pd.DataFrame
        每期的因子值
    benchmark: str
        要减去的指数的暴露，为None则不减
    """
    data = pd.Series(np.empty(position.shape[0]), index=position.index)
    if benchmark:
        weights = wind.get_index_weight("AIndexHS300FreeWeight", benchmark)
    for date in position.index:
        if benchmark:
            offset_days = -date.day              # 计算当前的基准因子暴露
            while 1:
                try:
                    offset = pd.tseries.offsets.DateOffset(months=1, days=offset_days)
                    weight = weights.loc[date + offset] / 100
                    break
                except KeyError:
                    offset_days -= 1
        absolute_exposure = ((position.loc[date] * factor_value.loc[date]).sum()
                             / (position.loc[date].sum() + 1e-5))
        if benchmark:
            benchmark_exposure = (weight * factor_value.loc[date]).sum()
            relative_exposure = absolute_exposure - benchmark_exposure
            data.loc[date] = relative_exposure
        else:
            data.loc[date] = absolute_exposure
    return data
