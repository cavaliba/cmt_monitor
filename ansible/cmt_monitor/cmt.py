#!/usr/bin/python3
# Cavaliba - 2020 - CMT_monitor - cmt.py

import os
import socket
import sys
import time
import datetime
import argparse
import signal
import yaml
import json
import re

import psutil
import requests

# ---

MAX_EXECUTION_TIME=50
HOME_DIR = os.path.dirname(__file__)

RATE_LIMIT_FILE = os.path.join(HOME_DIR, "alert.last")

# ---

ARGS={}
CONF={}
SESSION = requests.session()



# ----------------------------------------------------------
# logit
# ----------------------------------------------------------
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def logit(line):
    now = datetime.datetime.today().strftime("%Y/%m/%d - %H:%M:%S")
    print(now + ' : ' + line)

def debug(*items):
    if ARGS['debug']:
        print('DEBUG:',' '.join(items))

# ----------------------------------------------------------
# Timeout stop
# ----------------------------------------------------------
def signal_handler(signum, frame):
    raise Exception("Timed out!")
    exit()

# ----------------------------------------------------------
# Args on CLI
# ----------------------------------------------------------
def parse_arguments():

    parser = argparse.ArgumentParser(description='CMT - Cavaliba Monitoring')

    #parser.add_argument('--conf', dest="config_file", type=str ,help="configuration file")
    parser.add_argument('--report', help='send data to Graylog/Gelf servers', 
        action='store_true', required=False)
    parser.add_argument('--alert', help='send alerts to Teams', 
        action='store_true', required=False)
    parser.add_argument('--teamstest', help='send test message to teams and exit', 
        action='store_true', required=False)
    parser.add_argument('--checkconfig', help='checkconfig and exit', 
        action='store_true', required=False)
    parser.add_argument('--debug', help='verbose/debug output', 
        action='store_true', required=False)
    parser.add_argument('modules', nargs='*',  
        action='append', help='modules to check')

    return vars(parser.parse_args())


def is_check_in_args(name):

    modules = ARGS['modules'][0]
    if name in modules  or len(modules) == 0 :
        return True
    debug(name, "check not in ARGS")
    return False

# ------------------------------------------------------------
# Config
# ------------------------------------------------------------
def load_conf():

    # conf.yml
    config_file = os.path.join(HOME_DIR, "conf.yml")
    conf = load_conf_file (config_file)

    # conf.d/*/yml  to ease ansible deployment
    config_dir = os.path.join(HOME_DIR, "conf.d")

    for item in os.scandir(config_dir):
        if item.is_file(follow_symlinks=False):
            if item.name.endswith('.yml'):
                debug("Config File : ",item.path)
                conf2 = load_conf_file (item.path)
                if conf2:
                    conf = merge_conf (conf, conf2)

    debug("DEBUG - Configuration loaded")
    debug(json.dumps(conf, indent=2))
    
    return conf

# -----------
# load a single file
def load_conf_file(config_file):
    
    with open(config_file) as f:
        conf = yaml.load(f, Loader=yaml.FullLoader)
        #print(CONF)
        #print(json.dumps(CONF, indent=2))
    return conf

# -----------
# merge to config : concat keys and merge lists values only
def merge_conf(conf, conf2):
    res = conf 
    for key, value in conf2.items():
       if key in conf and key in conf2:
            if isinstance(value, list):
                # merge :
                for item in value:
                    res[key].append(item)
                # or else keep value from first conf
    return res

# -----------
def get_conf_or_default(key, default):
    if key in CONF:
        return CONF[key]
    else:
        return default


def is_check_in_conf(name):
    if 'checks' in CONF:
        if name in CONF['checks']:
            return True
    debug(name, "not in conf")
    return False


def is_check_active(name):
    # check in conf
    if is_check_in_conf(name) and is_check_in_args(name):
            return True
    debug(name, "check not active")
    return False

# ------------------------------------------------------------
# TEAMS
# ------------------------------------------------------------
def teams_send(url=None, color="0000FF",title="CMT Alert", message="n/a", origin="n/a"):

    message = """
{{
    "@type": "MessageCard",
    "@context": "http://schema.org/extensions",
    "summary": "Monitoring",
    "themeColor": "{}",
    "sections": [{{
        "activityTitle": "{}",
        "activitySubtitle": "{}",
        "activityText": "{}",
        "markdown": false
    }}],
}}
""".format(color, title, origin, message)


    headers = {
        'Content-Type' : 'application/json'
    }

    try:
        r = requests.post(url,headers=headers, data=message)
        return r.status_code
    except:
        return 0


def teams_geturl(channel="test"):
    url = ""
    for item in CONF['teams_channel']:
        if item['name'] == channel:
            url = item['url']
    return url


def teams_test():
    url = teams_geturl(channel="test")
    origin = CONF['cmt_group'] + '/' + CONF['cmt_node']
    color="0000FF"
    title = "TEST TEST from " + origin
    message = "Test message from CMT. Please ignore."
    r = teams_send(url=url, title=title, message=message ,color=color, origin=origin)
    logit("Teams test : " + str(r) )

# ------------------------------------------------------------
# ALERT rate limit
# ------------------------------------------------------------

def get_last_send():

    t = 0
    #if os.path.isfile(RATE_LIMIT_FILE) :

    try:
        file = open(RATE_LIMIT_FILE,"r")
        t = int(file.readline())
        file.close()
    except:
        t = 0

    return t

def set_last_send(t):

    try:
        file = open(RATE_LIMIT_FILE,"w")
        file.write(str(t))
        file.close()
    except:
        pass
    return



# ------------------------------------------------------------
# GRAYLOG / GELF
# ------------------------------------------------------------
def send_graylog_http_gelf(url, data=""):
    
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

    try:
        r = SESSION.post(url, data=data, headers=headers)    
        debug("Message sent to graylog(http/gelf) : " + str(r.status_code))
    except:
        logit("Error - couldn't send graylod message (http/gelf) to " + str(url))

def send_graylog_udp_gelf(host, port=12201, data=""):

    #data = '"demo":"42"'
    #mess = '{ "version":"1.1", "host":"host-test", "short_message":"CMT gelf test", ' + data + ' }'  

    binpayload = bytes(str(data),"utf-8")

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (host, port)

    try:
        sent = sock.sendto(binpayload, server_address)
        sock.close()
        debug("Message sent to graylog(udp/gelf)")
    except:
        logit("Error - couldn't send graylod message (udp/gelf) to " + str(host))

# ----------------------------------------------------------
# class
# ----------------------------------------------------------

class CheckItem():

    ''' Store one single data point with optional status/alert/info.'''

    def __init__(self, name, value, description=""):
        self.name = name
        self.value = value
        self.description = description

        self.alert = False
        self.alert_message = ""
        self.unit = ""

    # ex.
    # load1, load5 ...
    

class Check():

    '''Stores multiple checkItem related to a single Check function.
       Each Check is sent as one message to  a metrology server like Graylog/Elastic.
       Holds alerts for each check item.
       Alerts are sent globally at the Report level.
    '''

    def __init__(self, checkname="unknown", info="n/a"):

        self.checkname = checkname
        self.info = info

        try:
            self.group = CONF['cmt_group']
        except:
            self.group = 'unknown'

        try:
            self.node = CONF['cmt_node']
        except:
            self.node = 'unknown'
        

        self.checkitems=[]
        self.lines=[]
        
        self.alert = 0


    def add_item(self, item):

        ''' add a CheckItem instance to the Check items list '''

        self.checkitems.append(item)
        
        if item.alert:
            self.alert += 1


    def build_graylog_message(self):


        graylog_data = '"version":"1.1",' 
        #graylog_data += '"host":"{}",'.format(self.node)
        graylog_data += '"host":"{}_{}",'.format(self.group,self.node)

        graylog_data += '"short_message":"cmt_check {}",'.format(self.checkname)

        for item in self.checkitems:
            graylog_data += '"cmt_{}":"{}",'.format(item.name, item.value)
            debug("DEBUG - build graylog data : ", str(item.name), str(item.value))

        if self.alert > 0:
            has_alert = "yes"
        else:
            has_alert= "no"
        graylog_data += '"cmt_alert":"{}",'.format(has_alert)

        graylog_data += '"cmt_group":"{}",'.format(self.group)
        graylog_data += '"cmt_node":"{}",'.format(self.node)
        graylog_data += '"cmt_check":"{}",'.format(self.checkname)

        graylog_data = '{' + graylog_data + '}'
        return graylog_data


    def print_to_cli(self):

        print()
        print(bcolors.OKBLUE + bcolors.BOLD + "Check", self.checkname, bcolors.ENDC)

        for i in self.checkitems:    
            print("{:20} {:15} - {}".format(i.name, i.value, i.description))
        

    def send_to_server(self):

        if ARGS["report"]:
            message = "cmt - " + self.checkname
            graylog_data = self.build_graylog_message()  
            
            for item in CONF['graylog_udp_gelf_servers']:
                host=item['host']
                port=item['port']
                send_graylog_udp_gelf(host=host, port=port, data=graylog_data)

            for item in CONF['graylog_http_gelf_servers']:
                url=item['url']
                send_graylog_http_gelf(url=url, data=graylog_data)


class Report():
    
    '''A Rport stores all the Checks from a single run of CMT.
    Alerts are sent to Teams/... at the end of the Report
    '''

    def __init__(self):

        self.checks = []
        self.alert = 0


    def add_check(self, c):

        self.checks.append(c)
        self.alert += c.alert


    def print_alerts_to_cli(self):

        print()

        if self.alert == 0:
            print(bcolors.OKGREEN + bcolors.BOLD + "No alerts.", bcolors.ENDC)
        else:

            print(bcolors.FAIL + bcolors.BOLD + "Alerts :", bcolors.ENDC)
            print('--------')
            for c in self.checks:
                for i in c.checkitems:
                    if i.alert:
                        print (i.alert_message)
        print()


    def send_alerts(self):

        ''' Send alerts to Teams channels '''

        # check if alert exists
        if self.alert == 0:
            debug("Alerts : no alerts to be sent.")
            return

        # check rate_limit
        t1 = int(get_last_send())
        t2 = int(time.time())
        rate = int(get_conf_or_default("teams_rate_limit",3600))

        if t2-t1 <= rate:
            logit("Alerts : too many alerts (rate-limit) - no alert sent to Teams")
            return

        # get alert channel
        url = teams_geturl(channel="alert")
        if len(url) == 0:
            logit("Alerts : no 'alert' channel - no alert sent to Teams")
            return


        # prepare message
        origin = CONF['cmt_group'] + '/' + CONF['cmt_node']
        color = "FF0000"
        title = "ALERT from " + origin
        
        message = ""
        for c in self.checks:
            for i in c.checkitems:
                if i.alert:
                    message += i.alert_message
                    message += '<br>\n'
        debug("MESSAGE : ",message)              
        
        # send alert
        r = teams_send(url=url, title=title, message=message ,color=color, origin=origin)
        if r == 200:
            logit("Alerts : alert sent to Teams ")
        else:
            logit("Alerts : couldn't send alert to Teams - response  " + str(r))

        # update rate_limit
        set_last_send(t2)


# =====================================================================
# Checks functions
# =====================================================================

def check_load():
    
    c = Check(checkname='load')

    # (1.17, 0.86, 0.52)
    load = os.getloadavg()

    l1  = CheckItem('load1',load[0])
    l1.description ='CPU Load Average, one minute'
    c.add_item(l1)

    l5  = CheckItem('load5',load[1])
    l5.description='CPU Load Average, 5 minutes'
    c.add_item(l5)

    l15 = CheckItem('load15',load[2])
    l15.description='CPU Load Average, 15 minutes'
    c.add_item(l15)
    
    return c


def check_cpu():

    '''Get CPU percentage. No alert. Send cpu float value.'''

    c = Check(checkname='cpu') 
    cpu = psutil.cpu_percent(interval=2)

    i  = CheckItem('cpu',cpu,"CPU Percentage")   
    c.add_item(i)

    return c


def check_memory():

    '''Collect memory percent, used, free, available'''

    c = Check(checkname='memory') 
      
    # svmem(total=2749374464, available=1501151232, percent=45.4, used=979968000, 
    # free=736043008, active=1145720832, inactive=590102528, buffers=107663360, 
    # cached=925700096, shared=86171648)
    
    memory = psutil.virtual_memory()
    
    m1  = CheckItem('memory_percent',memory.percent,"Memory used (percent)")
    c.add_item(m1)

    m2  = CheckItem('memory_used',memory.used,"Memory used (bytes)")
    c.add_item(m2)

    m3  = CheckItem('memory_available',memory.available,"Memory available (bytes)")
    c.add_item(m3)

    return c


def check_swap():

    c = Check(checkname='swap') 
    # sswap(total=2147479552, used=0, free=2147479552, percent=0.0, sin=0, sout=0)
    swap = psutil.swap_memory()

    m1 = CheckItem('swap_percent',swap.percent,"Swap used (percent)")
    c.add_item(m1)

    m2 = CheckItem('swap_used',swap.used,'Swap used (bytes)')
    c.add_item(m2)

    return c

def check_boottime():

    c = Check(checkname='boottime') 
    boottime = int( time.time() - psutil.boot_time() )
    days = int (boottime / 86400)

    m1 = CheckItem('boottime',boottime,"Seconds since last reboot")
    c.add_item(m1)

    m2 = CheckItem('boottime_days',days,'Days since last reboot')
    c.add_item(m2)

    return c


# instance checks from list

def check_mounts(item):
    c = Check(checkname='mount') 
    return c


def check_disks(item):

    c = Check(checkname='disk') 
    path = item['path']
    alert_threshold = int(item['alert'])

    # sdiskusage(total=21378641920, used=4809781248, free=15482871808, percent=22.5)
    disk=psutil.disk_usage(path)

    ci = CheckItem('disk',path,"Path")
    c.add_item(ci)

    ci = CheckItem('disk_total',disk[0],"Total (Bytes)")
    c.add_item(ci)

    ci = CheckItem('disk_free',disk[2],"Free (Bytes)")
    c.add_item(ci)

    ci = CheckItem('disk_percent',disk[3],"Used (percent)")
    if disk[3] > alert_threshold:
        ci.alert=True
        ci.alert_message = "check_disk for {} - critical capacity alert ({} %)".format(path,disk[3])
    c.add_item(ci)

    return c


def check_urls(item):

    c = Check(checkname='url') 

    name = item['name']
    url = item['url']
    pattern = item['pattern']
    
    ci = CheckItem('url',name,'')
    c.add_item(ci)


    try:
        resp = requests.get(url, timeout=3)
    except:
        #alert_add("check_url - {} - no response to query".format(name))
        ci = CheckItem('url_status','nok','')
        ci.description = 'no response to query'
        c.add_item(ci) 
        return c

    if resp.status_code != 200:
        ci = CheckItem('url_status','nok','')
        ci.description = 'bad response code : ' + str(resp.status_code)
        ci.alert = True
        ci.alert_message =  "check_url - {} - bad http code response ({})".format(name,resp.status_code)
        c.add_item(ci) 
        return c

    # check pattern
    mysearch = re.search(pattern,resp.text)
    if not mysearch:
        ci = CheckItem('url_status','nok','')
        ci.description = 'expected pattern not found'
        ci.alert=True
        ci.alert_message = "check_url - {} - expected pattern not found.".format(name)
        c.add_item(ci) 
        return c

    ci = CheckItem('url_status','ok','')
    c.add_item(ci) 

    return c

# --------------
# Checks - TODO
# --------------

# check_process
# check_path_exists
# check_socket_listen
# check_tcp_socket
# check_ping

# check_mount
# check_ntp
# check_file_count


# check_systemctl_status

# check_dir_size
# check_file_count
# check_file_age
# check_file_content
# check_line_in_file
# check_apache_status
# check_fpm_ping
# check_fpm_status
# check_redis
# check_nfs
# check_mysql

# check_lastlog
# check_account

# check_sql_query
# check_elastic_query
# check_external_script


    #tcp=psutil.net_connections(kind='tcp4')


    # sdiskpart(device='/dev/sda1', mountpoint='/', fstype='ext4', 
    #               opts='rw,relatime,errors=remount-ro,data=ordered')
    # partitions=psutil.disk_partitions(all=False)

    #users = psutil.users()
    #[suser(name='giampaolo', terminal='pts/2', host='localhost', started=1340737536.0, pid=1352),
    #    suser(name='giampaolo', terminal='pts/3', 
    #             host='localhost', started=1340737792.0, pid=1788)]

    #{'name': 'python3', 'cpu_times': pcputimes(user=0.39, system=0.3, 
    #    children_user=0.0, children_system=0.0), 
    #    'memory_info': pmem(rss=27049984, vms=123904000, shared=13443072, text=3883008, 
    #    lib=0, data=13901824, dirty=0), 'username': 'phil', 'pid': 3125}
    #for proc in psutil.process_iter(['pid', 'name', 'username','cpu_times','memory_info']):
    #     #print(proc.info)



# =====================================================================
# MAPs : map Check names to python functions
# =====================================================================

CHECK_MAP = {
    "load"     : check_load,
    "cpu"      : check_cpu,
    "memory"   : check_memory,
    "swap"     : check_swap,
    "boottime" : check_boottime,

}

CHECK_MAP_MULTIPLE = {
    "mounts"    : check_mounts,
    "disks" : check_disks,
    "urls" : check_urls,
}


# =====================================================================

if __name__=="__main__":

    # set global timer to limit global duration
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(MAX_EXECUTION_TIME)   #  seconds
    
    print()
    logit(bcolors.BOLD + "CMT Stating" + bcolors.ENDC)
    print('-' * 36)


    ARGS = parse_arguments()    

    # conf.yml and conf.d/*.yml
    CONF = load_conf()

    # TODO : check config option


    # Send test message to Teams
    if ARGS["teamstest"]:
        teams_test()
        exit()

    # TODO : list modules


    report = Report()

    # single checks
    for key in CHECK_MAP:
        if is_check_active(key):        
            check = CHECK_MAP[key]()
            check.print_to_cli()
            check.send_to_server()
            report.add_check(check)

    # multiple checks (list of items in conf)
    for key in CHECK_MAP_MULTIPLE:
        if is_check_active(key):        
            if key in CONF:
                for item in CONF[key]:
                    check = CHECK_MAP_MULTIPLE[key](item)
                    check.print_to_cli()
                    check.send_to_server()
                    report.add_check(check)

    # alerts
    report.print_alerts_to_cli()
    if ARGS["alert"]:
        report.send_alerts()



