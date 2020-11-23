---
title: check_boottime
---

# Boottime

**BOOTTIME** collects the number of seconds and days since last reboot of the local Virtual Machine or server.

## Enable the module

Enable de `boottime` check in the configuration :

    # conf.yml

	checks:
  	  - boottime

## Additional parameters

This module as no additional parameter.


## Alerts

This module doesn't compute nor report alerts.


## Output to ElasticSearch

This module sends one message with the following fields:

	cmt_check: boottime
	+
	cmt_boottime_days: #int (days)
	cmt_boottime_seconds: #int (seconds)

## CLI usage and output

	$ ./cmt.py boottime
	--------------------------------------------------
	CMT - Version 0.9 - (c) Cavaliba.com - 2020/10/20
	2020/10/25 - 20:14:19 : Starting ...
	--------------------------------------------------
	cmt_group :  cmtdev
	cmt_node  :  vmpio

	Check boottime 
	cmt_boottime_seconds   97880 seconds                 
	cmt_boottime_days      1 days                        

	No alerts. 


