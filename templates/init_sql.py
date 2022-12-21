import os
import time
import pymysql

DB_HOST = os.getenv('DB_HOST', 'db')
DB_ROOT_PASSWD = os.getenv('DB_ROOT_PASSWD', '')


def wait_for_mysql():
    while True:
        try:
            pymysql.connect(host=DB_HOST, port=3306, user='root', passwd=DB_ROOT_PASSWD)
        except Exception as e:
            print ('waiting for mysql server to be ready: %s', e)
            time.sleep(2)
            continue
        print('mysql server is ready')
        return


wait_for_mysql()
os.system('mysql -h $DB_HOST -p$DB_ROOT_PASSWD -e "create database ccnet_db charset utf8";')
os.system('mysql -h $DB_HOST -p$DB_ROOT_PASSWD -e "create database seafile_db charset utf8";')
os.system('mysql -h $DB_HOST -p$DB_ROOT_PASSWD -e "create database dtable_db charset utf8";')

os.system('mysql -h $DB_HOST -p$DB_ROOT_PASSWD ccnet_db </opt/seatable/seatable-server-latest/sql/mysql/ccnet.sql')
os.system('mysql -h $DB_HOST -p$DB_ROOT_PASSWD seafile_db </opt/seatable/seatable-server-latest/sql/mysql/seafile.sql')
os.system('mysql -h $DB_HOST -p$DB_ROOT_PASSWD dtable_db </opt/seatable/seatable-server-latest/sql/mysql/dtable.sql')

print('Init sql success')
