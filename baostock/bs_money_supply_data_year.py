#!/usb/bin/python
#-*- coding:utf-8 -*-

from sqlalchemy import create_engine
import datetime
import time
import baostock as bs
import pandas as pd

def save_money_supply_data_year(start_date, end_date):
    '''
    获取货币供应量(年底余额)
    :param start_date:
    :param end_date:
    :return:
    '''
    bs.login()
    rs = bs.query_money_supply_data_year(start_date=start_date, end_date=end_date)
    data_list = []
    while (rs.error_code == '0') & rs.next():
        data_list.append(rs.get_row_data())
    result = pd.DataFrame(data_list, columns=rs.fields)
    engine = create_engine('mysql+pymysql://root:root@localhost:3306/stock_quant?charset=utf8')
    result.to_sql('bs_money_supply_data_year', engine, index=True)
    bs.logout()

if __name__ == '__main__':
    start = datetime.datetime.now()
    start_year = int(time.strftime('%Y', time.localtime(time.time()))) - 10
    # start_date = '{}-{}'.format(start_year, '01')
    end_year = time.strftime('%Y', time.localtime(time.time()))
    # end_date = '{}-{}'.format(end_year, '12')
    save_money_supply_data_year(str(start_year), end_year)
    end = datetime.datetime.now()
    print('Running time: %s Seconds' % (end - start))