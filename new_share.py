#!/usb/bin/python
#-*- coding:utf-8 -*-

from sqlalchemy import create_engine
import tushare as ts
import datetime
import time

def save_new_share(start_date, end_date):
    '''
        获取新股上市列表数据
        :return:
        '''
    engine = create_engine('mysql+pymysql://root:root@localhost:3306/stock_quant?charset=utf8')
    ts.set_token('428031aafb294e841ad21237fca19c91d0483e83435294728abcffeb')
    pro = ts.pro_api()
    # 获取多个公司高管全部数据
    df = pro.new_share(start_date=start_date, end_date=end_date)
    df.to_sql('new_share', engine, index=True)

if __name__ == "__main__":
    start = datetime.datetime.now()
    start_year = int(time.strftime('%Y', time.localtime(time.time()))) - 3
    start_date = '{}{}'.format(start_year, '0101')
    end_year = time.strftime('%Y', time.localtime(time.time()))
    end_date = '{}{}'.format(end_year, '1231')
    save_new_share(start_date, end_date)
    end = datetime.datetime.now()
    print('Running time: %s Seconds' % (end - start))