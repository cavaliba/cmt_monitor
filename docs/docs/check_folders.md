---
title: check_folders
---

# Folders

**FOLDERS** analyze one or more folder in the filesystem and performs various checks to cover various situation / folder type.

It can check for existence, size, number of files, file size, file age, or existing filenames inside the folders. It can scan recursively subfolders.


## Enable the module

Enable the module in the configuration :

    # conf.yml

	modules:
  	  folder:
  	     enable: yes

## Additional parameters

This check requires additional parameters to define each FOLDER to be checked :

	# conf.yml
	
	folder:

      my_folder_name
		  path               : /path/to/folder
		  [recursive]        : yes/no ; default = no
	      [no_store]         : yes/no ; default no ; don't store the filelist in memory (big dirs)
	      [filter_extension] : string : e.g. ".pdf .txt .hl7 .conf"  ; AND condition 
	      [filter_regexp]    : string, python regexp : e.g. '.*.conf$'
		  [target:
		     files_max       : 400
		     files_min       : 2
		     size_max:       : (folder)
		     size_min:       : (folder)      
		     age_max:        : seconds, (file)
		     age_min:        : seconds (file)
		     has_files: 
		         - filename1
		         - filename2
		     ()min_bytes:    : TODO (file)
		     ()max_bytes:    : TODO
		   ]


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

	Check folder 
	cmt_folder_path        /tmp  () 
	cmt_folder_name        /tmp  () 
	cmt_folder_files       3 files ()  - Number of files in folder /tmp
	cmt_folder_dirs        15 dirs ()  - Number of dirs/subdirs in folder /tmp
	cmt_folder_size        425 bytes (425.0 B)  - Total Size (bytes)
	cmt_folder_age_min     84283 sec ()  - Min age (seconds)
	cmt_folder_age_max     84478 sec ()  - Max age (seconds)
	NOK                    /tmp : expected file not found (secret.pdf)

	Check folder 
	cmt_folder_path        /missing  () 
	cmt_folder_name        /missing  () 
	NOK                    /missing missing







