---
title: check_mysql
---

# MYSQL Module
*Version : 1.8+*

This module provides:

* simple and standard metrology for MySQL and MariaDB servers
* slave monitoring for master/slave topologies

All host/port/credentials are to be configurer in a mysql.cnf file format.

As for all modules, metrology is sent to all configured targets : Graylog, ElasticSearch, InfluxDB. And alerts are sent to pager if threshold and conditions are met.


## Enable the module

Enable the module in the configuration (optional) :

    # conf.yml
    
	modules:
  	  mysql:
  	     enable: yes


## common parameters

See [config page](config.md) for common check parameters.

## specific parameters

	# conf.yml
	mysql:

	    mytestdbcheck:
	      defaults_file: /opt/cmt/mysql.cnf
	          #  [client]
	          #  host     = 127.0.0.1
	          #  user     = root
	          #  password = xxxxxxx
	          #  port     = 3306
	          #  socket   = /var/run/mysqld/mysqld.sock
	      is_slave: yes
	      max_behind: 300
	      alert_max_level: notice
	      alert_delay: 300

## Standard metrics collected

- `cmt_mysql_connection`:  Threads_connected from SHOW GLOBAL STATUS ; concurrent clients.

- `cmt_mysql_runner`:  Threads_running from SHOW GLOBAL STATUS ; active clients.

- `cmt_mysql_memory`:  Memory from SHOW GLOBAL STATUS

- `cmt_mysql_read_rate`:  Derivative (accross runs) of Com_select

- `cmt_mysql_write_rate`:  Derivative of Com_insert + update + delete

- `cmt_mysql_query_rate`:  Derivative of Queries from SHOW GLOBAL STATUS

- `cmt_mysql_cx_rate`:  Derivative for Connections from SHOW GLOBAL STATUS


## Slave metrics collected

When *is_slave* is configured, the following metrics are collected. 

	cmt_slave_io_run         Yes - Slave_IO_Running
	cmt_slave_sql_run        Yes - Slave_SQL_Running
	cmt_slave_master_logfile mysql-bin.000004 - Master_Log_File
	cmt_slave_relayfile      mysql-bin.000004 - Relay_Master_Log_File
	cmt_slave_behind         0 - Seconds_Behind_Master

An alert is triggered when io_run or sql_run are not *Yes* or when slave_behind is too high (configuration), meaning
that the slave server is out-of-sync with its master server.

## CLI Output (example)
	
	$ cmt -s mysql

	Check mysql 
	cmt_mysql_version        10.3.23-MariaDB-1:10.3.23+maria~bionic-log
	cmt_mysql_connection     2
	cmt_mysql_runner         7
	cmt_mysql_memory         276053016 bytes  [276.1 MB]
	cmt_mysql_read_rate      0.0 - r/sec
	cmt_mysql_write_rate     0.0 - w/sec
	cmt_mysql_query_rate     0.05 - q/sec
	cmt_mysql_cx_rate        0.01 - connection/sec
	OK                       mydbmaster - cx=2 cx/s=0.01 r/s=0.0 w/s=0.0 q/s=0.05 mem=276053016

	Check mysql 
	cmt_mysql_version        10.3.23-MariaDB-1:10.3.23+maria~bionic
	cmt_mysql_connection     1
	cmt_mysql_runner         8
	cmt_mysql_memory         277474552 bytes  [277.5 MB]
	cmt_mysql_read_rate      0.0 - r/sec
	cmt_mysql_write_rate     0.0 - w/sec
	cmt_mysql_query_rate     0.03 - q/sec
	cmt_mysql_cx_rate        0.01 - connection/sec
	cmt_mysql_slave_io_run   Yes - Slave_IO_Running
	cmt_mysql_slave_sql_run  Yes - Slave_SQL_Running
	cmt_mysql_slave_mpos     mysql-bin.000004 - Master_Log_File
	cmt_mysql_slave_rpos     mysql-bin.000004 - Relay_Master_Log_File
	cmt_mysql_slave_behind   0 - Seconds_Behind_Master
	OK                       mydbslave - slave 0 sec. behind (limit = 180) - cx=1 cx/s=0.01 r/s=0.0 w/s=0.0 q/s=0.03 mem=277474552




