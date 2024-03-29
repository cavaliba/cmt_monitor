---
title: version
---

# Releases

## 3.0beta2 - 2022/11/15

    bug: influx output has double ,,
    bug: remove quotes in influx output
    bug : http_proxy in global CONF
    conf: global : prefix option (default 'cmt_') for GELF and INFLUX
    conf: global : add authkey option to authenticate message in metrology servers
    conf: timerange option : nohrange : exclude a time range (opposite of hrange)
    output: rename output field : node_env to env
    output: rename output field : id to key
    output: remove cmt_message (=> short_message) in graylog 
    output: rename field : alert to state
    output: updated field source is group.node variable (graylg/elastic)
    output: add field groupnode == group.node
    option: conf --template  to display a full configuration example
    module URL : obfuscate_url option (default: param) ; values : param|full|no



## 2.4 - 2022/06
    reverse_severity option : inverse condition for severity (negative check)
    tested on elastic 8.2 (http://127.0.0.1:9200/cmt/_doc/?pipeline=timestamp)
    removed cmt_alert (> alert) and xmt_severuty (> severity) output fields
    removed cmt_node_location ; use tag instead
    removed cmt_node_role ; use tag instead    



## 2.3 - 2022/01/23
    CLI clean : rename severity label NONE to OK
    CLI clean : removed alert state from CLI output
    CLI clean : mysql: send to debug instead of log for connection error
    updated certificate module : new option (name) , simplified thresholds, new attributes reported, timeout
    url : check for expected pattern in response header in addition to response page
    folder : new targets : permission, uid, gid
    


## 2.2 - 2021/12/19

    feature: CLI output cosmetic
    feature: new metrology fields (severity, alert) for human display 
    feature: add --pager option to CLI to limit pagers (for tests , or cron ...)
    change: previous CLI option  --pager is now --pager_enable
    change: previous CLI option  --pagertest is now --pager_test
    feature: module Load uses os.cpu_count to estimate alert
    feature :  start_offset - new global option to delay start / spread the load on metrology servers (cron mode)
    bug: cmt_severity is int ; no quote in metrology
    bug: mutliline field values in elastic are now sent as single line (separator = ;)


## 2.1 - 2021/11/28

    feat: display alert transitions (new.active.down) in CLI output
    feat: http_proxy and https_proxy option in global, metrology and pager entries 
    feat: http_code option for metrology/pager entries (success response code)
    refactor: rewrite Pager module ; per pager rate_limit ; managed/allnotifications mode
    feat: pager rate_limit option by pager/in pager configuration only
    feat: nopersist ARG for CLI : ignore previous run, hysteresis/delay for alerts
    bug: module disks : missing include for severity handling
    bug: incorrect version display (2.0 , expected 2.1beta>2.1)
    bug: incorrect handling of severity_max  for severity == NOTICE
    breaking: removed old alerting model (alert/warn/notice) ; severity/alert only


## 2.1beta - 2021/11/21

    feat: alert modele rewrite : cmt_severity, cmt_alert
    feat: send_rawdata new option per metrology (send multi-events events) ; default no
    feat: rawdata_prefix new option (default: raw) : prefix for fields sent to metrology, for rawdata/multievent 
    feat: rawdata events are named {rawdata_prefix}_{checkname}_{keyname}
    feat: single_measurement new influx option ;  send all events as cmt measurement (default) or per module measurement
    bug: influxdb ; better rebalance tags/fields for cardinality
    bug: multiline datapoints are not sent to influx ; breaks line protocol
    deprecated: old alerting model (alert/warn/notice) ; severity/alert only

## 2.0 - 2021/11/12

    module URL : new option username/password for basic auth
    module URL : new option http_code (default 200) expected in reply
    module URL : new option pattern_reject for pattern which MUST NOT be present in response
    module FOLDER : new option send_list to send file listing with size, date, perms, uid/gid
    (beta) new module SENDFILE - sends an external json file to metrology servers
    (beta) new module MYSQLDATA
    new global option: business_hours (default: 08:30:00 17:30:00) for timerange, bh/nbh


## 2.0 beta - 2021/10/26

    feature: display skipped tests
    feature(beta): pagerduty (managed) mode
    added : severity_max + cmt_severity (critical, error, warning, notice, none )
    added option ssl_verify to http targets influx/graylog/elasticseach
    bug : CLI output displays realtime results before hysteris/up/down processing(pager feature only)
    bug : influxdb/batch mode when mutliple targets
    bug : tags key/value in influxdb must be sent as string
    removed modules section from config
    removed alert_delay in module config
    removed alert_max_level in module config
    removed frequency in module_config


## 1.8.2 - 2021/07/24

    bugfixe : influxdb - password variable mismatch (typo)
    bugfixe : influxdb - double quote for string field values only
    feature : influxdb - add send_tags option
    minor : check if unknown module requested in ARGS


## 1.8.1 - 2021/07/18

    bugfix - batch send metrology (influx) only if --report/cron
    bugfix - added double quotes around tags values in Influxdb line protocol
    feature - added cmt_ prefix before Influx measurement names (to avoid collision in single db usecase)
    bugfix - mysql module - slave status retrieval
    feature - mysql module - credentials in defaults-file only (security)
    feature - mysql module - standard indicators


## 1.8beta - 2021/07/11 BETA

    feature: module mysql

## 1.7 - 2021/07/11

    feature: added influxdb V1/V2 metrology server support ; batch mode, V1/V2, timestamp options...


## 1.7beta - 2021/05/15

    bugfix: module folder : filter_regexp missing when not recursive
    bugfix: module folder : display name in ouputs


## 1.6.1 - 2021/04/18

    bugfix : folder module : has_recent, has_old mismatch
    feature: folder module : check valid targets
    feature: send cmt_version in metrology events


## 1.6 - 2021/04/04

    feature: ElasticSearch 6/7 remote metrology server type
    feature: module folder : has_recent, has_old targets
    feature: module load : alert on threshold1/5/15 in config
    feature: module swap : alert on threshold percentage
    feature: module memory : alert on threshold percentage
    feature: module boottime : alert on threshold days
    feature: module cpu : alert on threshold percentage
    feature: updated CLI color output
    deprecated : cmt_alert/cmt_warning/cmt_notice ; cmt_notification=1/2/3 instead


## 1.5 - 2021/03/28

    feature: display config_file in report header
    feature: tags/key-value option in global/check conf sections


## 1.4.0 - 2021/03/21

    feature: root_required configuration for checks when root privilege is mandatory
    feature: module folder: send_content option in folder module
    feature: module url: timeout and http proxy options : http_proxy, https_proxy, noenv
    feature: --check option for specific checkname filtering when run as CLI
    feature: new module send ; pipe a result to cmt for immediate send to metrology


## 1.3.1 - 2021/01/10

    bugfix  : module mount ; parse all modules (not disk only)
    bugfix  : ansible role / copy src and modules to /opt/cmt/src
    bugfix  : handle http remote conf exception
    feature : added alert_max_level:none option (along with alert, warn, notice)
    feature : module folder with regexp/extension option
    feature : module process with seach_arg option
    quality: more documentation

## 1.3.0 - 2021/01/02

    bugfix: confd_load : ssl_verify, redirect set to False
    feature: cmt_check : contains the name of the check instead of the module name (deprecated)
    feature: cmt_notification = alert + warn + notice
    feature: GELF fields without quote for numerical values => no more elastic index templates.
    quality: code refactor/split modules ; lint

## 1.2.1 - 2020/12/20

    bugfix: cmt.PAGER TIMEOUT
    feature: Persist remote conf
    feature: remoteconf type (/txt/group_node.txt vs api )

## 1.2.0 - 2020/12/13

    aleternate conf format : 'module' top entries with checks below
    refactor to cmt_helper.py


## 1.1.1 - 2020/12/09 

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



## old

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


