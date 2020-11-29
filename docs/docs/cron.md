---
title: cron
---

# CMT used in automatic mode / crontab



## configure crontab

    $ sudo crontab -e

    * * * * * /usr/local/bin/cmt --conf /opt/cmt/conf.yml --report --pager --persist

## config file: --conf

If not provided, main config file will be searched for in /opt/cmt/conf.yml.

If the python script is used instead of the binay, the conf.yml will be the one next to the cmt.py script.

## option:  --report

Requires CMT to send metrology event to remote server (report to server).

## option:  --pager

Requires CMT to send Pager alert if any.


## option:  --persist

Requires CMT to persist some data accross consecutive runs. Not needed in CLI mode.

Some modules (may) use such data to compute delta/derivatives accross runs.

Some alert mechanisms use such data to estimate if an alert is not a transcient event.

