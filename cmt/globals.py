# cavaliba.com - 2020 - 2021
# globals.py

import os
import sys

import requests
requests.packages.urllib3.disable_warnings()
SESSION = requests.session()

# -----------------
VERSION = "CMT - (c) cavaliba.com - Version 2.2 - 2021/12/19"
VERSION_NUMBER = "2.2"

# default ; can be overrided in configuration files
MAX_EXECUTION_TIME = 55


# HOME_DIR = os.path.dirname(__file__)
# determine if application is a script file or frozen exe from PyInstaller
if getattr(sys, 'frozen', False):
    # HOME_DIR = os.path.dirname(sys.executable)
    HOME_DIR = "/opt/cmt"
elif __file__:
    # HOME_DIR = os.path.dirname(__file__)
    HOME_DIR = "/opt/cmt"


# http access to remote url for additional config
REMOTE_CONFIG_TIMEOUT = 3

# post to Teams
TEAMS_TIMEOUT = 5
PAGERDUTY_TIMEOUT = 5

# Hystereis
# delay before going to alerting state
DEFAULT_HYSTERESIS_ALERT_DELAY = 120
# delay before resuming to normal state
# DEFAULT_HYSTERESIS_NORMAL_DELAY = 120

# persist
DEFAULT_PERSIST_FILE = os.path.join(HOME_DIR, "persist.json")

# Used to load / merge config
DEFAULT_CONF_TOP_ENTRIES = ['global', 'modules', 'checks', 'metrology_servers', 'pagers']


# Colors for CLI output
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BLACK = '\033[90m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


GRAYLOG_HTTP_TIMEOUT = 5
# can be switched to True if no response during current RUN
GRAYLOG_HTTP_SUSPENDED = False

# for elastic
METROLOGY_HTTP_TIMEOUT = 5
METROLOGY_HTTP_SUSPENDED = False


METROLOGY_INFLUXDB_TIMEOUT = 5
METROLOGY_INFLUXDB_SUSPENDED = False

# map.py with all imports from modules
GLOBAL_MODULE_MAP = {}


# --------------------------
# SEVERITY levels (ordered)
# --------------------------
SEVERITY_CRITICAL = 1
SEVERITY_ERROR = 2
SEVERITY_WARNING = 3
SEVERITY_NOTICE = 4
SEVERITY_NONE = 5

def get_severity_label(severity):

    if severity == SEVERITY_CRITICAL:
        return "CRITICAL"
    elif severity == SEVERITY_ERROR:
        return "ERROR"
    elif severity == SEVERITY_WARNING:
        return "WARNING"
    elif severity == SEVERITY_NOTICE:
        return "NOTICE"
    else:
        return "OK"

# ------------------------
# ALERTS events (trigger)
# ------------------------
ALERT_NONE = 0
ALERT_NEW = 1
ALERT_ACTIVE = 2
ALERT_DOWN = 3


def get_alert_symbol(alert):

    if alert == ALERT_NONE:
        return '( ) '
    if alert == ALERT_NEW:
        return '(+) '
    if alert == ALERT_ACTIVE:
        return '(=) '
    if alert == ALERT_DOWN:
        return '(-) '
    return '(?) '

def get_alert_label(alert):

    if alert == ALERT_NONE:
        return 'NONE'
    if alert == ALERT_NEW:
        return 'NEW'
    if alert == ALERT_ACTIVE:
        return 'ACTIVE'
    if alert == ALERT_DOWN:
        return 'DOWN'
    return 'NA'



# ------------------------
# ARGS - cli parameters
# ------------------------
# args.py / argparse
ARGS = {}

# ----------------------------
# CONF - aggregate all sources
# ----------------------------

CONF = {}

# ----------------------------
# Persistance data
# ----------------------------

PERSIST = {}
