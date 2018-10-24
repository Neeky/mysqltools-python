"""
针对mtls.variable中的各个variable进行测试
"""

# -*- coding: utf8 -*-

import sys
import os
import unittest
cwd = os.getcwd()
sys.path.append(cwd)

from mtls import variable,replication
from test_base import mysql_host,mysql_port,mysql_user,mysql_password

class MtlsTest(unittest.TestCase):
    """
    针对mtls.variable中定义的各个variable的获取方式进行测试，用于查看返回的各个值是否正常
    """
    def get_variable(self,cls):
        v = cls(host=mysql_host,port=mysql_port,user=mysql_user,password=mysql_password)
        return v.value

    def is_int(self,cls,msg=''):
        v = self.get_variable(cls)
        print("{cls.variable_name:32} = {v}".format(cls=cls,v=v))
        self.assertEqual(type(v),int,msg)

    def is_str(self,cls,msg=''):
        v = self.get_variable(cls)
        print("{cls.variable_name:<32} = {v}".format(cls=cls,v=v))
        self.assertEqual(type(v),str,msg)


    def test_ServerID(self):
        self.is_int(variable.ServerID)

    def test_BaseDir(self):
        self.is_str(variable.BaseDir)

    def test_DataDir(self):
        self.is_str(variable.DataDir)

    def test_Port(self):
        self.is_int(variable.Port)

    def test_CharacterSetServer(self):
        self.is_str(variable.CharacterSetServer)

    def test_Socket(self):
        self.is_str(variable.Socket)

    def test_ReadOnly(self):
        self.is_int(variable.ReadOnly)

    def test_SkipNameResolve(self):
        self.is_int(variable.SkipNameResolve)

    def test_LowerCaseTableNames(self):
        self.is_int(variable.LowerCaseTableNames)

    def test_ThreadCacheSize(self):
        self.is_int(variable.ThreadCacheSize)

    def test_TableOpenCache(self):
        self.is_int(variable.TableOpenCache)

    def test_TableDefinitionCache(self):
        self.is_int(variable.TableDefinitionCache)

    def test_TableOpenCacheInstances(self):
        self.is_int(variable.TableOpenCacheInstances)

    def test_MaxConnections(self):
        self.is_int(variable.MaxConnections)

    def test_BinlogFormat(self):
        self.is_str(variable.BinlogFormat)

    def test_LogBin(self):
        self.is_int(variable.LogBin)

    def test_BinlogRowsQueryLogEvents(self):
        self.is_int(variable.BinlogRowsQueryLogEvents)

    def test_LogSlaveUpdates(self):
        self.is_int(variable.LogSlaveUpdates)

    def test_ExpireLogsDays(self):
        self.is_int(variable.ExpireLogsDays)

    def test_BinlogCacheSize(self):
        self.is_int(variable.BinlogCacheSize)

    def test_SyncBinlog(self):
        self.is_int(variable.SyncBinlog)

    def test_ErrorLog(self):
        self.is_str(variable.ErrorLog)

    def test_GtidMode(self):
        self.is_str(variable.GtidMode)

    def test_EnforceGtidConsistency(self):
        self.is_str(variable.EnforceGtidConsistency)

    def test_MasterInfoRepository(self):
        self.is_str(variable.MasterInfoRepository)

    def test_RelayLogInfoRepository(self):
        self.is_str(variable.RelayLogInfoRepository)

    def test_SlaveParallelType(self):
        self.is_str(variable.SlaveParallelType)

    def test_SlaveParallelWorkers(self):
        self.is_int(variable.SlaveParallelWorkers)

    def test_InnodbDataFilePath(self):
        self.is_str(variable.InnodbDataFilePath)

    def test_InnodbTempDataFilePath(self):
        self.is_str(variable.InnodbTempDataFilePath)

    def test_InnodbBufferPoolFilename(self):
        self.is_str(variable.InnodbBufferPoolFilename)

    def test_InnodbLogGroupHomeDir(self):
        self.is_str(variable.InnodbLogGroupHomeDir)

    def test_InnodbLogFilesInGroup(self):
        self.is_int(variable.InnodbLogFilesInGroup)

    def test_InnodbLogFileSize(self):
        self.is_int(variable.InnodbLogFileSize)

    def test_InnodbFileformat(self):
        v = self.get_variable(variable.Version)
        if v.startswith('8'):
            #8.0.x 以上版本已经不再有innodb_file_format参数
            pass
        else:
            self.is_str(variable.InnodbFileformat)

    def test_InnodbFilePerTable(self):
        self.is_int(variable.InnodbFilePerTable)

    def test_InnodbOnlineAlterLogMaxSize(self):
        self.is_int(variable.InnodbOnlineAlterLogMaxSize)

    def test_InnodbOpenFiles(self):
        self.is_int(variable.InnodbOpenFiles)

    def test_InnodbPageSize(self):
        self.is_int(variable.InnodbPageSize)

    def test_InnodbThreadConcurrency(self):
        self.is_int(variable.InnodbThreadConcurrency)

    def test_InnodbReadIoThreads(self):
        self.is_int(variable.InnodbReadIoThreads)

    def test_InnodbWriteIoThreads(self):
        self.is_int(variable.InnodbWriteIoThreads)

    def test_InnodbPurgeThreads(self):
        self.is_int(variable.InnodbPurgeThreads)

    def test_InnodbLockWaitTimeout(self):
        self.is_int(variable.InnodbLockWaitTimeout)

    def test_InnodbSpinWaitDelay(self):
        self.is_int(variable.InnodbSpinWaitDelay)

    def test_InnodbAutoincLockMode(self):
        self.is_int(variable.InnodbAutoincLockMode)

    def test_InnodbStatsAutoRecalc(self):
        self.is_int(variable.InnodbStatsAutoRecalc)

    def test_InnodbStatsPersistent(self):
        self.is_int(variable.InnodbStatsPersistent)

    def test_InnodbStatsPersistentSamplePages(self):
        self.is_int(variable.InnodbStatsPersistentSamplePages)

    def test_InnodbBufferPoolInstances(self):
        self.is_int(variable.InnodbBufferPoolInstances)

    def test_InnodbAdaptiveHashIndex(self):
        self.is_int(variable.InnodbAdaptiveHashIndex)

    def test_InnodbChangeBuffering(self):
        self.is_str(variable.InnodbChangeBuffering)

    def test_InnodbChangeBufferMaxSize(self):
        self.is_int(variable.InnodbChangeBufferMaxSize)

    def test_InnodbFlushNeighbors(self):
        self.is_int(variable.InnodbFlushNeighbors)

    def test_InnodbFlushMethod(self):
        self.is_str(variable.InnodbFlushMethod)

    def test_InnodbDoublewrite(self):
        self.is_int(variable.InnodbDoublewrite)

    def test_InnodbLogBufferSize(self):
        self.is_int(variable.InnodbLogBufferSize)

    def test_InnodbFlushLogAtTimeout(self):
        self.is_int(variable.InnodbFlushLogAtTimeout)

    def test_InnodbFlushLogAtTrxCommit(self):
        self.is_int(variable.InnodbFlushLogAtTrxCommit)

    def test_InnodbBufferPoolSize(self):
        self.is_int(variable.InnodbBufferPoolSize)

    def test_Autocommit(self):
        self.is_str(variable.Autocommit)

    def test_InnodbOldBlocksPct(self):
        self.is_int(variable.InnodbOldBlocksPct)

    def test_InnodbOldBlocksTime(self):
        self.is_int(variable.InnodbOldBlocksTime)

    def test_InnodbReadAheadThreshold(self):
        self.is_int(variable.InnodbReadAheadThreshold)

    def test_InnodbRandomReadAhead(self):
        self.is_int(variable.InnodbRandomReadAhead)

    def test_InnodbBufferPoolDumpPct(self):
        self.is_int(variable.InnodbBufferPoolDumpPct)

    def test_InnodbBufferPoolDumpAtShutdown(self):
        self.is_int(variable.InnodbBufferPoolDumpAtShutdown)

    def test_InnodbBufferPoolLoadAtStartup(self):
        self.is_int(variable.InnodbBufferPoolLoadAtStartup)

    def test_QueryCacheLimit(self):
        if not self.get_variable(variable.Version).startswith('8'):
            self.is_int(variable.QueryCacheLimit)

    def test_QueryCacheMinResUnit(self):
        if not self.get_variable(variable.Version).startswith('8'):
            self.is_int(variable.QueryCacheMinResUnit)

    def test_QueryCacheSize(self):
        if not self.get_variable(variable.Version).startswith('8'):
            self.is_int(variable.QueryCacheSize)

    def test_QueryCacheType(self):
        if not self.get_variable(variable.Version).startswith('8'):
            self.is_int(variable.QueryCacheType)

    def test_Version(self):
        self.is_str(variable.Version)



if __name__=="__main__":
    unittest.main()





