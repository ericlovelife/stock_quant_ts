#!/usb/bin/python
#-*- coding:utf-8 -*-

from sqlalchemy import create_engine
import datetime
import baostock as bs
import pandas as pd

def bs_save_stock_basic():
    '''
    获取股票和指数
    :return:
    '''
    bs.login()
    rs = bs.query_stock_basic()
    data_list = []
    while (rs.error_code == '0') & rs.next():
        data_list.append(rs.get_row_data())
    result = pd.DataFrame(data_list, columns=rs.fields)
    engine = create_engine('mysql+pymysql://root:root@localhost:3306/stock_quant?charset=utf8')
    result.to_sql('bs_stock_basic', engine, index=True)
    bs.logout()

if __name__ == '__main__':
    bs_save_stock_basic()