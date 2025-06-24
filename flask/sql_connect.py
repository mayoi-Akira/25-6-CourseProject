import pymysql


def connect():
    con = pymysql.connect(host='localhost',
                          port=3306,
                          user='root',
                          password='112358',
                          database='root',
                          charset='utf8')
    return con
