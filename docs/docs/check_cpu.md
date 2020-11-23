---
title: check_cpu
---

# CPU

**CPU** collects and reports global CPU usage (percent) for the local Virtual Machine or server.

## Enable the module

Enable de `cpu` module in the configuration :

    # conf.yml

	checks:
  	  - cpu

## Additional parameters

This module as no additional parameter.


## Alerts

This module doesn't compute nor report alerts.


## Output to ElasticSearch

This module sends one message with the following fields:

	cmt_check: cpu
	+
	cmt_cpu:  #float - percentage of CPU in use

## CLI usage and output

	/dev/cmt_monitor$ ./cmt.py cpu
	--------------------------------------------------
	CMT - Version 0.9 - (c) Cavaliba.com - 2020/10/20
	2020/10/25 - 17:27:16 : Starting ...
	--------------------------------------------------
	cmt_group :  cmtdev
	cmt_node  :  vmpio

	Check cpu 
	cmt_cpu                11.8 %                        

	No alerts. 


