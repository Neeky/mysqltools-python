#-*- coding:utf8 -*-

"""
模拟多个会话连接进数据库
"""

import time
from threading import Thread
from mysql import connector

class MySQLSession(Thread):
    """
    """

    def __init__(self, user_name, user_password, host="127.0.0.1", port=3306, sql="select 'mysqltools-python' as softname ;"):
        Thread.__init__(self)
        self.user_name = user_name
        self.user_password = user_password
        self.host = host
        self.port = port
        self.sql = sql
    
        self._conn = None
        self.daemon = True

        if sql.lower().startswith("select"):
            self.is_select_sql = True

    def run(self):
        # 不释放了等待进行退出
        cnx = connector.connect(host=self.host,port=self.port,user=self.user_name,password=self.user_password)
        cursor = cnx.cursor()
        while True:
            cursor.execute(self.sql)
            if self.is_select_sql:
                _ = cursor.fetchall()
            else:
                cnx.commit()
            time.sleep(0.5)
    

def create_sessions(user_name, user_password, host="127.0.0.1", port=3306, sql="select 'mysqltools-python' as softname ;",count = 7):
    sessions = []
    for i in range(count):
        session = MySQLSession(user_name,user_password,host,port,sql)
        sessions.append(session)
        session.start()
    