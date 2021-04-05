---
title: Home
---

# Welcome to CMT Documentation

*Current release : 1.6 - 2021/04/04*

## Overwiew - CMT is a simple monitoring agent

CMT is a small footprint agent, with a single file configuration, available for most standard Linux OS. Once deployed on a system, it collects various data and monitors local/remote services. 

## Send to ElasticSearch/Graylog

Collected data is sent to Metrology servers like ElasticSearch/Graylog. These data points may carry alert information or warning levels for central alerting or display (Kibana for example).

## Alerts and Pager to Teams

If various conditions are met (or not met), CMT can also send direct alerts / pagers notifications to Teams channel.

## Use as CLI

For sysadmin, CMT can be used as command line tool on each server during various sysadmin or software configuration tasks. One single run provides an immediate health check of all the configured check items.

## Data model / ElasticStack data storage

CMT provides a clean and well organized  data model to enable an efficient metrology storage and further processing of collected data. You can then build various dashborad for data analysis and correlation,  for reporting, finer alerting, etc.


## Deploy easily

CMT is provided as a standalone binary for most recent linux distributions. Download and get running. Optionnaly yon can download and run directly the python3 code with a few mandatory librairies (yaml, requests, psutils, ...)

## Modular

Ultimately, due to its simple configuration and modular design, it is very easy to add new checks or new modules, thus enabling a single tool to cover technical and functionnal monitoring and alerting needs.

## Command and shortcuts

* `cmt --help`
* (...)

## CMT remote management

CMT optionally supports additional configuration items from a remote URL, downloaded at runtime. It enables various modification from a central server (enable or disable some modules and check, require additional checks, ...). 

No assumption is made on the remote server providing additional configuration. It can be as simple as text files from a shared Web server. It can also be an API to your existing systems which have to respond for a given CMT node, 
with a slice of configuration to be merged in the node's local configuration.


## Modules and Checks

Think of module has class of check for a specific family of items,  like URL, folder, process, disk... Modules are internally implemented as small  python file in the checks/ folder.

Checks are instance of module execution. Each check create one metrology message or event. A check can carry several datapoint (checkitems). Each checks carries optionnal alert,warning, notice information and a message formatted for human reading.

Each Check depending on his Module capacbilities can set information such as alert, warning, notice that will be sent back to metrology servers and possibly direct Pagers services.

Pager notifications are sent only once per CMT exectuion at most. It is intended for (very) standalone usage of CMT, 
whereas advanced usage with many nodes will benefit from Pager notification fired from central systms where
decisions can be made from many/all monitoring sources.

CMT provides various configuration to ease configuring alert levels, frequency, rate-limit, max level,  threshold, and other **stop switches** to garantee a clean thread of monitoring data to Metrology servers and Pagers.


## CMT automated run from crontab

CMT is intended to run from crontab, every minute. It has a built-in max-duration security to prevent unfinished 
executing to overcrowd a server.

## Deployment layout

    /usr/local/bin/cmt  # binary standalone

    /opt/cmt            # Home dir
        cmt             # cmt binary agent if prefered over /usr/local/bin
        cmt*.py         # python3 version
        checks/*.py     # modular checks
        conf.yml        # configuration what to measure / where to send
        conf.d/         # additional configuration (eg. ansible additive deployment)
        persist.json    # optional data persistance across run

## Why another monitoring tool ?

The initial requirements were :

* small footprint agent, easy to deploy (drop anywhere ...)
* clean metric data structure (multi-tenant, multi-customers, multi nodes)
* simple configuration file (one for all)
* data agnostic: technical, business, ...
* push rather than pull : push data to metrology servers
* data is sent to very standard ElasticSearch DataStore, private or in the cloud
* modular design for easy extension / additional checks or modules
* minimal learning curve : drop the binary, edit the conf, run as cron/CLI, send to Elasticsearch, create Dashboard.
* ansible aware for mass deployement and standardization
* usable as CLI directly on each system
* open source and hopefully well documented enough

None of the reviewed tools covered this exact set of requirements, some being too specific on technical metrics, others requiring a steep learning curve (eg. to extend), other used specific datastore and needed very specific protocol to be allowed (network/firewalls) between agents and datastore ...


## Enjoy

CMT is free to use, free to extend. Experiment, Adopt, Enjoy, Contribute.

