"""Wind数据库接口"""
import sys
import pandas as pd
from sqlalchemy.sql import select
from . import tables
from ...common.localize import LOCALIZER
from ...common.settings import CONFIG
from ...common.db.sql import SQLClient

__all__ = ['WIND_CONNECTION', 'tables', 'get_wind_data']


def get_sql_connection():
    """Returns a SQLClient object with settings in `config.cfg`"""
    return SQLClient(
        host=CONFIG.WIND_HOST,
        port=CONFIG.WIND_PORT,
        db_driver=CONFIG.WIND_DB_DRIVER,
        db_type=CONFIG.WIND_DB_TYPE,
        db_name=CONFIG.WIND_DB_NAME,
        username=CONFIG.WIND_USERNAME,
        password=CONFIG.WIND_PASSWORD,
    )


def __get_field(table, fieldname):
    if hasattr(table, fieldname):
        return getattr(table, fieldname)
    raise AttributeError("Table `%s` has no field `%s`" % (table.__tablename__, fieldname))


@LOCALIZER.wrap("wind")
def get_wind_rawdata(table):
    """从Wind数据库获取数据

    Parameters
    ----------
    table
        要读的SQL表, 参考`quant.data.wind.tables`
    """
    if isinstance(table, str):
        table = getattr(tables, table)
    columns = table.__table__.columns
    wind_connection = get_sql_connection()
    data = pd.read_sql(select(columns), wind_connection.engine)
    return data


@LOCALIZER.wrap("wind", exclude=['index', 'columns', 'parse_dates'])
def get_wind_data(table, field, index=None, columns=None, parse_dates=True):
    """从Wind数据库获取数据，并转换为以股票代码为列、日期为行的格式

    Parameters
    ----------
    table
        要读的SQL表, 参考`quant.data.wind.tables`
    field
        作为值的字段
    index
        作为index的字段
    columns
        作为columns的字段
    parse_dates: bool, optional
        是否将index字段转换为datetime

    Returns
    -------
        pd.DataFrame
    """
    if isinstance(table, str):
        table = getattr(tables, table)
    columns = columns or tables.DEFAULT_FIELDS[table]["columns"]
    index = index or tables.DEFAULT_FIELDS[table]["index"]
    field_ = __get_field(table, field)
    index_ = __get_field(table, index)
    columns_ = __get_field(table, columns)
    sql_statement = select([field_, index_, columns_])
    wind_connection = get_sql_connection()
    data = pd.read_sql(sql_statement, wind_connection.engine)
    data = data.pivot(index=index, columns=columns, values=field)
    if parse_dates:
        data.index = pd.to_datetime(data.index)
    return data


