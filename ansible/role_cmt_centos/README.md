Role Name
=========


Role Variables
--------------
   
    # group_vars
    cmt_group: mygroup
    cmt_node: "{{ inventory_hostname }}"
    cmt_node_location: my_datacenter
    cmt_default_graylog: http://my_graylog_server/
    cmt_alert_pager: not_defined
    cmt_test_pager: not_defined

    ---
    # defaults

    cmt_deploy: yes

    cmt_local_bin: cmt/cmt-1.2.0-centos64.bin
    cmt_local_src:  cmt/git

    cmt_group: na
    cmt_node: na
    cmt_node_env: na
    cmt_node_role: na
    cmt_node_location: na
    cmt_enable: "yes"
    cmt_enable_pager: "no"
    cmt_alert_max_level: alert

    cmt_default_graylog: http://localhost/gelf/
    cmt_alert_pager: https://noname/webhook/
    cmt_test_pager: https://noname/webhook/





Dependencies
------------

A list of other roles hosted on Galaxy should go here, plus any details in regards to parameters that may need to be set for other roles, or variables that are used from other roles.

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:


    - hosts: vmadmin
      gather_facts: yes

      roles:
        - cmt_centos7

License
-------

BSD

Author Information
------------------

An optional section for the role authors to include contact information, or a website (HTML is not allowed).
