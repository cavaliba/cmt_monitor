---
title: check_mysql
---

# Url

**BETA 1.8**

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

	    mydb:
	       alert_max_level: notice
	       #is_master: no
	       is_slave: no
	       max_behind: 300


## Output
	
	cmt_mysql_version        10.3.23-MariaDB-1:10.3.23+maria~bionic
	cmt_slave_io_run         No - Slave_IO_Running
	cmt_slave_sql_run        No - Slave_SQL_Running
	cmt_slave_master_logfile n/a - Master_Log_File
	cmt_slave_relayfile      n/a - Relay_Master_Log_File
	cmt_slave_behind         999999999 - Seconds_Behind_Master
	NOTICE                   mysql - slave IO not running





