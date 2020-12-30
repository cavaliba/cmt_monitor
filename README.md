CAVALIBA - CMT Monitor 
======================

(c) Cavaliba.com 2020 - Version 1.3.0 alpha  - 2020/12/30

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

    sudo cp cmt.###.bin /usr/local/bin/cmt
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
See included file docs/


LICENSE
-------
See LICENSE file. Opensurce Software with a 3 points BDS-like license.


SUPPORT
-------
CMT is provided as-is and no direct support is available at the moment. 

Feel free to drop a note at contact@cavaliba.com anyway.


RELEASE
--------

see RELEASE file.


COPYRIGHT
---------

    (c) Cavaliba.com - 2020

