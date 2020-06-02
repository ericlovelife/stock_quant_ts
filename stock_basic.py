#!/usb/bin/python
#-*- coding:utf-8 -*-
from sqlalchemy import create_engine
import tushare as ts

def save_stock_basic():
    '''
    获取股票列表
    :return:
    '''
    engine = create_engine('mysql+pymysql://root:root@localhost:3306/stock_quant?charset=utf8')
    ts.set_token('428031aafb294e841ad21237fca19c91d0483e83435294728abcffeb')
    pro = ts.pro_api()
    stock_basic_fields = 'ts_code,symbol,name,area,industry,fullname,enname,market,exchange,curr_type,is_hs,list_date'
    df = pro.stock_basic(exchange='', list_status='L', fields=stock_basic_fields)
    df.to_sql('stock_basic', engine, index=True)

if __name__=='__main__':
    save_stock_basic()