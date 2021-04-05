---
title: check_cpu
---

# CPU

**CPU** collects and reports global CPU usage (percent) for the local Virtual Machine or server.

## Enable the module

Enable the module in the configuration :

    # conf.yml

	modules:
  	  cpu:
  	     enable: yes

### Add a check

	cpu:
	  mycpucheck:
	    enable: yes
	    alert_max_level: notice
  	     threshold: 80.5              # percentage

## Additional parameters
*new v1.6*

    threshold: float ; percentage threshold before raising an alert


## Alerts

Alert can be adjusted with common `enable_pager` and `alert_max_level` options.


## Output to ElasticSearch

This module sends one message with the following fields:

	cmt_check: cpu
	+
	cmt_cpu:  #float - percentage of CPU in use

## CLI usage and output

	/dev/cmt_monitor$ ./cmt.py cpu

	Check cpu 
	cmt_cpu                13.5 % ()  - CPU Percentage
	OK                     usage : 13.5 %



