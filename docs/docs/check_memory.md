---
title: check_memory
---

# Memory

**MEMORY** collects and reports global memory (RAM) usage for the local Virtual Machine or server.

## Configure

    # conf.yml

	memory:

  	  mymemory:
  	     enable: yes
  	     enable_pager: no
  	     severity_max: warn
  	     threshold: 75.8              # percentage

## Additional parameters
*new v1.6*

    threshold: float ; percentage threshold before raising an alert


## Alerts

Alert can be adjusted with common `enable_pager` and `severity_max` options.


## Output to Metrology

This module sends one message with the following fields:

	cmt_check: memory
	+
	cmt_memory_available: #int (bytes)
	cmt_memory_used: #int (bytes)
	cmt_memory_percent: #float (percent)

## CLI usage and output

	$ ./cmt.py memory
	
	Check memory 
	cmt_memory_percent     86.1 % ()  - Memory used (percent)
	cmt_memory_used        2031271936 bytes (2.0 GB)  - Memory used (bytes)
	cmt_memory_available   382902272 bytes (382.9 MB)  - Memory available (bytes)
	cmt_memory_total       2749349888 bytes (2.7 GB)  - Memory total (bytes)
	OK                     used 86.1 % - used 2.0 GB - avail 382.9 MB - total 2.7 GB




