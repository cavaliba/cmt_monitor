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

## Additional parameters

This module as no additional parameter.


## Alerts

This module doesn't compute nor report alerts.


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



