---
title:  Introduction to Metrology servers for CMT
---


CMT can send data to metrology servers, when run from cron `--cron` or with the `--report` option.


## Supported remote servers

CMT can send data to:

* ElasticSearch 6 / 7 with standard json over HTTP (since CMT version 1.6)
* InfluxDB V1/V2 starting with cmt 1.7+ ; line protocol over HTTP
* Graylog 2 or 3 with a GELF connector over HTTP protocol
* Graylog 2 or 3 with a GELF connector over UDP network protocol

Elasticsearch 7 should work fine but is yet untested. You may need to use the index name only and omit the '_type' part of the target URL (/cmt/data will become /cmt).

SSL/TLS (HTTPS) URLs can be configured instead of clear HTTP.

HTTP protocol is a TCP-connected protocol. If the remote server is slow or unavailable, CMT will detect and prevent any slowdown by cancelling data transfer for the run.

UDP protocol has the main advantage to not require a network connection from CMT agent to remote server. It's fire and forget. But it is not always available across network boundaries and firewalls.



## Which remote server is better ?

If unsure go with Graylog. It provides an all-included log aggregation system also based on an underlying Elasticsearch storage. The configuration is easy with a clean Web user interface. It helps manage protocols/connectors (inputs), index rotation, authentication, dashboard, alerts, etc. all from that simple and nice UI. Graylog has a narrower audience than Elastic. You can add Kibana later on top of the underlying Elasticsearch.

ElasticSearch is one of the most popular NoSQL datastore. It's a great choice as you may already have an available Elasticsearch server running in your systems. You'll need Kibana for powerful vizualisation and you'll have to configure index and alias creation, index rotation ... 

InfluxDB is easy to setup, and can provide very adequate Visulization (Grafana), Dashboards and Alerting.

You can specify multiple metrology servers in the configuration. They will all receive all the collected data.



## Graylog server configuration

You need to configure either :

* a GELF input over HTTP, say on port 8080
* a GELF input over UDP, say on port 12201

You can also add rsyslog and beats protocol to collect logfiles and various file oriented data (with filebeat)

Your cmt configuration will be

    metrology_servers:

      graylog_test1:
          type: graylog_udp_gelf
          host: 10.10.10.13
          port: 12201
          enable: yes
      
      graylog_test2:
          type: graylog_http_gelf
          url: http://10.10.10.13:8080/gelf
          enable: yes


##  Elastic server configuration

You need to configure :

* an index
* a timestamp pipeline
* optionally, an alias and and index automatic rollover
* a kibana system to visualize and process ingested CMT data.

Your CMT  configuration will thus be :

    metrology_servers:      

        my_elastic_remote_server:
          type: elastic_http_json
          url: http://my_remote_host:9200/cmt/data/?pipeline=timestamp
          enable: yes



Here is a minimal Elastic cheatsheet you may use from the server hosting elastic to get started:

    
    ## open access (dev mode only)  elasticsearch.yml
    network.host: 0.0.0.0
    discovery.type: single-node
    
    ## version
    curl localhost:9200
    curl localhost:9200/_cat
    curl localhost:9200/_cat/indices/
    curl localhost:9200/_cat/indices?v
    curl localhost:9200/_cat/indices?v&pretty

    ## delete index
    curl -XDELETE  localhost:9200/cmt

    ## create index
    curl -XPUT  localhost:9200/cmt

    ## insert json test data
    curl -XPOST -H "Content-Type: application/json" localhost:9200/cmt/data/ -d '{ "key1":"value1" }'

    ## query index
    curl  localhost:9200/cmt/_search?pretty

    ## create a timestamp pipeline
    curl -XPUT 'localhost:9200/_ingest/pipeline/timestamp' -H 'Content-Type: application/json' -d '
    {
    "description": "Creates a timestamp when a document is initially indexed",
    "processors": [   { "set": { "field": "_source.timestamp", "value": "{{_ingest.timestamp}}" }} ]
    }
    '
    ## insert with pipeline
    curl -XPOST -H "Content-Type: application/json" localhost:9200/cmt/data/?pipeline=timestamp -d '{ "key1":"value1" }'


## InfluxDB configuration
*new with cmt 1.7+*

You need to configure :

* an influxdb server (V1/V2) accessible with http/https regular curl-like calls
* an influxdb database
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
          enable: yes


A minimal cheatsheet to setup influxdb V1.8 (on Centos here)

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