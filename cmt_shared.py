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
# from cmt_globals import *


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
    if cmt.ARGS['debug'] or cmt.ARGS['debug2']:
        print('DEBUG :',' '.join(items))

def debug2(*items):
    if cmt.ARGS['debug2']:
        print('DEBUG2:',' '.join(items))

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

    parser.add_argument('--cron', help='equiv to report, alert, persist, short output',
        action='store_true', required=False)


    parser.add_argument('--report', help='send events to Metrology servers',
        action='store_true', required=False)
    parser.add_argument('--pager', help='send alerts to Pagers',
        action='store_true', required=False)
    parser.add_argument('--persist', help='persist data accross CMT runs (use in cron)',
        action='store_true', required=False)

    parser.add_argument('--conf', help='specify alternate yaml config file',
        action='store', required=False)

    parser.add_argument('modules', nargs='*',
        action='append', help='modules to check')
    parser.add_argument('--listmodules', help='display available modules',
        action='store_true', required=False)
    parser.add_argument('--available', help='display available entries found for modules (manual run on target)',
        action='store_true', required=False)


    parser.add_argument('--pagertest', help='send test message to teams and exit',
        action='store_true', required=False)
    parser.add_argument('--no-pager-rate-limit', help='disable pager rate limit',
        action='store_true', required=False)

    parser.add_argument('--checkconfig', help='checkconfig and exit',
        action='store_true', required=False)
    parser.add_argument('--version', '-v', help='display current version',
        action='store_true', required=False)
    parser.add_argument('--debug', help='verbose/debug output',
        action='store_true', required=False)
    parser.add_argument('--debug2', help='more debug',
        action='store_true', required=False)
    parser.add_argument('--devmode', help='dev mode, no pager, no remote metrology',
        action='store_true', required=False)
    
    parser.add_argument('--short','-s', help='short compact cli output',
        action='store_true', required=False)



    return vars(parser.parse_args())


# ------------------------------------------------------------
# Configuration management
# ------------------------------------------------------------
def load_conf():

    debug("Load conf")

    conf = load_conf_master()
    conf = conf_add_default_modules(conf)
    conf = load_conf_dirs(conf)
    conf = load_conf_remote(conf)

    return conf



def load_conf_master():

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
    conf = conf_add_top_entries(conf)

    return conf


def load_conf_dirs(conf):

    debug("Load conf dirs")

    # load_confd
    loadconfd = conf['global'].get("load_confd","no")

    if loadconfd == False or loadconfd =="no" :
        return conf

    # conf.d/*/yml  to ease ansible or modular configuration
    config_dir = os.path.join(cmt.HOME_DIR, "conf.d")

    # check if conf.d exists
    if not os.path.exists(config_dir):
        debug ("no conf.d/ found. Ignoring.")
        return conf

    # scan and merge
    for item in os.scandir(config_dir):
        if item.is_file(follow_symlinks=False):
            if item.name.endswith('.yml'):
                debug2("Additionnal config file found : ",item.path)
                conf2 = conf_load_file(item.path)
                conf2 = conf_add_top_entries(conf2)
                conf = conf_merge(conf, conf2)

    return conf


def load_conf_remote(conf):

    debug("Load remote conf")

    # load remote config from conf_url parameter
    if 'conf_url' in conf['global']:

        url = conf['global']['conf_url']
        gro = conf['global'].get("cmt_group","nogroup")
        nod = conf['global'].get("cmt_node","nonode")

        # if url[-1] == '/':
        #     url = url + "{}_{}.txt".format(gro,nod)
        url = url + "?group={}&node={}".format(gro,nod)
        
        debug("Remote config URL : ", url)


        text_conf2 = conf_load_http(url)
        conf2 = yaml.safe_load(text_conf2)
        if conf2 is None:
            conf2={}
        conf2 = conf_add_top_entries(conf2)
        conf = conf_merge(conf, conf2)

    debug("Configuration loaded")
    debug2(json.dumps(conf, indent=2))

    return conf

# -----------
def conf_add_default_modules(conf):

    for key in cmt.GLOBAL_MODULE_MAP:
        #print("  - ", key )
        if key not in conf['modules']:
            conf['modules'][key] = {}
    return conf

# -----------
def conf_add_top_entries(conf):

    # add missing top entries
    for item in cmt.DEFAULT_CONF_TOP_ENTRIES:
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
def conf_load_http(url):

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
    for topitem in cmt.DEFAULT_CONF_TOP_ENTRIES:
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
        # DEFAULT : True
        return True

    timerange = cmt.CONF['modules'][module].get("enable", "yes")

    if is_timeswitch_on(timerange):
        return True

    debug("module not enabled in conf : ", module)
    return False


def conf_get_hysteresis(check):
    ''' return configuration for alert_delay, resume_delay
        with inheritance: check, module, global, DEFAULT.
    '''

    alert_delay = 0

    if "alert_delay" in check.conf:
        alert_delay = int(check.conf["alert_delay"])

    elif "alert_delay" in cmt.CONF['modules'][check.module]:
        alert_delay =  int(cmt.CONF['modules'][check.module]['alert_delay'])

    else:
        alert_delay = cmt.CONF['global'].get("alert_delay", cmt.DEFAULT_HYSTERESIS_ALERT_DELAY)

    return alert_delay

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


def pager_test():

    pagerconf = cmt.CONF['pagers'].get('test')
    url = pagerconf.get('url')
    debug ("pager url :", url)

    origin = cmt.CONF['global']['cmt_group'] + '/' + cmt.CONF['global']['cmt_node']
    color="0000FF"
    title = "TEST TEST from " + origin
    message = "Test message to Teams. Please ignore."
    if cmt.ARGS['devmode']:
        # DEVMODE to stdout
        print("DEVMODE : url=({}), title=({}), message=({}), color=({}), origin=({})".format(url, title, message, color, origin))
        return
    # REAL
    r = teams_send(url=url, title=title, message=message ,color=color, origin=origin)
    logit("Teams test : " + str(r) )


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

    graylog_data += '"cmt_node_env":"{}",'.format(check.node_env)
    graylog_data += '"cmt_node_role":"{}",'.format(check.node_role)
    graylog_data += '"cmt_node_location":"{}",'.format(check.node_location)

    graylog_data += '"cmt_module":"{}",'.format(check.module)
    graylog_data += '"cmt_check":"{}",'.format(check.module)    # deprecated
    graylog_data += '"cmt_id":"{}",'.format(check.get_id())

    # cmt_message  : Check name + check.message + all items.alert_message
    m ="{} - ".format(check.module)
    m = m + check.get_message_as_str()
    graylog_data += '"short_message":"{}",'.format(m)
    graylog_data += '"cmt_message":"{}",'.format(m)
    #print("ooo    ",m)

    # check items key/values
    for item in check.checkitems:
        graylog_data += '"cmt_{}":"{}",'.format(item.name, item.value)
        debug("Build gelf data : ", str(item.name), str(item.value))

    # cmt_alert ?
    if check.alert > 0:
        has_alert = "yes"
    else:
        has_alert= "no"
    graylog_data += '"cmt_alert":"{}",'.format(has_alert)

    # cmt_warn ?
    if check.warn > 0:
        has_warn = "yes"
    else:
        has_warn= "no"
    graylog_data += '"cmt_warning":"{}",'.format(has_warn)

    # cmt_notice ?
    if check.notice > 0:
        has_notice = "yes"
    else:
        has_notice= "no"
    graylog_data += '"cmt_notice":"{}"'.format(has_notice)


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
        return key in self.dict

    def get_key(self,key , value = None):
        return self.dict.get(key,value)


    def set_key(self, key, value):
        self.dict[key]=value


    def delete_key(self,key):
        self.dict.pop(key, None)


    def load(self):
        debug("Persist.load() : ", self.file)
        data = ""
        try:
            with open(self.file,"r") as fi:
                data=fi.read()
        except:
            debug("ERROR - Persist() : couldn't read file {}".format(self.file))
        # decoding the JSON to dictionay
        try:
            self.dict = json.loads(data)
        except:
            debug("ERROR - Persist() : couldn't decode data")


    def save(self):

        debug("Persist.write() : ", self.file)
        data = json.dumps(self.dict, indent=2)
        try:
            with open(self.file,"w") as fi:
                fi.write(data)
        except:
            debug("ERROR - Persist() : couldn't write file {}".format(self.file))




# ----------------------------------------------------------
# Class CheckItem
# ----------------------------------------------------------

class CheckItem():

    ''' Store one single data point '''

    def __init__(self, name, value, description="", unit=''):
        self.name = name
        self.value = value
        self.description = description
        self.unit = unit

    def fmt_bytes(self,num, suffix='B'):
        for unit in ['','K','M','G','T','P','E','Z']:
            if abs(num) < 1000.0:
                return "%3.1f %s%s" % (num, unit, suffix)
            num /= 1000.0
        return "%.1f %s%s" % (num, 'Y', suffix)

    def fmt_hms(self, sec):
        a = datetime.timedelta(seconds = sec)
        return str(a)

    def human(self):
        '''Build an optional ()  human formatted string for some units values'''
        if self.unit == 'bytes':
            x = self.fmt_bytes(int(self.value))
            return str(x)
        elif self.unit == 'seconds':
            x = self.fmt_hms(int(self.value))
            return x
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

    def __init__(self, module="nomodule", name="noname", conf = {}):

        self.group = cmt.CONF['global'].get('cmt_group','nogroup')
        self.node = cmt.CONF['global'].get('cmt_node', 'nonode')
        self.node_env = cmt.CONF['global'].get('cmt_node_env', 'noenv')
        self.node_role = cmt.CONF['global'].get('cmt_node_role', 'norole')
        self.node_location = cmt.CONF['global'].get('cmt_node_location', 'nolocation')
        self.module = module
        self.name = name

        self.message = []

        self.alert = 0
        self.warn = 0
        self.notice = 0
        self.checkitems=[]

        # set by framework after Check is performed, if pager_enable and alert>0
        self.pager = False

        # fields from conf
        self.conf = conf


        # persist values from previous run for same get_id()
        id = self.get_id()
        self.persist = cmt.PERSIST.get_key(id,{})

        # compute alert_max_level
        self.alert_max_level = "alert"   # DEFAULT
        # check level ?
        a = conf.get('alert_max_level','')
        if a in ['alert','notice','warn']:
            self.alert_max_level = a
        else:
            # module level ?
            b = cmt.CONF['modules'][self.module].get('alert_max_level','')
            if b in ['alert','notice','warn']:
                self.alert_max_level = b
            else:
                # global level
                c = cmt.CONF['global'].get('alert_max_level','')
                if c in ['alert','notice','warn']:
                    self.alert_max_level = c



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


    def adjust_alert_max_level(self, level = ""):

        if level == "":
            level = self.alert_max_level

        debug("adjust alert_max_level to : ", level)

        if level == "alert":
            return

        if level == "warn":
            self.notice = self.warn
            self.warn = self.alert
            self.alert = 0
            return

        if level == "notice":
            self.notice = self.alert
            self.alert = 0
            self.warn = 0


    def frequency(self):
        ''' 
        verify and update run frequency (cron mode).
        Return True/False if allowed/not alloowed to run.
        Update PERSIST() object
        '''
        # last run for this check ?
        freqpersist = cmt.PERSIST.get_key("frequency", {})
        id = self.get_id()
        freqlastrun = freqpersist.get(id,0)

        # frequency for this specific check ?
        f = self.conf.get('frequency',-1)

        if f == -1:
            debug("Frequency: no Frequency at check level")
            # frequency at the module level ?
            modconf = cmt.CONF['modules'].get(self.module, {})
            f2 = modconf.get('frequency',-1)

            # no frequency specified, return True / no persist
            if f2 == -1:
                debug("Frequency: no Frequency at module level")
                return True
            else:
                f = f2

        # yes, compare value / delta ; update persist if Run
        now = int(time.time())
        delta = int ( now - freqlastrun )
        if delta > f:
            freqpersist[id] = now
            cmt.PERSIST.set_key("frequency",freqpersist)
            debug("Frequency: allowed {} > {} (f={}, delta={})".format(now, freqlastrun, f, delta))
            return True

        # too early
        debug("Frequency: not allowed : f={}, delta={}".format(f, delta))
        return False


    def  hysteresis_filter(self):

        ''' Apply Hystereris up/down to alert for this check :
            - consecutive alerts (duration) needed to define real alert
            - consecutire no_alert (idem) needed to define return to noalert
        '''

        # seconds for state transition normal to alert (if alert)
        alert_delay = conf_get_hysteresis(self)

        hystpersist = cmt.PERSIST.get_key("hysteresis", {})
        id = self.get_id()
        hystpersist_item = hystpersist.get(id,{})

        hystlastrun = hystpersist_item.get('lastrun',0)
        now = int(time.time())
        delta = int ( now - hystlastrun )

        duration_alert = hystpersist_item.get('duration_alert',0)
        oldstate = hystpersist_item.get('state','normal')

        newstate = oldstate

        #print("Hysteresis", duration_alert, delta, alert_delay)

        if self.alert > 0 :
            if oldstate == "normal":
                duration_alert += delta
                if duration_alert > alert_delay:
                    # transition to up
                    debug2("Transition to alert", duration_alert, delta, alert_delay)
                    newstate = "alert"
        else:
            newstate = "normal"
            duration_alert = 0

        # not yet a real alert
        if self.alert > 0 and newstate == "normal":
            # adjust to warn ; not a transition
            self.adjust_alert_max_level("warn")

        # write to Persist
        # lastrun
        # BUG
        hystpersist_item['lastrun'] = now
        hystpersist_item['duration_alert'] = duration_alert
        hystpersist_item['state'] = newstate
        hystpersist[id] = hystpersist_item
        cmt.PERSIST.set_key("hysteresis",hystpersist)



    def print_to_cli_short(self):

        head = bcolors.OKGREEN     + "OK     " + bcolors.ENDC

        if self.alert > 0:
            head = bcolors.FAIL    + "NOK    " + bcolors.ENDC
        elif self.warn > 0:
            head = bcolors.WARNING + "WARN   " + bcolors.ENDC
        elif self.notice > 0:
            head = bcolors.OKBLUE  + "NOTICE " + bcolors.ENDC

        #print(head, self.get_message_as_str())
        print("{:12} {:12} {}".format(head, self.module, self.get_message_as_str()))


    def print_to_cli_detail(self):

        print()
        print(bcolors.OKBLUE + bcolors.BOLD + "Check", self.module, bcolors.ENDC)

        for i in self.checkitems:

            v = str (i.value) 
            if len(str(i.unit)) > 0:
                v = v + ' ' + str(i.unit) + ' '
            if len (str(i.human())) > 0:
                v = v + ' [' + i.human() + ']'
            if len (i.description) > 0:
                v = v + ' - ' + i.description

            print("cmt_{:20} {}".format(i.name, v))


        head = bcolors.OKGREEN     + "OK     " + bcolors.ENDC

        if self.alert > 0:
            head = bcolors.FAIL    + "NOK    " + bcolors.ENDC
        elif self.warn > 0:
            head = bcolors.WARNING + "WARN   " + bcolors.ENDC
        elif self.notice > 0:
            head = bcolors.OKBLUE  + "NOTICE " + bcolors.ENDC

        print("{:33} {}".format(head, self.get_message_as_str()))


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

        self.pager = False

    def add_check(self, c):

        self.checks.append(c)
        self.alert += c.alert
        self.warn += c.warn
        self.notice += c.notice

        # propagate Pager from check to report
        if c.pager:
            self.pager = True

    def print_alerts_to_cli(self):
        ''' print pager/alerts to CLI '''

        print()
        print("Notification Summary")
        print("--------------------")
        print()
        if self.notice == 0:
            print(bcolors.OKBLUE + bcolors.BOLD + "No notice", bcolors.ENDC)
        else:
            print(bcolors.OKBLUE + bcolors.BOLD + "Notice", bcolors.ENDC)
            for c in self.checks:
                    if c.notice > 0:
                        print ("{:15s} : {}".format(c.module, c.get_message_as_str()))

        print()
        if self.warn == 0:
            print(bcolors.OKGREEN + bcolors.BOLD + "No warnings", bcolors.ENDC)
        else:
            print(bcolors.WARNING + bcolors.BOLD + "Warnings", bcolors.ENDC)
            for c in self.checks:
                    if c.warn > 0:
                        print ("{:15s} : {}".format(c.module, c.get_message_as_str()))
        print()
        if self.alert == 0:
            print(bcolors.OKGREEN + bcolors.BOLD + "No alerts", bcolors.ENDC)
        else:
            print(bcolors.FAIL + bcolors.BOLD + "Alerts", bcolors.ENDC)
            for c in self.checks:
                    if c.alert > 0:
                        print ("{:15s} : {}".format(c.module, c.get_message_as_str()))
        print()


    def print_recap(self):
        ''' display one line with number of checks, alert, warn, notice.'''
        pass
        ck = 0
        alert = 0
        warn = 0
        notice = 0
        for c in self.checks:
            ck += 1
            if c.alert > 0:
                alert += 1
            if c.warn > 0:
                warn += 1
            if c.notice > 0:
                notice += 1
        nok = alert + warn + notice
        ok = ck - nok
        print()
        logit("Done - {} checks - {} ok - {} nok - {} alerts - {} warning - {} notice.".format(
            ck, ok, nok, alert,warn,notice,
            ))

    def send_alerts_to_pager(self):

        ''' Send alerts to Pagers '''

        # check if alert exists
        if not self.pager:
            debug("Pager : no Pager to be fired")
            return

        # check if Pager enabled globally (global section, master switch)
        tmp = cmt.CONF['global'].get("enable_pager", "no")
        if not is_timeswitch_on(tmp):
            debug("Pager  : disabled/inactive in global config.")
            return

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

        # check rate_limit
        t1 = int (cmt.PERSIST.get_key("pager_last_send", 0))
        t2 = int(time.time())
        rate = int (cmt.CONF['global'].get("pager_rate_limit",7200))

        if not cmt.ARGS['no_pager_rate_limit']:
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
                    message += 'ALERT: '
                    message += c.get_message_as_str()
                    message += '<br>\n'
                if c.warn > 0:
                    message += 'WARN: '
                    message += c.get_message_as_str()
                    message += '<br>\n'
                if c.notice > 0:
                    message += 'NOTICE: '
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
        cmt.PERSIST.set_key("pager_last_send",t2)




