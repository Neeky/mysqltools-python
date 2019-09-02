# mysqltools-python权威指南
---
主编&作者:**蒋乐兴**

wechat:**jianglegege**

email:**1721900707@qq.com**

homepage:**http://www.sqlpy.com**

---

- [关于](#关于)
- [安装](#安装)
- [数据库监控项采集 -- mtls-monitor](#数据库监控项采集)
- [数据库备份 -- mtls-backup](#数据库备份)
- [慢查询日志切片分析 -- mtls-log ](#慢查询日志切片分析)
- [tcp端口连通性测试 -- mtls-http](#tcp端口连通性测试)
- [查询给定目录中的大文件 -- mtls-big-files](#查询给定目录中的大文件)
- [温和删除表中的行 -- mtls-delete-rows](#温和删除表中的行)
- [温和文件截断 -- mtls-file-truncate](#温和文件截断)
- [数据库性能测试 -- mtls-perf-bench](#数据库性能测试)
- [断开所有的客户端连接 -- mtls-kill-all-connections](#断开所有的客户端连接)
- [统计慢查询文件中的SQL类型与热点表 -- mtls-sql-distribution](#统计慢查询文件中的SQL类型与热点表)
- [表的最晚更新时间统计 -- mtls-file-stat](#表的最晚更新时间统计)
- [找出长时间没有使用过的表 -- mtls-expired-tables](#找出长时间没有使用过的表)
---

## 关于
   **1、** mysqltools-python 是一个 专为 dba 服务的 python 工具包，主要的目的在于把一些锁定程序化，一方面可以提高劳动生产率，另一方面可以节约 dba 的时间。

   ---

   **2、** 目前工具包中集成的工具列表
   
   |**工具名**|**功能说明**|
   |---------|-----------|
   |mtls-monitor| 监控项采集 |
   |mtls-backup|  自动化备份数据库 |
   |mtls-delete-rows| 分批(温和)删除大表中的行|
   |mtls-file-truncate| 分批(温和)的截断物理文件|
   |mtls-big-files| 查询出给定目录下的大文件名|
   |mtls-http| tcp(http)端口连通性测试|
   |mtls-log | 慢查询日志切片|
   |mtls-perf-bench| 数据库跑分工具(开发中)|
   |mtls-kill-all-connections | 杀死所有的客户端连接|
   |mtls-sql-distribution | 统计慢查询文件中的SQL类型与热点表 |
   |mtls-file-stat| 表的最晚更新时间统计|
   |mtls-expired-tables|找出长时间没有使用过的表| 

   ---

## 安装
   **目前mysqltools-python支持python-3.x 下的所有版本,可以直接通过pip来安装**
   ```
   pip3 install mysqltools-python
   ```
   输出如下：
   ```
   Collecting mysqltools-python                                                                       
     Using cached    https://files.pythonhosted.org/packages/46/da/de9495da7bf0ee9225a1f1988ab5cb4e8573388338df1e55d8b5272c413a/mysqltools-python-2.18.09.01.tar.   gz                                         
   Requirement already satisfied: mysql-connector-python>=8.0.12 in /usr/local/python-3.6.2/lib/python3.6/site-packages (from mysqltools-python)                                                            
   Requirement already satisfied: protobuf>=3.0.0 in /usr/local/python-3.6.2/lib/python3.6/site-packages (from    mysql-connector-python>=8.0.12->mysqltools-python)                                        
   Requirement already satisfied: setuptools in /usr/local/python-3.6.2/lib/python3.6/site-packages (from    protobuf>=3.0.0->mysql-connector-python>=8.0.12->mysqltools-python)                            
   Requirement already satisfied: six>=1.9 in /usr/local/python-3.6.2/lib/python3.6/site-packages (from    protobuf>=3.0.0->mysql-connector-python>=8.0.12->mysqltools-python)                              
   Installing collected packages: mysqltools-python                                                   
     Running setup.py install for mysqltools-python ... done                                          
   Successfully installed mysqltools-python-2.18.9.1                                                  
   You are using pip version 9.0.1, however version 18.0 is available.                                
   You should consider upgrading via the 'pip install --upgrade pip' command.
   ```

   安装完成后你就可以使用mysqltools-python提供的两个命令行工具(mtls-montir,mtls-backup)和一个模块包(mtls)了；比如我们可以通过mtlsmonitor来看一上MySQL启动后执行了多少Select语句
   ```
   mtls-monitor --host=127.0.0.1 --port=3306 --user=monitor --password=monitor0352 ComSelect
   ```
   ```
   44
   ```

   ---

## 数据库监控项采集
   **1): mysqltools-python已经实现的监控项列表**

   *监控项名*                         |               *简介*                |               *采集方式*        
   ----------------------------------|----------------------------------- |----------------------------------------------
   |`mysql配置(variable)相关的监控项列表`|如果人为修改了mysql参数(variable)并引起了问题、那么对关键参数的监控就能方便的定位问题
   |`-- ServerID`                    | 对应server_id                      | variable |
   |`-- BaseDir`                     | 对应basedir                        | variable |
   |`-- DataDir`                     | 对应datadir                        | variable |
   |`-- Port`                        | 对应port                           | variable |
   |`-- CharacterSetServer`          | 对应character_set_server           | variable |
   |`-- Socket`                      | 对应socket                         | variable |
   |`-- ReadOnly`                    | 对应readonly                       | variable |
   |`-- SkipNameResolve`             | 对应skip_name_resolve              | variable |
   |`-- LowerCaseTableNames`         | 对应lower_case_table_names         | variable |
   |`-- ThreadCacheSize`             | 对应thread_cache_size 、线程池的大小、如果池有空闲的线程、那么新的连接就不单独创建新的线程了 |variable|
   |`-- TableOpenCache`              | 对应table_open_cache               | variable |
   |`-- TableDefinitionCache`        | 对应table_definition_cache         | variable |
   |`-- TableOpenCacheInstances`     | 对应table_open_cache_instance      | variable |
   |`-- MaxConnections`              | 对应max_connections                | variable |
   |`-- BinlogFormat`                | 对应binlog_format                  | variable |
   |`-- LogBin`                      | 对应log_bin                        | variable |
   |`-- BinlogRowsQueryLogEvents`    | 对应binlog_rows_query_log_events   | variable |
   |`-- LogSlaveUpdates`             | 对应log_slave_updates              | variable |
   |`-- ExpireLogsDays`              | 对应expire_logs_days               | variable |
   |`-- BinlogCacheSize`             | 对应binlog_cache_size              | variable |
   |`-- SyncBinlog`                  | 对应sync_binlog                    | variable |
   |`-- ErrorLog`                    | 对应error_log                      | variable |
   |`-- GtidMode`                    | 对应gtid_mode                      | variable |
   |`-- EnforceGtidConsistency`      | 对应enforce_gtid_consistency       | variable |
   |`-- MasterInfoRepository`        | 对应master_info_repository         | variable |
   |`-- RelayLogInfoRepository`      | 对应relay_log_info_repository      | variable |
   |`-- SlaveParallelType`           | 对应slave_parallel_type            | variable |
   |`-- SlaveParallelWorkers`        | 对应slave_parallel_workers         | variable |
   |`-- InnodbDataFilePath`          | 对应innodb_data_file_path          | variable |
   |`-- InnodbTempDataFilePath`      | 对应innodb_temp_data_file_path     | variable |
   |`-- InnodbBufferPoolFilename`    | 对应innodb_buffer_pool_filename    | variable |
   |`-- InnodbLogGroupHomeDir`       | 对应innodb_log_group_home_dir      | variable |
   |`-- InnodbLogFilesInGroup`       | 对应innodb_log_file_in_group       | variable |
   |`-- InnodbLogFileSize`           | 对应innodb_log_file_size           | variable |
   |`-- InnodbFileformat`            | 对应innodb_fileformat              | variable |
   |`-- InnodbFilePerTable`          | 对应innodb_file_per_table          | variable |
   |`-- InnodbOnlineAlterLogMaxSize` | 对应innodb_online_Alter_log_max_size      |variable |
   |`-- InnodbOpenFiles`             | 对应innodb_open_files              | variable |
   |`-- InnodbPageSize`              | 对应innodb_page_size               | variable |
   |`-- InnodbThreadConcurrency`     | 对应innodb_thread_concurrency      | variable |
   |`-- InnodbReadIoThreads`         | 对应innodb_read_io_threads         | variable |
   |`-- InnodbWriteIoThreads`        | 对应innodb_write_io_threads        | variable |
   |`-- InnodbPurgeThreads'`         | 对应innodb_purge_threads           | variable |
   |`-- InnodbLockWaitTimeout`       | 对应innodb_lock_wait_timeout       | variable |
   |`-- InnodbSpinWaitDelay`         | 对应innodb_spin_wait_delay         | variable |
   |`-- InnodbAutoincLockMode`       | 对应innodb_autoinc_lock_mode       | variable |
   |`-- InnodbStatsAutoRecalc`       | 对应innodb_stats_auto_recalc       | variable |
   |`-- InnodbStatsPersistent`       | 对应innodb_stats_persistent        | variable |
   |`-- InnodbStatsPersistentSamplePages`    |对应innodb_stats_persistent_sample_pages    | variable |
   |`-- InnodbBufferPoolInstances`   | 对应innodb_buffer_pool_instances   | variable |
   |`-- InnodbAdaptiveHashIndex`     | 对应innodb_adaptive_hash_index     | variable |
   |`-- InnodbChangeBuffering`       | 对应innodb_change_buffering        | variable |
   |`-- InnodbChangeBufferMaxSize`   | 对应innodb_change_buffer_max_size  | variable |
   |`-- InnodbFlushNeighbors`        | 对应innodb_flush_neighbors         | variable |
   |`-- InnodbFlushMethod`           | 对应innodb_flush_method            | variable |
   |`-- InnodbDoublewrite`           | 对应innodb_doublewrite             | variable |
   |`-- InnodbLogBufferSize`         | 对应innodb_log_buffer_size         | variable |
   |`-- InnodbFlushLogAtTimeout`     | 对应innodb_flushLog_at_timeout     | variable |
   |`-- InnodbFlushLogAtTrxCommit`   | 对应innodb_flushLog_at_trx_commit  | variable |
   |`-- InnodbBufferPoolSize`        | 对应innodb_buffer_pool_size        | variable |
   |`-- Autocommit`                  | 对应autocommit                     | variable |
   |`-- InnodbOldBlocksPct`          | 对应innodb_lld_blocks_pct          | variable |
   |`-- InnodbOldBlocksTime`         | 对应innodb_old_blocks_time         | variable |
   |`-- InnodbReadAheadThreshold`    | 对应innodb_read_ahead_threshold    | variable |
   |`-- InnodbRandomReadAhead`       | 对应innodb_random_read_ahead       | variable |
   |`-- InnodbBufferPoolDumpPct`     | 对应innodb_buffer_pool_dump_pct    | variable |
   |`-- InnodbBufferPoolDumpAtShutdown` |对应innodb_buffer_pool_dump_at_shutdown | variable |
   |*********************************|                                   |      |
   |`mysql状态(status)相关监控`        | 通过对status进行监控可得知mysql当前的性能表现
   |`-- AbortedClients`              | 对应aborted_clients 、client异常退出使得连接没有被正常关闭的次数       | status | 
   |`-- AbortedConnects`             | 对应borted_connects 、没有成功连接到server端的次数                   | status |
   |`-- BinlogCacheDiskUse`          | 对应binlog_cache_disk_use 、使用临时文件存储事务语句的次数            | status |
   |`-- BinlogCacheUse`              | 对应binlog_cache_user 、使用binlog_cache存储事务语句的次数           | status |
   |`-- BinlogStmtCacheDiskUse`      | 对应binlog_stmt_cache_disk_use 、非事务语句使用临时文件存储的次数     | status |
   |`-- BinlogStmtCacheUse`          | 对应binlog_stmt_cache_use 、非事务语句使用binlog_cache存储的次数     | status |
   |`-- BytesReceived`               | 对应bytes_received、从客户端收到的字节数                            | status |
   |`-- BytesSent`                   | 对应bytes_sent、发送给客户端的字节数                                | status |
   |`-- ComBegin`                    | 对应com_begin、         语句执行的次数                             | status |
   |`-- ComCallProcedure`            | 对应com_call_procedure、语句执行的次数                             | status |
   |`-- ComChangeMaster`             | 对应com_change_master、 语句执行的次数                             | status |
   |`-- ComCommit`                   | 对应com_commit、        语句执行的次数                             | status |
   |`-- ComDelete`                   | 对应com_delete、        语句执行的次数                             | status |
   |`-- ComDeleteMulti`              | 对应com_delete_multi、  语句执行的次数                             | status |
   |`-- ComInsert`                   | 对应com_insert、        语句执行的次数                             | status |
   |`-- ComInsertSelect`             | 对应com_insert_select、 语句执行的次数                             | status |
   |`-- ComSelect`                   | 对应com_select、        语句执行的次数                             | status |
   |`-- ComUpdate`                   | 对应com_update、        语句执行的次数                             | status |
   |`-- ComUpdateMulti`              | 对应com_update_multi、  语句执行的次数                             | status |
   |`-- Connections`                 | 对应connections、尝试连接的次数                                    | status |
   |`-- CreatedTmpDiskTable`         | 对应created_tmp_disk_table、创建磁盘临时表的次数                    | status |
   |`-- CreatedTmpFiles`             | 对应created_tmp_files、创建临时文件的次数                           | status |
   |`-- CreatedTmpTables`            | 对应created_tmp_tables、创建临时表的次数                            | status |
   |`-- ComCreateTable`              | 对应com_create_table 记录create table 的次数                      | status |
   |`-- ComDropTable`                | 对应com_drop_table   记录drop table 的次数                        | status |
   |`-- ComRenameTable`              | 对应com_rename_table 记录rename table 的次数                      | status |
   |`-- InnodbBufferPoolDumpStatus`  | 对应innodb_buffer_pool_dump_status innodb_xx_dump的进度          | status |
   |`-- InnodbBufferPoolLoadStatus`  | 对应innodb_buffer_pool_load_status innodb_xx_load的进度          | status |
   |`-- InnodbBufferPoolResizeStatus`| 对应innodb_buffer_pool_resize_status              进度           | status |
   |`-- InnodbBufferPoolBytesData`   | 对应innodb_buffer_pool_bytes_data buffer_pool中的数据量(单位字节)  | status |
   |`-- InnodbBufferPoolPagesData`   | 对应innodb_buffer_pool_pages_data buffer_pool中数据页面数         | status |
   |`-- InnodbBufferPoolPagesDirty`  | 对应innodb_buffer_pool_pages_dirty buffer_pool中脏页数量          | status |
   |`-- InnodbBufferPoolBytesDirty`  | 对应innodb_buffer_pool_bytes_dirty buffer_pool中脏数据量(单位字节) | status |
   |`-- InnodbBufferPoolPagesFlushed`| 对应innodb_buffer_pool_pages_flushed 请求刷新出buffer_pool的页面数 | status |
   |`-- InnodbBufferPoolPagesFree`   | 对应innodb_buffer_pool_pages_free buffer_pool中空闲页面数         | status |
   |`-- InnodbBufferPoolPagesMisc`   | 对应innodb_buffer_pool_pages_misc buffer_pool  total_page -(free + data) | status |
   |`-- InnodbBufferPoolPagesTotal`  | 对应innodb_buffer_pool_pages_total buffer_pool 总项目数          | status |
   |`-- InnodbBufferPoolReadAhead`   | 对应innodb_buffer_pool_read_ahead 由read-ahead机制读入的页面数     | status |
   |`-- InnodbBufferPoolReadAheadEvicted`   | 对应innodb_buffer_pool_read_ahead_evicted 由raed-ahead机制读入的页面中、由于读入后没有被访问而淘汰的页  面
   |`-- InnodbBufferPoolReadRequests`| 对应innodb_buffer_pool_read_requests 逻辑读的次数(读buffer_pool)  | status |
   |`-- InnodbBufferPoolReads`       | 对应innodb_buffer_pool_reads 物理读的次数(读磁盘)                  | status |
   |`-- InnodbBufferPoolWaitFree`    | 对应innodb_buffer_pool_wait_free 等待有可用页面的次数              | status |
   |`-- InnodbBufferPoolWriteRequests`|对应innodb_buffer_pool_write_requests 请求写buffer_pool的次数     | status |
   |`-- InnodbDataFsyncs`            | 对应innodb_data_fsyncs fsyncs()函数调用的次数                     | status |
   |`-- InnodbDataPendingFsyncs`     | 对应innodb_data_pending_fsyncs 当前挂起的fsyncs操作               | status |
   |`-- InnodbDataPendingReads`      | 对应innodb_data_pending_reads 当前挂起的读操作                    | status |
   |`-- InnodbDataPendingWrites`     | 对应innodb_data_pending_writes 当前挂起的写操作                   | status |
   |`-- InnodbDataRead`              | 对应innodb_data_read 自启动后读了多少数据进buffer_pool             | status |
   |`-- InnodbDataReads`             | 对应innodb_data_reads 自启动后读了多少次数据进buffer_pool          | status |
   |`-- InnodbDataWrites`            | 对应innodb_data_writes 自启动后写了多少次数据到buffer_pool         | status |
   |`-- InnodbDataWritten`           | 对应innodb_data_written 自启动后写了多少数据到buffer_pool          | status |
   |`-- InnodbDblwrPagesWritten`     | 对应innodb_dblwr_pages_written double_write写入到磁盘的页面数量   | status |
   |`-- InnodbDblwrWrites`           | 对应innodb_dblwr_writes double_write 执行的次数                 | status |
   |`-- InnodbLogWaits`              | 对应innodb_log_waits 写日志时的等待次数                           | status |
   |`-- InnodbLogWriteRequests`      | 对应innodb_log_write_requests 写请求次数                        | status |
   |`-- InnodbLogWrites`             | 对应innodb_log_writes 写磁盘的次数                               | status |
   |`-- InnodbOsLogFsyncs`           | 对应innodb_os_log_fsyncs fsync()函数调用的次数(针对redo log file) | status |
   |`-- InnodbOsLogPendingFsyncs`    | 对应innodb_os_log_pending_fsyncs 挂起的fsync操作数量             | status |
   |`-- InnodbOsLogPendingWrites`    | 对应innodb_os_log_pending_writes 挂起的write操作数量             | status |
   |`-- InnodbOsLogWritten`          | 对应innodb_os_log_written 写入的字节数量                         | status |
   |`-- InnodbPagesCreated`          | 对应innodb_pages_created  创建的页面数量                         | status |
   |`-- InnodbPagesRead`             | 对应innodb_pages_read 从buffer_pool中读出的页面数量               | status |
   |`-- InnodbPagesWritten`          | 对应innodb_pages_written 向buffer_pool写入的页面数量             | status |
   |`-- InnodbRowLockCurrentWaits`   | 对应innodb_row_lock_current_waits 当前的行锁等待数量              | status |
   |`-- InnodbRowLockTime`           | 对应innodb_row_lock_time 花费在获取行锁上的总时间                  | status |
   |`-- InnodbRowLockTimeAvg`        | 对应innodb_row_lock_time_avg 花费在获取行锁上的平均时间            | status |
   |`-- InnodbRowLockTimeMax`        | 对应innodb_row_lock_time_max 花费在获取行锁上的最大时间            | status |
   |`-- InnodbRowLockWaits`          | 对应innodb_row_lock_waits 行锁等待的总次数                       | status |
   |`-- InnodbRowsDeleted`           | 对应innodb_rows_deleted 删除的行数                              | status |
   |`-- InnodbRowsInserted`          | 对应innodb_rows_inserted 插入的行数                             | status |
   |`-- InnodbRowsRead`              | 对应innodb_rows_read 读取的行数                                 | status |
   |`-- InnodbRowsUpdated`           | 对应innodb_rows_updated 更新的行数                              | status |
   |`-- LogSequenceNumber`           | 对应show engine innodb status 中的LogSequenceNumber            | innodb |
   |`-- LogFlushedUpTo`              | 对应show engine innodb status 中的LogFlushedUpTo               | innodb |
   |`-- PagesFlushedUpTo`            | 对应show engine innodb status 中的PagesFlushedUpTo             | innodb |
   |`-- LastCheckpointAt`            | 对应show engine innosb status 中的LastCheckpointAt             | innodb |
   |`-- OpenTableDefinitions`        | 对应open_table_definitions 缓存中的.frm文件数量                  | status |
   |`-- OpenTables`                  | 对应open_tables 当前打开的表的数量                               | status |
   |`-- OpenedTableDefinitions`      | 对应opened_table_definitions 曾经缓存过的.frm文件数量             | status |
   |`-- OpenedTables`                | 对应opened_tables 曾经打开过的表                                 | status |
   |`-- SlowQueries`                 | 对应slow_queries  慢查询的次数据                                 | status |
   |`-- TableLocksImmediate`         | 对应table_locks_immediate 立即就可以获得表锁的次数                 | status |
   |`-- TableLocksWaited`            | 对应table_ocks_waited 表锁等待的次数                             | status |    
   |`-- TableOpenCacheOverflows`     | 对应table_open_cache_overflows 表打开又关闭的次数                | status |
   |`-- ThreadsCached`               | 对应threads_cached 当前线程池中线程的数量                         | status |
   |`-- ThreadsConnected`            | 对应threads_connected 当前打开的连接                            | status |
   |`-- ThreadsCreated`              | 对应threads_created   为了处理连接所创建的线程总数                 | status |
   |`-- ThreadsRunning`              | 对应threads_running   非sleep状态下的线程数                      | status |
   |`-- Uptime`                      | 对应uptime 从启动开始到现在已经运行了多少秒                         | status | 
   |`-- BinlogFile`                  | 对应show master status 中的File列，追踪当前写的哪个binlog文件      | show master status |
   |`-- BinlogPosition`              | 对应show master status 中的Position列，追踪当前binlog文件的大小    | show master status |          
   |`-- MgrTotalMemberCount`         | mgr集群中成员的数量                                             | p_s    |
   |`-- MgrOnLineMemberCount`        | mgr集群中online状态下的成员数量                                  | p_s    |
   |`-- MgrMemberState`              | 当前mgr成员的状态                                               | p_s    | 
   |`-- MgrCountTransactionsInQueue` | 当前mgr成员上等待进行冲突检查的事务数量                            | p_s    |
   |`-- MgrCountTransactionsChecked` | 当前mgr成员上已经完成冲突检测的事务数量                            | p_s    |
   |`-- MgrCountConflictsDetected`   | 当前mgr成员上没能通过冲突检测的事务数量                            | p_s    |
   |`-- MgrTransactionsCommittedAllMembers`|当前mgr成员上已经应用的事务总数量                            | p_s    |
   |`-- RplSemiSyncMasterClients`    | 当前master端处理半同步状态的slave数量                             | status |
   |`-- RplSemiSyncMasterStatus`     | master的半同步状态                                              | status |
   |`-- RplSemiSyncMasterNoTx`       | 没有收到半同步slave确认的事务数量                                  | status |
   |`-- RplSemiSyncMasterYesTx`      | 有收到半同步slave确认的事务数量                                    | status |
   |`-- RplSemiSyncSlaveStatus`      | slave的半同步状态                                               | status |
   |`-- SlaveIORunning`              | IO线程的状态(-2:说明当前实例是master,0:非Yes,1:Yes)               | show slave status |
   |`-- SlaveSQLRunning`             | SQL线程的状态(-2:说明当前实例是master,0:非Yes,1:Yes)              | show slave status |
   |`-- SecondsBehindMaster`         | 主从延时多久(-2:说明当前实例是master,-1:None,其它:延时的秒数)       | show slave status |
   |`-- MySQLDiscovery`              | zabbix Low-level discovery 接口   用于MySQL自动发现             |                   |
   |`-- DiskDiscovery`               | zabbix Low-level discovery 接口   用于磁盘自动发现               |                   |

   **2): 监控工具mtlsmonitor的使用方式**
   ```
   mtls-monitor --host=<主机IP> --port=<端口> --user=<MySQL用户名> --password=<MySQL用户密码> <监控项名>
   ``` 
   比如说我想查看innodb层面的行锁等待次数(InnodbRowLockWaits) 那我就可以这样做
   ```
   mtls-monitor --host=127.0.0.1 --port=3306 --user=monitor --password=monitor0352 InnodbRowLockWaits
   ```
   ```
   0
   ```

   **3): 与zabbix结合后的效果**
   >cpu

   <img src="./imgs/cpu.png">

   >mem

   <img src="./imgs/mem.png">

   >net

   <img src="./imgs/net.png">

   >reads

   <img src="./imgs/reads.png">

   >writes

   <img src="./imgs/writes.png">

   >rs

   <img src="./imgs/rs.png">

   >transaction

   <img src="./imgs/t.png">

   >innodb

   <img src="./imgs/ibrw.png">

   **4):**

   **在我的另一个项目`mysqltools`中是有把这个监控项与zabbix结合的，见`https://github.com/Neeky/mysqltools`**

   ---  

## 数据库备份
   ****
   见 <a href="https://github.com/Neeky/mysqltools"> mysqltools 中备份相关章节</a>

   ---

## tcp端口连通性测试
   **有时候我们想确认到目标主机的端口的网络是否能连通，以 192.168.1.4 主机上的 8080 端口为例吧，我怎么确认到这个端口是不是通的呢？解决方案就是在这个ip和端口上起一个tcp监听，然后一测就知道了**

   **第一步：192.168.1.4 主机上运行 mtlshttp 命令让它起一个到8080端口的 tcp 监听**
   ```bash
   mtls-http --ip=192.168.1.4 --port=8080
   2019-03-23 09:52:54.714280 | prepare start block http server
   2019-03-23 09:52:54.714427 | server binds on 192.168.1.4:8080
   ```
   **第二步：检测连通性(我在这里使用浏览器来检测)**
   <img src="./imgs/mtlshttp.png">

   **其它检测方法也是可行的**
   ```html
   curl http://192.168.1.4:8080/


   <html>
                   <head>
                       <title> block http server </title>
                   </head>
                   <body>
                       <h1>mtlshttp is working ...</h1>
                   </body>
               </html>
   ```
   ```bash
   telnet 192.168.1.4 8080


   Trying 192.168.1.4...
   Connected to 192.168.1.4.
   Escape character is '^]'.
   ```
   >特别感谢 工程师 HanGang 对上述接口的测试 https://github.com/Han-Gang

   ---

## 查询给定目录中的大文件
   **mtlsbigfiles 用于分析给定目录下哪几个文件比较大**
   ```bash
   mtls-big-files /usr/local/homebrew/var/mysql/ 
   ******************************************************
   |FILE PATH                                 | FILE SIZE| 
   ******************************************************
   |/usr/local/homebrew/var/mysql/ibdata1     | 12.6 MB 
   |/usr/local/homebrew/var/mysql/ibtmp1      | 12.6 MB 
   |/usr/local/homebrew/var/mysql/undo_001    | 12.6 MB 
   |/usr/local/homebrew/var/mysql/undo_002    | 12.6 MB 
   |/usr/local/homebrew/var/mysql/mysql.ibd   | 26.2 MB 
   |/usr/local/homebrew/var/mysql/ib_logfile1 | 50.3 MB 
   |/usr/local/homebrew/var/mysql/ib_logfile0 | 50.3 M


   mtls-big-files /usr/local/homebrew/var/mysql/  --limit=3
   ******************************************************
   |FILE PATH                                 | FILE SIZE| 
   ******************************************************
   |/usr/local/homebrew/var/mysql/mysql.ibd   | 26.2 MB 
   |/usr/local/homebrew/var/mysql/ib_logfile1 | 50.3 MB 
   |/usr/local/homebrew/var/mysql/ib_logfile0 | 50.3 MB 
   ```
   ---

## 慢查询日志切片分析
   **官方提供的mysqldumpslow工具已经非常好用了，但是有一个问题还是存在的比如说我只想对特定时间段内的慢查询做分析；这个时候我们就要手工写bash脚本来“切”日志了；像我这样并不是特别认同bash编程风格的DBA来说身体上是拒绝的，但是同样的需求不只一次的重复在工作中出现时，我想我有写点什么东西的必要了；这就有了mtls-log这个命令行工具** 

   **1): 查看mtls-log命令行帮助信息**
   ```bash
   mtls-log --help
   usage: mtls-log [-h] [--slow-log-file SLOW_LOG_FILE] [--starttime STARTTIME]
                  [--endtime ENDTIME] [--charset CHARSET] [--top TOP]
                  {log_slice,hot_table,hot_uid,hot_client}
   
   positional arguments:
     {log_slice,hot_table,hot_uid,hot_client}
   
   optional arguments:
     -h, --help            show this help message and exit
     --slow-log-file SLOW_LOG_FILE
                           slow log file absolute path
     --starttime STARTTIME
                           slow log start time flag
     --endtime ENDTIME     slow log end time flag
     --charset CHARSET
     --top TOP
   ```
   **mtls-log 有三个主要的功能 a): log_slice 它可以从慢查询日志中切出“特定时间段”内的那部分日志 b): hot_table 它可以系统慢查询中最频繁出现的表 c): 统计出最容易引起慢查询的客户端主机的ip**

   ---

   **2):log_slice 切出特定时间段内的慢查询**

   a): 确定那些时间段内有慢查询产生
   ```bash
   cat slow_query.log | grep '# Time'
   # Time: 181022  0:03:40
   # Time: 181022  0:03:41
   # Time: 181022  0:03:42
   # Time: 181022  0:03:43
   # Time: 181022  0:15:53
   # Time: 181022  0:15:54
   # Time: 181022  0:17:35
   # Time: 181022  0:17:36
   # Time: 181022  0:17:37
   # Time: 181022  0:17:38

   ```
   
   b): 通过mtls-log切出“# Time: 181022  0:03:43” 到 “# Time: 181022  0:15:53” 这个时段内的查询查询,并把日志保存到/tmp/s.log文件中
   ```bash
   mtls-log --slow-log-file=slow_query.log \
    --starttime='# Time: 181022  0:03:43' --endtime='# Time: 181022  0:15:53' \
    log_slice > /tmp/s.log
   ```
   可以看到/tmp/s.log就是对应时间段内的慢查询
   ```bash
   # Time: 181022  0:03:43
   # User@Host: user_app[user_app] @  [192.168.136.214]
   # Query_time: 0.515818  Lock_time: 0.000261 Rows_sent: 30  Rows_examined: 104
   SET timestamp=1540137823;
   SELECT xxx ... ... ...

   ... ... ... 

   UPDATE ... ... ... 
   # Time: 181022  0:15:53
   ```

   **3): hot_table 统计慢查询中出现次数最多表名(默认top=7)**
   ```bash
   mtls-log --slow-log-file=/tmp/s.log hot_table
   TABLE_NAME                       COUNTER
   ------------------------------------------------
    tempdb.sbtest01         101
    tempdb.sbtest02         97
    tempdb.sbtest03         64
    tempdb.sbtest04         50
    tempdb.sbtest05         30
    tempdb.sbtest06         24
    tempdb.sbtest07         1
   ```

   **4): hot_client 统计慢查询中出现的客户端的IP地址(默认top=7)**
   ```bash
   mtls-log --slow-log-file=/tmp/s.log hot_client
   CLIENT_HOST_IP                   COUNTER
   ------------------------------------------------
   192.168.136.214                   270
   192.168.136.216                   260
   192.168.136.210                   100
   ```
   mtlslog 的定位是mysqldumpslow的一个补充
   
   ---

## 温和删除表中的行
   **有时候我们会遇到一些大表，比如说单表 500G 这种场景下不管是 DDL 还是 DML 效率都不高。如果表里面有些数据已经过时了，删除这些无效的数据，通常来讲是一个不错的选择。**

   **在删除无效数据的时候有些要注意的地方，不能一下子全部删除完，这样就会造成瞬间有大量磁盘IO，进而影响业务；针对这类的场景通常是每一次删除非常少的行，如 1000 行然后执行 n 次删除操作。**

   **针对上面的场景我们提供了 `mtls-delete-rows` 它会从 --sql-file 指定的文件中读取要执行的 sql 语句，然后在 sql 语句的后面加上 limit ; 每条 sql 语句都会在一个循环中执行，循环的退出条件是 sql 删除了 0 行；然后再进入执行下一条语句的循环。**

   **1、** 假设 tempdb.t 就是我们要执行删除操作的大表
   ```sql
   select count(*) from tempdb.t;                                                             
   +----------+
   | count(*) |
   +----------+
   |  1048576 |
   +----------+
   1 row in set (0.12 sec)
   ```
   **2、** 要执行的删除语句是
   ```bash
   cat /tmp/dlt.sql 
   delete from tempdb.t where id <= 12000;
   ````
   **3、** 通过 mtls-delete-rows 完分批执行的操作
   ```bash
   # view 参数用来查看 mtlsdeleterows 会对 sql 语句进行怎样的处理
   mtls-delete-rows --host=127.0.0.1 --port=3306 --user=root --password=mtls0352 \
   --rows=100 --sql-file=/tmp/dlt.sql view

   2019-07-26 20:37:27,176 INFO formatted sql statement : delete from tempdb.t where id <= 12000 limit 100;

   # exec 参数才会真正的执行删除操作
   mtlsdeleterows --host=127.0.0.1 --port=3306 --user=root --password=mtls0352 --rows=100 --sql-file=/tmp/dlt.sql exec

   2019-07-26 20:53:35,413 INFO 100 row(s) affected by delete from tempdb.t where id <= 12000 limit 100; 
   2019-07-26 20:53:36,422 INFO 100 row(s) affected by delete from tempdb.t where id <= 12000 limit 100; 
   2019-07-26 20:53:37,430 INFO 100 row(s) affected by delete from tempdb.t where id <= 12000 limit 100; 
   2019-07-26 20:53:38,440 INFO 100 row(s) affected by delete from tempdb.t where id <= 12000 limit 100; 
   ...
   ...
   2019-07-26 20:53:53,561 INFO 100 row(s) affected by delete from tempdb.t where id <= 12000 limit 100; 
   2019-07-26 20:53:54,569 INFO 100 row(s) affected by delete from tempdb.t where id <= 12000 limit 100; 
   2019-07-26 20:53:55,576 INFO 1 row(s) affected by delete from tempdb.t where id <= 12000 limit 100; 
   2019-07-26 20:53:56,578 INFO compelete
   ```
   **4、** 更多选项可以查看帮助
   ```bash
   mtls-delete-rows --help                                                     
   usage: mtls-delete-rows [-h] [--host HOST] [--port PORT] [--user USER]                              
                         [--password PASSWORD] [--sleep-time SLEEP_TIME]
                         [--rows ROWS] [--sql-file SQL_FILE]
                         [--encoding ENCODING]
                         {view,exec}
   
   positional arguments:
     {view,exec}
   
   optional arguments:
     -h, --help            show this help message and exit
     --host HOST           mysql host
     --port PORT           mysql port
     --user USER           mysql user
     --password PASSWORD   mysql user's password
     --sleep-time SLEEP_TIME
                           sleep time per batch
     --rows ROWS           rows per batch
     --sql-file SQL_FILE   file containt sql statement
     --encoding ENCODING   sql file encoding default utf8
   ```
   ---

## 温和文件截断
   **1、** 有时候我们会遇到下面的场景，一个文件已经非常大了，如果直接 rm 删除的话，这个东西可能会占用大量的IO带宽。于是我们就需要一个慢慢减小文件大小的工具，mtls-file-truncate 就是这个场景的一个解决方案。

   
   **2、** 假设我们要删除 /tmp/V982112-01.zip 这个文件
   ```bash
   ll /tmp/

   -rw-r--r--@ 1 jianglexing  staff  437235344  5  3 11:31 V982112-01.zip
   ```
   **3、** 用 mtls-file-truncate 来完成一秒删除(截断)一点点
   ```bash
   mtls-file-truncate --chunk=32 /tmp/V982112-01.zip

   2019-07-27 12:46:40,618 INFO file /tmp/V982112-01.zip size 437235344(byte)    chunck size 33554432(byte)
   2019-07-27 12:46:40,619 INFO truncate file to 403680912 byte(s)
   2019-07-27 12:46:41,625 INFO truncate file to 370126480 byte(s)
   2019-07-27 12:46:42,631 INFO truncate file to 336572048 byte(s)
   2019-07-27 12:46:43,636 INFO truncate file to 303017616 byte(s)
   2019-07-27 12:46:44,641 INFO truncate file to 269463184 byte(s)
   2019-07-27 12:46:45,645 INFO truncate file to 235908752 byte(s)
   2019-07-27 12:46:46,651 INFO truncate file to 202354320 byte(s)
   2019-07-27 12:46:47,656 INFO truncate file to 168799888 byte(s)
   2019-07-27 12:46:48,659 INFO truncate file to 135245456 byte(s)
   2019-07-27 12:46:49,663 INFO truncate file to 101691024 byte(s)
   2019-07-27 12:46:50,668 INFO truncate file to 68136592 byte(s)
   2019-07-27 12:46:51,673 INFO truncate file to 34582160 byte(s)
   2019-07-27 12:46:52,679 INFO truncate file to 1027728 byte(s)
   2019-07-27 12:46:53,682 INFO compelete
   ```
   查看完成后的效果
   ```bash
   ll /tmp/
   
   -rw-r--r--@ 1 jianglexing  staff   0  7 27 12:46 V982112-01.zip
   ```
   **4、** 更多的使用技巧可以查看帮助信息
   ```bash
   mtls-file-truncate --help
   usage: mtls-file-truncate [-h] [--chunk CHUNK] [--sleep-time SLEEP_TIME] file
   
   positional arguments:
     file                  file path
   
   optional arguments:
     -h, --help            show this help message and exit
     --chunk CHUNK         chunk size default 4 (MB)
     --sleep-time SLEEP_TIME
                           sleep time per truncate
   ```
   ---

## 数据库性能测试
   **mtls-perf-bench 的目标，我们希望在申请到一个数据库实例的时候对其进行一下性能测试，有人会说了大哥，这活 sysbench 不是会干吗？一点都没有错 sysbench 是可以做性能测试，它非常的优秀，以致于成为了业界一个事实的标准。**

   **sysbench 也有它不好的地方，主要在于它的表结构是“固定”的，我们用 sysbench 可以测试出来上百万的qps，用我们自己的表结构可以跑多少分呢？mtls-perf-bench 想解决在特定表结构下的性能的测量问题。**

   **mtls-perf-bench 希望通过测试发现参数上可以调整的地方，这样可以更早的发现实例存在的配置问题，之后也希望 mtls-perf-bench 可以作为一个诊断分析的工具。**

   ---

   **0、** 在目标实例上创建测试用户并授权
   ```sql
   create user mpb@'%' identified by '123456';
   grant all on tempdb.* to mpb@'%';
   ```

   **1、** 创建表
   ```bash
   mtls-perf-bench --host=127.0.0.1 --port=3306 --user=mpb --password=123456 \
   --ints=4 --floats=2 --varchars=2 create

   2019-07-29 14:58:56,581  mtls-perf-bench  9031  MainThread  INFO  create table sql statement: create table tempdb.t ( id int not null auto_increment primary key,i0 int not null,i1 int not null,i2 int not null,i3 int not null,c0 varchar(128) not null,c1 varchar(128) not null,f0 float not null,f1 float not null);
   2019-07-29 14:58:56,619  mtls-perf-bench  9031  MainThread  INFO  complete
   ```
   ```sql
   show create table t;
   
   CREATE TABLE `t` (
     `id` int(11) NOT NULL AUTO_INCREMENT,
     `i0` int(11) NOT NULL,
     `i1` int(11) NOT NULL,
     `i2` int(11) NOT NULL,
     `i3` int(11) NOT NULL,
     `c0` varchar(128) COLLATE utf8mb4_general_ci NOT NULL,
     `c1` varchar(128) COLLATE utf8mb4_general_ci NOT NULL,
     `f0` float NOT NULL,
     `f1` float NOT NULL,
     PRIMARY KEY (`id`)
   ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
   ```
   **2、** insert 性能测试
   ```bash
   mtls-perf-bench --host=127.0.0.1 --port=3306 --user=mpb --password=123456    --ints=4 --floats=2 --varchars=2 --parallel=4 --rows=20000 insert
   2019-07-29 17:40:20,574  mtls-perf-bench  18671  MainThread  INFO  start time = 1564393220.574386
   2019-07-29 17:40:20,574  mtls-perf-bench  18671  MainThread  INFO  ****
   2019-07-29 17:40:20,574  mtls-perf-bench  18671  MainThread  INFO  ****
   2019-07-29 17:40:20,574  mtls-perf-bench  18671  Thread-1  INFO  sql statement: insert into tempdb.t (i0,i1,i2,i3,c0,c1,f0,f1) values(%s,%s,%s,%s,%s,%s,%s,%s)
   2019-07-29 17:40:20,575  mtls-perf-bench  18671  Thread-2  INFO  sql statement: insert into tempdb.t (i0,i1,i2,i3,c0,c1,f0,f1) values(%s,%s,%s,%s,%s,%s,%s,%s)
   2019-07-29 17:40:20,575  mtls-perf-bench  18671  Thread-3  INFO  sql statement: insert into tempdb.t (i0,i1,i2,i3,c0,c1,f0,f1) values(%s,%s,%s,%s,%s,%s,%s,%s)
   2019-07-29 17:40:20,575  mtls-perf-bench  18671  Thread-4  INFO  sql statement: insert into tempdb.t (i0,i1,i2,i3,c0,c1,f0,f1) values(%s,%s,%s,%s,%s,%s,%s,%s)
   2019-07-29 17:40:36,117  mtls-perf-bench  18671  MainThread  INFO  ****
   2019-07-29 17:40:36,117  mtls-perf-bench  18671  MainThread  INFO  ****
   2019-07-29 17:40:36,117  mtls-perf-bench  18671  MainThread  INFO  stop time = 1564393236.117363
   2019-07-29 17:40:36,117  mtls-perf-bench  18671  MainThread  INFO  TPS:1286.75 duration 15.54(s)
   ```
   >可以看到四个迸发下tps为 1286.75 

   **3、** 清理环境
   ```bash
   mtls-perf-bench --host=127.0.0.1 --port=3306 --user=mpb --password=123456  drop 
   ```

   **4、** 更多用法请查看帮助手册
   ```bash
   mtls-perf-bench --help
   usage: mtls-perf-bench [-h] [--host HOST] [--port PORT] [--user USER]
                          [--password PASSWORD] [--database DATABASE]
                          [--table TABLE] [--parallel PARALLEL] [--rows ROWS]
                          [--log-level {info,debug,error}]
                          [--auto-primary-key {False,True}] [--ints INTS]
                          [--floats FLOATS] [--doubles DOUBLES]
                          [--varchars VARCHARS] [--varchar-length VARCHAR_LENGTH]
                          [--decimals DECIMALS]
                          [--decimal-precision DECIMAL_PRECISION]
                          [--decimal-scale DECIMAL_SCALE]
                          {create,drop,insert}
   
   positional arguments:
     {create,drop,insert}
   
   optional arguments:
     -h, --help            show this help message and exit
     --host HOST           mysql host
     --port PORT           mysql port
     --user USER           mysql user
     --password PASSWORD   mysql user \'s passowrd
     --database DATABASE   work schema(database)
     --table TABLE         work table
     --parallel PARALLEL   parallel workers
     --rows ROWS           rows
     --log-level {info,debug,error}
     --auto-primary-key {False,True}
                           whether table has primary key
     --ints INTS           int column counts
     --floats FLOATS       float column counts
     --doubles DOUBLES     double column counts
     --varchars VARCHARS   varchar column counts
     --varchar-length VARCHAR_LENGTH
                           varchar column length default 128
     --decimals DECIMALS   decimal column counts
     --decimal-precision DECIMAL_PRECISION
                           total digits length
     --decimal-scale DECIMAL_SCALE
                           the scale of decimal(the number of digits to the right
                           of the decimal point)
   ```

   **其它**

   目前 mtls-perf-bench 支持的操作

   |**操作名**|**注释**|
   |---------|-------|
   |create   | 根据给定的参数创建表|
   |insert   | 执行插件操作并记录tps|
   |select   | 执行查询操作并记录qps(开发中)|
   |update   | 执行更新操作并记录tps(开发中)|
   |delete   | 执行删除操作并记录tps(开发中)|
   |drop     | 删除表|
   
   **mtls-perf-bench 优势与劣势**

   0、mtls-perf-bench 支持灵活的指定表的列数与类型

   1、mtls-perf-bench 支持单进程和多进程两种工作模式

   ---

## 断开所有的客户端连接
   **有些时候出于一些特殊的原因，我们想把所有的客户端连接都 kill 掉**
   
   **1、** kill 之前
   ```sql
   show processlist;
   +----+-----------------+-----------+------+---------+------+------------------------+------------------+
   | Id | User            | Host      | db   | Command | Time | State                  | Info             |
   +----+-----------------+-----------+------+---------+------+------------------------+------------------+
   |  4 | event_scheduler | localhost | NULL | Daemon  |  229 | Waiting on empty queue | NULL             |
   | 13 | root            | localhost | NULL | Query   |    0 | starting               | show processlist |
   | 14 | root            | localhost | NULL | Sleep   |   10 |                        | NULL             |
   +----+-----------------+-----------+------+---------+------+------------------------+------------------+
   3 rows in set (0.01 sec)
   ```
   ---

   **2、** 发起 kill 指令
   ```bash
   mtls-kill-all-conections --host=127.0.0.1 --user=root --port=3306 --password='xxxxx'

   2019-08-07 15:30:21,353 INFO kill 13;
   2019-08-07 15:30:21,354 INFO kill 14;
   ```
   >mtls-kill-all-conections 对 event、Dump 线程开了白名单，所以他们不会被 kill 掉。

   ---

## 统计慢查询文件中的SQL类型与热点表
   **用于分类统计慢查询文件中各类 SQL 出现的次数，热点表出现的次数**
   ```bash
   mtls-sql-distribution slow.log 


   ------------------------------------------------
   SQL出现频率如下:                                     
   ------------------------------------------------
   select                  |25                     
   insert                  |19                     
   update                  |0                      
   delete                  |0                      
   ------------------------------------------------
   
   
   ------------------------------------------------
   表名出现频率如下:                                      
   ------------------------------------------------
   t                                       |21     
   tempdb.t                                |20     
   data_locks                              |1      
   ------------------------------------------------
   ```
   >说明 select 出现了 25 次，insert 出现了 19 次； t 表在慢查询中出现了 21 次 ... ...

   **1、更多用法可以查看帮助信息**
   ```bash
   mtls-sql-distribution  --help
   usage: mtls-sql-distribution [-h] [--limit LIMIT] sqlfile
   
   positional arguments:
     sqlfile        slow query log file
   
   optional arguments:
     -h, --help     show this help message and exit
     --limit LIMI
   ``` 

   ---

## 表的最晚更新时间统计
   **mtls-file-stat 用于分析某一时间点之后就再没有更新过的表，比如说一套系统上线好几年了，经过了 n 次迭代，
   有一些表早就不用了，但是并没有对它进行删除，这就使得这些占用的空间永远不会被释放，mtls-file-stat 就是用来
   找出这些可疑的表**

   **以找出 2019-08-20T00:00:00 后再也没有更新过的文件为例子**
   ```bash
   cd /database/mysql/data/

   mtls-file-stat --baseline=2019-08-20T00:00:00 3306
   2019-08-22 16:35:16,528 INFO 准备扫描目录 3306
   2019-08-22 16:35:16,528 INFO 准备扫描目录 3306/#innodb_temp
   2019-08-22 16:35:16,528 INFO 准备扫描目录 3306/mysql
   2019-08-22 16:35:16,528 INFO 准备扫描目录 3306/performance_schema
   2019-08-22 16:35:16,530 INFO 准备扫描目录 3306/sys
   2019-08-22 16:35:16,530 INFO 准备扫描目录 3306/tempdb
   
   
   3306 目录下文件统计信息明细 (order by mtime 小于 2019-08-20T00:00:00):
   --------------------------------------------------------------------------------------------------------------------
   file-path                                        | mtime                | atime                | ctime               
   --------------------------------------------------------------------------------------------------------------------
   3306/auto.cnf                                    | 2019-07-24T18:52:46  | 2019-08-21T14:35:14  | 2019-07-24T18:52:46 
   3306/tempdb/t2.ibd                               | 2019-08-06T11:30:08  | 2019-08-21T14:35:13  | 2019-08-06T11:30:08 
   3306/tempdb/t3.ibd                               | 2019-08-14T14:14:29  | 2019-08-21T14:35:13  | 2019-08-14T14:14:2
   ```
   更新多信息可以查看帮助
   ```bash
   mtls-file-stat --help
   usage: mtls-file-stat [-h] [--order-by {atime,mtime,ctime}]
                         [--baseline BASELINE]
                         topdir
   
   positional arguments:
     topdir
   
   optional arguments:
     -h, --help            show this help message and exit
     --order-by {atime,mtime,ctime}
     --baseline BASELIN
   ```
   ---


## 找出长时间没有使用过的表
   **如果一张表有好几十天都没有写入了，这个往往是因为业务已经不再使用这张表，但是忘记了 drop 它，mtls-expired-tables 就是用于找出这种可疑的表**

   找出最晚写入时间小于一天前的表
   ```bash
   mtls-expired-tables --not-used-days=1 /database/mysql/data/3306

   2019-09-02 14:33:24,289 INFO 分析数据目录(/database/mysql/data/3306)
   2019-09-02 14:33:24,289 INFO 准备过虑出最近修改日期(mtime) < 2019-09-01T14:33:24.289396

   tempdb.ti
   ```
   也支持直接保存到文件
   ```bash
   mtls-expired-tables --not-used-days=1 /database/mysql/data/3306 > /tmp/expired-tables.log
   
   2019-09-02 14:37:12,880 INFO 分析数据目录(/database/mysql/data/3306)
   2019-09-02 14:37:12,880 INFO 准备过虑出最近修改日期(mtime) < 2019-09-01T14:37:12.880759
   ```
   


   ---








