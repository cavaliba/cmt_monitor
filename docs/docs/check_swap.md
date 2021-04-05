---
title: check_swap
---

# Swap

**SWAP** collects and reports global swap usage for the local Virtual Machine or server.

## Enable the module

Enable the module in the configuration :

    # conf.yml

	swap:
  	  myswap:
  	     enable: yes
  	     alert_max_level: warn
  	     threshold: 5.4

## Additional parameters
*new v1.6*

    thresholdd: float ; percentage threshold before raising an alert

## Alerts

Alert can be adjusted with common `enable_pager` and `alert_max_level` options.


## Output to ElasticSearch

This module sends one message with the following fields:

	cmt_check: swap
	+
	cmt_swap_used: #int (bytes)
	cmt_swap_total: #int (bytes)
	cmt_swap_percent: #float (percent)

## CLI usage and output

	$ ./cmt.py swap

	Check swap 
	cmt_swap_percent       13.9 % ()  - Swap used (percent)
	cmt_swap_used          297443328 bytes (297.4 MB)  - Swap used (bytes)
	cmt_swap_total         2147479552 bytes (2.1 GB)  - Swap total (bytes)
	OK                     used: 13.9 % /  297.4 MB - total 2.1 GB


