---
title: check_load
---

# Load Average

**LoadAverage** is a very good first indication that a Virtul Machine or Server has too much work to do. Load Average is roughly the number of CPU needed to cover the requested amount of work devoted to CPUs (not including IO wait, ...). A temporary high load (several times higher than the number of CPU) for a short duration may not be critical.


## Enable the module

Enable the module in the configuration :

    # conf.yml

	modules:
  	  load:
  	     enable: yes

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

	Check load 
	cmt_load1              0.55  ()  - CPU Load Average, one minute
	cmt_load5              0.57  ()  - CPU Load Average, 5 minutes
	cmt_load15             0.6  ()  - CPU Load Average, 15 minutes
	OK                     1/5/15 min : 0.55  0.57  0.6


