---
title:  Introduction to Metrology servers for CMT
---


CMT can send data to metrology servers, when run from cron `--cron` or with the `--report` option.


## Supported remote servers

CMT can send data to:

* ElasticSearch 6 / 7 with standard json over HTTP (since CMT version 1.6)
* Graylog 2 or 3 with a GELF connector over HTTP protocol
* Graylog 2 or 3 with a GELF connector over UDP network protocol

Elasticsearch 7 should work fine but is yet untested. You may need to use the index name only and omit the '_type' part of the target URL (/cmt/data will become /cmt).

SSL/TLS (HTTPS) URLs can be configured instead of clear HTTP.

HTTP protocol is a TCP-connected protocol. If the remote server is slow or unavailable, CMT will detect and prevent any slowdown by cancelling data transfer for the run.

UDP protocol has the main advantage to not require a network connection from CMT agent to remote server. It's fire and forget. But it is not always available across network boundaries and firewalls.



## Which remote server is better ?

If unsure go with Graylog. It provides an all-included log aggregation system also based on an underlying Elasticsearch storage. The configuration is easy with a clean Web user interface. It helps manage protocols/connectors (inputs), index rotation, authentication, dashboard, alerts, etc. all from that simple and nice UI. Graylog has a narrower audience than Elastic. You can add Kibana later on top of the underlying Elasticsearch.


ElasticSearch is one of the most popular NoSQL datastore. It's a great choice as you may already have an available Elasticsearch server running in your systems. You'll need Kibana for powerful vizualisation and you'll have to  
configure index and alias creation, index rotation ... 



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


