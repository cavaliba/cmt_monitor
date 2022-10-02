# cavaliba.com - 2021
# conf.py

import os
import sys
import time
import datetime
import json
import yaml
import requests
import hashlib


import globals as cmt
from logger import logit, debug, debug2

requests.packages.urllib3.disable_warnings()

# ------------------------------------------------------------
# Configuration management
# ------------------------------------------------------------


def load_conf():

    ''' main entry to load global conf '''

    debug("Load conf")
    conf = load_conf_master()
    load_conf_dirs(conf)  # includes merge
    return conf


def load_conf_master():

    ''' load first config file aka root/master config file '''

    debug("Load master conf")

    if cmt.ARGS['conf']:
        config_file = cmt.ARGS['conf']
    else:
        config_file = os.path.join(cmt.HOME_DIR, "conf.yml")

    debug("Config file : ", config_file)

    if not os.path.exists(config_file):
        logit('Config file not found : ' + config_file)
        sys.exit()

    # load master conf
    conf = conf_load_file(config_file)
    conf["__config_file"] = config_file
    
    conf_add_top_entries(conf)
    
    return conf


def load_conf_dirs(conf):
    ''' loop over conf.d/*.yml files and load/merge them.'''

    debug("Load conf dirs")

    # load_confd
    loadconfd = conf['global'].get("load_confd", "no")

    if not loadconfd or loadconfd == "no":
        return conf

    # conf.d/*/yml  to ease ansible or modular configuration
    config_dir = os.path.join(cmt.HOME_DIR, "conf.d")

    # check if conf.d exists
    if not os.path.exists(config_dir):
        debug("no conf.d/ found. Ignoring.")
        return conf

    # scan and merge
    for item in os.scandir(config_dir):
        if item.is_file(follow_symlinks=False):
            if item.name.endswith('.yml'):
                debug("Additionnal config file found : ", item.path)
                conf2 = conf_load_file(item.path)
                conf_add_top_entries(conf2)
                conf_merge(conf, conf2)

    return conf

# ---


def load_conf_remote(conf):

    ''' fetch a remote URL with additional conf ; merge '''

    debug("Load remote conf")

    # load remote config from conf_url parameter
    if 'conf_url' in conf['global']:

        url = conf['global']['conf_url']
        gro = conf['global'].get("cmt_group", "nogroup")
        nod = conf['global'].get("cmt_node", "nonode")

        if url.endswith("/txt/"):
            url = url + "{}_{}.txt".format(gro, nod)

        url = url + "?group={}&node={}".format(gro, nod)

        debug("Remote config URL : ", url)

        remote_txt = conf_load_http(url)
        remote_conf = None

        if remote_txt is not None:
            remote_conf = yaml.safe_load(remote_txt)
            if not type(remote_conf) is dict:
                remote_conf = None

        cachedconf = cmt.PERSIST.get_key("remote_conf_cache", None)
        cachedconf_age = cmt.PERSIST.get_key("remote_conf_cache_age", 0)

        if int(time.time() - cachedconf_age) > 86400:
            # too old
            cachedconf = None

        if remote_conf is None:
            remote_conf = cachedconf

        if remote_conf is not None:
            cmt.PERSIST.set_key("remote_conf_cache", remote_conf)
            cmt.PERSIST.set_key("remote_conf_cache_age", int(time.time()))
            cmt.PERSIST.save()
            conf_add_top_entries(remote_conf)
            conf_merge(conf, remote_conf)

    debug("Configuration loaded")
    debug2(json.dumps(conf, indent=2))


# -----------
# load a single file

def conf_load_file(config_file):

    with open(config_file) as f:
        conf = yaml.load(f, Loader=yaml.SafeLoader)
        # print(json.dumps(CONF, indent=2))

    # verify content
    if conf is None:
        return {}

    return conf


def conf_load_http(url):

    headers = {
        'Content-Type': 'application/text'
    }

    if cmt.ARGS['devmode']:
        print("DEVMODE : GET ", url, headers)

    # real
    try:
        r = requests.get(url, headers=headers,
                         verify=False,
                         allow_redirects=False,
                         timeout=cmt.REMOTE_CONFIG_TIMEOUT
                         )
    except Exception as e:
        logit("Load remote conf failed (network) : {}".format(e))
        return None

    if r.status_code != 200:
        debug("Load remote conf failed : {}".format(+ r.status_code))
        return None

    debug("Load remote conf OK : ", r.text)
    return r.text


def conf_merge(conf1, conf2):

    debug("merge conf")

    # new conf format Ver. 1.2.0
    for topitem in cmt.GLOBAL_MODULE_MAP:
        for k in conf2[topitem]:
            conf1[topitem][k] = conf2[topitem][k]


def conf_add_top_entries(conf):
    ''' complete conf with optionnal/default top level entries.'''

    # add missing top entries
    for item in cmt.DEFAULT_CONF_TOP_ENTRIES:
        if item not in conf:
            debug2("No {} entry in config ; added automatically.".format(item))
            conf[item] = {}

    # new conf format Ver. 1.2.0
    for item in cmt.GLOBAL_MODULE_MAP:
        if item not in conf:
            debug2("No {} entry in config ; added automatically.".format(item))
            conf[item] = {}

# ------------------------------------------------------------------------
# conf utilities
# ------------------------------------------------------------------------

def md5String(data):
    m=hashlib.md5()
    data = data.encode('utf-8')
    m.update(data)
    return m.hexdigest() 


def get_startoffset():

    # try to get offset from conf
    try:
        offset = int(cmt.CONF['global']['start_offset'])
        return offset % 60
    except:
        pass

    # default to compute offset from group/node names
    group = cmt.CONF['global'].get('cmt_group', 'nogroup')
    node = cmt.CONF['global'].get('cmt_node', 'nonode')
    data = group + node
    hexdata = md5String(data)
    firsthex = "0x"+hexdata[0:2]
    pause = int(firsthex,0)
    #print("HEXDATA = ",hexdata, firsthex, pause)
    return pause % 60

def is_timeswitch_on(myconfig):
    ''' check if a date/time time range is active
        myconfig can be :
              yes, 24/7
              no
              after YYYY-MM-DD hh:mm:ss
              before YYYY-MM-DD hh:mm:ss
              hrange  hh:mm:ss hh:mm:ss
              8/5, bh, ho, business_hours   (Mon-Fri 8h30-18h)
              nbh, hno, non_business_hours
        returns True or False if current datatime match myconfig
    '''

    # yaml gotcha
    myconfig = str(myconfig)

    if myconfig == "True" or myconfig == "yes" or myconfig == "true" or myconfig == "24/7":
        return True

    if myconfig == "False" or myconfig == "no" or myconfig == "false":
        return False

    myarray = myconfig.split()
    action = myarray.pop(0)

    if action == "after":
        mynow = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        target = ' '.join(myarray)
        # print(mynow)
        if mynow >= target:
            return True
        return False

    if action == "before":
        mynow = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        target = ' '.join(myarray)
        if mynow <= target:
            return True
        return False

    if action == "hrange":
        mynow = datetime.datetime.today().strftime("%H:%M:%S")
        if mynow >= myarray[0] and mynow <= myarray[1]:
            return True
        return False

    if action == "ho" or action == "bho" or action == "8/5" or action =="business_hours":

        business_hours = cmt.CONF['global'].get('business_hours', '08:30:00 17:30:00')
        (hmin, hmax) = business_hours.split()

        myday = datetime.datetime.today().strftime("%a")
        myhour = datetime.datetime.today().strftime("%H:%M:%S")
        if myday in ["Sat", "Sun"]:
            return False
        if myhour < hmin or myhour > hmax:
            return False
        return True

    if action == "hno" or action == "nbh"  or action == "non_business_hours":

        business_hours = cmt.CONF['global'].get('business_hours', '08:30:00 17:30:00')
        (hmin, hmax) = business_hours.split()

        myday = datetime.datetime.today().strftime("%a")
        myhour = datetime.datetime.today().strftime("%H:%M:%S")
        if myday in ["Mon", "Tue", "Wed", "Thu", "Fri"]:
            if myhour >= hmin or myhour <= hmax:
                return False
        return True

    # default, unknown / no match
    return False


def get_proxies(conf):
    ''' 
    Get global and local (check) proxies configuration. Local overrides Global.
    Use noenv http_proxy option to ignore OS/ENV proxies  and use direct access.
    '''
    proxies = {} 
    my_global_http_proxy = cmt.CONF['global'].get('http_proxy',"")
    my_global_https_proxy = cmt.CONF['global'].get('https_proxy',my_global_http_proxy) 
    my_http_proxy = conf.get('http_proxy',my_global_http_proxy)
    my_https_proxy = conf.get('https_proxy',my_global_https_proxy) 
    if my_http_proxy != "":
        proxies["http"] = my_http_proxy
    if my_https_proxy != "":
        proxies["https"] = my_https_proxy
    noenv = False
    if my_http_proxy == "noenv":
        noenv = True
    return proxies, noenv   


def print_template():
    '''option --template displays a full template for conf.yml'''

    template = """
---
# Cavaliba / cmt_monitor / conf.yml - TEMPLATE
# CMT Version: 3.0


# Example configuration / template 

# Global section
# --------------

global:
  cmt_group: mycompany
  cmt_node: vm1
  cmt_node_env: dev
  enable: yes
  start_offset: 2
  enable_pager: yes
  alert_delay: 90
  business_hours: 08:00:00 18:00:00
  #conf_url: http://localhost/txt/
  max_execution_time: 55
  load_confd: yes
  #http_proxy: http://[login[:pass]@]proxyhost:port
  #https_proxy: https://[login[:pass]@]proxyhost:port
  tags: demo os=linux os_ver=debian10
  #prefix: cmt_
  #authkey: random_string_keepsecret_ingress_filter_in_metrology_pipelines

# Metrology section
# -----------------

metrology_servers:

  my_graylog_udp:
    type: graylog_udp_gelf
    host: mygraylog.company.com
    port: 12201
    send_rawdata: yes
    rawdata_prefix : raw
    enable: yes
  
  my_graylog_http:
    type: graylog_http_gelf
    url: http://mygraylog.company.com:8080/gelf
    send_rawdata: yes
    rawdata_prefix : raw
    #http_proxy: noenv
    #http_proxy: http://[login[:pass]@]proxyhost:port
    #https_proxy: https://[login[:pass]@]proxyhost:port
    #http_code: 202 
    #ssl_verify: yes
    enable: yes

  my_elastic:
    type: elastic_http_json
    send_rawdata: yes
    rawdata_prefix : raw
    url: http://myelastic.company.com:9200/cmt/data/?pipeline=timestamp
    #http_proxy: noenv
    #http_proxy: http://[login[:pass]@]proxyhost:port
    #https_proxy: https://[login[:pass]@]proxyhost:port
    #http_code: 201
    #ssl_verify: yes
    enable: yes

  # influxdb V1 & V2
  my_influxdb:
    type: influxdb
    url: http://myinflux:8086/write?db=cmt&u=cmt&p=mysecret
    token: toto
    #username: cmt
    #password : mysecret
    # timestamp : msec, sec, nsec ; anything else, no timestamp
    time_format: msec
    batch: yes
    single_measurement: yes
    send_tags: no
    send_rawdata: no
    rawdata_prefix : raw      
    #http_proxy: noenv
    #http_proxy: http://[login[:pass]@]proxyhost:port
    #https_proxy: https://[login[:pass]@]proxyhost:port 
    #ssl_verify: yes
    #http_code: 204
    enable: yes


# Pager section
# -------------
# type : team_channel, teams (idem), pagerduty
# mode : managed (ratelimit, hysteresis by CMT), allnotifications

pagers:

  myteams:
    type: teams 
    mode: managed
    url: https://outlook.office.com/webhook/xxxxx/IncomingWebhook/yyyyyyyyyyyyyyy
    #http_proxy: noenv
    #http_proxy: http://[login[:pass]@proxyhost:port
    #https_proxy: https://[login[:pass]]@proxyhost:port 
    #http_code: 200
    #ssl_verify: yes
    #rate_limit: 7200
    enable: yes

  mypagerduty:
    type: pagerduty
    mode: allnotifications
    url: https://events.pagerduty.com/v2/enqueue
    key: XXXXXXXXXXXXXXXXXXXXXXXx
    #http_proxy: noenv
    #http_proxy: http://[login[:pass]@proxyhost:port
    #https_proxy: https://[login[:pass]]@proxyhost:port 
    #ssl_verify: yes
    #http_code: 202
    #rate_limit: 7200
    enable: yes



# checks section
# --------------

# module_name:
#
#   checkname:
#      [enable]           : timerange ; default yes
#      [severity_max]     : critical, error, warning, notice, none
#      [enable_pager]     : timerange ; default NO ; need global/pager to be enabled ; sent if alert found
#      [alert_delay]      : delay before transition from normal to alert (if alert) ; seconds  ; DEFAULT 120 
#      [frequency]        : min seconds between runs ; needs --cron in ARGS ; overrides module config
#      [root_required]    : [yes|no(default)] -  new 1.4.0 - is root privilege manadatory for this check ?
#      [tags]             : tag1 tag2[=value] ... ; list of tags ; no blank space aroung optional "=value"
#      arg1               : specific to module (see doc for each module)
#      arg2               : specific to module  
#      (...)

load:

  myload:
    enable: yes
    severity_max: warning
    threshold1: 6.0
    threshold5: 4.0
    threshold15: 2.0
    #tags: local1 local2=43

cpu:

  mycpu:
    enable: yes
    severity_max: warning

memory:

  mymemory:
    enable: yes
    frequency: 10
    # percent
    threshold: 80.5
    severity_max: warning


boottime:

  myboottime:
    enable: yes
    # days
    threshold: 180
    severity_max: warning

swap:
  myswap:
    enable: yes
    # percent
    threshold: 11.3
    severity_max: warning

disk:

  disk_root:
    path: /
    alert: 80
    severity_max: warning

  disk_boot:
    path: /boot
    alert: 90
    severity_max: warning

# ---------
url:

  www.cavaliba.com:
    enabled: after 2020-01-01
    url: https://www.cavaliba.com/
    pattern: "Cavaliba"
    allow_redirects: yes
    ssl_verify: yes
    #host: toto
    #http_proxy: XXX
    #https_proxy: XXX
    severity_max: warning

  www_non_existing:
    enabled: after 2020-01-01
    url: http://www.nonexisting/
    severity_max: warning

  google:
    url: https://www.google.com/
    severity_max: warning

  yahoo:
    url: https://www.yahoo.com/
    allow_redirects: yes
    ssl_verify: yes
    severity_max: warning

  via_proxy_cavaliba:
    enabled: yes
    url: https://www.cavaliba.com/
    http_proxy: http://62.210.205.232:8080
    severity_max: warning

  url_noenv_proxy:
    url: http://www.monip.org/
    http_proxy: noenv
    severity_max: warning

  url_test_timeout:
    url: http://slowwly.robertomurray.co.uk/delay/4000/url/http://google.co.uk
    timeout: 2
    severity_max: warning

  url_authenticated:
    url: https://www.auth-needed.com/login
    username: mylogin
    password: mysecret

  url_httpcode401:
    url: https://www.auth-needed.com/login
    http_code: 401

  url_patternreject:
    url: http://www.myservice.com/status/
    pattern_reject: 'class="error"'

# ---------
mount:

  mount_root:
    path: /
    severity_max: warning

  mount_mnt:
    path: /mnt
    severity_max: warning


  mount_critical:
    path: /critical
    severity_max: critical
    enable_pager: yes

# ---------
process:

  redis:
    psname: redis
    enable_pager: no
    severity_max: warning

  apache:
    psname: httpd
    severity_max: warning

  cron:
    psname: cron
    search_arg: "-f"
    severity_max: warning
  
  ssh:
    psname: sshd
    severity_max: warning

  ntp:
    psname: ntpd
    severity_max: warning

  mysql:
    psname: mysqld
    severity_max: warning

  php-fpm:
    psname: php-fpm
    enable_pager: yes
    severity_max: warning

# ---------
ping:

  ping_vm1:
    host: 192.168.0.1
    severity_max: warning

  ping_locahost:
    host: localhost
    severity_max: warning

  www.google.com:
    host: www.google.com
    severity_max: warning

  wwwtest:
    host: www.test.com    
    severity_max: warning

  badname:
    host: www.averybadnammme_indeed.com  
    severity_max: warning

# ---------
folder:

  test_recursive100:
    path: /opt/cmt/testdata/arbo100
    severity_max: critical
    recursive: yes

  test_extension:
    path: /opt/cmt/testdata
    severity_max: warning
    recursive: yes
    filter_extension: ".conf .hl7"

  test_regexp:
    path: /opt/cmt/testdata
    severity_max: warning
    recursive: yes
    filter_regexp: '^Makefile$'

  test_regexp_no_recurse:
    path: /opt/cmt/testdata
    severity_max: warning
    recursive: no
    filter_regexp: '^Makefile$'

  test_regexp_ext:
    path: /opt/cmt/testdata
    severity_max: warning
    recursive: yes
    filter_regexp: '.*.conf$'

  test_wrong_target:
    path: /opt/cmt/testdata
    severity_max: warning
    target:
       is_blabla:

  test_hasfile:
    path: /opt/cmt/testdata
    severity_max: error
    recursive: no
    target:
       has_files:
            - secret.pdf
            #- secret2.pdf

  test_age_min:
    path: /opt/cmt/testdata
    severity_max: error
    target:
       age_min: 1000

  test_age_max:
    path: /opt/cmt/testdata
    severity_max: notice
    target:
       age_max: 300

  test_files_min:
    path: /opt/cmt/testdata
    severity_max: warning
    target:       
       files_min: 3

  test_files_max:
    path: /opt/cmt/testdata
    severity_max: warning
    target:
       files_max: 10

  test_size_min:
    path: /opt/cmt/testdata
    severity_max: warning
    target:
       size_min: 100000
       
  test_size_max:
    path: /opt/cmt/testdata
    severity_max: error
    target:
       size_max: 10

  test_has_recent:
    path: /opt/cmt/testdata
    target:
       has_recent: 3600
    severity_max: warning

  test_has_old:
    path: /opt/cmt/testdata
    target:
       has_old: 86400
    severity_max: warning

  test_missing:
    path: /opt/cmt/testdata/missing
    severity_max: warning

  test_missing:
    path: /opt/cmt/testdata/file_missing.txt
    severity_max: warning

  test_missing_reversed:
    path: /opt/cmt/testdata/file.txt
    reverse_severity: warning

  test_nostore:
    path: /opt/cmt/testdata/file.txt
    recursive: yes
    no_store: yes
    severity_max: warning

  folder_root:
    path: /root
    root_required: yes
    severity_max: warning

  folder_list:
    path: /opt/cmt
    recursive: yes
    send_list: yes

  test_permission:
    path: /opt/cmt/testdata/permission.txt
    recursive: no
    target:
      permission: -rw-rw-r--

  test_permissions:
    path: /opt/cmt/testdata/permissions
    recursive: yes
    target:
      permission: -rw-rw-r--
      uid: 1000
      gid: 1000


# ---------
certificate:

  cert_google:
    hostname: google.com
    # name: google.com
    # port: 443
    # warning_in: 7
    # notice_in: 30
    # severity_max: critical     # when expired
  
  cert_ip_google:
    hostname: 142.250.201.174
    port: 443
    name: google.com

  cert_duck:
    hostname: duckduckgo.com
    alert_in: 1 week
    severity_max: warning

  cert_broken:
    hostname: duckduckgo.com
    port: 80
    severity_max: warning

  yahoo:
    hostname: yahoo.com
    port: 443
    severity_max: warning

# ---------
socket:

  redis:
    socket: local tcp 6379
    #socket: local tcp port | remote tcp host port
    connect: yes
    #send: 
    #pattern:
    severity_max: warning

  www_google:
     socket: remote www.google.com tcp 443
     connect: yes
     #send: 
     #pattern:
     severity_max: warning


send:

  test_token1:
    attribute: test
    comment: "a test comment for token1 - cmt_test will be created in elastic"
    unit: "no_unit"
    severity_max: warning

sendfile:

  # [ { "user":"fred", "last-login-days":4 },
  #   { "user":"jack", "last-login-days":7 },
  #   { "user":"igor", "last-login-days":9 }  ]

  mysendfile:
    jsonfile: /opt/cmt/demo.json
    frequency: 3600


mysql:

  mydb:
    defaults_file: /opt/cmt/mysql.cnf
        #  [client]
        #  host     = 127.0.0.1
        #  user     = root
        #  password = xxxxxxx
        #  port     = 3306
        #  socket   = /var/run/mysqld/mysqld.sock
    is_slave: yes
    max_behind: 300
    alert_delay: 300
    severity_max: warning

mysqldata:

  # creates raw_myuser_username, and raw_myuser_years
  myuser:
    defaults_file: /opt/cmt/mysql.cnf
        #  [client]
        #  host     = 127.0.0.1
        #  user     = readonlylogin
        #  password = xxxxxxx
        #  port     = 3306
        #  socket   = /var/run/mysqld/mysqld.sock
    query: select user,age from cmt_test.table1 limit 10
    columns:
      user: username
      age: years
    maxlines: 10
    frequency: 300


# -------------------------------------
# timerange fields (from documentation)
# -------------------------------------
# yes, 24/7                    : always
# no                           : never
# after YYYY-MM-DD hh:mm:ss    : after time of the day
# before YYYY-MM-DD hh:mm:ss   : before ... 
# hrange hh:mm:ss hh:mm:ss     : time intervall
# ho, bh, business_hours       : 8h30/18h mon>fri - see global configuration for custom time
# nbh,hno, non_business_hours  : !(8h30/18h mon>fri)
#
# ------------------------------------
# conf.d/*.yml also included with :
# - main conf has higher priority
# - first level lists merged
# ------------------------------------

"""

    print(template)