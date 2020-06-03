#!/usb/bin/python
#-*- coding:utf-8 -*-

from sqlalchemy import create_engine
import tushare as ts
import datetime

def save_stk_managers():
    '''
        获取上市公司管理层
        积分需要2000以上
        :return:
        '''
    engine = create_engine('mysql+pymysql://root:root@localhost:3306/stock_quant?charset=utf8')
    ts.set_token('428031aafb294e841ad21237fca19c91d0483e83435294728abcffeb')
    pro = ts.pro_api()
    # 获取多个公司高管全部数据
    df = pro.stk_managers(ts_code='000001.SZ,600000.SH')
    df.to_sql('stk_managers', engine, index=True)

if __name__ == "__main__":
    start = datetime.datetime.now()
    save_stk_managers()
    end = datetime.datetime.now()
    print('Running time: %s Seconds' % (end - start))