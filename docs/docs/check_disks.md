---
title: check_disks
---

# Disks

**DISKS** checks one or more disk capacity on Linux filesystem, as returned by `df -k` command.


## Enable the check

Enable de `disks` check in the configuration :

    # conf.yml
	checks:
  	  - disks

## Additional parameters

This check requires additional parameters to define each disk to be checked :

	# conf.py
	disks:
	  - path: /
	    alert: 94
	  - path: /home
	    alert: 70

The first parameter is the name of the disk (df -k).
The second parameter is the percent threshold before sending an alert.

## Alerts

This check sends an alert and adds alert fields if a mount point is not present.

output:

	cmt_alert: yes
	cmt_alert_message: string


## Output to ElasticSearch

This module sends one message for each mount point, with the following fields:

	cmt_check: disk
	+
	cmt_disk: /path/to/disk
	cmt_disk_total: #int (bytes)
	cmt_disk_free: #int (bytes)
	cmt_disk_percent: #float (percent)  [percent used]

## CLI usage and output

	$ ./cmt.py disks
	--------------------------------------------------
	CMT - Version 0.9 - (c) Cavaliba.com - 2020/10/20
	2020/10/25 - 20:28:31 : Starting ...
	--------------------------------------------------
	cmt_group :  cmtdev
	cmt_node  :  vmpio

	Check disk 
	cmt_disk               /                             
	cmt_disk_total         67595886592 bytes (67.6 GB)   
	cmt_disk_free          51310575616 bytes (51.3 GB)   
	cmt_disk_percent       20.0 %               

	No alerts. 



