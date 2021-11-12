---
title: check_process
---

# Process

**PROCESS** checks if one or more process is running.


## Configure

This check requires parameters to define each disk to be checked :


Syntax: 

	process:

	  checkname:			     : choose a name for this check - sent to metrology 
	    psname: string           : exact name of the process to be found
	    [search_arg: string]     : optional paramter of the process command line

	    + common parameters for checks : enable, enable_pager, alarm_max_level, alert_delay, ...
	    (see config page)


Example :

    process:

	  cron:
	    psname: cron
		search_arg: "-f"

	  redis:
	    psname: redis

      graylog
        psname: java
        search_arg: '/usr/share/graylog-server/graylog.jar'
	
	  apache:
	    psname: httpd

	  ssh:
	    psname: sshd

	  ntp:
	    psname: ntpd

	  mysql:
	    psname: mysqld

	  php-fpm:
	    psname: php-fpm


### `search_arg`
*new in version 1.3.1*

This optional parameter indicates that arguments given to the process command line must be
checked against the provided string. Useful for java or nodejs process where the real
task is a parameter of the java (nodejs) main binary.

## Alerts

This check sends an alert and adds alert fields if a process is not running.


## Output to Metrology

This module sends one message for each mount point, with the following fields:

	cmt_check: process
	+
	cmt_process_name: string   (config name, not process real name)
	cmt_process_status : ok/nok
	cmt_process_cpu: float
	cmt_process_memory: int (bytes)

## CLI usage and output

	$ ./cmt.py process -s

	NOK     process      process redis missing (redis, None)
	NOK     process      process apache missing (httpd, None)
	OK      process      process cron found (cron, -f) - memory rss 3.0 MB - cpu 0.0 sec.
	OK      process      process ssh found (sshd, None) - memory rss 5.6 MB - cpu 0.04 sec.
	NOK     process      process ntp missing (ntpd, None)
	OK      process      process mysql found (mysqld, None) - memory rss 88.9 MB - cpu 0.66 sec.
	NOK     process      process php-fpm missing (php-fpm, None)



