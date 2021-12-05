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
  	     security_max: warning
  	     threshold1: 6.0
        threshold5: 4.0
        threshold15: 2.0


    threshold1: raise an alert if load 1 minute is above this value (multiplied by the number of available CPUs)
    threshold5: raise an alert if load 5 minutes is above this value (id.)
    threshold15: raise an alert if load 15 minutes is above this value (id.)

default values : 6, 4 and 2.

## Alerts and severity

By default, severity is either CRITICAL or NONE.

Severity can be adjusted with common `severity_max` option.


## Output to Metrology

This module sends one message with the following fields:

	cmt_module:    load

	cmt_check:     name of the check
	cmt_load_cpu:  int - number of available CPUs detected
	cmt_load1:     float - value of 1 minute Load Average
	cmt_load5:     float - value of 5 minute Load Average
	cmt_load15:    float - value of 15 minute Load Average



# CLI OUTPUT

   $ cmt load


	------------------------------------------------------------------
	load myload
	------------------------------------------------------------------
	cmt_load_cpu             2 - Available CPUs
	cmt_load1                0.3 - CPU Load Average, one minute
	cmt_load5                6.11 - CPU Load Average, 5 minutes
	cmt_load15               7.78 - CPU Load Average, 15 minutes
	CRITICAL ( )  : load-15/cpu is above threshold : 7.78 > 2 (x 2 cpus)

	2021/12/05 - 19:55:58 : SEVERITY=CRITICAL - 0/1 OK (0 %) - 1 NOK : 1 criticial - 0 error - 0 warning - 0 notice.


