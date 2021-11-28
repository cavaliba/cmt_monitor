---
title:  InfluxDB for CMT
---

# InfluxDB metrology servers


## InfluxDB configuration
*new with cmt 1.7+*

You need to configure :

* an influxdb server (V1/V2) accessible with http/https regular curl-like calls
* an influxdb database for CMT
* a user with write permissions to said database
* an optional retention policy

You can then use InfluxDB and/or Grafana to visualize and send alerts.

Your CMT  configuration will thus be :

    metrology_servers:

      # Compatible with influxdb V1 & V2
      influxdb_test:
          type: influxdb
          url: http://10.10.10.13:8086/write?db=cmt
          # url: http://10.10.10.13:8086/write?db=cmt&u=username&p=password
          # url: http://10.10.10.13:8086/api/v2/write?db=cmt
          time_format: msec              # msec, sec, nsec ; anything else, no timestamp
          batch: yes                     # send all data point at the end of cmt ; default = yes
          send_tags: yes                 # add all cmt_tag_XX in the influx tag list ; default = no
          token: mysecrettotokenken      # if token authentication is used server-side
          username: cmt                  # if header auth is prefered rathen than in the url
          password : cmt
          [http_proxy]                   # http://[login[:pass]@proxyhost:port  ; use noenv value to skip os/env     
          [https_proxy]                  # https://[login[:pass]]@proxyhost:port  ; default to http_proxy          
          [ssl_verify: no]               # default: no
          [http_code: 200]               # http_code for success          
          send_rawdata: no               # yes/no (default) : do we send multi-events (e.g. from mysqldata, or sendfile )
          rawdata_prefix : raw           # prefix for field names and tag names (default raw)
          single_measurement: yes        # influx line protocol: global *cmt* measurement name or per module
          enable: yes


## InfluxDB cheatsheet

A minimal cheatsheet to setup influxdb V1.8 (on Centos here):

    cat <<EOF | sudo tee /etc/yum.repos.d/influxdb.repo
    [influxdb]
    name = InfluxDB Repository - RHEL \$releasever
    baseurl = https://repos.influxdata.com/rhel/\$releasever/\$basearch/stable
    enabled = 1
    gpgcheck = 1
    gpgkey = https://repos.influxdata.com/influxdb.key
    EOF

    yum install influxdb
    => 1.8

    sudo systemctl start influxdb
    sudo systemctl enable influxdb

    vi /etc/influxdb/influxdb.conf

    # firewall-cmd --add-port=8086/tcp
    # firewall-cmd --add-port=8086/tcp --permanent

And a quick cheatsheet to configure influxdb V1.8


    # influx

    Connected to http://localhost:8086 version 1.8.6
    InfluxDB shell version: 1.8.6

    > create database cmt

    > show databases
    name: databases
    
    name
    ----
    _internal
    cmt

    > use cmt
    Using database cmt

    > insert cmt_test,cmt_host=hostA,cmt_group=groupA,cmt_check=mytest cmt_test=1.5

    > select * from cmt_test
    name: cmt_test
    time                cmt_check cmt_group cmt_host cmt_test
    ----                --------- --------- -------- --------
    1625932660193314010 mytest    groupA    hostA    1.5


    > CREATE USER admin WITH PASSWORD '.......' WITH ALL PRIVILEGES

    > show users;
    user  admin
    ----  -----
    admin true


    GRANT ALL PRIVILEGES TO <username>
    REVOKE ALL PRIVILEGES FROM <username>

    > CREATE USER cmt WITH PASSWORD '.......'

    GRANT [READ,WRITE,ALL] ON <database_name> TO <username>
    REVOKE [READ,WRITE,ALL] ON <database_name> FROM <username>
    SHOW GRANTS FOR <user_name>
    SET PASSWORD FOR <username> = '<password>'
    DROP USER username

    curl -i -XPOST 'http://10.10.10.13:8086/write?db=cmt' --data-binary "cmt_test,cmt_node=test,cmt_group=test,cmt_check=mytest,cmt_node_env=test cmt_value1=1,cmt_value2=2" -v

    curl -i -XPOST 'http://localhost:8086/write?db=mydb' --data-binary @cpu_data.txt

    V2
    curl -i -XPOST 'http://localhost:8086/api/v2/write?bucket=db/rp&precision=ns' \
      --header 'Authorization: Token username:password' \
      --data-raw 'cpu_load_short,host=server01,region=us-west value=0.64 1434055562000000000'

    curl -G http://localhost:8086/query \
      -u todd:influxdb4ever \
      --data-urlencode "q=SHOW DATABASES"

    curl -G "http://localhost:8086/query?u=todd&p=influxdb4ever" \
      --data-urlencode "q=SHOW DATABASES"