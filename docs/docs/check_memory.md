---
title: check_memory
---

# Memory

**MEMORY** collects and reports global memory (RAM) usage for the local Virtual Machine or server.

## Enable the module

Enable de `memory` check in the configuration :

    # conf.yml

	checks:
  	  - memory

## Additional parameters

This module as no additional parameter.


## Alerts

This module doesn't compute nor report alerts.


## Output to ElasticSearch

This module sends one message with the following fields:

	cmt_check: memory
	+
	cmt_memory_available: #int (bytes)
	cmt_memory_used: #int (bytes)
	cmt_memory_percent: #float (percent)

## CLI usage and output

	$ ./cmt.py memory
	--------------------------------------------------
	CMT - Version 0.9 - (c) Cavaliba.com - 2020/10/20
	2020/10/25 - 20:10:56 : Starting ...
	--------------------------------------------------
	cmt_group :  cmtdev
	cmt_node  :  vmpio

	Check memory 
	cmt_memory_percent     85.8 %                        
	cmt_memory_used        1557790720 bytes (1.6 GB)     
	cmt_memory_available   296288256 bytes (296.3 MB)    

	No alerts. 



