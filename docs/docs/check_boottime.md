---
title: check_boottime
---

# Boottime

**BOOTTIME** collects the number of seconds and days since last reboot of the local Virtual Machine or server. You can build dashboards to monitor host without reboot.

### configure

	# conf.yml
	
	boottime:

       my_boottime:
	     enable: yes
         severity_max: warning
         threshold: 75               # days
         frequency: 3600             # seconds


## Additional parameters
*new v1.6*

    threshold: float ; days before raising an alert


## Alerts

Alert can be adjusted with common `enable_pager` and `severity_max` options.


## Output to Metrology

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
                     


