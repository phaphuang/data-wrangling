#  -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import pandas as pd
import MySQLdb
from sqlalchemy import create_engine

# set pandas encoding to utf-8
pd.options.display.encoding = str('utf-8')

def main():
    df = pd.read_csv('lottery_th.csv', index_col=0, converters={'first_price': lambda x: str(x), 'last_second_price': lambda x: str(x)})
    df.replace(['มกราคม','กุมภาพันธ์','มีนาคม','เมษายน','พฤษภาคม','มิถุนายน','กรกฎาคม','สิงหาคม','กันยายน','ตุลาคม','พฤศจิกายน','ธันวาคม'],
               [1,2,3,4,5,6,7,8,9,10,11,12],
               inplace=True)
    df.sort_values(by=['year','month','day'], inplace=True, ascending=False)
    df.reset_index(inplace=True, drop=True)
    #print(df)

    engine = create_engine('mysql+mysqldb://root:@localhost/lottery')
    with engine.connect() as conn, conn.begin():
        df.to_sql('lottery_db', conn, if_exists='replace')

'''
def insert_to_database(sql_command, values):
    db = MySQLdb.connect(host="localhost",
                         user="root",
                         passwd="",
                         db="lottery",
                         charset="utf8")
    try:
        print("=============== CONNECTION SUCCESSFUL =================")
        cursor = db.cursor()

        try:
            cursor.execute(sql_command, values)
            db.commit()
            print("============= Insert Data! ==============")
        except Exception, e:
            print(e)
            db.rollback()

        db.close()
    except MySQLdb.Error:
        print("==================== ERROR IN CONNECTION =================")
'''

if __name__ == '__main__':
    main()
