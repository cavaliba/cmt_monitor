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
	      [no_store]         : yes/no ; default no (store) ; if true don't store the filelist in memory (big dirs)
	      [filter_extension] : string : e.g. ".pdf .txt .hl7 .conf"  ; boolean OR 
	      [filter_regexp]    : string, python regexp : e.g. '.*.conf$'
		  [send_content]     : if path is a file, send 200 first chars as cmt_file_content attribute
		  [send_list]        : yes/no (default no, need no_store) ; send list of files, size, uid,gid, perms
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


path

    path to the folder or file

recursive

    if set to yes, the folder is analyzed recusirvely. Beware of large folders.


no_store

    default to no (store)
    set to yes for big folders, don't store in-memory, don't compute some targets (has_files)

filter_extension

    only processes files with one of the provided extensions (OR'ed)

filter_regexp

     only processes files with a name matchnig this regexp 


send_content

	if path is a file, send 200 first chars of the file
	attribute : cmt_file_content    

send_list

	New in 2.0
	Sends the  list of processed files with path, name, size, uid,gid, perms
	Useful to display folder content (backups, queue, ...) in a dashboard
	yes/no, default is no , needs no_store set to no (store !)
	attribute : cmt_file_list
	
target

    one or more command / subchecks against that folder, to be expressed in desired target state
    Think idempotence like in Ansible
    See below for explanation of the various targets.


## Targets

Targets define the desired state of a folder, folder hierarchy (recurse) or single file.

- `exist` (implicit target) : the folder or file must exist.

- `files_min`: minimum number of files in the folder ; usefull for backup folders

- `files_max`: maximum number of files in the folder ; usefull for queues/buffer

- `size_min`: minimal total size of the folder (bytes)

- `size_max`: maximal  size of the folder (bytes)

- `age_min`: **all** files must be old ; older than age_min  (seconds)
 
- `age_max`:  **all** files must be recent ; younger than age_max (seconds) ; usefull for queues/buffer

- `has_recent`: **some** files must be recent ; useful to check backup folders (fresh backups)

- `has_old`: **some** files must be old ; useful to check backup folders (archive/historical backups)

- `has_files`: list of exact filenames to be found ; `no_store` must be set to no.


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







