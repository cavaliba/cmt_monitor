---
title: directory_structure
---

##  directory /opt/cmt

The following layout is standard for cmt :


    /opt/cmt/$ tree -L 1
    ├── cmt-xx-bin     : binary version of cmt (also in /usr/local/bin/cmt)
    ├── persist.json   : persitent data accross cmt runs
    ├── mysql.cnf      : optionnal mysql credentials if needed
    ├── conf.yml       : default main configuration file
    └── conf.d/        : additional configuration files go here 
       ├── demo.yml
       ├── apache.yml
       ├── backup.yml
       ├── ...
       └── README