# encoding:utf-8
# @CreateTime: 2022/1/26 9:57
# @Author: Xuguangchun
# @FlieName: connect_mysql.py
# @SoftWare: PyCharm

import pymysql


class OperationMysql:
    def __init__(self):
        self.conn = pymysql.connect(
            user='xuguangchun',
            password='test123456',
            host='localhost',
            port=3306,
            database='newsinfomation',
            cursorclass=pymysql.cursors.DictCursor
        )  # 查询以字典返回
        self.cursor = self.conn.cursor()  # 初始化游标对象

    def find_db(self, mysql):
        self.cursor.execute(mysql)
        result = self.cursor.fetchall()
        print(result)
        return result

    def insert_db(self, mysql, values):
        try:
            self.cursor.execute(mysql, values)
            self.conn.commit()
        except:
            self.conn.rollback()
        self.conn.close()
        self.cursor.close()

    def delete_db(self, mysql):
        try:
            self.cursor.execute(mysql)
            self.conn.commit()
        except:
            self.conn.rollback()    # 错误回滚
        self.conn.close()
        self.cursor.close()

# if __name__ == '__main__':
#     connect = OperationMysql()
#     sql2 = 'select title from news'
#
#     connect.find_db(mysql=sql2)
#
#     sql = 'insert into news(title, fu_title) values(%s, %s)'

#     title = 'My name is '
#     fu_title = 'XUGUANCGHUN1'
#     values = (title, fu_title)
#     connect.insert_db(mysql=sql, values=values)

