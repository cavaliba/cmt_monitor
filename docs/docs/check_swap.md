---
title: check_swap
---

# Swap

**SWAP** collects and reports global swap usage for the local Virtual Machine or server.

## Enable the module

Enable de `swap` check in the configuration :

    # conf.yml

	checks:
  	  - swap

## Additional parameters

This module as no additional parameter.


## Alerts

This module doesn't compute nor report alerts.


## Output to ElasticSearch

This module sends one message with the following fields:

	cmt_check: swap
	+
	cmt_swap_used: #int (bytes)
	cmt_swap_percent: #float (percent)

## CLI usage and output

	$ ./cmt.py swap
	--------------------------------------------------
	CMT - Version 0.9 - (c) Cavaliba.com - 2020/10/20
	2020/10/25 - 20:12:33 : Starting ...
	--------------------------------------------------
	cmt_group :  cmtdev
	cmt_node  :  vmpio

	Check swap 
	cmt_swap_percent       34.3 %                        
	cmt_swap_used          736362496 bytes (736.4 MB)    

	No alerts. 

