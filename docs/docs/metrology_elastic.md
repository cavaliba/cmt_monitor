---
title:  ElasticStack for CMT
---

# Elasticsearch metrology servers


##  prerequisite

You need to configure :

* an elastic 6 or 7 standard server
* an index for CMT
* a timestamp pipeline to add a relatime timestamp
* optionally, an alias and and index automatic rollover
* a kibana system to visualize and process ingested CMT data.

## CMT configuration


    metrology_servers:      
        my_elastic_remote_server:
          type: elastic_http_json
          url: http://my_remote_host:9200/cmt/data/?pipeline=timestamp
          [http_proxy]                   # http://[login[:pass]@proxyhost:port  ; use noenv value to skip os/env     
          [https_proxy]                  # https://[login[:pass]]@proxyhost:port  ; default to http_proxy   
          [http_code: 200]               # http_code for success
          [ssl_verify: yes]
          send_rawdata: no               # yes/no (default) : do we send multi-events (e.g. from mysqldata, or sendfile )
          rawdata_prefix: raw
          enable: yes

## Elastic cheatsheet

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

