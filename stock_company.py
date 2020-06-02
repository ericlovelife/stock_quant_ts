#!/usb/bin/python
#-*- coding:utf-8 -*-

from sqlalchemy import create_engine
import tushare as ts
import datetime

def save_stock_company():
    engine = create_engine('mysql+pymysql://root:root@localhost:3306/stock_quant?charset=utf8')
    ts.set_token('428031aafb294e841ad21237fca19c91d0483e83435294728abcffeb')
    pro = ts.pro_api()
    fields = 'ts_code,exchange,chairman,manager,secretary,reg_capital,setup_date,province,city,introduction,website,email,office,employees,main_business,business_scope'
    dfSZSE = pro.stock_company(exchange='SZSE', fields=fields)
    dfSSE = pro.stock_company(exchange='SSE', fields=fields)
    df = dfSZSE.append(dfSSE)
    df.to_sql('stock_company', engine, index=True)

if __name__ == '__main__':
    start = datetime.datetime.now()
    save_stock_company()
    end = datetime.datetime.now()
    print('Running time: %s Seconds' % (end - start))