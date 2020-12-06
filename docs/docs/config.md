---
title: configuration
---

##  conf.yml

CMT use one or more configuration files to know what kind of checks to perform, what threshold or alert conditions are defined, and to which remote server the collected data must be sent.

The YAML file `conf.yml` is the standard configuration file for CMT.

By default, it is located next to `cmy.py` or `cmt` binay program.


## --conf myconf.yml  option

you can specify an alternate configuration file :

    $ cmt --conf /my/dir/cmt/conf.yml

This let you have different execution contexts of CMT on the same Server.

## Folder conf.d/

Every file in the conf.d/ folder next to the conf.yml is merged into the configuration at run time. This design helps manage a bigger configuration with devops / deployment tools like Ansible.

When deploying a new component on a CMT monitored system which needs more monitoring (process, socket, path, response time, urls availabity, ...) just drop a file in the conf.d folder with additionnal checks to perform.

Each additional file must be a valid

## Folder structure

	/opt/cmt_monitor$ tree -L 1
	.
	├── cmt
	├── cmt.py
	├── (...)	
	├── conf.yml     <= main configuration file
	└── conf.d/      <= additional configuration files go in there 
	   ├── demo.yml
	   ├── apache.yml
	   ├── folder_backup.yml
	   └── README


## Configuration structure

The complete configuration for a CMT run has 5 sections :

1. a global section (global)
2. a metrology server section
3. a pager servers section
4. a module section  to enable/disable various modules
5. a checks section with all  individual checks parameters (module dependent)


## Configuration Reference 

	===========================================================
	Configuration Reference
	===========================================================

	[ ] is optional, available
	( ) is on the roadmap


	--------------------------------
	timerange field
	--------------------------------
	- yes
	- no
	- after YYYY-MM-DD hh:mm:ss
	- before YYYY-MM-DD hh:mm:ss
	- hrange hh:mm:ss hh:mm:ss
	- ho   (8h30/18h mon>fri)
	- hno  (! (8h30/18h mon>fri))

	----------------------
	Global
	----------------------

	global:
	  cmt_group: cavaliba
	  cmt_node: dev_vm1

	  [cmt_node_env]       : string: prod, dev, qa, test, form, preprod, qualif ...
	  [cmt_node_role]      : string ; appli_front_1, db_3
	  [cmt_node_location]  : string, geographical position

	  [enable]             : timerange ; DEFAULT = yes; master switch (no inheritance)
	  [enable_pager]       : timerange ; DEFAULT = no ; master switch (no inheritance)
	  [pager_rate_limit]   : seconds ; default 7200
	  [conf_url]           : https://.../api/  (/group_node.txt if url ends by /)
	  [max_execution_time] : seconds ; DEFAULT 5
	  [load_confd]         : yes/no ; DEFAULT no
	  [alert_max_level]    : alert, warn, notice   ; lower priority ;
	  [alert_delay]        : delay before transition to alert (if alert) ; seconds/DEFAULT 120 


	----------------------
	Metrology Servers
	----------------------

	metrology_servers:

	  graylog_test1:
	      type: graylog_udp_gelf
	      host: 10.10.10.13
	      port: 12201
	  graylog_test2:
	      type: graylog_tcp_gelf
	      url: http://10.10.10.13:8080/gelf

	      [enable]                : timerange ; default = yes ; master switch      
	      ()secret_key

	----------------------
	Pager services
	----------------------

	pagers:
	  alert              : mandatory entry 'alert'
	     type            : team_channel
	     url             : Teams channel URL
	     [enable]        : timerange ; DEFAULT = no ; master switch / no inheritance
	     ()secret_key    : 
	     ()add_tags
	         tag: value
	         tag: value
	  test               : mandatory 'test' entry for ARG --pagertest
	     type            : team_channel
	     url             :   
	     [enable]        : timerange ; DEFAULT = no  test:
	     ()secret_key    : 


	---------------------------
	Modules
	---------------------------
	modules are enabled by default

	modules:
	  name:               : module name : ex load , cpu, swap, ...
	    enable            : timerange ; default yes
	  name:               : load 
	    enable            : timerange ; default yes
	    [alert_max_level] : alert, warn, notice (scale down)  ; overwrites global entry
	    [alert_delay]     : delay before transition from to alert ; seconds/DEFAULT 120 
	    [frequency]       : min seconds between runs ; needs --cron in ARGS


	--------------------------
	Checks instances
	--------------------------

	general check config
	---------------------
	checks
	  checkname             : string - unique id
	      module            : module name (load, cpu, url)
	      arg1              : specific to module
	      arg2              : specific to module  
	      (...)

	      [enable]          : timerange ; default yes  
	      [alert_max_level] : alert, warn, notice (scales down) ; overwrites global / module
	      [enable_pager]    : timerange ; default NO ; need global/pager to be enabled 
	      [alert_delay]     : delay before alert ; DEFAULT 120 
	      [frequency]       : min seconds between runs ; needs --cron in ARGS ; overrides module config


	specific check options
	----------------------
	load:
	  module : load

	cpu:
	  module : cpu

	swap:
	  module : swap

	memory:
	  module : memory

	boottime
	  module : boottime  

	mount:
	  module        : mount
	  path          : /path/to/mountpoint

	disk:
	  module        : disk
	  path          : /absolute/path
	  alert         : INT [percent before alert]

	process
	  module        : process
	  psname        : string  (system process name)

	url:
	  module            : url
	  url               : https://www.cavaliba.com/
	  [pattern]         : "Cavaliba" ; DEFAULT = ""
	  [allow_redirects] : yes ; default = no
	  [ssl_verify]      : yes ; default = no
	  [host]            : optionnal hostname header (Host: xxx)


	ping
	   module          : ping
	   host            : 192.168.0.1
	 

	folder
	  module            : folder
	  folder_name       : string, unique value
	  path              : /path/to/folder
	  recursive         : yes  ; default = no
	  ()[]filter: *.txt : TODO 
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


	certificate
	  module: certificate
	  hostname: hostname.com
	  port:                         # defaults to 443 if not specified
	  alert_in:   1 week            # DEFAULT 3 days ; format  X years Y months ... weeks, days, hours"
	  warning_in: 1 month           # DEFAULT 2 weeks
	  notice_in:  3 months          # DEFAULT 2 months



## Global Section
*new v1.0.0* : all entries in the global section must be under **global** yaml top entry.


### cmt_group

This field is sent as-is in every JSON message sent by CMT running the configuration.

It may be a customer name, an application name (to which this node belongs), etc.

	# conf.yml
	cmt_group: customer_XXX


### cmt_node

This field is sent as-is in every JSON message sent by CMT running the configuration.

It may be the name of the Server or Virtual Machine.

	# conf.yml
	cmt_group: node-05-france-grignan

### cmt_node_role
*new v1.0.0*
Optional.


### cmt_node_env
*new v1.0.0*
Optional.


### cmt_node_location
*new v1.0.0*
Optional.


###	metrology_servers

A list of one or more remote (or local) server which accept standardized GELF/Elastic/Graylog message over UDP or HTTP.

Every GELF server will receive all message sent by CMT.

GELF is basically JSON with a few mandatory fields.

GELF over UDP is the simpler and more efficient protocol. UDP has no coupling between the client (CMT) and the server (GRAYLOG/Logstash/Elastic). It's fire'n forget. GELF over UDP (here) has low/no security. Data in the clear ...

GELF over HTTP(s)/TCP introduces coupling between CMT and the remote server. A timeout/maxduration mechanism is used by CMT to limit its global execution time. HTTP can be  a TLS/SSL URL providing additional security (encryption, endpoint authentication)

See Graylog/GELF documentation for more information.

  graylog_test1:
      type: graylog_udp_gelf
      host: 10.10.10.13
      port: 12201
  graylog_test2:
      type: graylog_tcp_gelf
      url: http://10.10.10.13:8080/gelf

      [enable]                : timerange ; default = yes ; master switch
      ()secret_key


### Pager / Teams 

The Microsoft Teams tool uses channels, subscription and notification and  is well suited in the business field, to send and receive alerts and notification.

Each CMT agent can send alerts directly when certain conditions are met.

Two Teams channel must  be defined in the configuration : 
* one for the real Alerts  (Channel named *alert*)
* onf for test / heartbeat message (Channel named *test*)

The Teams URL must be provided for each Channel


	pagers:
	  alert              : mandatory entry 'alert'
	     type            : team_channel
	     url             : https://outlook.office.com/webhook/xx../IncomingWebhook/yyyy...
	     [enable]        : timerange ; DEFAULT = no ; master switch / no inheritance
	     ()secret_key    : 
	     ()add_tags
	         tag: value
	         tag: value
	  test               : mandatory 'test' entry for ARG --pagertest
	     type            : team_channel
	     url             : https://outlook.office.com/webhook/xx/IncomingWebhook/yyy...
	     [enable]        : timerange ; DEFAULT = no  test:
	     ()secret_key    : 
	     ()add_tags
	         tag: value
	         tag: value


A global pager rate limit is available in the ... global section. A master switch to disable immediately all Pager notification is also available in the global section.

## Modules

Available moules

	
	Modules:
	  - load
	  - cpu
	  - memory
	  - swap
	  - boottime
	  - disks
	  - urls
	  - mounts
	  - process
	  - pings
	  - folders


## Specific Checks configuration

See the various document (from the sidebar) for each check/module configuration.



## Example configuration conf.yml
	
	---
	# Cavaliba / cmt_monitor / conf.yml
	# V 1.0.0

	# Global Section
	# --------------

	global:
	  cmt_group: cavaliba
	  cmt_node: vmxupm
	  cmt_node_env: dev
	  cmt_node_role: dev_cmt
	  cmt_node_location: Ladig
	  enable: yes
	  enable_pager: yes
	  conf_url: http://localhost/cmt/conf/
	  pager_rate_limit: 3600
	  max_execution_time: 10
	  load_confd: yes
	  alert_max_level: alert
	  alert_delay: 90

	# Remote metrology servers
	# ------------------------
	# to store and present data, with alert/warning/notice infos

	metrology_servers:
	  graylog_test1:
	      type: graylog_udp_gelf
	      host: 10.10.10.13
	      port: 12201
	      enable: yes
	  graylog_test2:
	      type: graylog_http_gelf
	      url: http://10.10.10.13:8080/gelf
	      enable: yes

	# Pager services
	# --------------
	# to send live alerts to human

	pagers:
	  alert:
	    type: team_channel
	    url: https://outlook.office.com/webhook/xx../IncomingWebhook/yyyy...
	    enable: yes
	  test:
	    type: team_channel
	    url: https://outlook.office.com/webhook/xx../IncomingWebhook/yyyy...
	    enable: no
	     
	# List of enabled modules
	# -----------------------
	modules:

	  load:
	    enable: yes
	    alert_max_level: notice

	  cpu:
	    enable: yes

	  memory:
	    enable: yes

	  swap:
	    enable: yes

	  boottime:
	    enable: yes

	  ntp:
	    enable: yes

	  disk:
	    enable: yes

	  url:
	    enable: yes

	  mount:
	    enable: yes
	    alert_max_level: notice    

	  process:
	    enable: yes

	  ping:
	    enable: yes
	    alert_max_level: warn    

	  folder:
	    enable: yes
	    #alert_delay: 70
	    #alert_max_level: alert


	# List of checks to perform 
	# --------------------------

	checks:

	# load
	  my_load:
	    module: load
	    enable: yes
	    alert_max_level: alert

	# cpu
	  my_cpu:
	    module: cpu
	    enable: yes
	    alert_max_level: alert

	# memory
	  my_memory:
	    module: memory
	    enable: yes
	    alert_max_level: alert

	# boottime
	  boottime:
	    module: boottime
	    enable: yes
	    alert_max_level: alert

	# swap
	  my_swap:
	    module: swap
	    enable: yes
	    alert_max_level: alert

	# disk  
	  my_disk_root:
	    module: disk
	    path: /
	    alert: 80
	  my_disk_boot:
	    module: disk
	    path: /boot
	    alert: 90

	# url
	  main_website:
	    module: url
	    enabled: after 2020-01-01
	    url: https://www.cavaliba.com/
	    pattern: "Cavaliba"
	    allow_redirects: yes
	    ssl_verify: yes
	    #host: toto
	  www_non_existing_for_test:
	    module: url
	    enabled: after 2020-01-01
	    url: http://www.nonexisting/
	    #pattern: ""


	#mount
	  my_mount_root:
	    module: mount
	    path: /
	  my_mount_mnt:
	    module: mount
	    path: /mnt

	# process
	  redis:
	    module: process
	    psname: redis
	    enable_pager: no
	  apache:
	    module: process
	    psname: httpd
	  cron:
	    module: process
	    psname: cron
	  ssh:
	    module: process
	    psname: sshd
	  ntp:
	    module: process
	    psname: ntpd
	  mysql:
	    module: process
	    psname: mysqld
	  php-fpm:
	    module: process
	    psname: php-fpm
	    enable_pager: yes

	# ping
	  ping_vm1:
	    module: ping
	    host: 192.168.0.1
	  ping_locahost:
	    module: ping
	    host: localhost
	  ping_google:
	    module: ping
	    host: www.google.com
	  wwwtest:
	    module: ping
	    host: www.test.com    
	  badname:
	    module: ping
	    host: www.averybadnammme_indeed.com  
	    
	# folder
	  folder_mytmp:
	    module: folder
	    path: /tmp
	    alert_max_level: alert
	    #alert_delay: 30
	    target:
	       is_blabla:
	       #age_min: 1000
	       #age_max: 300
	       #files_min: 3
	       #files_max: 10
	       #size_min: 100000
	       #size_max: 10
	       has_files:
	            - secret.pdf
	            #- secret2.pdf
	  folder_number2:
	    module: folder
	    path: /missing


	# ---------------------------------------------------------
	# if set global,  conf.d/*.yml also included and merged
	# ---------------------------------------------------------



