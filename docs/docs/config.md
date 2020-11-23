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

The complete configuration for a CMT run has 3 sections :

1. a global configuration section
2. a list of checks that are enabled
3. specific parameters for each item to be monitored (check dependent)


## Global configuration

	cmt_group: cmtdev
	cmt_node: vmpio

	# GELF/Elastic servers for data reports
    # -------------------------------------	
	graylog_udp_gelf_servers:
	  - name: graylog_test
	    host: 10.10.10.13
	    port: 12201

	graylog_http_gelf_servers:
	  - name: graylog_test
	    url: http://10.10.10.13:8080/gelf

	# Teams channels for alerts
	# ---------------------------

	teams_channel:
	   - name: alert
	     url: https://outlook.office.com/webhook/xxxx(...)xxxx/IncomingWebhook/yyyy(...)
	   - name: test
	     url: https://outlook.office.com/webhook/xxxx(...)xxx/IncomingWebhook/yyyy(...)yyy

	# Rate limit message to Teams to max one every XX seconds
	teams_rate_limit: 3600


### cmt_group

This field is sent as-is in every JSON message sent by CMT running the configuration.

It may be a customer name, an application name (to which this node belongs), etc.

	# conf.yml
	cmt_group: customer_XXX


### cmt_node

This field is sent as-is in every JSON message sent by CMT running the configuration.

It may be the name of the Server or Virtual Machine.

	# conf.yml
	cmt_group: node-05-france-lyon


###	graylog_udp_gelf_servers

A list of one or more remote (or local) server which accept standardized GELF UDP message. 

Every GELF server will receive all message sent by CMT.

GELF is basically JSON with a few mandatory fields.

GELF over UDP (here) has low/no security. Data in the clear ...

This is the simpler and more efficient protocol. UDP has no coupling between the client (CMT) and the server (GRAYLOG/Logstash/Elastic). It's fire'n forget.

See Graylog/GELF documentation for more information.

	# conf.yml
	graylog_udp_gelf_servers:
	  - name: graylog_test
	    host: 10.10.10.13
	    port: 12201
	  - name: graylog_test2
	    host: 10.10.10.14
	    port: 12201
	    (...)


###	graylog_tcp_gelf_servers

A list of one or more remote (or local) server which accept standardized GELF message over HTTP/HTTPS protocol.

This configuration is useful when only HTTP(s) protocol is available accross network boundaries. You can enable TLS (https) to improve confidentiality.

Note that HTTP/TCP introduces coupling between CMT and the remote server. A timeout/maxduration mechanism is used by CMT to limit its global execution time.

See Graylog/GELF documentation for more information.

	# conf.yml
	graylog_http_gelf_servers:
	  - name: graylog_test
	    url: http://10.10.10.13:8080/gelf
	  - name: graylog_test2
	    url: http://10.10.10.14:8080/gelf
	    (...)  

### Teams channel configuration

The Microsoft Teams tool uses channels, subscription and notification and  is well suited in the business field, to send and receive alerts and notification.

Each CMT agent can send alerts directly when certain conditions are met.

Two Teams channel may be defined in the configuration : 
* one for the real Alerts
* onf for test / heartbeat message.

The Teams URL must be provided for each Channel


	# conf.yml
	teams_channel:
	   - name: alert
	     url: https://outlook.office.com/webhook/xxx(...) xxx/IncomingWebhook/yyyy(...)yyy
	   - name: test
	     url: https://outlook.office.com/webhook/xxx(...) xxx/IncomingWebhook/yyyy(...)yyy

### Teams rate limit

A simple rate-limit for Teams message is implemented in CMT.

The `teams_rate_limit`configuration defines the minimal number of seconds between any two alerts sent to Teams.

	# conf.yml
	teams_rate_limit: 3600

## Checks enabled

The second section of the configuration enables the desired checks :

	# conf.yml
	checks:
	  - load
	  - cpu
	  - memory
	  - swap
	  - boottime
	  - ntp
	  - disks
	  - urls
	  - mounts
	  - process
	  - pings
	  - folders


## Specific Checks configuration

See the various document (from the sidebar) for each check/module configuration.



## Example configuration


	/dev/cmt_monitor$ more conf.yml
	
	---
	# Cavaliba / cmt_monitor / conf.yml

	# -----------------------------
	# Global
	# -----------------------------

	cmt_group: cmtdev
	cmt_node: vmpio

	# -----------------------------
	# GELF servers for data reports
	# -----------------------------

	graylog_udp_gelf_servers:
	  - name: graylog_test
	    host: 10.10.10.13
	    port: 12201

	graylog_http_gelf_servers:
	  - name: graylog_test
	    url: http://10.10.10.13:8080/gelf

	# ---------------------------
	# Teams channels for alerts
	# ---------------------------

	teams_channel:
	   - name: alert
	     url: https://outlook.office.com/webhook/xxxxxxx/IncomingWebhook/yyyyyyy
	   - name: test
	     url: https://outlook.office.com/webhook/xxxxx/IncomingWebhook/yyyyyyy

	# Rate limit message to Teams to max one every XX seconds
	teams_rate_limit: 3600

	# ------------------------
	# Available checks
	# ------------------------

	checks:
	  - load
	  - cpu
	  - memory
	  - swap
	  - boottime
	  - ntp
	  - disks
	  - urls
	  - mounts
	  - process
	  - pings
	  - folders

	# ----------------------------
	# Parameters for checks
	# ----------------------------

	disks:
	  - path: /
	    alert: 94


	urls:
	  - url: https://www.cavaliba.com/
	    name: www.cavaliba.com
	    pattern: "Cavaliba"
	    allow_redirects: yes
	    ssl_verify: yes
	  - url: http://demo.cavaliba.com/
	    name: demo.cavaliba.com
	    pattern: "SIRENE"


	mounts:
	  - /
	  - /boot


	process:
	  - name: redis
	    psname: redis
	  - name: apache
	    psname: httpd
	  - name: cron
	    psname: cron
	  - name: sshd
	    psname: sshd
	  - name: ntpd
	    psname: ntpd
	  - name: mysqld
	    psname: mysqld
	  - name: php-fpm
	    psname: php-fpm


	pings:
	  - 192.168.0.1
	  - localhost
	  - 127.0.0.1
	  - www.cavaliba.com


	folders:
	  - path: /tmp
	    name: mytmp
	    target:
	       age_min: 1000
	       age_max: 300
	       files_min: 3
	       files_max: 10
	       size_min: 100000
	       size_max: 10
	       has_files:
	            - aaa
	            - bbb
	  - path: /tmp/absent
	    name: numbertwo
	  - path: /tmp/empty
	    name: number3

	# ------------------------------------
	# conf.d/*.yml also included with :
	# - main conf has higher priority
	# - first level lists merged
	# ------------------------------------
