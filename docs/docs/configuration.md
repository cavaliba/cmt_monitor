---
title: configuration
---

##  conf.yml

CMT uses one or more configuration files to know what kind of checks to perform, what threshold or alert conditions are defined, and to which remote server the collected data must be sent.

The YAML file `conf.yml` is the main configuration file for CMT.

By default, it is located in `/opt/cmt/conf.yml`


You can specify an alternate configuration file at run time (CLI or crontab) :

    $ cmt --conf /my/dir/cmt/conf.yml

This let you have different execution contexts for CMT on the same Server.


## conf.d/*.yml for additional configurations

Every yaml file in the conf.d/ folder next to the conf.yml is merged into the configuration at run time. This design helps manage a bigger configuration with devops / deployment tools like Ansible.

This feature can be enabled in the main configuration file (disabled by default) :

	global:
		load_confd: yes

When deploying a new component on a CMT monitored system which needs more monitoring (process, socket, path, response time, urls availabity, ...) just drop a file in the conf.d folder with additionnal checks to perform.

Each additional file must be a valid CMT yaml file.


## HTTP remote configuration

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



## conf.yml sections

The complete configuration for a CMT run has 5 sections :

1. global section (global)
2. metrology server section
3. pager servers section
4. checks sections with all individual checks parameters (module dependent)


## conf.yml : global section

	# ----------------------
	# Global
	# ----------------------

	global:

	  cmt_group: cavaliba  : group name, customer name, system name
	  cmt_node: dev_vm1    : node name (physical / virtual name / cmt instance)
	  [cmt_node_env]       : string: prod, dev, qa, test, form, preprod, qualif ...
	  [cmt_node_role]      : string ; appli_front_1, db_3
	  [cmt_node_location]  : string, geographical position
	  [enable]             : timerange ; DEFAULT = yes; master switch (no inheritance below)
	  [start_offset]       : int, seconds ; in cron mode, start is delayed by this or a calculated offset in seconds
	  [enable_pager]       : timerange ; DEFAULT = no ; master switch (no inheritance)
	  [business_hours]     : 08:30:00 17:30:00 (default) ; set min/max timerange for BH/HO and NBH/HNO hours
	  [conf_url]           : https://.../api/  (/group_node.txt if url ends by /txt/) + ?group=group&node=node
	  [max_execution_time] : seconds ; DEFAULT 55
	  [load_confd]         : yes/no ; DEFAULT no
    [http_proxy]         : http://[login[:pass]@proxyhost:port  ; use noenv value to skip os/env     
    [https_proxy]        : https://[login[:pass]]@proxyhost:port  ; default to http_proxy   
	  [alert_delay]        : seconds of repeated NOK check before trigering an alert  ; DEFAULT 120 ; each check can override the global value
    [tags]               : tag1 tag2[=value] ; list of tags ; no blank around optional "=value"


## conf.yml : metroloy servers

Metrology servers represent remote graylog/elasticsearch/influxdb systems where collected data must be sent.

See metrology pages for complete option description.

Supported type:

* graylog_udp_gelf
* graylog_tcp_gelf
* elastic_http_json
* influxdb


		# ----------------------
		# Metrology Servers
		# ----------------------

		metrology_servers:

	    mytarget:
	        type:          string
	        [enable:]      timerange, yes,no, 24/7, bh, nbh, range...
	        (...)          (specific options)

		  my_graylog_test1:
		      type: graylog_udp_gelf
		      (...)

		  my_graylog_test2:
		      type: graylog_tcp_gelf
		      (...)

		  # Elastic Stack
		  my_elastic_remote_http_server:
		      type: elastic_http_json
		      (...)

		  # influxdb V1 & V2
		  my_influxdb:
		      type: influxdb
		      (...)

See the metrology pages for additional informations.


### conf.yml : alerts and pagers

Pager services represent remote systems to which alerts are sent, when human immediate action ot attention is needed.

Supported type:

		* team_channel
		* teams (same as team)
		* pagerduty (experimental)

All events sent to metrology also have severity/alert fields which carry information about alerting.

In conf.yml: 

	# ----------------------
	# Pager services
	# ----------------------

	pagers:

	    my_pager1:
	       type                : team_channel, teams, pagerduty (experimental), smtp(to be done)
	       enable              : timerange

	    my_pager2:
	       type                : team_channel, teams, pagerduty (experimental), smtp(to be done)
	       enable              : timerange

      (...)


See the pager & alerts page for additional informations on alerts.


### conf.yml : checks to be performed

Checks are the individual monitoring operations. This is were all checks are defined.

Checks are grouped under `module` entries which defines the class of test to be performed.

Checks have options available to all checks, and options specific to the type of check (the module) being performed.

`checkname` must be unique accross all cmt configuration.


	# --------------------------
	# Checks
	# --------------------------
	
	modulename1:             : one from the various supported modules    
	
	  checkname1:            : free string - unique id in the module scope - aoid dot/special chars in name

        [enable]           : timerange ; default yes  ; yes, no, before, after, hrange, ho, hno, 24/7, ...
	      [enable_pager]     : timerange ; default no ; need global/pager to be enabled ; sent if alert found
	      [alert_delay]      : min. seconds before alert  ; DEFAULT 120  ; higher precedence
	      [frequency]        : min seconds between runs ; needs --cron in ARGS ; overrides module config
        [root_required]    : [yes|no(default)] -  new 1.4.0 - is root privilege manadatory for this check ?
        [tags]             : tag1 tag2[=value] ... ; list of tags ; no blank around optional "=value"
        [severity_max]     : critical, error, warning, notice, none  (default : critical)
	      arg1               : specific to module (see doc for each module)
	      arg2               : specific to module  
	      (...)

      checkname2:
          ...


## Option details

### enable: [timerange option]

Scope: global, metrology, pager, check

It defines if :

* CMT must run globally  (global section, default = yes)
* if a module is enabled (default = yes)
* if a metrology server should reveive data (default = yes)
* if a pager should receive notifications (default = no)
* if a single check should be performed (default = yes)

See `timerange option` for possible values.



### enable_pager: [timerange option]

Scope: global, pager, check

Values : timerange field

Default : no

For an alert to be sent to a pager, this option must be explicity active at *ALL* levels:

* global section
* pager section (name: enable)
* at individual checks requiring a pager notification.


### alert_delay : seconds

Scope: global, module, check

This option helps implement an hysteresis mechanism to remove transient events 
which shouldn't be reported as alerts nor sent as notification to pagers.

It defines a mimimal duration during which an alert confidtion must be present, before firing a real alert.

Before that delay, an alert is sent as a warning.


### severity_max

Scope: check

Values: critical (default), error, warning, none

Defines the maximum  level of severity of a raw check to be further processed (deduplication, hysteresis, rate_limit of alerts).

* critical : for production and immediate failure of a critical component.
* error : for production and immediate failure of a non-critical compoent, or failure of non-production items
* warning : a failure will soon happen
* notice : attention needed, no failure soon


### load_confd : yes/no

Scope: global

Default: no

It defines if a conf.d/ folder must be scanned and .yml files merged to current configuration.



### conf_url

Scope: global


Remote URL from which additional configuration may be fetched, persisted locally, and merged at each run.

If it ends by `/txt/`, CMT appends a `/group_node.txt` value. Use case : static remote server with a text file for 

In other case, CMT appends `?group=group&node=node` to pass parameters to an API.

Remote configuration is designed to implement muting for alerts/pagers/metrology on various condition, without the need for editing local configuration files.



### max_execution_time : seconds

Scope: global

Default : 55 seconds

when run from crontab, the CMT process kills itself after this amount of time. A monitoring tool should no disturb its host. We are not quantical (yet).



### timerange field values

`timerage` fields can take more values than the basic yes/no:

		# -------------------------------------
		# timerange fields (from documentation)
		# -------------------------------------
		# yes, 24/7                    : always
		# no                           : never
		# after YYYY-MM-DD hh:mm:ss    : after time of the day
		# before YYYY-MM-DD hh:mm:ss   : before ... 
		# hrange hh:mm:ss hh:mm:ss     : time intervall
		# ho, bh, business_hours       : 8h30/18h mon>fri - see global configuration for custom time
		# nbh,hno, non_business_hours  : !(8h30/18h mon>fri)


use global configuration item (business_hours) to set different default values


### root_required

Scope: check

Values : yes, no 

Default : no

Some checks require root permissions to be run. E.g. : count files inside protected folders.



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

Optional



### cmt_node_env
*new v1.0.0*

Optional


### cmt_node_location
*new v1.0.0*

Optional


### tags
*new v1.5*

Scope: global, check

Values : line of tag names, blankspace separated, with optional =value for each tag

Default : none

Add a list of tags fields (think labels or key/value pairs) in the data sent to metrology servers. Tags can be declared in the global section or in each individual checks. Do not add blank around `=`. Tags from global and check section are merged.

Example:
    
    global:
       tags: tag1 production mydate=2021/03 size=4 foldertype=test 

will add the following info to outuput:

    cmt_tag_tag1: 1
    cmt_tag_production: 1
    cmt_tag_mydate: '2021/03'
    cmt_tag_size: 4
    cmt_tag_foldertype: 'test'




## Modules

Available moules

	
	Modules:
	  - load
	  - cpu
	  - memory
	  - swap
	  - boottime
	  - disk
	  - url
	  - mounts
	  - process
	  - ping
	  - folder
	  - certificate
	  - socket
	  - send
	  - sendfile
	  - mysql
	  - mysqldata



## Specific Checks configuration

See the various document (from the sidebar) for each check/module configuration.



## Example configuration conf.yml
	
See the page [config_example.md](configuration_example) for a complete configuration.


