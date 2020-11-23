---
title: check_pings
---

# Pings

**PINGS** checks if one or more host is reachable by standard ping command..

## Enable the check

Enable de `pings` check in the configuration :

    # conf.yml
	checks:
  	  - pings

## Additional parameters

This check requires additional parameters to define each mount point to be checked :

	# conf.py
	pings:
	  - 192.168.0.1
	  - localhost
	  - 127.0.0.1
	  - www.cavaliba.com


## Alerts

This check sends an alert and adds alert fields if a mount point is not present.

output:

	cmt_alert: yes
	cmt_alert_message: string (not responding)


## Output to ElasticSearch

This module sends one message for each mount point, with the following fields:

	cmt_check: ping
	+
	cmt_ping: hostname
	cmt_ping_status: ok/nok

## CLI usage and output

	$ ./cmt.py pings
	--------------------------------------------------
	CMT - Version 0.9 - (c) Cavaliba.com - 2020/10/20
	2020/10/25 - 21:19:17 : Starting ...
	--------------------------------------------------
	cmt_group :  cmtdev
	cmt_node  :  vmpio

	Check ping 
	cmt_ping               192.168.0.1                   
	cmt_ping_status        OK                   

	Check ping 
	cmt_ping               localhost                     
	cmt_ping_status        OK                   

	Check ping 
	cmt_ping               127.0.0.1                     
	cmt_ping_status        OK                   

	Check ping 
	cmt_ping               www.cavaliba.com                
	cmt_ping_status        OK                   

	No alerts. 




