# cavaliba.com - 2021
# conf.py

import os
import sys
import time
import datetime
import json
import yaml
import requests

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
    conf_add_top_entries(conf)
    conf_add_default_modules(conf)

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
        # print(CONF)
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
    except requests.exceptions.RequestException as e:
        debug("Load remote conf failed : {} - {}".format(r.status_code, e))
        return None

    if r.status_code != 200:
        debug("Load remote conf failed : {}".format(+ r.status_code))
        return None

    debug("Load remote conf OK : ", r.text)
    return r.text


def conf_merge(conf1, conf2):

    debug("merge conf")
    for topitem in cmt.DEFAULT_CONF_TOP_ENTRIES:
        for k in conf2[topitem]:
            conf1[topitem][k] = conf2[topitem][k]

    # new conf format Ver. 1.2.0
    for topitem in cmt.GLOBAL_MODULE_MAP:
        for k in conf2[topitem]:
            conf1[topitem][k] = conf2[topitem][k]


def conf_add_default_modules(conf):
    ''' complete conf with optionnal/default module entries.'''

    for key in cmt.GLOBAL_MODULE_MAP:
        if key not in conf['modules']:
            conf['modules'][key] = {}


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
    myconfig = str(myconfig)

    if myconfig == "True" or myconfig == "yes" or myconfig == "true":
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

    if action == "ho":
        myday = datetime.datetime.today().strftime("%a")
        myhour = datetime.datetime.today().strftime("%H:%M:%S")
        if myday in ["Sat", "Sun"]:
            return False
        if myhour < "08:30:00" or myhour > "18:00:00":
            return False
        return True

    if action == "hno":
        myday = datetime.datetime.today().strftime("%a")
        myhour = datetime.datetime.today().strftime("%H:%M:%S")
        if myday in ["Mon", "Tue", "Wed", "Thu", "Fri"]:
            if myhour >= "08:30:00" or myhour <= "18:00:00":
                return False
        return True

    # default, unknown / no match
    return False


def is_module_active_in_conf(module):
    ''' check if module (name) is enabled in config '''

    if module not in cmt.CONF['modules']:
        debug("module not in conf :", module)
        # DEFAULT : True
        return True

    timerange = cmt.CONF['modules'][module].get("enable", "yes")

    if is_timeswitch_on(timerange):
        return True

    debug("module not enabled in conf : ", module)
    return False


def get_hysteresis(check):
    ''' return configuration for alert_delay, resume_delay
        with inheritance: check, module, global, DEFAULT.
    '''

    alert_delay = 0

    if "alert_delay" in check.conf:
        alert_delay = int(check.conf["alert_delay"])

    elif "alert_delay" in cmt.CONF['modules'][check.module]:
        alert_delay = int(cmt.CONF['modules'][check.module]['alert_delay'])

    else:
        alert_delay = cmt.CONF['global'].get("alert_delay",
                                             cmt.DEFAULT_HYSTERESIS_ALERT_DELAY
                                             )

    return alert_delay
