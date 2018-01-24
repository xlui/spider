# coding:utf-8
# 数据库模块，封装 MySQL 的操作
import pymysql
from Config.config import host, port, database, user, passwd


class MySQL:
    def __init__(self) -> None:
        super().__init__()
        self.__connection = pymysql.connect(host=host, port=port, database=database, user=user, passwd=passwd)
        self.__connection.set_charset('utf8')

    def execute(self, sql):
        with self.__connection.cursor() as cursor:
            effect_rows = cursor.execute(sql)
            self.__connection.commit()
        return effect_rows, cursor.fetchall()

    def close(self):
        self.__connection.close()


if __name__ == '__main__':
    mysql = MySQL()
    mysql.execute("create table test(id int, msg char(10))")
    er, result = mysql.execute("insert into test values(1, 'hello')")
    print(er)
    er, result = mysql.execute('select * from test')
    print(er, result)
