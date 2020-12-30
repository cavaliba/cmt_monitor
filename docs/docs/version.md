---
title: version
---

# Releases

## 1.3.0alpha - latest

   cmt_check : private name of the check (not module name anymore)
   

## 1.2.1 - 2020/12/20

    bug fixe cmt.PAGER TIMEOUT
    Persist remote conf
    remoteconf type (/txt/group_node.txt vs api )

## 1.2.0 - 2020/12/13

    aleternate conf format : 'module' top entries with checks below
    refactor to cmt_helper.py


## 1.1.1 - 2020/12/09 

    bug fixe - parse error if empty remote conf
    build binary for debian 8 64bits

## 1.1.0 - 2020/12/06

    x module_certificate
    x module_folder :bug in dir count ; option no_store ; handle single_file
    x ARG : --cron
    x nicer output (summary, humanize)
    x CONF : frequency (--cron) for module and checks
    x module socket


## 1.0.0 - 2020/11/29

    x conf : conf.d on/off : global load_confd yes/no
    x remote conf : send group.node as parameters (or as file.txt )  
    x ARG : --debug2
    x ARG : --no-pager-rate-limit
    x ARG : --persist
    x give persist to modules
    x default homedir = /opt/cmt
    x conf: enable_pager for check
    x Pager events contain all alert/warn/notice messages
    x hysteresis up (alert_delay in global/module/check)
    x cmt_node_env [prod,form, pre,qual, test, dev]
    x cmt_node_role: string
    x cmt_node_location
    x Pattern optionnal in module URL
    x removed module_*_status checkItems (not needed any more ; use alert/warning/notice)
    x module url : add "host" option (virtualhost header)

## 1.0.0.RC

    x new alert/warn/notice ; simplified ChecKItems
    x class Persist()
    x Secu : injection de config/parametres dans appels shell ; subprocess
    x max execution time in conf
    x remote conf : http://host/conf/..../  (+group_node.txt if trailing /) 
    x level alert/warn/notice by framework


## 1.0.0.beta

    x  major redesign - new config with dict ; no uuid ; single MAP

## 1.0.0.alpha - Breaking changes

    x new modules structure in config ; checks deprecated
    x timerange + enable option in global/modules/check
    x ARG : --devmode
    x conf: global send_to_pager (timerange, default = no)
    x conf: teams channel : enable 
    x global : field: cmt_message ; compact status
    x cli: compact display ; status only ;   ARG : compact display option (--status)
    x uuid/id in conf and events ; uuid = group.node.module.id ; id = check specific value
    x check objet given to (not created by) each Chech module
    x config merge more clever !
    x conf_url option : remote config to be fetched and  merged into main/additional configs



## old

## 0.9
    x (0.9) bug : binary version find local conf.yml
    x (0.9) feature : recursive folder check option (recursive: yes/no)
    x (0.9) Documentation MkDocs (framzwork)
    x => 2020-10-25 - PUSH GITHUB v0.9

## 0.8
    x (0.8) refactor : split checks in separate files (2020/10/20)

## 0.7

    x (0.7) accept missing check entries in configuration (urls, disks, ...) : MODULE_LIST
    x (0.7) checks : folders
    x test pyinstaller (0.7 : 10 MB)

## 0.6

    x (0.6) abort if missing config file
    x (0.6) abort if missing item 'checks' in config file
    x (0.6) accept missing conf.d
    x (0.6) accept missing graylog_servers_* entries in config
    x (0.6) timeout when sending http/gelf to graylog + suspended if previous errors
    x (0.6) timeout when sending to Teams
    x (0.6) conf option : --conf filename

## 0.5

    x (0.5) check_url : requests : verify = False, allow_redirects = False
    x (0.5) check_url : requests : requests.packages.urllib3.disable_warnings()
    x (0.5) check_url : with response time  cmt_url_msec (int)
    x (0.5) check_url : verify options for each URL
    x (0.5) option : available (process, mounts)
    x (0.5) check_mounts : with available option
    x (0.5) check_pings

## 0.4

    x (0.4) check_process



    x conf YAML
    x cli / argparse
    x send data to graylog
    x send alerts to Teams
    x option --report
    x option --alert
    x log with timestamp  (for cron.log)
    x alert vs global_alert
    x name group/node
    x gitlab,  README.md, conf.yml.ori
    x find conf.yml basedir > commit V 0.1
    x requirements.txt : pyyaml, requests, psutil
    x config multi-file for  ansible
    x get_config_or_default()
    x debug() option and function
    x output to gelf over http
    x added cmt_check/cmt_node/cmt_group fields
    x teams alerts rate limited in configuration
    x error if empty list in conf (merge + checks)
    x logs : /var/log/cmt/cmt.log + logrotate (ansible)
    x FullLoader > SafeLoader
    x send alert for URL failed
    x ansible role centos 7, centos 8
    x option --list-modules
    x cli print version
    x cli print available modules
    x nicer cli print format with  units (MB, GB, % ...)


