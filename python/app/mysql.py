# coding:utf-8
# 数据库模块，封装 MySQL 的操作
import pymysql

from config.config import host, port, database, user, passwd


class MySQL:
    def __init__(self) -> None:
        super().__init__()
        self.__connection = pymysql.connect(host=host, port=port, database=database, user=user, passwd=passwd)
        self.__connection.set_charset('utf8')

    def execute(self, sql):
        """Execute a sql statement and return the effected rows and output

        :param sql: sql statement to be run
        :return: effected rows and sql output
        """
        with self.__connection.cursor() as cursor:
            effect_rows = cursor.execute(sql)
            self.__connection.commit()
        return effect_rows, cursor.fetchall()

    def close(self):
        self.__connection.close()


def db_init():
    db = MySQL()
    db.execute('DROP TABLE IF EXISTS urls')
    db.execute('CREATE TABLE urls('
               '  id INT AUTO_INCREMENT PRIMARY KEY, '
               '  city CHAR(20), '
               '  url VARCHAR(128)'
               ') ENGINE=INNODB CHAR SET=utf8')
    db.execute('DROP TABLE IF EXISTS cities')
    db.execute('CREATE TABLE cities('
               '  id INT AUTO_INCREMENT PRIMARY KEY,'
               '  city_name CHAR(20),'
               '  city_url VARCHAR(128),'
               '  page INT'
               ') ENGINE=INNODB CHAR SET=utf8')
    db.close()


if __name__ == '__main__':
    # mysql = MySQL()
    # mysql.execute('DROP TABLE IF EXISTS test')
    # mysql.execute("CREATE TABLE test(id INT, msg CHAR(10))")
    # er, result = mysql.execute("INSERT INTO test VALUES (1, 'hello'), (2, 'world')")
    # print(er, result)
    # er, result = mysql.execute('SELECT * FROM test')
    # print(er, result)

    db_init()
