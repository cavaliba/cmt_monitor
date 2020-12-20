---
title: configuration
---

##  conf.yml

CMT uses one or more configuration files to know what kind of checks to perform, what threshold or alert conditions are defined, and to which remote server the collected data must be sent.

The YAML file `conf.yml` is the standard configuration file for CMT.

By default, it is located in /opt/cmt/conf.yml or next to `cmy.py` program.


## --conf myconf.yml  option

you can specify an alternate configuration file :

    $ cmt --conf /my/dir/cmt/conf.yml

This let you have different execution contexts of CMT on the same Server.

## Folder conf.d/

Every taml file in the conf.d/ folder next to the conf.yml is merged into the configuration at run time. This design helps manage a bigger configuration with devops / deployment tools like Ansible.

This feature can be disabled in the main configuration file :

	global:
		load_confd: yes

When deploying a new component on a CMT monitored system which needs more monitoring (process, socket, path, response time, urls availabity, ...) just drop a file in the conf.d folder with additionnal checks to perform.

Each additional file must be a valid CMT yaml file.


## remote configuration
*new 1.2.1*

CMT can fetch a remote configuration file according to the global configuration :

	global:
  		conf_url: http://localhost/txt/
  		conf_url: http://localhost/api/

This remote configuration - if found - is merged in the main yaml file(and conf.d/*). This feature lets you use a central repository for additional configurations to enable/disable/suspend checks centrally, etc.

If the conf_url ends with `/txt/`, CMT will append a /group_node.txt to the rquested URL. You can thus manage configuration remotely with simple text files on any static web server.

Any other conf_url value will be queried as specified. It can be a specific file or any API endpoint.

CMT will always append a `?group=group&node=node` string to conf_url to inform a remote API about the requesting node.

Remote configuration is persisted locally in case of no-response from remote server. Persistance last for one day at most of no reply. After that period, cached remote conf is discarded.

## Folder structure

	/opt/cmt/$ tree -L 1
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
5. checks sections with all  individual checks parameters (module dependent)


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

	  [enable]             : timerange ; DEFAULT = yes; master switch (no inheritance below)
	  [enable_pager]       : timerange ; DEFAULT = no ; master switch (no inheritance)
	  [pager_rate_limit]   : seconds ; default 7200
	  [conf_url]           : https://.../api/  (/group_node.txt if url ends by /txt/) + ?group=group&node=node
	  [max_execution_time] : seconds ; DEFAULT 55
	  [load_confd]         : yes/no ; DEFAULT no
	  [alert_max_level]    : alert, warn, notice  ; levels are shifted to respect this limit.
	  [alert_delay]        : delay before transition to alert (if alert) ; seconds/DEFAULT 120 


	----------------------
	Metrology Servers
	----------------------

	metrology_servers:

	  graylog_test1:
	      type: graylog_udp_gelf
	      host: 10.10.10.13
	      port: 12201
	      [enable]                : timerange ; default = yes ; master switch      

	  graylog_test2:
	      type: graylog_tcp_gelf
	      url: http://10.10.10.13:8080/gelf
	      [enable]                : timerange ; default = yes ; master switch      

	----------------------
	Pager services
	----------------------

	pagers:
	  alert              : mandatory entry 'alert'
	     type            : team_channel
	     url             : Teams channel URL
	     [enable]        : timerange ; DEFAULT = no ; master switch / no inheritance

	  test               : mandatory 'test' entry for ARG --pagertest
	     type            : team_channel
	     url             :   
	     [enable]        : timerange ; DEFAULT = no 


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
	
	module                  : module name

	  checkname             : string - unique id in the module scope

          [enable]          : timerange ; default yes ; yes, no, before, after, hrange, ho, hno
	      [alert_max_level] : alert, warn, notice (scale down)  ; overwrites global & module entry
	      [enable_pager]    : timerange ; default NO ; need global/pager to be enabled ; sent if alert found
	      [alert_delay]     : delay before transition from normal to alert (if alert) ; seconds  ; DEFAULT 120 
	      [frequency]       : min seconds between runs ; needs --cron in ARGS ; overrides module config

	      arg1              : specific to module (see doc for each module)
	      arg2              : specific to module  
	      (...)


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
	  - certificate
	  - socket


## Specific Checks configuration

See the various document (from the sidebar) for each check/module configuration.



## Example configuration conf.yml
	
	---
	# Cavaliba / cmt_monitor / conf.yml

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

	load:

	  my_load:
	    enable: yes
	    alert_max_level: alert

	cpu

	  my_cpu:
	    enable: yes
	    alert_max_level: alert

	memory

	  my_memory:
	    enable: yes
	    alert_max_level: alert

	boottime

	  my_boottime:
	    enable: yes
	    alert_max_level: alert

	swap

	  my_swap:
	    enable: yes
	    alert_max_level: alert

	disk  

	  my_disk_root:
	    path: /
	    alert: 80
	  my_disk_boot:
	    path: /boot
	    alert: 90

	url

	  main_website:
	    enabled: after 2020-01-01
	    url: https://www.cavaliba.com/
	    pattern: "Cavaliba"
	    allow_redirects: yes
	    ssl_verify: yes
	    #host: toto
	  www_non_existing_for_test:
	    enabled: after 2020-01-01
	    url: http://www.nonexisting/
	    #pattern: ""


	mount

	  my_mount_root:
	    path: /
	  my_mount_mnt:
	    path: /mnt

	process

	  redis:
	    psname: redis
	    enable_pager: no
	  apache:
	    psname: httpd
	  cron:
	    psname: cron
	  ssh:
	    psname: sshd
	  ntp:
	    psname: ntpd
	  mysql:
	    psname: mysqld
	  php-fpm:
	    psname: php-fpm
	    enable_pager: yes

	ping

	  ping_vm1:
	    host: 192.168.0.1
	  ping_locahost:
	    host: localhost
	  ping_google:
	    host: www.google.com
	  wwwtest:
	    host: www.test.com    
	  badname:
	    host: www.averybadnammme_indeed.com  
	    
	folder

	  folder_mytmp:
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
	    path: /missing


	certificate:

	  cert_google:
	    hostname: google.com
	    port: 443
	    alert_in: 1 week 
	    warning_in: 3 months
	    notice_in: 6 months

	  duck:
	    hostname: duckduckgo.com
	    alert_in: 1 week

	  broken:
	    hostname: duckduckgo.com
	    port: 80
	    alert_in: 2 week

	  yahoo:
	    hostname: yahoo.com
	    port: 443
	    alert_in: 2 week

	socket:

	  redis:
	    socket: local tcp 6379
	    #socket: local tcp port | remote tcp host port
	    connect: yes
	    #send: 
	    #pattern:

	  www_google:
	    socket: remote www.google.com tcp 443
	    connect: yes
	    #send: 
	    #pattern:


	# ---------------------------------------------------------
	# if set global,  conf.d/*.yml also included and merged
	# ---------------------------------------------------------



## Alternate / deprecated checks structure

You can specficy individual checks in the following (deprecated) format:

    checks:
         my_checkname:
             module: module_name
             arg1: value1
             arg2: value2 
             (...)