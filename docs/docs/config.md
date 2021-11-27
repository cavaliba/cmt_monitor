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


In the following lines : 

	[ ] is optional, available
	( ) is on the roadmap



### conf.yml : global section

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
	  [enable_pager]       : timerange ; DEFAULT = no ; master switch (no inheritance)
	  [business_hours]     : 08:30:00 17:30:00 (default) ; set min/max timerange for BH/HO and NBH/HNO hours
	  [pager_rate_limit]   : seconds ; default 7200
	  [conf_url]           : https://.../api/  (/group_node.txt if url ends by /txt/) + ?group=group&node=node
	  [max_execution_time] : seconds ; DEFAULT 55
	  [load_confd]         : yes/no ; DEFAULT no
    [http_proxy]         : http://[login[:pass]@proxyhost:port  ; use noenv value to skip os/env     
    [https_proxy]        : https://[login[:pass]]@proxyhost:port  ; default to http_proxy   
	  [alert_max_level]    : alert, warn, notice, none  ; levels are shifted to respect this limit.
	  [alert_delay]        : min. seconds before alert  ; DEFAULT 120  ; lower precedence
    [tags]               : tag1 tag2[=value] ; list of tags ; no blank around optional "=value"

### conf.yml : metroloy servers

Metrology servers represent remote graylog/elasticsearch systems where collected data must be sent.

See metrology pages for complete option description.

	# ----------------------
	# Metrology Servers
	# ----------------------

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

	  # Elastic Stack
	  my_elastic_remote_http_server:
	          type: elastic_http_json
	          url: http://my_remote_host:9200/cmt/data/?pipeline=timestamp
	          enable: yes

	  # influxdb V1 & V2
	  my_influxdb:
	      type: influxdb
	      url: http://10.10.10.13:8086/write?db=cmt
	      # msec, sec, nsec ; anything else, no timestamp
	      time_format: msec
	      batch: yes
	      send_tags: yes
	      token: toto
	      #username: cmt
	      #password : cmt
	      enable: yes


### conf.yml : pager services

Pager services represent remote systmes to which alerts or notifications are sent, when human immediate action is needed.

In `managed mode`, CMT handles delay and rate-limit before firing an alert.

In `allnotifications`, CMT sends all alerts/warn/notice to remote Pagers which will be in charge of deduplication, rate-limit and proper human notification. 

Use wisely, syadmin sleep is precious !


	# ----------------------
	# Pager services
	# ----------------------

	pagers:

	  general_pagername:         
	    type                : team_channel, teams, pagerduty, smtp (to be done)
	    mode                : managed(default), allnotifications
	    url                 : Teams channel URL
	    [enable]            : timerange ; DEFAULT = yes ; master switch / no inheritance
	    [http_proxy]        : http://[login[:pass]@proxyhost:port  ; use noenv value to skip os/env     
	    [https_proxy]       : https://[login[:pass]]@proxyhost:port  ; default to http_proxy   
	    [http_code: 200]    : http_code for success
	    [ssl_verify: yes]   : default: no

	  myteams_ops:     
	     type            : teams
	     url             : https://client.webhook.office.com/webhookb2/XXXXXXX
	     [enable]        : timerange ; DEFAULT = no 

	  # new V2.0
	  pagerduty_dev:
	    enable: yes
	    type: pagerduty
	    mode: managed
	    url: https://events.pagerduty.com/v2/enqueue
	    key: xxxxxxxxxxx


### conf.yml : checks to be performed

Checks are the individual monitoring operations. Thinks as instance of modules. This is were all checks are defined.

Checks have options available to all checks, and options specific to the type of check (the module) being performed.

`checkname` must be unique accross all cmt configuration.


	# --------------------------
	# Checks
	# --------------------------
	
	modulename:                  
	
	  checkname1:            : free string - unique id in the module scope - aoid dot/special chars in name

        [enable]           : timerange ; default yes ; yes, no, before, after, hrange, ho, hno
	      [enable_pager]     : timerange ; default NO ; need global/pager to be enabled ; sent if alert found
	      [alert_delay]      : min. seconds before alert  ; DEFAULT 120  ; higher precedence
	      [frequency]        : min seconds between runs ; needs --cron in ARGS ; overrides module config
        [root_required]    : [yes|no(default)] -  new 1.4.0 - is root privilege manadatory for this check ?
        [tags]             : tag1 tag2[=value] ... ; list of tags ; no blank around optional "=value"

	      [alert_max_level]  : alert, warn, notice, none (scale down)  ; overwrites global & module entry
        [severity_max]     : critical, error, warning, notice, none  (default : critical)

	      arg1               : specific to module (see doc for each module)
	      arg2               : specific to module  
	      (...)

      checkname2:

          ...



## Option details



### enable: [timerange option]

Scope: global, metrology, pager, module, check

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

For an alert to be sent to a pager, this option must be set at *ALL* levels:

* global section
* pager section (name: enable)
* at individual checks requiring a pager notification.




### pager_rate_limit : seconds

Scope: global

Default : 7200 seconds

Pager notifications won't be sent more frequently than `pager_rate_limit` seconds by this CMT instance.





### alert_delay : seconds

Scope: global, module, check

This option helps implement an hysteresis mechanism to remove transient events 
which shouldn't be reported as alerts nor sent as notification to pagers.

It defines a mimimal duration during which an alert confidtion must be present, before firing a real alert.

Before that delay, an alert is sent as a warning.




### alert_max_level

Scope:  global, module, check ; lower wins.

Values: alert(default), warn, notice, none


It defines the maximum alert informations detected by a module run, that will be reported to the metrology servers. 

When set to alert (default), alert conditions are sent as alert, when collected from the modules.

When set to warn, one shift is performed : alerts become warn, warn becom notice, notice are discarded (data is sent, but fields describing alerts, warnings, notice, notifications are set to 0).

When set to warn, two shifts are performed : alerts become notice, the rest is discarded.

When set to none, all level are discarded, no values are reported to metrolgoy servers.

**soon to be deprecated**


### severity_max

Scope: check

Values: critical (default), error, warning, none

Will replace alert_max_level. Defines the maximum  level of severity of a raw check to be further processed (deduplication, hysteresis, rate_limit of alerts).

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

	--------------------------------
	timerange field
	--------------------------------
	- yes
	- no
	- after YYYY-MM-DD hh:mm:ss
	- before YYYY-MM-DD hh:mm:ss
	- hrange hh:mm:ss hh:mm:ss
	- bh or ho  -  (8h30/17h30 mon>fri) : business hours
	- nbh or hno - (! (8h30/17h30 mon>fri)) : non-business hours

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


##	metrology_servers

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


ElasticSearch

  elastic_test:
      type: elastic_http_json
      url: http://10.10.10.51:9200/cmt/data/?pipeline=timestamp
      ssl_verify: yes
      enable: yes

InfluxDB 

  # CMT V1.7+ ; compatible with influxdb V1 & V2

  influxdb_test:
      type: influxdb
      # V1
      url: http://10.10.10.13:8086/write?db=cmt
      # V2
      # url: 
      # msec, sec, nsec ; anything else, no timestamp
      time_format: msec
      batch: yes
      send_tags: yes
      token: toto
      #username: cmt
      #password : cmt
      ssl_verify: yes
      enable: yes


## Pager / Teams 

The Microsoft Teams tool uses channels, subscription and notification and  is well suited in the business field, to send and receive alerts and notification.

Each CMT agent can send alerts directly when certain conditions are met.

Two Teams channel must  be defined in the configuration : 
* one for the real Alerts  (Channel named *alert*)
* onf for test / heartbeat message (Channel named *test*)

The Teams URL must be provided for each Channel

  myteams:
    type: teams 
    mode: managed
    url: https://outlook.office.com/webhook/xxxxx/IncomingWebhook/yyyyyyyyyyyyyyy
    enable: yes

## Pager Pagerduty (experimental)

  mypagerduty:
    type: pagerduty
    mode: allnotifications
    url: https://events.pagerduty.com/v2/enqueue
    key: XXXXXXXXXXXXXXXXXXXXXXXx
    enable: yes


A global pager rate limit is available in the ... global section. A master switch to disable immediately all Pager notification is also available in the global section.

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


