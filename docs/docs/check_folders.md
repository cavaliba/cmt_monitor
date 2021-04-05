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

## Additional parameters

This check requires additional parameters to define each FOLDER to be checked :

	# conf.yml
	
	folder:

      my_folder_name
		  path               : /path/to/folder
		  [recursive]        : yes/no ; default = no
	      [no_store]         : yes/no ; default no ; don't store the filelist in memory (big dirs)
	      [filter_extension] : string : e.g. ".pdf .txt .hl7 .conf"  ; boolean OR 
	      [filter_regexp]    : string, python regexp : e.g. '.*.conf$'
		  [send_content]     : if path is a file, send 200 first chars as cmt_file_content attribute
		  [target:
		     files_max       : 400
		     files_min       : 2
		     size_max:       : (folder)
		     size_min:       : (folder)      
		     age_max:        : seconds, (file)  : all files must be younger than value (queue)
		     age_min:        : seconds (file)   : all files must be older than value
		     has_recent      : seconds - some files must be younger than value - V1.6
		     has_old         : seconds - some files must be older than value - V1.6
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

Targets define the desired state of a folder, folder hierarchy (recurse) or single file.

- `exist` (implicit target) : the folder or file must exist.

- `files_min`: minimum number of files in the folder ; usefull for backup folders

- `files_max`: maximum number of files in the folder ; usefull for queues/buffer

- `size_min`: minimal total size of the folder (bytes)

- `size_max`: maximal  size of the folder (bytes)

- `age_min`: **all** files must be older than age_min  (seconds)
 
- `age_max`:  **all** files must be younger than age_max (seconds) ; usefull for queues/buffer

- `has_recent`: **some** files must be young ; useful to check backup folders (fresh backups)

- `has_old`: **some** files must be old ; useful to check backup folders (archive/historical backups)

- `has_files`: list of exact filenames to be found


## Alerts

This check sends an alert and adds alert fields if a folder doesn't match its target state.


Alert message:

- missing : the folder doesn't exist
- too few files
- too many files
- too big
- too small
- some files are too old 
- some files are too young
- missing young file
- missing old file
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
	cmt_file_content:           (200 chars of file)

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







