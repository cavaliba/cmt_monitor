---
title: check_process
---

# Process

**PROCESS** checks if one or more process is running.


## Enable the module

Enable the module in the configuration :

    # conf.yml

	modules:
  	  process:
  	     enable: yes

## Additional parameters

This check requires additional parameters to define each disk to be checked :


	process:
	  redis:
	    psname: redis
	    enable_pager: no
	  apache:
	    psname: httpd
	  cron:
	    psname: cron
	  ssh:
	    psname: sshd
	  ntp:
	    psname: ntpd
	  mysql:
	    psname: mysqld
	  php-fpm:
	    psname: php-fpm
	    enable_pager: yes



The first parameter is the name of the process to be reported to cental server.
The second parameter is the exact process name to be checked in the process list.

## Alerts

This check sends an alert and adds alert fields if a process is not running.



## Output to ElasticSearch

This module sends one message for each mount point, with the following fields:

	cmt_check: process
	+
	cmt_process_name: string   (config name, not process real name)
	cmt_process_status : ok/nok
	cmt_process_cpu: float
	cmt_process_memory: int (bytes)

## CLI usage and output

	$ ./cmt.py process

	Check process 
	cmt_process_name       redis  () 
	NOK                    redis missing (redis)

	Check process 
	cmt_process_name       apache  () 
	NOK                    apache missing (httpd)

	Check process 
	cmt_process_name       cron  () 
	cmt_process_memory     2899968 bytes (2.9 MB)  - rss
	cmt_process_cpu        0.04 seconds (0:00:00)  - cpu time, user
	OK                     cron found (cron) - memory rss 2.9 MB - cpu 0.04 sec.

	Check process 
	cmt_process_name       ssh  () 
	cmt_process_memory     3899392 bytes (3.9 MB)  - rss
	cmt_process_cpu        0.05 seconds (0:00:00)  - cpu time, user
	OK                     ssh found (sshd) - memory rss 3.9 MB - cpu 0.05 sec.

	Check process 
	cmt_process_name       ntp  () 
	NOK                    ntp missing (ntpd)

	Check process 
	cmt_process_name       mysql  () 
	cmt_process_memory     56307712 bytes (56.3 MB)  - rss
	cmt_process_cpu        20.76 seconds (0:00:20)  - cpu time, user
	OK                     mysql found (mysqld) - memory rss 56.3 MB - cpu 20.76 sec.

	Check process 
	cmt_process_name       php-fpm  () 
	NOK                    php-fpm missing (php-fpm)





