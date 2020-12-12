CAVALIBA - CMT Monitor 
======================

(c) Cavaliba.com 2020 - Version 1.1.1 - 2020/12/09

CMT Monitor is a simple software agent to  :

* collect standard OS, Middleware, Network ... and Custom metrics
* check application and remote URLs  for response and pattern
* send alerts to Pager (Teams channels)
* send data to Metrology servers (GELF/graylog) based on ElasticStack for futur reporting and alerting
* help troubleshoot outage when run as CLI
* easy automation and deploy with Ansible ; easy one-file configuration

get from github
---------------

    git clone https://github.com/cavaliba/cmt_monitor.git

Elastic Index template
----------------------

Load template to elasticsearch for proper field type definition :

    curl -X PUT -d @'cmt_elastic_template.json' -H 'Content-Type: application/json' 'http://localhost:9200/_template/cavaliba-custom-mapping?pretty'

documentation
--------------

http://www.cavaliba.com/cmt/doc/index.html


see help
--------

    $ ./cmt.py --help

    usage: cmt.py [-h] [--cron] [--report] [--pager] [--persist] [--conf CONF]
                  [--listmodules] [--available] [--pagertest]
                  [--no-pager-rate-limit] [--checkconfig] [--version] [--debug]
                  [--debug2] [--devmode] [--short]
                  [modules [modules ...]]

    CMT - Cavaliba Monitoring

    positional arguments:
      modules               modules to check

    optional arguments:
      -h, --help            show this help message and exit
      --cron                equiv to report, alert, persist, short output
      --report              send events to Metrology servers
      --pager               send alerts to Pagers
      --persist             persist data accross CMT runs (use in cron)
      --conf CONF           specify alternate yaml config file
      --listmodules         display available modules
      --available           display available entries found for modules (manual
                            run on target)
      --pagertest           send test message to teams and exit
      --no-pager-rate-limit
                            disable pager rate limit
      --checkconfig         checkconfig and exit
      --version, -v         display current version
      --debug               verbose/debug output
      --debug2              more debug
      --devmode             dev mode, no pager, no remote metrology
      --short, -s           short compact cli output


setup from binary
-----------------

    sudo cp cmt.bin /usr/local/bin/cmt
    sudo chown root:root /usr/loca/bin/cmt
    sudo chmod 755 /usr/local/bin/cmt
    $ cmt --version

setup from source
-----------------

Install requirements.txt.

    python3 -m pip install -r requirements.txt

Copy conf.yml.ori to conf.yml and adapt.

    cp conf.yml.ori conf.yml
    vi conf.yml

Add additional configurations

    vi conf.d/demo.yml

Use locally as CLI with --available option to identifiy items to monitor.


CLI - run manually
------------------

    $ ./cmt.py -s

    ------------------------------------------------------------
    CMT - Version 1.1.0 - (c) Cavaliba.com - 2020/12/06
    ------------------------------------------------------------
    cmt_group      :  cavaliba
    cmt_node       :  vmxupm

    OK      load         1/5/15 min : 0.11  0.17  0.22
    OK      cpu          usage : 1.5 %
    OK      memory       used 66.7 % - used 1.5 GB - avail 915.4 MB - total 2.7 GB
    OK      boottime     days since last reboot : 0 days - 7:25:51 sec.
    OK      swap         used: 0.4 % /  9.2 MB - total 2.1 GB
    OK      disk         path : / - used: 32.7 % - used: 20.9 GB - free: 43.0 GB - total: 67.4 GB 
    OK      disk         path : /boot - used: 32.7 % - used: 20.9 GB - free: 43.0 GB - total: 67.4 GB 
    OK      url          www.cavaliba.com - https://www.cavaliba.com/ [Host: ] - http=200 - 102 ms ; pattern OK
    NOK     url          www_non_existing - http://www.nonexisting/ [Host: ] - no response to query
    OK      mount        path / found
    NOTICE  mount        path /mnt not found
    OK      socket       local redis localhost tcp/6379 - alive: yes - count: 0
    NOK     process      apache missing (httpd)
    OK      process      cron found (cron) - memory rss 2.9 MB - cpu 0.01 sec.
    OK      process      ssh found (sshd) - memory rss 5.3 MB - cpu 0.04 sec.
    NOK     process      ntp missing (ntpd)
    OK      process      mysql found (mysqld) - memory rss 88.5 MB - cpu 3.9 sec.
    NOK     process      php-fpm missing (php-fpm)
    OK      ping         192.168.0.1 ok
    OK      ping         localhost ok
    OK      ping         www.google.com ok
    WARN    ping         www.test.com not responding
    WARN    ping         www.averybadnammme_indeed.com not responding
    NOK     folder       /tmp : expected file not found (secret.pdf)
    NOK     folder       /missing missing
    NOK     folder       /tmp/ab.txt missing
    OK      folder       folder_big_nostore (/usr/lib) ok - 20874 files, 2038 dirs, 2617963928 bytes [2.6 GB] - targets 0/0
    WARN    certificate  50 day(s) left for SSL certificate google.com:443
    OK      certificate  338 day(s) left for SSL certificate duckduckgo.com:443
    NOK     certificate  no certificate found for duckduckgo.com:80
    OK      certificate  114 day(s) left for SSL certificate yahoo.com:443
    OK      socket       remote www_google www.google.com tcp/443 - alive: yes - count: 0
    NOTICE  mount        path /merge not found
    OK      url          demo.cavaliba.com - http://demo.cavaliba.com/ [Host: ] - http=200 - 183 ms ; pattern OK

    2020/12/06 - 16:42:52 : Done - 34 checks - 21 ok - 13 nok - 8 alerts - 3 warning - 2 notice.



crontab
-------


    $ sudo crontab -e

    */2 * * * * /usr/local/bin/cmt --cron


Available Modules
-----------------

    $ ./cmt.py --listmodule
    CMT - Version 1.1.0 - (c) Cavaliba.com - 2020/12/06

      -  load
      -  cpu
      -  memory
      -  swap
      -  boottime
      -  mount
      -  disk
      -  url
      -  process
      -  ping
      -  folder
      -  certificate
      -  socket


REFERENCE
---------
See included file REFERENCE.txt


LICENSE
-------
See LICENSE file. Opensurce Software with a 3 points BDS-like license.


SUPPORT
-------
CMT is provided as-is and no direct support is available at the moment. 

Feel free to drop a note at contact@cavaliba.com anyway.


REVISION
--------

    2020-06-14 - 0   - initial version
    2020-06-14 - 0.1 - conf.yml directory from crontab
    2020-06-14 - 0.2 - added conf.d/*.yml additional configurations
    2020-06-27 - 0.3 - OO oriented design with CheckItems, Checks, Reports
    2020-06-27 - 0.4 - check_process

    2020-08-09 - 0.5
        check_urls (no warnings, no redirects, msec, no ssl, options per URL)
        check_mounts
            option: --available
        check_pings
    
    2020-09-27 - 0.6
        check (abort) if config file exists
        check (abort) if no 'checks' item in config
        ignore (accept) missing conf.d
        ignore (accept) missing entries in conf: graylog servers
        timeout when sending http/gelf to graylog + suspended flag if previous errors
        timeout when sending http to Teams channels
        conf option : --conf filename

    2020-10-04 - 0.7
        accept missing check entries in configuration
        checks : folders (exists, size, #files, max/min age, filename, ...)

    2020-10-20 - 0.8
        modular refactoring & split : one check per file

    2020-10-25 - 0.9
        bug: binary version couldn't file local conf.yml (pyinstaller)
        check_folders : added option 'recursive'
        documentation framework

    2020-11-17 - 1.0.alpha - not production ready

    2020-11-24 - 1.0.0.RC - new configuration structure

    2020-11-29 - 1.0.0
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

    2020-12-06 - 1.1.0
        module_certificate
        module_folder :bug in dir count ; option no_store ; handle single_file
        ARG : --cron
        nicer output (summary, humanize)
        CONF : frequency (--cron) for module and checks
        module socket

COPYRIGHT
---------

    (c) Cavaliba.com - 2020

