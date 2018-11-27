from .base import ShowMaster

class BinlogFile(ShowMaster):
    show_master_name="File"

class BinlogPosition(ShowMaster):
    show_master_name="Position"

class BinlogDoDB(ShowMaster):
    show_master_name="Binlog_Do_DB"

class BinlogIgnoreDB(ShowMaster):
    show_master_name="Binlog_Ignore_DB"

