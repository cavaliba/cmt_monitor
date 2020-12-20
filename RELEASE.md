RELEASE.md
==========


## 1.2.1 - 2020/12/20

    bug fixe cmt.PAGER TIMEOUT
    Persist remote conf
    remoteconf type (/txt/group_node.txt vs api )


## 1.2.0 - 2020/12/13

    aleternate conf format : module top entries with checks below


## 1.1.1. - 2020/12/09

    bug fixe - parse error if empty remote conf
    refactor to cmt_helper.py
    build binary for debian 8 64bits

## 1.1.0 - 2020/12/06

    module_certificate
    module_folder :bug in dir count ; option no_store ; handle single_file
    ARG : --cron
    nicer output (summary, humanize)
    CONF : frequency (--cron) for module and checks
    module socket
    
## 1.0.0 - 2020/11/29

    conf : conf.d on/off : global load_confd yes/no
    remote conf : send group.node as parameters (or as file.txt )  
    ARG : --debug2
    ARG : --no-pager-rate-limit
    ARG : --persist
    give persist to modules
    default homedir = /opt/cmt
    conf: enable_pager for check
    Pager events contain all alert/warn/notice messages
    hysteresis up (alert_delay in global/module/check)
    cmt_node_env [prod,form, pre,qual, test, dev]
    cmt_node_role: string
    cmt_node_location
    Pattern optionnal in module URL
    removed module_*_status checkItems (not needed any more ; use alert/warning/notice)
    module url : add "host" option (virtualhost header)

## 1.0.0.RC - 2020-11-24

    new configuration structure
    new alert/warn/notice ; simplified ChecKItems
    class Persist()
    Secu : injection de config/parametres dans appels shell ; subprocess
    max execution time in conf
    remote conf : http://host/conf/..../  (+group_node.txt if trailing /) 
    level alert/warn/notice by framework


## 1.0.0.alpha - 2020-11-17

    new modules structure in config ; checks deprecated
    timerange + enable option in global/modules/check
    ARG : --devmode
    conf: global send_to_pager (timerange, default = no)
    conf: teams channel : enable 
    global : field: cmt_message ; compact status
    cli: compact display ; status only ;   ARG : compact display option (--status)
    uuid/id in conf and events ; uuid = group.node.module.id ; id = check specific value
    check objet given to (not created by) each Chech module
    config merge more clever !
    conf_url option : remote config to be fetched and  merged into main/additional configs


# OLD

## 2020-10-25 - 0.9

    bug: binary version couldn't file local conf.yml (pyinstaller)
    check_folders : added option 'recursive'
    documentation framework

## 2020-10-20 - 0.8

    modular refactoring & split : one check per file


## 2020-10-04 - 0.7

    accept missing check entries in configuration
    checks : folders (exists, size, #files, max/min age, filename, ...)


## 2020-09-27 - 0.6

    check (abort) if config file exists
    check (abort) if no 'checks' item in config
    ignore (accept) missing conf.d
    ignore (accept) missing entries in conf: graylog servers
    timeout when sending http/gelf to graylog + suspended flag if previous errors
    timeout when sending http to Teams channels
    conf option : --conf filename

## 2020-08-09 - 0.5

    check_urls (no warnings, no redirects, msec, no ssl, options per URL)
    check_mounts
        option: --available
    check_pings

## 2020-06-27 - 0.4 - check_process

## 2020-06-27 - 0.3 - better OO oriented design with CheckItems, Checks, Reports

## 2020-06-14 - 0.2 - added conf.d/*.yml additional configurations

## 2020-06-14 - 0.1 - conf.yml directory from crontab

## 2020-06-14 - 0   - initial version
