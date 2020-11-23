
CAVALIBA - CMT Monitor 
==========================
(c) Cavaliba 2020 - V. 0.3

CMT Monitor is a simple software agent to help :

* collect standard OS metrics
* collect middleware status and metrics
* check application and remote URLs  for response and pattern
* send alerts to Teams channels
* send data to graylog/elastic stack for futur reporting and alerting
* diagnose outage when run as CLI


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

    usage: cmt.py [-h] [--report] [--teamstest] [--alert] [modules [modules ...]]

    CMT - Cavaliba Monitoring

    positional arguments:
      modules      modules to check

    optional arguments:
      -h, --help   show this help message and exit
      --report     send reports to graylog and co
      --teamstest  send test to teams
      --alert      send alerts to teams



configuration
-------------

Install requirements.txt.

    python3 -m pip install -r requirements.txt


Copy conf.yml.ori to conf.yml and adapt.

    cp conf.yml.ori conf.yml
    vi conf.yml

Add additional configurations

    vi conf.d/demo.yml

run manually
------------

    $ ./cmt.py 
    ----------------------------------------
    2020/06/14 - 19:08:32 : Starting
    ----------------------------------------

    cmt_disk             : /
    cmt_disk_total       : 67370528768
    cmt_disk_used        : 18411159552
    cmt_disk_free        : 45506723840
    cmt_disk_percent     : 28.8

    cmt_load1            : 0.01
    cmt_load5            : 0.25
    cmt_load15           : 0.22

    cmt_cpu              : 0.7

    cmt_memory_percent   : 51.6
    cmt_memory_used      : 1152327680
    cmt_memory_available : 1331470336

    cmt_swap_used        : 36077568
    cmt_swap_percent     : 1.7

    cmt_boottime         : 15475
    cmt_boottime_days    : 0

    cmt_url              : www.cavaliba.com
    cmt_url_status       : ok

    cmt_url              : demo.cavaliba.com
    cmt_url_status       : ok

    Alerts
    ------
    none.

crontab
-------

copy to /opt/cavaliba (for example) and:

    crontab -e
    */5 * * * * /usr/bin/python3 /opt/cavaliba/cmt.py --report  >> /var/log/cavaliba/cmt_monitor.log 2>&1


LICENSE
-------
See LICENSE file. Opensurce Software with a 3 points BDS-like license.


SUPPORT
-------
CMT is provided as-is and no direct support is available at the moment. 

Feel free to drop a note at contact@cavaliba.com anyway.

REVISION
--------

    2020-06-14 - V0   - initial version
    2020-06-14 - V0.1 - conf.yml directory from crontab
    2020-06-14 - V0.2 - added conf.d/*.yml additional configurations
    2020-06-27 - V0.3 - OO oriented design with ChecksItems, Checks, Reports



(c) Cavaliba - 2020

