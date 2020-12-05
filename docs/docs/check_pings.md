---
title: check_pings
---

# Pings

**PING** checks if one or more host is reachable by standard ping command.

## Enable the module

Enable the module in the configuration :

    # conf.yml

	Module:
  	  ping:
  	     enable: yes

## Additional parameters

This check requires additional parameters to define each mount point to be checked :

	# ping
	  ping_vm1:
	    module: ping
	    host: 192.168.0.1
	  ping_locahost:
	    module: ping
	    host: localhost
	  www.google.com:
	    module: ping
	    host: www.google.com
	  wwwtest:
	    module: ping
	    host: www.test.com    
	  badname:
	    module: ping
	    host: www.averybadnammme_indeed.com  


## Alerts

This check sends an alert and adds alert fields if a mount point is not present.


## Output to ElasticSearch

This module sends one message for each mount point, with the following fields:

	cmt_check: ping
	+
	cmt_ping: hostname
	cmt_ping_status: ok/nok

## CLI usage and output

	$ ./cmt.py pings

	Check ping 
	cmt_ping               192.168.0.1  () 
	OK                     192.168.0.1 ok

	Check ping 
	cmt_ping               localhost  () 
	OK                     localhost ok

	Check ping 
	cmt_ping               www.google.com  () 
	OK                     www.google.com ok

	Check ping 
	cmt_ping               www.test.com  () 
	WARN                   www.test.com not responding

	Check ping 
	cmt_ping               www.averybadnammme_indeed.com  () 
	WARN                   www.averybadnammme_indeed.com not responding





