---
title: check_boottime
---

# Boottime

**BOOTTIME** collects the number of seconds and days since last reboot of the local Virtual Machine or server. You can build dashboards to monitor host without reboot.

## Enable the module

Enable the module in the configuration :

    # conf.yml

	Module:
  	  boottime:
  	     enable: yes

### Add a check

	  boottime:
	    module: boottime
	    enable: yes
	    alert_max_level: alert


## Additional parameters

This module as no additional parameter.


## Alerts

This module doesn't compute nor report alerts.


## Output to ElasticSearch

This module sends one message with the following fields:

	cmt_module: boottime
	+
	cmt_boottime_days: #int (days)
	cmt_boottime_seconds: #int (seconds)

## CLI usage and output

	$ ./cmt.py boottime
 
	Check boottime 
	cmt_boottime_seconds   83790 seconds (23:16:30)  - Seconds since last reboot
	cmt_boottime_days      0 days ()  - Days since last reboot
	OK                     days since last reboot : 0 days - 23:16:30 sec.
                     


