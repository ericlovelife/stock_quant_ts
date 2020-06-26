#!/usb/bin/python
#-*- coding:utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.types import VARCHAR
import datetime
import baostock as bs
import pandas as pd
import pymysql
import math

def query_all_stock_profit_data():
    connection = pymysql.connect(db='stock_quant', user='root', password='root', host='127.0.0.1', port=3306,
                                 charset='utf8')
    engine = create_engine('mysql+pymysql://root:root@localhost:3306/stock_quant?charset=utf8')
    cursor = connection.cursor()
    cursor.execute("select * from bs_stock_basic where type = 1")
    result = cursor.fetchall()
    quarters =[1, 2, 3, 4]
    current_month = datetime.datetime.now().month
    current_quarter = math.ceil(current_month/3)
    current_year_quarters = range(1, current_quarter + 1)
    current_year = datetime.datetime.now().year
    result_profit_list = []
    for data in result:
        stock_code = data[1]
        ipo_date = data[3]
        ipo_year = int(ipo_date.split('-')[0])
        ipo_month = int(ipo_date.split('-')[1])
        ipo_quarter = math.ceil(ipo_month/3)
        ipo_quaters = range(ipo_quarter, 5)
        stock_name = data[2]
        print(stock_name,ipo_date,ipo_year,ipo_month,ipo_quaters)
        for year in range(ipo_year, current_year + 1):
            print(year,current_year,ipo_year)
            if year == current_year:
                #当前季度的
                for quarter in current_year_quarters:
                    profit_list = []
                    rs_profit = bs.query_profit_data(code=stock_code, year=year, quarter=quarter)
                    while (rs_profit.error_code == '0') & rs_profit.next():
                        result_profit_list.append(rs_profit.get_row_data())
            elif year == ipo_year:#ipo当年的季度
                for quarter in  ipo_quaters:
                    profit_list = []
                    rs_profit = bs.query_profit_data(code=stock_code, year=year, quarter=quarter)
                    while (rs_profit.error_code == '0') & rs_profit.next():
                        result_profit_list.append(rs_profit.get_row_data())
            else:
                for quarter in quarters:
                    profit_list = []
                    rs_profit = bs.query_profit_data(code=stock_code, year=year, quarter=quarter)
                    while (rs_profit.error_code == '0') & rs_profit.next():
                        result_profit_list.append(rs_profit.get_row_data())
    fields = ['code', 'pubDate', 'statDate', 'roeAvg', 'npMargin', 'gpMargin', 'netProfit', 'epsTTM', 'MBRevenue', 'totalShare', 'liqaShare']
    result_profit = pd.DataFrame(result_profit_list, columns=fields)
    result_profit.to_sql('bs_stock_profit', engine, index=True)
    connection.close()

def query_one_stock_profit_data(stock_code, year, quarter):
    '''
    查询季频估值指标盈利能力
    '''
    profit_list = []
    rs_profit = bs.query_profit_data(code=stock_code, year=year, quarter=quarter)
    print(rs_profit.fields)
    while (rs_profit.error_code == '0') & rs_profit.next():
        profit_list.append(rs_profit.get_row_data())
    return profit_list

if __name__ == '__main__':
    start = datetime.datetime.now()
    bs.login()
    query_all_stock_profit_data()
    bs.logout()
    end = datetime.datetime.now()
    print('Running time: %s Seconds' % (end - start))