#!/usb/bin/python
#-*- coding:utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.types import VARCHAR
import datetime
import baostock as bs
import pandas as pd
import pymysql

def query_all_stock_profit_data():
    connection = pymysql.connect(db='stock_quant', user='root', password='root', host='127.0.0.1', port=3306,
                                 charset='utf8')
    cursor = connection.cursor()
    cursor.execute("select * from bs_stock_basic where type = 1")
    result = cursor.fetchall()
    quarters =[1, 2, 3, 4]
    for data in result:
        stock_code = data[1];
        ipo_date = data[3];
        stock_name = data[2]
        for quarter in quarters:
            query_one_stock_profit_data(stock_code, ipo_date, stock_name,quarter)
    connection.close()

def query_one_stock_profit_data(stock_code,ipo_date,stock_name,quarter):
    # 登陆系统
    bs.login()
    # 查询季频估值指标盈利能力
    profit_list = []
    split_ipo_date = ipo_date.split('-')
    rs_profit = bs.query_profit_data(code=stock_code, year=split_ipo_date[0], quarter=quarter)
    while (rs_profit.error_code == '0') & rs_profit.next():
        profit_list.append(rs_profit.get_row_data())
    engine = create_engine('mysql+pymysql://root:root@localhost:3306/stock_quant?charset=utf8')
    result_profit = pd.DataFrame(profit_list, columns=rs_profit.fields)
    result_profit.to_sql('bs_stock_profit', engine, if_exists='replace',index=False)
    # result_profit.to_sql('bs_stock_profit', engine, if_exists='replace',dtype={'index':VARCHAR(result_profit.index.get_level_values('index').str.len().max())})
    bs.logout()

if __name__ == '__main__':
    start = datetime.datetime.now()
    query_all_stock_profit_data()
    end = datetime.datetime.now()
    print('Running time: %s Seconds' % (end - start))