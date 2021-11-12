---
title: check_load
---

# Load Average

**LoadAverage** is a very good first indication that a Virtul Machine or Server has too much work to do. Load Average is roughly the number of CPU needed to cover the requested amount of work devoted to CPUs (not including IO wait, ...). A temporary high load (several times higher than the number of CPU) for a short duration may not be critical.


## Configure

	load:

  	  myload:
  	     enable: yes
  	     enable_pager: no
  	     security_max: warn
  	     threshold1: 8.2
        threshold5: 4.3
        threshold15: 3.5

## Additional parameters

*New V1.6*

   threshold1: raise an alert if load 1 minute is above this value
   threshold5: raise an alert if load 5 minutes is above this value
   threshold15: raise an alert if load 15 minutes is above this value

default values : 999999 (no alert !)

Note: should be adjusted to a multiple of the number of vCPU.


## Alerts

Alert can be adjusted with common `enable_pager` and `alert_max_level` options.


## Output to Metrology

This module sends one message with the following fields:

	cmt_check: load
	+
	cmt_load1:  #float - value of 1 minute Load Average
	cmt_load5:  #float - value of 5 minute Load Average
	cmt_load15: #float - value of 15 minute Load Average

## Errors

	------------------------------------------------------------
	CMT - (c) cavaliba.com - Version 1.6-alpha - 2021/03/28
	------------------------------------------------------------
	cmt_group      :  cavaliba
	cmt_node       :  vmxupm
	config file    :  ./conf.yml

	oooo 0.43 10.3
	oooo 0.29 8.4
	oooo 0.33 0.01

	Check load 
	cmt_tag_global_tag1      1
	cmt_tag_global_tag2      value2
	cmt_load1                0.43 - CPU Load Average, one minute
	cmt_load5                0.29 - CPU Load Average, 5 minutes
	cmt_load15               0.33 - CPU Load Average, 15 minutes
	NOK                      load15 above threshold : 0.33 > 0.01 

   NOK  load15 above threshold : 0.33 > 0.01 

## CLI usage and output


	/dev/cmt_monitor$ ./cmt.py load

	Check load 
	cmt_load1              0.55  ()  - CPU Load Average, one minute
	cmt_load5              0.57  ()  - CPU Load Average, 5 minutes
	cmt_load15             0.6  ()  - CPU Load Average, 15 minutes
	OK                     1/5/15 min : 0.55  0.57  0.6


