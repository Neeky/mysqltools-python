"""
根据给定的类型完全随机的从它的值域中取值。

select table_schema,table_name,column_name,column_type,extra from information_schema.columns where table_name="t";
+--------------+------------+-------------+-------------+----------------+
| TABLE_SCHEMA | TABLE_NAME | COLUMN_NAME | COLUMN_TYPE | EXTRA          |
+--------------+------------+-------------+-------------+----------------+
| tempdb       | t          | id          | int         | auto_increment |
| tempdb       | t          | x           | int         |                |
+--------------+------------+-------------+-------------+----------------+
2 rows in set (0.00 sec)

"""
import os
import copy
import uuid
import random
import string
import logging
from mysql import connector
from datetime import datetime

name = os.path.basename(__file__)
logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s",level=logging.INFO)


class Number(object):
    """
    所有随机数值类型的基类
    """
    min_value = 0
    max_value = 127

    def __init__(self,min_value=None,max_value=None):
        """
        Paramter
        --------
        min_value: int

        max_value: int

        """

        self.min_value = min_value if min_value is not None else self.__class__.min_value
        self.max_value = max_value if max_value is not None else self.__class__.max_value

    def __getitem__(self, index):
        """
        """
        return random.randint(self.min_value, self.max_value)

    def __len__(self):
        """
        """
        return self.max_value - self.min_value

    def __next__(self):
        return self[0]

    def __iter__(self):
        """
        """
        return self

TinyInt = Number

class Bool(Number):
    """
    Bool 数的随机生成器
    """
    def __getitem__(self,index):
        return (Number.__getitem__(self,index) % 2) == 0

class SmallInt(Number):
    """
    SmallInt 的随机生成器
    """
    min_value = 0
    max_value = 32767

class MediumInt(Number):
    """
    MediumInt 的随机生成器
    """
    max_value = 8388607

class Int(Number):
    """
    Int 的随机生成器
    """
    max_value = 2147483647

class BigInt(Number):
    """
    BigInt 的随机生成器
    """
    max_value = 9223372036854775807

class Float(Int):
    """
    """
    def __getitem__(self,index):
        """
        """
        return Int.__getitem__(self,0) + random.random()

Double = Float


class Char(object):
    """
    """
    # 字符中只包含字母和数字
    letters = [item for item in string.ascii_letters + string.digits]

    def __init__(self,max_length=None):
        """
        Char , VarChar 类型随机值的生成器
        """
        self.max_length = max_length if max_length is not None else 24
        self.letters = copy.copy(self.__class__.letters)
        
        # 最多只生成 24 个字符的字符串
        if self.max_length > 24:
            self.max_length = 24 

    def __getitem__(self,index):
        """
        """
        random.shuffle(self.letters)
        return ''.join(self.letters[0:self.max_length])

    def __len__(self):
        return self.max_length

    def __next__(self):
        return self[0]

    def __iter__(self):
        return self

VarChar = Char


class Uuid(object):
    """
    """
    def __getitem__(self,index):
        """
        """
        return str(uuid.uuid4())
    
    def __len__(self):
        return 128

    def __next__(self):
        return self[0]

    def __iter__(self):
        return self


class DateTime(Number):
    """
    """
    def __init__(self):
        """
        """
        now = int(datetime.now().timestamp())
        detal = int(now/10)
        self.min_value = now - detal
        self.max_value = 2145888000 # timestamp 安全
    
    def __getitem__(self,index)->datetime:
        """
        """
        tmp_second = random.randint(self.min_value, self.max_value)
        return datetime.fromtimestamp(tmp_second)

class Date(DateTime):
    """
    """
    def __getitem__(self,index):
        return self.__class__.__getitem__(self,0).date()
    
class Time(DateTime):
    """
    """
    def __getitem__(self,index):
        return self.__class__.__getitem__(self,0).time()

Timestamp = DateTime


class TableMeta(object):
    """
    查询给定表的元数据
    """

    def __init__(self,host='127.0.0.1',port=3306,user='appuser',password="123456",database="tempdb",table="t"):
        """
        """
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.table = table

        self.cnx = None
        self.meta = []
        self.err = None
        try:
            self.cnx = connector.connect(host=self.host,port=self.port,user=self.user,password=self.password)
            self.cursor = self.cnx.cursor()
            self.cursor.execute("select table_schema,table_name,column_name,column_type,extra from information_schema.columns where table_schema= %s and table_name= %s ;",(self.database,self.table))
            for _,_,column_name,column_type,extra in self.cursor.fetchall():
                _name,_type = self._parser_meta(column_name,column_type,extra)
                if _name is not None:
                    self.meta.append((_name,_type))
            
        except Exception as err:
            self.err = err
            logging.error(str(err))
            logging.exception(str(err))
        finally:
            if hasattr(self.cnx,'close'):
                self.cnx.close()
        
    def _parser_meta(self,column_name,column_type,extra):
        """
        """
        # 如果是自增列让 MySQL 自动自增
        if extra == 'auto_increment':
            return (None,None)
        
        if column_type.startswith(b'int'):
            return(column_name,Int())
        
        if column_type.startswith(b'tinyint(1)'):
            return(column_name,Bool())
        
        if column_type.startswith(b'tinyint'):
            return(column_name,TinyInt())
        
        if column_type.startswith(b'smallint'):
            return(column_name,SmallInt())

        if column_type.startswith(b'mediumint'):
            return(column_name,MediumInt())

        if column_type.startswith(b'bigint'):
            return(column_name,BigInt())

        if column_type.startswith(b'float') or column_type.startswith(b'double'):
            return(column_name,Float())

        # 处理 uuid 的情况
        if column_name.endswith('uuid') and (column_type.startswith(b'varchar') or column_type.startswith(b'char')):
            _,n = column_type.split(b'(')
            number,_ = n.split(b')')
            length = int(number.decode('utf8'))
            if length >= 36:
                return (column_name,Uuid())

        # 处理 varchar | char 的情况
        if column_type.startswith(b'varchar') or column_type.startswith(b'char'):
            _,n = column_type.split(b'(')
            number,_ = n.split(b")")
            length = int(number.decode('utf8'))

            return(column_name,Char(length))

        # 处理时间日期类型
        if column_type.startswith(b'datetime'):
            return(column_name,DateTime())

        if column_type.startswith(b'timestamp'):
            return(column_name,Timestamp())

        if column_type.startswith(b'date'):
            return(column_name,Date())

        if column_type.startswith(b'time'):
            return(column_name,Time())

        # 应该永远都不会执行到这里
        return None,None
        
    def __getitem__(self,index):
        return self.meta[index]
    
    def __len__(self):
        return len(self.meta)

    def __iter__(self):
        return next(self)

    def __next__(self):
        yield from self.meta

    def __del__(self):
        if hasattr(self.cnx,'close'):
            self.cnx.close()

class DMLSQL(object):
    """
    自动生成 DML-SQL 语句,这些语句可以让 cursor.execute 直接执行.
    """
    def __init__(self,database:str="tmpdb",table:str="t",meta=None):
        """
        """
        self.database = database
        self.table = table
        self.meta = meta
        self.sql = None
        self.gens = []
        for _,gen in self.meta:
            self.gens.append(gen)
    
    def _values(self):
        return [next(_) for _ in self.gens]

    def __str__(self):
        """
        """
        raise NotImplementedError()

    def __getitem__(self,index):
        """
        """
        tmp_sql = str(self)
        tmp_value = self._values()
        return(tmp_sql,tmp_value)

class InsertSQL(DMLSQL):
    """
    """
    def __str__(self):
        """
        insert into tempdb.t(c1,c2,c3,c4,c5,c6,c7,c8,x) values (%s,%s,%s,%s,%s,%s,%s,%s,%s);
        """
        if self.sql != None:
            return self.sql
        
        cols = [_[0] for _ in self.meta if _[0] != None]
        vls = ("%s," * len(cols))[0:-1]
        cols = ','.join(cols)
        sql = f"insert into {self.database}.{self.table}({cols}) values ({vls});"
        self.sql = sql
        return sql
    
    






    

            
            

