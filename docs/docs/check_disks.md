---
title: check_disks
---

# Disks

**DISKS** checks one or more disk capacity on Linux filesystem, as returned by `df -k` command.


## Enable the module

Enable the module in the configuration :

    # conf.yml

	modules:
  	  disk:
  	     enable: yes

### Add a check

    disk:
      disk_root:
        path: /
        alert: 80


## Additional parameters

This check requires additional parameters to define each disk to be checked :

* path 
* alert threshold (percentage)

The first parameter is the name of the disk (df -k).
The second parameter is the percent threshold before sending an alert.

## Alerts

This check sends an alert and adds alert fields if a mount point is not present.


## Output to ElasticSearch

This module sends one message for each mount point, with the following fields:

	cmt_check: disk
	+
	cmt_disk: /path/to/disk
	cmt_disk_total: #int (bytes)
	cmt_disk_free: #int (bytes)
	cmt_disk_percent: #float (percent)  [percent used]

## CLI usage and output

	$ ./cmt.py disk

	Check disk 
	cmt_disk               /  ()  - Path
	cmt_disk_total         67370528768 bytes (67.4 GB)  - Total (Bytes)
	cmt_disk_used          20698943488 bytes (20.7 GB)  - Used (Bytes)
	cmt_disk_free          43218939904 bytes (43.2 GB)  - Free (Bytes)
	cmt_disk_percent       32.4 % ()  - Used (percent)
	OK                     path : / - used: 32.4 % - used: 20.7 GB - free: 43.2 GB - total: 67.4 GB 

	Check disk 
	cmt_disk               /boot  ()  - Path
	cmt_disk_total         67370528768 bytes (67.4 GB)  - Total (Bytes)
	cmt_disk_used          20698943488 bytes (20.7 GB)  - Used (Bytes)
	cmt_disk_free          43218939904 bytes (43.2 GB)  - Free (Bytes)
	cmt_disk_percent       32.4 % ()  - Used (percent)
	OK                     path : /boot - used: 32.4 % - used: 20.7 GB - free: 43.2 GB - total: 67.4 GB 



