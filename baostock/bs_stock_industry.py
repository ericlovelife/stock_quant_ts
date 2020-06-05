#!/usb/bin/python
#-*- coding:utf-8 -*-

from sqlalchemy import create_engine
import datetime
import baostock as bs
import pandas as pd

def bs_save_stock_industry():
    '''
    获取行业信息
    :return:
    '''
    bs.login()
    rs = bs.query_stock_industry()
    industry_list = []
    while (rs.error_code == '0') & rs.next():
        industry_list.append(rs.get_row_data())
    engine = create_engine('mysql+pymysql://root:root@localhost:3306/stock_quant?charset=utf8')
    result = pd.DataFrame(industry_list, columns=rs.fields)
    result.to_sql('bs_stock_industry', engine, index=True)
    bs.logout()

if __name__ == '__main__':
    bs_save_stock_industry()