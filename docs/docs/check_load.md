---
title: check_load
---

# Load Average

**LoadAverage** is a very good first indication that a Virtul Machine or Server has too much work to do. Load Average is roughly the number of CPU needed to cover the requested amount of work devoted to CPUs (not including IO wait, ...). A temporary high load (several times higher than the number of CPU) for a short duration may not be critical.


## Enable the module

Enable de `load` module in the configuration :

    # conf.yml

	checks:
  	  - load

## Additional parameters

This module as no additional parameter.


## Alerts

This module doesn't compute nor report alerts.


## Output to ElasticSearch

This module sends one message with the following fields:

	cmt_check: load
	+
	cmt_load1:  #float - value of 1 minute Load Average
	cmt_load5:  #float - value of 5 minute Load Average
	cmt_load15: #float - value of 15 minute Load Average

## CLI usage and output


	/dev/cmt_monitor$ ./cmt.py load

	--------------------------------------------------
	CMT - Version 0.9 - (c) Cavaliba.com - 2020/10/20
	2020/10/25 - 17:24:04 : Starting ...
	--------------------------------------------------
	cmt_group :  cmtdev
	cmt_node  :  vmpio

	Check load 
	cmt_load1              0.48                          
	cmt_load5              0.43                          
	cmt_load15             0.35                          

	No alerts. 

