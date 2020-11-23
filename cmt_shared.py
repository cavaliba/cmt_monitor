# cavaliba.com - 2020 - CMT_monitor - cmt.py 
# cmt_shared.py
#    - common functions, class and structures


import os
import socket
import sys
import time
import datetime
import argparse
import yaml
import json

import requests
requests.packages.urllib3.disable_warnings()

import cmt_globals as cmt
from cmt_globals import *


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

def abort(line):
    now = datetime.datetime.today().strftime("%Y/%m/%d - %H:%M:%S")
    print(now + ' : ' + line)
    print("ABORTING.")
    sys.exit()

def debug(*items):
    if cmt.ARGS['debug']:
        print('DEBUG:',' '.join(items))

# def debug2(*items):
#     if cmt.ARGS['debug2'] or cmt.ARGS['debug']:
#         print('DEBUG2:',' '.join(items))

# ----------------------------------------------------------
# Helper functions
# ----------------------------------------------------------

def is_timeswitch_on(myconfig):
    ''' check if a date/time time range is active
        myconfig can be :
              yes
              no
              after YYYY-MM-DD hh:mm:ss
              before YYYY-MM-DD hh:mm:ss
              hrange  hh:mm:ss hh:mm:ss
              ho   (Mon-Fri 8h30-18h)
              hno
        returns True or False if current datatime match myconfig
    '''

    # yaml gotcha
    myconfig = str (myconfig)

    if myconfig == "True" or myconfig == "yes" or myconfig == "true":
        return True

    if myconfig == "False" or myconfig =="no"  or myconfig == "false":
        return False
    
    myarray = myconfig.split()
    action = myarray.pop(0)
    
    if action  == "after":
        mynow = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        target = ' '.join(myarray)
        #print(mynow)
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

    if action == "ho":
        myday  = datetime.datetime.today().strftime("%a")
        myhour = datetime.datetime.today().strftime("%H:%M:%S")
        if myday in ["Sat","Sun"]:
            return False
        if myhour < "08:30:00" or myhour > "18:00:00":
            return False
        return True

    if action == "hno":
        myday  = datetime.datetime.today().strftime("%a")
        myhour = datetime.datetime.today().strftime("%H:%M:%S")
        if myday in ["Mon","Tue","Wed","Thu","Fri"]:
            if myhour >= "08:30:00" or myhour <= "18:00:00":
                return False
        return True

    # default, unknown / no match
    return False

# -----------------------------------------------------
# short commands
# -----------------------------------------------------
def display_version():
    print(cmt.VERSION)

def display_modules():
    display_version()
    print()
    print("Available modules")
    print("-----------------")

    for key in cmt.GLOBAL_MODULE_MAP:
        print("  - ", key )
    

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
#    parser.add_argument('--debug2', help='more debug', 
#        action='store_true', required=False)


    parser.add_argument('--status','-s', help='compact cli output with status only', 
        action='store_true', required=False)
    parser.add_argument('--devmode', help='dev mode, no pager, no remote metrology', 
        action='store_true', required=False)    
    parser.add_argument('modules', nargs='*',  
        action='append', help='modules to check')
    parser.add_argument('--version', '-v', help='display current version', 
        action='store_true', required=False)
    parser.add_argument('--listmodules', help='display available modules', 
        action='store_true', required=False)
    parser.add_argument('--available', help='display available entries found for modules (manual run on target)', 
        action='store_true', required=False)
    parser.add_argument('--conf', help='specify alternate yaml config file', 
        action='store', required=False)


    return vars(parser.parse_args())


# ------------------------------------------------------------
# Configuration management
# ------------------------------------------------------------

def load_conf():

    # TODO : accept config as a parameter, check default locations
    if cmt.ARGS['conf']: 
        config_file = cmt.ARGS['conf']    
    else:        
        config_file = os.path.join(cmt.HOME_DIR, "conf.yml")    
    
    debug("Config file : ", config_file)

    if not os.path.exists(config_file):
        abort('Config file not found : ' + config_file)
        sys.exit()

    # load master conf
    conf = conf_load_file(config_file)
    conf = conf_add_top_entries(conf)


    # conf.d/*/yml  to ease ansible or modular deployment
    config_dir = os.path.join(cmt.HOME_DIR, "conf.d")

    # check if conf.d exists
    if not os.path.exists(config_dir):
        debug ("no conf.d/ found. Ignoring.")
        return conf

    # scan and merge
    for item in os.scandir(config_dir):
        if item.is_file(follow_symlinks=False):
            if item.name.endswith('.yml'):
                debug("Additionnal config file found : ",item.path)
                conf2 = conf_load_file(item.path)
                conf2 = conf_add_top_entries(conf2)
                conf = conf_merge(conf, conf2)


    # load remote config from conf_url parameter
    if 'conf_url' in conf['global']:
        debug("Remote config URL : ", conf['global']['conf_url'])
        text_conf2 = conf_load_remote(conf['global']['conf_url'])
        conf2 = yaml.safe_load(text_conf2)
        if conf2 is None:
            conf2={}
        print(type(conf2),conf2)
        conf2 = conf_add_top_entries(conf2)
        conf = conf_merge(conf, conf2)

    debug("Configuration loaded")
    debug(json.dumps(conf, indent=2))
    
    return conf

# -----------
def conf_add_top_entries(conf):

    # add missing top entries
    # TODO : move list to DEFAULTs
    for item in ['global','modules','checks','metrology_servers', 'pagers']:
        if not item in conf:
            debug("No {} entry in config ; added automatically.".format(item))
            conf[item] = {}

    return conf

# -----------
# load a single file
def conf_load_file(config_file):
    
    with open(config_file) as f:
        conf = yaml.load(f, Loader=yaml.SafeLoader)
        #print(CONF)
        #print(json.dumps(CONF, indent=2))

    # # verify content  
    if conf is None:
        return {}
    #    abort("Bad config; Exiting.")
    #     sys.exit()

    return conf

# -----------
def conf_load_remote(url):

        headers = {
            'Content-Type' : 'application/text'
        }

        if cmt.ARGS['devmode']:
            print("DEVMODE : GET ",url,headers)

        # real
        try:
            r = requests.get(url,headers=headers, timeout = cmt.REMOTE_CONFIG_TIMEOUT)
            result = r.text
        except:
            result = "---\n"
        debug("remote conf:",result)
        return result

# -----------
def conf_merge(conf1, conf2):

    debug("merge conf ")
    for topitem in ['global','modules','checks','metrology_servers', 'pagers']:
        #print("  topitem = ", topitem,  "conf2 = " , conf2[topitem], type)
        #print (type(conf2[topitem]))
        for k in conf2[topitem]:
            #print("k=",k)
            conf1[topitem][k] = conf2[topitem][k]
    return conf1

# ------------------
def is_module_allowed_in_args(name):
    modules = cmt.ARGS['modules'][0]
    if name in modules  or len(modules) == 0 :
        return True
    debug(name, "module not in ARGS")
    return False

# ------------------
def is_module_active_in_conf(module):
    ''' check if module (name) is enabled in config '''

    if not module in cmt.CONF['modules']:
        debug("module not in conf :", module)
        return False

    timerange = cmt.CONF['modules'][module].get("enable", "yes")
    
    if is_timeswitch_on(timerange):
        return True
    
    debug("module not enabled in conf : ", module)
    return False


# ------------------------------------------------------------
#  Pager  TEAMS
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

    # SEND !
    if cmt.ARGS['devmode']:
        print("DEVMODE : ",url,headers,message)
        return 200
    # real
    try:
        r = requests.post(url,headers=headers, data=message, timeout = TEAMS_TIMEOUT)
        return r.status_code
    except:
        return 0


# def teams_is_channel_enabled(channel="test"):
#     for item in cmt.CONF['teams_channel']:
#         if item['name'] == channel:
#             tmp = item.get("enable", "no")
#             if is_timeswitch_on(tmp):
#                 return True
#     return False

def teams_get_url(channel="test"):
    url = ""
    for item in cmt.CONF['teams_channel']:
        if item['name'] == channel:
            url = item['url']
    return url


def teams_test():
    url = teams_get_url(channel="test")
    origin = cmt.CONF['cmt_group'] + '/' + cmt.CONF['cmt_node']
    color="0000FF"
    title = "TEST TEST from " + origin
    message = "Test message to Teams. Please ignore."
    if cmt.ARGS['devmode']:
        print("DEVMODE : ",url, title, message, color, origin)
        return
    # REAL
    r = teams_send(url=url, title=title, message=message ,color=color, origin=origin)
    logit("Teams test : " + str(r) )

# -----------------------
# Pager ALERT rate limit
# -----------------------

def get_last_send():

    t = 0

    cmt.PERSIST.get_key("teams_last_send")

    try:
        file = open(cmt.RATE_LIMIT_FILE,"r")
        t = int(file.readline())
        file.close()
    except:
        t = 0

    return t

def set_last_send(t):

    cmt.PERSIST.set_key("teams_last_send",t)


    try:
        file = open(cmt.RATE_LIMIT_FILE,"w")
        file.write(str(t))
        file.close()
    except:
        pass
    return


# ------------------------------------------------------------
# Metrology Servers 
# ------------------------------------------------------------


# GRAYLOG / GELF
# ---------------

def build_gelf_message(check):
    '''Prepare a GELF JSON message suitable to be sent to a Graylog GELF server.'''

    graylog_data = '"version":"1.1",' 
    graylog_data += '"host":"{}_{}",'.format(check.group, check.node)

    # common values
    graylog_data += '"cmt_group":"{}",'.format(check.group)
    graylog_data += '"cmt_node":"{}",'.format(check.node)
    graylog_data += '"cmt_module":"{}",'.format(check.module)
    # previous version : check (== module)
    graylog_data += '"cmt_check":"{}",'.format(check.module)
    graylog_data += '"cmt_id":"{}",'.format(check.get_id())

    # cmt_message  : Check name + check.message + all items.alert_message
    m ="cmt_check {}".format(check.module)
    m = m + check.get_message_as_str()
    graylog_data += '"short_message":"{}",'.format(m)
    graylog_data += '"cmt_message":"{}",'.format(m)

    # check items key/values
    for item in check.checkitems:
        graylog_data += '"cmt_{}":"{}",'.format(item.name, item.value)
        debug("Build gelf data : ", str(item.name), str(item.value))

    # cmt_alert ?
    if check.alert > 0:
        has_alert = "yes"
    else:
        has_alert= "no"
    
    graylog_data += '"cmt_alert":"{}"'.format(has_alert)

    graylog_data = '{' + graylog_data + '}'
    
    return graylog_data



def graylog_send_http_gelf(url, data=""):
    
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

    if cmt.GRAYLOG_HTTP_SUSPENDED:
        logit("suspended - HTTP graylog message (http/gelf) not sent to " + str(url))
        return

    if cmt.ARGS['devmode']:
        print("DEVMODE : graylog http : ", url, data, headers)
        return

    try:
        r = cmt.SESSION.post(url, data=data, headers=headers, timeout = cmt.GRAYLOG_HTTP_TIMEOUT)    
        debug("Message sent to graylog(http/gelf) ; status = " + str(r.status_code))
    except:
        logit("Error - couldn't send graylog message (http/gelf) to " + str(url))
        cmt.GRAYLOG_HTTP_SUSPENDED = True


def graylog_send_udp_gelf(host, port=12201, data=""):

    #data = '"demo":"42"'
    #mess = '{ "version":"1.1", "host":"host-test", "short_message":"CMT gelf test", ' + data + ' }'  


    if cmt.ARGS['devmode']:
        print("DEVMODE : graylog udp : ", host, port, data)
        return

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
# Class PERSIST
# ----------------------------------------------------------
class Persist():
    ''' Implement a persistent on-disk key/value structure, between cmt runs'''

    def __init__(self, file = None):    
        self.file = file
        self.dict = {}
        self.load()

    def has_key(self,key):
        pass

    def get_key(self,key):
        print("get_key", key)
        pass

    def set_key(self,key, value):
        print("set_key",key,value)
        pass

    def delete_key(self,key, value):
        pass

    def read(self):
        pass

    def load(self):
        pass

    def save(self):
        pass

    

# ----------------------------------------------------------
# Class CheckItem
# ----------------------------------------------------------

class CheckItem():

    ''' Store one single data point with optional status/alert/info.'''

    def __init__(self, name, value, description="", unit=''):
        self.name = name
        self.value = value
        self.description = description
        self.unit = unit

    def sizeof_fmt(self,num, suffix='B'):
        for unit in ['','K','M','G','T','P','E','Z']:
            if abs(num) < 1000.0:
                return "%3.1f %s%s" % (num, unit, suffix)
            num /= 1000.0
        return "%.1f %s%s" % (num, 'Y', suffix)


    def human(self):
        '''Build an optional ()  human formatted string for some units values'''
        if self.unit == 'bytes':
            x = self.sizeof_fmt(int(self.value))
            return '(' + str( x )  + ')'
        else:
            return ''

    
# ----------------------------------------------------------
# Class Check
# ----------------------------------------------------------

class Check():

    '''class Check():
       - Stores multiple CheckItem related to a single Check function run.
       - Each Check is sent as one message to a metrology server like Graylog/Elastic.
       - Count alerts from CheckItem : alert is sent as Yyes/no if any of the checkItem as an alert.
       - Pager alerts are sent globally at the Report level.
    '''

    def __init__(self, module="nomodule", name="noname"):

        self.group = cmt.CONF['global'].get('cmt_group','nogroup')
        self.node = cmt.CONF['global'].get('cmt_node', 'nonode')
        self.module = module
        self.name = name

        self.message = []

        self.alert = 0
        self.warn = 0
        self.notice = 0
        self.checkitems=[]    

    def add_message(self, m):

        self.message.append(m)


    def add_item(self, item):
        ''' add a CheckItem instance to the Check items list '''
        self.checkitems.append(item)          

    def get_id(self):
        ''' Returns unique check id '''
        return "{}.{}.{}.{}".format(self.group, self.node, self.module, self.name)

    def get_message_as_str(self):

        v = ""
        for mm in self.message:
            if len(v) > 0:
                v = v + " ; "
            v = v + mm 
        return v

    def print_to_cli(self):

        if not cmt.ARGS['status']:
            print()
            print(bcolors.OKBLUE + bcolors.BOLD + "Check", self.module, bcolors.ENDC)

        for i in self.checkitems:    

            v = str (i.value) + ' ' + str(i.unit) + ' ' + i.human()
            if len (i.description) > 0:
                v = v + ' - ' + i.description

            # special *_status lines : color + messages
            is_status = False

            if i.name.endswith("_status"):
                is_status = True

                if i.value == "ok":
                    v = bcolors.OKGREEN + "OK " + bcolors.ENDC
                else:
                    v = bcolors.FAIL + "NOK " + bcolors.ENDC
                
                # if len(self.message) > 0:
                #     v = v + " - " + self.message
                # for mm in self.message:
                #     if len(v) > 0:
                #         v = v + " ; "
                v = v + self.get_message_as_str()

            if not cmt.ARGS['status'] or is_status:
                print("cmt_{:18} {}".format(i.name, v))
        

    def send_metrology(self):
        
        ''' Send Check results (event, multiple CheckItems) 
            to metrology servers.
        '''

        graylog_data = build_gelf_message(self)  
        
        for metro in cmt.CONF['metrology_servers']:


            metroconf = cmt.CONF['metrology_servers'][metro]
            metrotype = metroconf.get('type', 'unknown')

            timerange = metroconf.get("enable", "yes")
            if not is_timeswitch_on(timerange):
                debug("Metrology server disabled in conf : ", metro)
                return

            if metrotype == "graylog_udp_gelf":
                host=metroconf['host']
                port=metroconf['port']
                graylog_send_udp_gelf(host=host, port=port, data=graylog_data)
                debug("Data sent to metrology server ", metro)

            elif metrotype == "graylog_http_gelf":
                url=metroconf['url']
                graylog_send_http_gelf(url=url, data=graylog_data)
                debug("Data sent to metrology server ", metro)

            else:
                debug("Unknown metrology server type in conf.")

# ----------------------------------------------------------
# Class Report
# ----------------------------------------------------------

class Report():
    
    '''A Report stores all the Checks from a single run of CMT.
       Pager alerts are sent to Pager targets at the end of the run.
    '''

    def __init__(self):

        self.checks = []
        self.alert = 0
        self.warn = 0
        self.notice = 0


    def add_check(self, c):

        self.checks.append(c)
        self.alert += c.alert
        self.warn += c.warn
        self.notice += c.notice


    def print_alerts_to_cli(self):
        ''' print pager/alerts to CLI '''


        print()
        if self.notice == 0:
            print(bcolors.OKGREEN + bcolors.BOLD + "No notice", bcolors.ENDC)
            print('---------')
        else:
            print(bcolors.OKBLUE + bcolors.BOLD + "Notice :", bcolors.ENDC)
            print('-----------')
            for c in self.checks:
                    if c.notice > 0:
                        print ("{:15s} : {}".format(c.module, c.get_message_as_str()))

        print()
        if self.warn == 0:
            print(bcolors.OKGREEN + bcolors.BOLD + "No warnings", bcolors.ENDC)
            print('-----------')
        else:

            print(bcolors.WARNING + bcolors.BOLD + "Warnings :", bcolors.ENDC)
            print('-----------')
            for c in self.checks:
                    if c.warn > 0:
                        print ("{:15s} : {}".format(c.module, c.get_message_as_str()))
        print()
        if self.alert == 0:
            print(bcolors.OKGREEN + bcolors.BOLD + "No alerts", bcolors.ENDC)
            print('-----------')
        else:

            print(bcolors.FAIL + bcolors.BOLD + "Alerts :", bcolors.ENDC)
            print('--------')
            for c in self.checks:
                    if c.alert > 0:
                        print ("{:15s} : {}".format(c.module, c.get_message_as_str()))
        print()



    

    def send_alerts_to_pager(self):

        ''' Send alerts to Pagers '''

        # check if alert exists
        if self.alert == 0:
            debug("Alerts : no alerts to be sent.")
            return

        # check if Pager enabled globally (global section, master switch)
        tmp = cmt.CONF['global'].get("enable_pager", "no")
        print(tmp)
        if not is_timeswitch_on(tmp):
            debug("Pager  : disabled/inactive in global config.")
            return

        # TODO send_alerts_to_metrology : additionnal "pager"

        # Find 'Alert' Pager         
        if not 'alert' in cmt.CONF['pagers']:
            debug("No alert pager configured.")
            return

        pagerconf = cmt.CONF['pagers'].get('alert')

        # check if the 'Alert' Pager is enabled
        tmp2 = pagerconf.get("enable", "no")
        if not is_timeswitch_on(tmp2):
            debug("Pager  : alert pager disbled in conf.")
            return

        # TODO : replace by Persist()

        # check rate_limit
        t1 = int(get_last_send())
        t2 = int(time.time())
        rate = int (cmt.CONF['global'].get("pager_rate_limit",7200))

        if not cmt.ARGS['devmode']:
            if t2-t1 <= rate:
                logit("Alerts : too many alerts (rate-limit) - no alert sent to Pager")
                return

        # get Teams alert channel url
        url = pagerconf.get('url')
        debug ("pager url :", url)

        # prepare message
        origin = cmt.CONF['global']['cmt_group'] + '/' + cmt.CONF['global']['cmt_node']
        color = "FF0000"
        title = "ALERT from " + origin
        
        message = ""
        for c in self.checks:
                if c.alert > 0:
                    message += c.get_message_as_str()
                    message += '<br>\n'
        debug("Pager Message : ",message)              
        
        # send alert
        r = teams_send(url=url, title=title, message=message ,color=color, origin=origin)
        if r == 200:
            logit("Alerts : alert sent to Teams ")
        else:
            logit("Alerts : couldn't send alert to Teams - response  " + str(r))

        # update rate_limit
        set_last_send(t2)



