---
title: check_mysqldata
---

# MYSQLDATA Module
*Version : 2.0*

This module provides a simple way to query MySQL/MariaDB databases and send responses (rows x columns) to metrology servers.

All host/port/credentials are to be configurer in a mysql.cnf file format.

Data is sent to all configured targets : Graylog, ElasticSearch, InfluxDB.

It uses the multievent pattern, with one global event for the execution of the check, and one or more event for each line in the response.

Column name mapping can be configured.



## configuration

	# conf.yml
	
	mysqldata:

	    mydb_users:
	      defaults_file: /opt/cmt/mysql.cnf
	      query: select user,age from cmt_test.table1 limit 10
	      maxlines: 200  ; maximum number of row to retrieve (default 200)
	      columns:
	        user: username
	        age: years
	      frequency: 3600

## mysql credentials

Create /opt/cmt/mysql.cnf (or /in/some/other/dir) and make it available to CMT only. 

Use a readonly account in mysql/mariadb to prevent accidental DB write.

	[client]
	host     = 127.0.0.1
	user     = root
	password = xxxxxxx
	port     = 3306
	socket   = /var/run/mysqld/mysqld.sock


## Results

Following events will be sent to metrology servers for each CMT run.


global event:

	cmt_message: mysqldata - db_query1 - 3 lines collected
	cmt_mysqldata_count: 3

3 data events:

    cmt_m_username: phil
    cmt_m_years: 42

    cmt_m_username: joe
    cmt_m_years: 23

    ...

With

	cmt_group, cmt_node, cmt_module, cmt_check, cmt_id, ... for each event.


