---
title: Data model
---

# Data model

This is a quick copy of the data structure available in elasticsearch / kibana.

## Reference

    ===========================================================
    OUTPUT - REFERENCE
    ===========================================================

    -------------------------------------------
    Global Output JSON/GELF
    -------------------------------------------

    cmt_group         : Customer / Platform ...
    cmt_node          : VM / instance
    cmt_node_env      : prod / qa / test / dev ...
    cmt_node_role     : string - free
    cmt_node_location : geographical / hosting
    cmt_module        : module name
    cmt_check         : module name - deprecated
    cmt_id            : group.node.module.name

    cmt_alert         : yes/no
    cmt_warning       : yes/no
    cmt_notice        : yes/no

    cmt_message       : one line for human / full recap / id. compact mode


    specific
      +cmt_*module*_*

    +GELF mandatory fields
      source: group_node
      short_message
      timestamps


    -------------------------------------------
    Module: load
    -------------------------------------------

    cmt_load1: #float
    cmt_load5: #float
    cmt_load15: #float

    -------------------------------------------
    Module: cpu
    -------------------------------------------

    cmt_cpu: #float

    -------------------------------------------
    Module: memory
    -------------------------------------------

    cmt_memory_available: #int (bytes)
    cmt_memory_used: #int (bytes)
    cmt_memory_percent: #float (percent)


    -------------------------------------------
    Module: swap
    -------------------------------------------

    cmt_swap_used: #int (bytes)
    cmt_swap_percent: #float (percent)

    -------------------------------------------
    Module: boottime
    -------------------------------------------

    cmt_boottime_days: #int (days)
    cmt_boottime_seconds: #int (seconds)

    -------------------------------------------
    Module: mount
    -------------------------------------------

    cmt_mount            : /path/to/mount

    -------------------------------------------
    Module: disk
    -------------------------------------------

    cmt_disk         : /path/to/disk
    cmt_disk_total   : #int (bytes)
    cmt_disk_free    : #int (bytes)
    cmt_disk_percent : #float (percent)  [used]

    -------------------------------------------
    Module: process
    -------------------------------------------

    cmt_process_name: string   (config name, not process real name)
    cmt_process_cpu: float?
    cmt_process_memory: int (bytes)

    -------------------------------------------
    Module: url
    -------------------------------------------

    cmt_url: url string
    cmt_url_name: url name
    cmt_url_msec: int        [response time in millisecond if available]

    -------------------------------------------
    Module: ping
    -------------------------------------------

    cmt_ping: hostname

    -------------------------------------------
    Module: folder
    -------------------------------------------
    2020/10/07 - v0.7
    2020/10/20 - v0.9 : + recursive: yes/no

    cmt_folder_name            : name
    cmt_folder_path            : path
    cmt_folder_files           : #count
    cmt_folder_dirs            : #count
    cmt_folder_size            : #bytes
    cmt_folder_size_max        : #bytes (folder)
    cmt_folder_size_min        : #bytes (folder)
    cmt_folder_age_min         :
    cmt_folder_age_max         :

    -------------------------------------------
    Module: certificate
    -------------------------------------------
    2020/12/05 - V1.1

    cmt_certificate_name          string         # entry name in conf.yml
    cmt_certificate_host          string         # host:port
    cmt_certificate_seconds       int (seconds)  # seconds before expiration
    cmt_certificate_days          int (days)     # days before expiration
    cmt_certificate_subject       string         # domain/subject name

    -------------------------------------------
    Module: socket
    -------------------------------------------
    2020/12/06 - V1.1

    cmt_socket_name      : string
    cmt_socket_type      : local/remote
    cmt_socket_proto     : tcp/udp
    cmt_socket_host      : host:port
    cmt_socket_count     : int (established)
    cmt_socket_alive     : yes/no  [LISTEN]
    cmt_socket_ping      : ok/nok


    