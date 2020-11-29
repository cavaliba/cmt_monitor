CAVALIBA - CMT Monitor 
======================

(c) Cavaliba.com 2020 - Version 1.0.0 - 2020/11/29

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

see help
--------

    ./cmt.py --help

    usage: cmt.py [-h] [--report] [--alert] [--teamstest] [--checkconfig]
                  [--debug] [--status] [--devmode] [--version] [--listmodules]
                  [--available] [--conf CONF]
                  [modules [modules ...]]

    CMT - Cavaliba Monitoring

    positional arguments:
      modules        modules to check

    optional arguments:
      -h, --help     show this help message and exit
      --report       send data to Graylog/Gelf servers
      --alert        send alerts to Teams
      --teamstest    send test message to teams and exit
      --checkconfig  checkconfig and exit
      --debug        verbose/debug output
      --status, -s   compact cli output with status only
      --devmode      dev mode, no pager, no remote metrology
      --version, -v  display current version
      --listmodules  display available modules
      --available    display available entries found for modules (manual run on
                     target)
      --conf CONF    specify alternate yaml config file


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

    $ ./cmt.py

    ------------------------------------------------------------
    CMT - Version 1.0.0.RC - (c) Cavaliba.com - 2020/11/22
    ------------------------------------------------------------
    2020/11/24 - 00:15:33 : Starting ...
    cmt_group :  cmtdev
    cmt_node  :  vmpio


    Check load 
    cmt_load1              0.29   - CPU Load Average, one minute
    cmt_load5              0.28   - CPU Load Average, 5 minutes
    cmt_load15             0.26   - CPU Load Average, 15 minutes
    OK                     Load : 0.29 0.28 0.26

    Check cpu 
    cmt_cpu                1.3 %  - CPU Percentage
    OK                     CPU = 1.3 %

    Check memory 
    cmt_memory_percent     63.9 %  - Memory used (percent)
    cmt_memory_used        1470623744 bytes (1.5 GB) - Memory used (bytes)
    cmt_memory_available   992591872 bytes (992.6 MB) - Memory available (bytes)
    OK                     memory : used 63.9 % - used 1470623744 bytes - avail 992591872 bytes 

    Check boottime 
    cmt_boottime_seconds   111284 seconds  - Seconds since last reboot
    cmt_boottime_days      1 days  - Days since last reboot
    OK                     Days since last reboot : 1 days (111284 sec.)

    Check swap 
    cmt_swap_percent       0.7 %  - Swap used (percent)
    cmt_swap_used          15466496 bytes (15.5 MB) - Swap used (bytes)
    OK                     swap used : 0.7 % 

    Check disk 
    cmt_disk               /   - Path
    cmt_disk_total         67370528768 bytes (67.4 GB) - Total (Bytes)
    cmt_disk_free          43532156928 bytes (43.5 GB) - Free (Bytes)
    cmt_disk_percent       31.9 %  - Used (percent)
    OK                     Disk / - bytes free 43532156928/67370528768  -  used percent 31.9 %

    Check disk 
    cmt_disk               /boot   - Path
    cmt_disk_total         67370528768 bytes (67.4 GB) - Total (Bytes)
    cmt_disk_free          43532156928 bytes (43.5 GB) - Free (Bytes)
    cmt_disk_percent       31.9 %  - Used (percent)
    OK                     Disk /boot - bytes free 43532156928/67370528768  -  used percent 31.9 %

    Check url 
    cmt_url_name           www.cavaliba.com  
    cmt_url                https://www.cavaliba.com/  
    cmt_url_msec           102 ms 
    cmt_url_status         ok  
    OK                     www.cavaliba.com - https://www.cavaliba.com/ - http=200 - 102ms ; pattern OK

    Check mount 
    cmt_mount              /  
    cmt_mount_status       ok   - ok/nok
    OK                     mount for / found

    Check mount 
    cmt_mount              /mnt  
    cmt_mount_status       nok   - ok/nok
    NOK                    mount for /mnt not found

    Check process 
    cmt_process_name       redis  
    cmt_process_status     nok   - ok/nok
    NOK                    process redis missing (redis)

    Check process 
    cmt_process_name       apache  
    cmt_process_status     nok   - ok/nok
    NOK                    process apache missing (httpd)

    Check process 
    cmt_process_name       cron  
    cmt_process_status     ok   - ok/nok
    cmt_process_memory     2998272 bytes (3.0 MB) - rss
    cmt_process_cpu        0.01 seconds  - cpu time, user
    OK                     process cron found (cron)

    Check process 
    cmt_process_name       ssh  
    cmt_process_status     ok   - ok/nok
    cmt_process_memory     5689344 bytes (5.7 MB) - rss
    cmt_process_cpu        0.02 seconds  - cpu time, user
    OK                     process ssh found (sshd)

    Check process 
    cmt_process_name       ntp  
    cmt_process_status     nok   - ok/nok
    NOK                    process ntp missing (ntpd)

    Check process 
    cmt_process_name       mysql  
    cmt_process_status     ok   - ok/nok
    cmt_process_memory     87769088 bytes (87.8 MB) - rss
    cmt_process_cpu        27.5 seconds  - cpu time, user
    OK                     process mysql found (mysqld)

    Check process 
    cmt_process_name       php-fpm  
    cmt_process_status     nok   - ok/nok
    NOK                    process php-fpm missing (php-fpm)

    Check ping 
    cmt_ping               192.168.0.1  
    cmt_ping_status        ok   - ok/nok
    OK                     ping to 192.168.0.1 ok

    Check ping 
    cmt_ping               localhost  
    cmt_ping_status        ok   - ok/nok
    OK                     ping to localhost ok

    Check ping 
    cmt_ping               www.google.com  
    cmt_ping_status        ok   - ok/nok
    OK                     ping to www.google.com ok

    Check ping 
    cmt_ping               www.test.com  
    cmt_ping_status        nok   - ok/nok
    WARN                   check_ping - www.test.com not responding

    Check ping 
    cmt_ping               www.averybadnammme_indeed.com  
    cmt_ping_status        nok   - ok/nok
    WARN                   check_ping - www.averybadnammme_indeed.com not responding

    Check folder 
    cmt_folder_path        /tmp  
    cmt_folder_name        /tmp  
    cmt_folder_files       3 files  - Number of files in folder /tmp
    cmt_folder_dirs        15 dirs  - Number of dirs/subdirs in folder /tmp
    cmt_folder_size        425 bytes (425.0 B) - Total Size (bytes)
    cmt_folder_age_min     111264 sec  - Min age (seconds)
    cmt_folder_age_max     111274 sec  - Max age (seconds)
    cmt_folder_status      nok   - ok/nok
    NOTICE                 /tmp : expected file not found (secret.pdf)

    Check folder 
    cmt_folder_path        /missing  
    cmt_folder_name        /missing  
    cmt_folder_status      nok   - ok/nok
    NOTICE                 /missing missing

    Check mount 
    cmt_mount              /merge  
    cmt_mount_status       nok   - ok/nok
    NOK                    mount for /merge not found

    Check url 
    cmt_url_name           demo.cavaliba.com  
    cmt_url                http://demo.cavaliba.com/  
    cmt_url_msec           187 ms 
    cmt_url_status         ok  
    OK                     demo.cavaliba.com - http://demo.cavaliba.com/ - http=200 - 187ms ; pattern OK

    Alerts / Warnings / Notice
    --------------------------

    Notice : 
    folder          : /tmp : expected file not found (secret.pdf)
    folder          : /missing missing

    Warnings : 
    ping            : check_ping - www.test.com not responding
    ping            : check_ping - www.averybadnammme_indeed.com not responding

    Alerts : 
    mount           : mount for /mnt not found
    process         : process redis missing (redis)
    process         : process apache missing (httpd)
    process         : process ntp missing (ntpd)
    process         : process php-fpm missing (php-fpm)
    mount           : mount for /merge not found



CLI compact form
---------------

    $ ./cmt.py -s

    ------------------------------------------------------------
    CMT - Version 1.0.0.RC - (c) Cavaliba.com - 2020/11/22
    ------------------------------------------------------------
    2020/11/24 - 00:16:11 : Starting ...
    cmt_group :  cmtdev
    cmt_node  :  vmpio

    Status (short) 
    --------------
    OK      Load : 0.45 0.32 0.28
    OK      CPU = 4.5 %
    OK      memory : used 63.9 % - used 1470234624 bytes - avail 992985088 bytes 
    OK      Days since last reboot : 1 days (111322 sec.)
    OK      swap used : 0.7 % 
    OK      Disk / - bytes free 43532144640/67370528768  -  used percent 31.9 %
    OK      Disk /boot - bytes free 43532144640/67370528768  -  used percent 31.9 %
    OK      www.cavaliba.com - https://www.cavaliba.com/ - http=200 - 102ms ; pattern OK
    OK      mount for / found
    NOK     mount for /mnt not found
    NOK     process redis missing (redis)
    NOK     process apache missing (httpd)
    OK      process cron found (cron)
    OK      process ssh found (sshd)
    NOK     process ntp missing (ntpd)
    OK      process mysql found (mysqld)
    NOK     process php-fpm missing (php-fpm)
    OK      ping to 192.168.0.1 ok
    OK      ping to localhost ok
    OK      ping to www.google.com ok
    WARN    check_ping - www.test.com not responding
    WARN    check_ping - www.averybadnammme_indeed.com not responding
    NOTICE  /tmp : expected file not found (secret.pdf)
    NOTICE  /missing missing
    NOK     mount for /merge not found
    OK      demo.cavaliba.com - http://demo.cavaliba.com/ - http=200 - 183ms ; pattern OK

    Alerts / Warnings / Notice
    --------------------------

    Notice : 
    folder          : /tmp : expected file not found (secret.pdf)
    folder          : /missing missing

    Warnings : 
    ping            : check_ping - www.test.com not responding
    ping            : check_ping - www.averybadnammme_indeed.com not responding

    Alerts : 
    mount           : mount for /mnt not found
    process         : process redis missing (redis)
    process         : process apache missing (httpd)
    process         : process ntp missing (ntpd)
    process         : process php-fpm missing (php-fpm)
    mount           : mount for /merge not found

crontab
-------

create /var/log/cavaliba folder and:

    crontab -e
    */5 * * * * /usr/bin/python3 /opt/cavaliba/cmt.py --report  >> /var/log/cavaliba/cmt_monitor.log 2>&1
    */5 * * * * /usr/local/bin/cmt -c-conf /opt/cmt_monitor/conf.yml --report  --alert >> /var/log/cavaliba/cmt_monitor.log 2>&1


Output / metric points
----------------------

Global

    cmt_group 
    cmt_node
    cmt_module
    cmt_check   [deprecated]
    cmt_id

    cmt_message
    cmt_alert

Module: load

    cmt_load1: #float
    cmt_load5: #float
    cmt_load15: #float

Module: cpu

    cmt_cpu: #float

Module: memory

    cmt_memory_available: #int (bytes)
    cmt_memory_used: #int (bytes)
    cmt_memory_percent: #float (percent)

Module: swap

    cmt_swap_used: #int (bytes)
    cmt_swap_percent: #float (percent)

Module: boottime

    cmt_boottime_days: #int (days)
    cmt_boottime_seconds: #int (seconds)

Module: mount

    cmt_mount            : /path/to/mount
    cmt_mount_status     : ok/nok


Module: disk

    cmt_disk         : /path/to/disk
    cmt_disk_total   : #int (bytes)
    cmt_disk_free    : #int (bytes)
    cmt_disk_percent : #float (percent)  [used]

Module: process

    cmt_process_name: string   (config name, not process real name)
    cmt_process_status : ok/nok
    cmt_process_cpu: float?
    cmt_process_memory: int (bytes)

Module: url

    cmt_url: url string
    cmt_url_name: url name
    cmt_url_status: ok/nok
    cmt_url_msec: int        [response time in millisecond if available]

Module: ping

    cmt_ping: hostname
    cmt_ping_status: ok/nok

Module: folder

    cmt_folder_name: name
    cmt_folder_path: path
    cmt_folder_status : ok/nok
    cmt_folder_files: #count
    cmt_folder_dirs: #count
    cmt_folder_size: #bytes
    cmt_folder_size_max: #bytes (folder)
    cmt_folder_size_min: #bytes (folder)
    cmt_folder_age_min:
    cmt_folder_age_max:


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


COPYRIGHT
---------

    (c) Cavaliba.com - 2020

