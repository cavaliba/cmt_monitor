---
title: check_process
---

# Process

**PROCESS** checks if one or more process is running.


## Enable the check

Enable de `process` check in the configuration :

    # conf.yml
	checks:
  	  - process

## Additional parameters

This check requires additional parameters to define each disk to be checked :

	# conf.py
	process:
	  - name: redis
	    psname: redis
	  - name: apache2
	    psname: httpd
	  - name: cron
	    psname: cron
	  - name: sshd
	    psname: sshd
	  - name: ntp
	    psname: chronyd
	  - name: mysqld
	    psname: mysqld
	  - name: php-fpm
	    psname: php72-fpm


The first parameter is the name of the process to be reported to cental server.
The second parameter is the exact process name to be checked in the process list.

## Alerts

This check sends an alert and adds alert fields if a process is not running.

output:

	cmt_alert: yes
	cmt_alert_message: string


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
	--------------------------------------------------
	CMT - Version 0.9 - (c) Cavaliba.com - 2020/10/20
	2020/10/25 - 20:33:22 : Starting ...
	--------------------------------------------------
	cmt_group :  cmtdev
	cmt_node  :  vmpio

	Check process 
	cmt_process_name       redis                         
	cmt_process_status     NOK                  

	Check process 
	cmt_process_name       apache2                        
	cmt_process_status     NOK                  

	Check process 
	cmt_process_name       cron                          
	cmt_process_status     OK                   
	cmt_process_memory     618496 bytes (618.5 KB)       
	cmt_process_cpu        0.07 seconds                  

	Check process 
	cmt_process_name       sshd                          
	cmt_process_status     OK                   
	cmt_process_memory     2772992 bytes (2.8 MB)        
	cmt_process_cpu        0.02 seconds                  

	Check process 
	cmt_process_name       ntp                          
	cmt_process_status     NOK                  

	Check process 
	cmt_process_name       mysqld                        
	cmt_process_status     OK                   
	cmt_process_memory     0 bytes (0.0 B)               
	cmt_process_cpu        11.71 seconds                 

	Check process 
	cmt_process_name       php72-fpm                       
	cmt_process_status     NOK                  

	Alerts : 
	--------
	check_process - redis missing (redis)
	check_process - apache missing (httpd)
	check_process - ntpd missing (ntpd)
	check_process - php-fpm missing (php-fpm)




