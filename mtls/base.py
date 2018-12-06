# -*- coding:utf8 -*-
"""
定义基类:
    ConnectorBase 代表一个到Mysql数据库的连接
    VariableBase  代表一个查询global variable的连接
    StatuBase     代表一个查询global statu   的连接
"""

__all__ = ['ConnectorBase','VariableBase','StatuBase','PsBase','ShowSlave']

import mysql.connector
import logging
import subprocess
import socket
import json

class Discovery(object):
    def __init__(self,value):
        self._value = value

    @property
    def value(self):
        return json.dumps(self._value)


def is_mysql_port(port):
    """传入一个端口、如果这个端口是MySQL协议用的，那么就返回这个端口，如果不是就返回None
    """
    client_socket = None
    try:
        client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        client_socket.connect(('127.0.0.1',port))
        client_socket.settimeout(0.1)
        #MySQL协议下是由Server端先发送握手信息到client的
        message = client_socket.recv(1024)
        message = message.decode('latin-1').lower()
        if 'password' in message:
            return port
    except Exception as e:
        return None
    finally:
        client_socket.close()

def mysql_discovery(*args,**kwargs):
    """查找主机上的MySQL服务并返回它们的监听的port  {"data": [{"{#MYSQLPORT}": 3306}]}
    """
    output = subprocess.check_output(['netstat','-ltn'])
    output = output.decode('latin-1').split('\n')[2:-1]
    result = {"data":[]}
    ports = []
    try:
        for line in output:
            _,_,_,host_and_port,*_ = line.split()
            index = host_and_port.rindex(":")
            port = int(host_and_port[index+1:])
            #只有在这个端口是被MySQL占用的情况下才返回
            if is_mysql_port(port):
                result["data"].append({"{#MYSQLPORT}":port})
    except Exception as e:
        print(e)
        exit()
    return Discovery(value=result)

def disk_discovery(*args,**kwargs):
    result = {"data":[]}
    message = subprocess.check_output(['lsblk',])
    message = message.decode('latin-1')
    for line in message.split('\n'):
        if 'disk' in line:
            disk_name,*_ = line.split()
            result['data'].append({"{#DISKNAME}":disk_name})
    return Discovery(value=result)


class ConnectorBase(object):
    """ConnectorBase代表一个与数据库之间的连接
    ConnectorBase实例的.cursor属性代表着一个连接到数据库的cursor对象
    """
    user='mtsuser'
    password='mts10352'
    host='127.0.0.1'
    port=3306
    _cnx=None
    _cursor=None
    _logger=None

    def __init__(self,host='127.0.0.1',port=3306,user='mtsuser',password='mts10352',database='information_schema',*args,**kws):
        self.host=host
        self.port=port
        self.user=user
        self.password=password
        self.database=database
        self._cnx=None
        self._cursor=None
        self._logger=None
        

    @property
    def cursor(self):
        """返回cursor对象、cursor对象可以完成对数据库的操作
        """
        if self._cursor != None:
            return self._cursor
        else:
            try:
                self._cnx=mysql.connector.connect(user=self.user,password=self.password,host=self.host,port=self.port,database=self.database)
                self._cursor=self._cnx.cursor()
                return self._cursor
            except Exception as e:
                error_message=str(e)
                self.logger.info(error_message)
                self.logger.info("exit")
                self.close()
                exit()
    
    @property
    def logger(self):
        """返回logger对象方便日志的输出
        """
        if self._logger != None:
            return self._logger
        else:
            self._logger=logging.getLogger("mts.base.{0}".format(self.__class__))
            stream_handler=logging.StreamHandler()
            formater=logging.Formatter("%(asctime)-24s %(levelname)-8s %(name)-24s : %(message)s")
            stream_handler.setFormatter(formater)
            self._logger.addHandler(stream_handler)
            self._logger.setLevel(logging.DEBUG)
            return self._logger

    def __str__(self):
        """自定义ConnectorBase对象的字符表示
        """
        obj_str="{0.__class__} instance (host={0.host},port={0.port},user={0.user},password={0.password} )".format(self)
        return obj_str

    def __del__(self):
        """资源回收
        """
        if self._cnx != None:
            self._cnx.close()
    
    def close(self):
        if self._cnx != None:
            self._cnx.close()
        

class VariableBase(ConnectorBase):
    """定义一个用于查询variable的类，类字符variable_name用于指定variable的名字，variable_type用于指定variable对应值的类型
    """
    variable_name=None
    variable_type="string"
    _variable_types=("string","byte","intger","percent","bool")
    _value=None

    def __init__(self,host='127.0.0.1',port=3306,user='mtsuser',password='mts10352',database='information_schema',
                 variable_name=None,variable_type="string",*args,**kws):
        super(VariableBase,self).__init__(host,port,user,password)
        if variable_name != None:
            self.variable_name=variable_name
            self.variable_type=variable_type

    
    def _get_value(self):
        try:
            self.cursor.execute("select @@{0} ;".format(self.variable_name))
            tmp_value=self.cursor.fetchone()
            if tmp_value != None and len(tmp_value)==1:
                return tmp_value[0]
            else:
                self.logger.info("variable {0} has a bad value {1}".format(self.variable_name,tmp_value))
                self.close()
                exit()
        except Exception as e:
                errore_message=str(e)
                self.logger.info(errore_message)
                self.logger.info("exit")
                self.close()
                exit()            

    
    @property
    def value(self):
        #format_mapper={'string':self.format_string_value,
        #               'byte'  :self.format_byte_value,
        #               'intger':self.format_intger_value,
        #               'bool'  :self.format_bool_value,
        #}
        if self._value == None:
            self._value=self._get_value()
        return self._value
        #return format_mapper[self.variable_type](self._value)

    #@property
    #def original_value(self):
    #    return self._get_value()

        
class StatuBase(ConnectorBase):
    statu_name="uptime"
    statu_type="intger"
    _statu_types=("string","byte","intger","percent","bool")
    _value=None

    def __init__(self,host='127.0.0.1',port=3306,user='mtsuser',password='mts10352',
                 statu_name=None,statu_type="intger",*args,**kw):
        super(StatuBase,self).__init__(host,port,user,password)
        if statu_name != None:
            self.statu_name=statu_name
            self.statu_type=statu_type
        self._value=None

    #def format_byte_value(self,raw_value):
    #    """
    #    由于statu 是由show global status like 'xxx' 得到的，所以它返回的是str,对于字节类型的statu,转换一下才行
    #    """
    #    return super(StatuBase,self).format_byte_value(int(self._value))

    def _get_value(self):
        if self._value != None:
            return self._value
        else:
            try:
                self.cursor.execute("show global status like '{0}' ;".format(self.statu_name))
                name_and_value=self.cursor.fetchone()
                if name_and_value == None:
                    self.logger.info("get a None value for statu {0} ".format(self.statu_name))
                    self.close()
                    exit()
                name,value=name_and_value
                self._value=value
                return self._value
            except Exception as e:
                error_message=str(e)
                self.logger.info(error_message)
                self.close()
                exit()

    @property
    def value(self):
        if self._value == None:
            self._value = self._get_value()
        return self._value
        #format_mapper={'string':self.format_string_value,
        #               'intger':self.format_intger_value,
        #               'byte'  :self.format_byte_value,}
        #return format_mapper[self.statu_type](self._get_value())

    #@property
    #def original_value(self):
    #    return self._get_value()
        

class PsBase(ConnectorBase):
    """
    所有与performance_schema操作相关的基类
    """


class ShowSlave(ConnectorBase):
    """通过show slave status 提取信息
    """
    #mysql-8.0.11 版本下('Waiting for master to send event', '127.0.0.1', 'repl', 3307, 60, 'mysql-bin.000001', 151, 'sqlstudio-relay-bin.000002', 357, 'mysql-bin.000001', 'Yes', 'Yes', '', '', '', '', '', '', 0, '', 0, 151, 561, 'None', '', 0, 'No', '', '', '', '', '', 0, 'No', 0, '', 0, '', '', 375, '2c9732e2-8740-11e8-9514-000c29cb87a3', 'mysql.slave_master_info', 0, None, 'Slave has read all relay log; waiting for more updates', 86400, '', '', '', '', '', '', '8e64b57f-83eb-11e8-be2f-000c29cb87a3:1', 1, '', '', '', '', 0)
    show_slave_name=None
    dimensions ={
        'Slave_IO_State':0,
        'Master_Host':1,
        'Master_User':2,
        'Master_Port':3,
        'Connect_Retry':4,
        'Master_Log_File':5,
        'Read_Master_Log_Pos':6,
        'Relay_Log_File':7,
        'Relay_Log_Pos':8,
        'Relay_Master_Log_File':9,
        'Slave_IO_Running':10,
        'Slave_SQL_Running':11,
        'Replicate_Do_DB':12,
        'Replicate_Ignore_DB':13,
        'Replicate_Do_Table':14,
        'Replicate_Ignore_Table':15,
        'Replicate_Wild_Do_Table':16,
        'Replicate_Wild_Ignore_Table':17,
        'Last_Errno':18,
        'Last_Error':19,
        'Skip_Counter':20,
        'Exec_Master_Log_Pos':21,
        'Relay_Log_Space':22,
        'Until_Condition':23,
        'Until_Log_File':24,
        'Until_Log_Pos':25,
        'Master_SSL_Allowed':26,
        'Master_SSL_CA_File':27,
        'Master_SSL_CA_Path':28,
        'Master_SSL_Cert':29,
        'Master_SSL_Cipher':30,
        'Master_SSL_Key':31,
        'Seconds_Behind_Master':32,
        'Master_SSL_Verify_Server_Cert':33,
        'Last_IO_Errno':34,
        'Last_IO_Error':35,
        'Last_SQL_Errno':36,
        'Last_SQL_Error':37,
        'Replicate_Ignore_Server_Ids':38,
        'Master_Server_Id':39,
        'Master_UUID':40,
        'Master_Info_File':41,
        'SQL_Delay':42,
        'SQL_Remaining_Delay':43,
        'Slave_SQL_Running_State':44,
        'Master_Retry_Count':45,
        'Master_Bind':46,
        'Last_IO_Error_Timestamp':47,
        'Last_SQL_Error_Timestamp':48,
        'Master_SSL_Crl':49,
        'Master_SSL_Crlpath':50,
        'Retrieved_Gtid_Set':51,
        'Executed_Gtid_Set':52,
        'Auto_Position':53,
        'Replicate_Rewrite_DB':54,
        'Channel_Name':55,
        'Master_TLS_Version':56,
        'Master_public_key_path':57,
        'Get_master_public_key':58
    }
    dimensions_55 = {
        'Slave_IO_State': 0,
        'Master_Host': 1,
        'Master_User': 2,
        'Master_Port': 3,
        'Connect_Retry': 4,
        'Master_Log_File': 5,
        'Read_Master_Log_Pos': 6,
        'Relay_Log_File': 7,
        'Relay_Log_Pos': 8,
        'Relay_Master_Log_File': 9,
        'Slave_IO_Running': 10,
        'Slave_SQL_Running': 11,
        'Replicate_Do_DB': 12, 
        'Replicate_Ignore_DB': 13,
        'Replicate_Do_Table': 14,
        'Replicate_Ignore_Table': 15,
        'Replicate_Wild_Do_Table': 16, 
        'Replicate_Wild_Ignore_Table': 17,
        'Last_Errno': 18,
        'Last_Error': 19,
        'Skip_Counter': 20,
        'Exec_Master_Log_Pos': 21,
        'Relay_Log_Space': 22,
        'Until_Condition': 23,
        'Until_Log_File': 24,
        'Until_Log_Pos': 25,
        'Master_SSL_Allowed': 26,
        'Master_SSL_CA_File': 27, 
        'Master_SSL_CA_Path': 28,
        'Master_SSL_Cert': 29, 
        'Master_SSL_Cipher': 30,
        'Master_SSL_Key': 31, 
        'Seconds_Behind_Master': 32,
        'Master_SSL_Verify_Server_Cert': 33,
        'Last_IO_Errno': 34,
        'Last_IO_Error': 35,
        'Last_SQL_Errno': 36,
        'Last_SQL_Error': 37,
        'Replicate_Ignore_Server_Ids': 38,
        'Master_Server_Id': 39,
        'Cur_Exec_Relay_Log_File': 40,
        'Cur_Exec_Relay_Log_Pos': 41,
        'Wanted_Purge_Relay_Log': 42,
        'Purged_Relay_Log': 43
    }

    def __init__(self,host='127.0.0.1',port=3306,user='mtsuser',password='mts10352',*args,**kw):
        super().__init__(host,port,user,password)
        self._value=None

    def _get_value(self):
        if self._value != None:
            return self._value
        else:
            try:
                #适配mysql-5.5.x版本的show slave status;
                self.cursor.execute("select @@version")
                mysql_version,*_ = self.cursor.fetchone()
                if '5.5' in mysql_version:
                    self.dimensions = self.dimensions_55

                self.cursor.execute("show slave status")    
                data = self.cursor.fetchone()
                if data == None:
                    self._value = "this node is master"
                    return self._value
                index = self.dimensions[self.show_slave_name]
                self._value = data[index]
                return self._value
            except Exception as e:
                error_message=str(e)
                self.logger.info(error_message)
                self.close()
                exit()  

    @property
    def value(self):
        if self._value == None:
            self._value = self._get_value()
        return self._value


class ShowMaster(ConnectorBase):
    """分析show master status 的输出
    """
    show_master_name = None
    dimensions = {
        'File':0,
        'Position':1,
        'Binlog_Do_DB':2,
        'Binlog_Ignore_DB':3,
        'Executed_Gtid_Set':4,
    }

    def __init__(self,host='127.0.0.1',port=3306,user='mtsuser',password='mts10352',*args,**kw):
        super().__init__(host,port,user,password)
        self._value=None

    def _get_value(self):
        if self._value != None:
            return self._value
        else:
            try:
                self.cursor.execute("show master status")    
                data = self.cursor.fetchone()
                index = self.dimensions[self.show_master_name]
                self._value = data[index]
                return self._value
            except Exception as e:
                error_message=str(e)
                self.logger.info(error_message)
                self.close()
                exit()  

    @property
    def value(self):
        if self._value == None:
            self._value = self._get_value()
        return self._value  



class InnodbStatus(ConnectorBase):
    """分析show engine innodb status 的输出
    """
    def __init__(self,host='127.0.0.1',port=3306,user='mtsuser',password='mts10352',*args,**kw):
        super().__init__(host,port,user,password)
        self._value=None

    def _get_value(self):
        if self._value != None:
            return self._value
        else:
            try:
                self.cursor.execute("show engine innodb status")    
                data = self.cursor.fetchone()
                self._value = data
                return self._value
            except Exception as e:
                error_message=str(e)
                self.logger.info(error_message)
                self.close()
                exit()  

    @property
    def value(self):
        if self._value == None:
            self._value = self._get_value()[2]
            
        return self._value

class InnodbStatusLog(InnodbStatus):
    """返回指定维度的数据
    """
    dimension = "Log sequence number"

    @property
    def value(self):
        _ = super().value
        for line in self._value.split('\n'):
            if self.dimension in line:
                *_,lsn = line.split(self.dimension)
                return lsn.strip()
        return -1