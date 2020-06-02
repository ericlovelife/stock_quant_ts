#!/usb/bin/python
#-*- coding:utf-8 -*-
from sqlalchemy import create_engine
import tushare as ts

def save_hs_const():
    '''
    获取沪股通
    :return:
    '''
    engine = create_engine('mysql+pymysql://root:root@localhost:3306/stock_quant?charset=utf8')
    ts.set_token('428031aafb294e841ad21237fca19c91d0483e83435294728abcffeb')
    pro = ts.pro_api()
    dfSH = pro.hs_const(hs_type='SH')
    dfSZ = pro.hs_const(hs_type='SZ')
    df = dfSH.append(dfSZ)
    df.to_sql('hs_const', engine, index=True)

if __name__ == '__main__':
    save_hs_const()