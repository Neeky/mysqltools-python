# -*- coding:utf8 -*-
"""

"""
import time
import psutil
from collections import namedtuple
from mysql import connector


def mem_info_generator(pid):
    """
    """
    process = psutil.Process(pid)
    while True:
        yield process.memory_info()
        time.sleep(1) 


class MySQLMemCostGather(object):
    """
    """
    def __init__(self,user,password,host="127.0.0.1",port=3306):
        self.cnx = connector.connect(host=host,port=port,user=user,password=password)
        self.cursor = self.cnx.cursor()

    def global_connection_memory(self):
        self.cursor.execute("show global status like 'Global_connection_memory'")
        _,value = self.cursor.fetchone()
        return int(value)

def global_connection_memory_generator(port=3306,user="root",password="dbma@0352"):
    try:
        gather = MySQLMemCostGather(user,password,port=port)
        while True:
            yield gather.global_connection_memory()
            #time.sleep(1)
    except Exception as err:
        while True:
            yield 0