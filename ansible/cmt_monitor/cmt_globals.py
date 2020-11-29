# cavaliba.com - 2020 - CMT_monitor - cmt.py 

# cmt_globals

import os
import sys
import requests


from checks.load import check_load
from checks.cpu import check_cpu
from checks.memory import check_memory
from checks.swap import check_swap
from checks.boottime import check_boottime
from checks.mount import check_mount
from checks.disk import check_disk
from checks.url import check_url
from checks.process import check_process
from checks.ping import check_ping
from checks.folder import check_folder


requests.packages.urllib3.disable_warnings()
SESSION = requests.session()

# -----------------
VERSION = "CMT - Version 1.0.0 - (c) Cavaliba.com - 2020/11/29"

MAX_EXECUTION_TIME = 50


#HOME_DIR = os.path.dirname(__file__)
# determine if application is a script file or frozen exe from PyInstaller
if getattr(sys, 'frozen', False):
    HOME_DIR = os.path.dirname(sys.executable)
    HOME_DIR = "/opt/cmt"
elif __file__:
    HOME_DIR = os.path.dirname(__file__)


#RATE_LIMIT_FILE = os.path.join(HOME_DIR, "alert.last")

GRAYLOG_HTTP_TIMEOUT = 5 

# http access to remote url for additional config
REMOTE_CONFIG_TIMEOUT = 3

# post to Teams
TEAMS_TIMEOUT = 5

# Hystereis
# delay before going to alerting state
DEFAULT_HYSTERESIS_ALERT_DELAY = 120
# delay before resuming to normal state
DEFAULT_HYSTERESIS_NORMAL_DELAY = 120

# persist
DEFAULT_PERSIST_FILE = os.path.join(HOME_DIR, "persist.json")


# =====================================================================
# Checks list & MAPs : map Check names to python functions
# =====================================================================

GLOBAL_MODULE_MAP = {
    "load"     : {"check": check_load     },
    "cpu"      : {"check": check_cpu      },
    "memory"   : {"check": check_memory   },
    "swap"     : {"check": check_swap     },
    "boottime" : {"check": check_boottime },
    "mount"    : {"check": check_mount    },
    "disk"     : {"check": check_disk     },
    "url"      : {"check": check_url      },
    "process"  : {"check": check_process  },
    "ping"     : {"check": check_ping     },
    "folder"   : {"check": check_folder   },
}


# ----------------------------
# Globals / can be changed
# ---------------------------


ARGS={}
CONF={}
PERSIST={}

# can be switched to True if no response during current RUN
# TODO : move to run-context ...
GRAYLOG_HTTP_SUSPENDED = False

