---
title: Home
---

# Welcome to CMT Documentation


## Overwiew - CMT is a simple monitoring agent

CMT is a small footprint python3 or binary agent thus available for many standard OS. Once deployed on a system, it collects various data and monitors local/remote services. 

## Send to ElasticSearch/Graylog
The collected data are sent to (any) ElasticSearch/Graylog data stores. These data points may carry alert information or warning levels for central alerting or display (Kibana for example).

## Alerts and Pager to Teams
If various conditions are met (or not met), CMT can also send direct alerts / pagers notifications to Teams channel.

## Use as CLI
You can also use CMT as command line tool on each server during various sysadmin or software configuration tasks.

## Data model / ElasticStack data storage
CMT provides a structured data model to improve metrology storage and organization of many monitoring data. You can then build efficent dashborad or data analysis and correlation for reporting, finer alerting, etc.

## Modular
Ultimately, due to its modular design, it is very easy to add new checks, thus enabling a single tool to cover technical and functionnal monitoring and alerting needs.

## Command and shortcuts

* `cmt --help`
* (...)


## Deployment layout

    /opt/cmt_monitor    # Home dir
        cmt             # cmt binary agent
        cmt.py          # or python3 version
        checks/*.py     # and all modular checks
        conf.yml        # configuration what to measure / where to send
        conf.d/         # additional configuration (eg. ansible additive deployment)


## Why another monitoring tool ?

The initial requirements were :

* clean metric data structure (multi-tenant, multi-customers, multi nodes)
* data is sent to very standard ElasticSearch DataStore, private or in the cloud
* modular design for easy extension / additional cehcks
* small footprint agent, easy to deploy (drop anywhere ...)
* simple configuration file (one for all)
* minimal learning curve
* covers technical metrics but also functionnal, url, app response, middleware status, ...
* ansible aware for mass deployement and standization
* usable as CLI directly on each system
* open source and hopefully well documented enough

None of the reviewed tools covered this exact set of requirements, some being too specific on some kind of metrics, others requiring a steep learning curve (eg. to extend), other used specific datastore and needed very specific protocol to be allowed (network/firewalls) between agents and datastore ...


