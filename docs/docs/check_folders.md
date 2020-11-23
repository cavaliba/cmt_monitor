---
title: check_folders
---

# Folders

**FOLDERS** analyze one or more folder in the filesystem and performs various checks to cover various situation / folder type.

It can check for existence, size, number of files, file size, file age, or existing filenames inside the folders. It can scan recursively subfolders.


## Enable the check

Enable de `folders` check in the configuration :

    # conf.yml
	checks:
  	  - folders

## Additional parameters

This check requires additional parameters to define each FOLDER to be checked :

	# conf.py
	folders:
	  - path: /tmp
	    (OPTIONAL)name: mytmp
	    (OPTIONAL)recursive: yes/no
	    target:
	       age_min: 120       (youngest file)
	       age_max: 3600      (oldest file)
	       files_min: 3    
	       files_max: 10
	       size_min: 100000   (folder total)
	       size_max: 10       (folder total)
	       has_files:
	            - aaa
	            - bbb
	  - path: /tmp/doesnt_exist
	    name: numbertwo



- `path`: the path to the folder
- `name`: the reported name to the monitoring server
- `recursive`: if set to yes, the folder is analyzed recusirvely. Beware of large folders.
- `target`: one or more command / subchecks against that folder, to be expressed in desired target state (think idempotence like in Ansible). See below for explanation of the various targets.


## Targets

Targets define the desired state of a folder.

- `exist` (implicit target) : the folder must exist.

- `age_min`, `age_max` (seconds) : the youngest file must be older than age_min. The oldest file must be younger than age_max. Useful for checking buffers that should be empty, or backup folders that should have old versions of backups.

- `files_min`, `files_max`: min or max number of files in the folder (or recursively in the folder hierarchy).


- `size_min`, `size_max`: min/max size of the folder (and subfolders if recursive is set to yes).

- `has_files`: list of exact filenames to be found in the folder (subfolders if recursive is set to yes).


## Alerts

This check sends an alert and adds alert fields if a folder doesn't match its target state.

output:

	cmt_alert: yes
	cmt_alert_message: string

Alert message:

- missing : the folder doesn't exist
- too few files
- too many files
- too big
- too small
- some files are too old 
- some files are too young
- expected file not found

## Output to ElasticSearch

This module sends one message for each mount point, with the following fields:

	cmt_check: folder
	+
	cmt_folder_name: name
	cmt_folder_path: path
	cmt_folder_status : ok/nok  (exists or not)
	cmt_folder_files: #count    (number of files)
	cmt_folder_dirs: #count     (number of subdirs)
	cmt_folder_size: #bytes     (whole folder)
	cmt_folder_size_max: #bytes (biggest file, whole folder)
	cmt_folder_size_min: #bytes (smallest file, whole folder)
	cmt_folder_age_min:         (youngest file)
	cmt_folder_age_max:         (oldest file)

## CLI usage and output

	$ ./cmt.py folders
	--------------------------------------------------
	CMT - Version 0.9 - (c) Cavaliba.com - 2020/10/20
	2020/10/25 - 21:08:44 : Starting ...
	--------------------------------------------------
	cmt_group :  cmtdev
	cmt_node  :  vmpio

	Check folder 
	cmt_folder_path        /tmp                          
	cmt_folder_name        mytmp                         
	cmt_folder_files       3                             
	cmt_folder_dirs        21                            
	cmt_folder_size        409 bytes (409.0 B)           
	cmt_folder_age_min     1017   sec                    
	cmt_folder_age_max     101134 sec                    
	cmt_folder_status      NOK                  

	Check folder 
	cmt_folder_path        /tmp/absent                   
	cmt_folder_name        numbertwo                     
	cmt_folder_status      NOK                  

	Check folder 
	cmt_folder_path        /tmp/empty                    
	cmt_folder_name        number3                       
	cmt_folder_status      NOK                  

	Alerts : 
	--------
	check_folder - /tmp : expected file not found (aaa.txt)
	check_folder - /tmp/absent missing
	check_folder - /tmp/empty missing






