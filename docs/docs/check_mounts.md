---
title: check_mounts
---

# Mounts

**Mounts** checks if one or more mount point in Linux filesystem are present.

## Enable the check

Enable de `mounts` check in the configuration :

    # conf.yml
	checks:
  	  - mounts

## Additional parameters

This check requires additional parameters to define each mount point to be checked :

	# conf.py
	mounts:
	  - /
	  - /boot
	  - /mnt/export
	  - /home

## Alerts

This check sends an alert and adds alert fields if a mount point is not present.

output:

	cmt_alert: yes
	cmt_alert_message: string


## Output to ElasticSearch

This module sends one message for each mount point, with the following fields:

	cmt_check: mount
	+
	cmt_mount: /path/to/mount
	cmt_mount_status: ok/nok

## CLI usage and output

	$ ./cmt.py mounts
	--------------------------------------------------
	CMT - Version 0.9 - (c) Cavaliba.com - 2020/10/20
	2020/10/25 - 20:18:27 : Starting ...
	--------------------------------------------------
	cmt_group :  cmtdev
	cmt_node  :  vmpio

	Check mount 
	cmt_mount              /                             
	cmt_mount_status       OK                   

	Check mount 
	cmt_mount              /boot                         
	cmt_mount_status       NOK                  

	Alerts : 
	--------
	check_mount - /boot not found



