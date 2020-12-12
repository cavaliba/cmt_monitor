#!/usr/bin/python3
# cavaliba.com - 2020 - CMT_monitor - cmt.py

import os
import sys
import time
import datetime
import signal
#import re

import psutil
import requests

# global variables
import cmt_globals as cmt

# shared functions and class
from cmt_shared import perform_check
from cmt_shared import logit, debug, debug2, abort, bcolors
from cmt_shared import parse_arguments
from cmt_shared import load_conf
from cmt_shared import display_version, display_modules
from cmt_shared import pager_test
from cmt_shared import is_module_active_in_conf
from cmt_shared import is_module_allowed_in_args
from cmt_shared import is_timeswitch_on

from cmt_shared import Report, Check, CheckItem
from cmt_shared import Persist

from cmt_helper import timeout_handler



# ------------
# Main entry
# ------------

if __name__=="__main__":


    cmt.ARGS = parse_arguments()

    if cmt.ARGS["version"]:
        display_version()
        sys.exit()

    # conf.yml and conf.d/*.yml and remote conf (url)
    cmt.CONF = load_conf()


    maxexec = cmt.CONF['global'].get("max_execution_time", cmt.MAX_EXECUTION_TIME)
    # set global timer to limit global duration
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(maxexec)   #  seconds


    # Persist
    cmt.PERSIST = Persist(file=cmt.DEFAULT_PERSIST_FILE)

    lastrun = cmt.PERSIST.get_key("cmt_last_run", 0)

    # check config option
    if cmt.ARGS["checkconfig"]:
        logit("config OK. use --debug to see full config.")
        sys.exit()

    # test if global run is enabled
    tmp = cmt.CONF.get('enabled','yes')
    if not is_timeswitch_on(tmp):
        logit("CMT disabled by global configuration.")
        sys.exit()

    # Send test message to Teams
    if cmt.ARGS["pagertest"]:
        pager_test()
        sys.exit()

    if cmt.ARGS["listmodules"]:
        display_modules()
        sys.exit()



    # check master switch / CMT disabled ?
    
    ts_global_enable = cmt.CONF['global'].get('enable', 'no')
    if not is_timeswitch_on(ts_global_enable):
        logit("CMT globally disabled by conf")
        sys.exit()

    # -----------------
    report = Report()
    report.print_header()


    # LOOP over each individual check in CONF
    for checkname in cmt.CONF['checks']:

        check_result = perform_check(checkname)

        if type(check_result) is str:
            if check_result == "break":
                break
            elif check_result == "continue":
                continue
        else:
            # add Check to report
            report.add_check(check_result)

    # -- end of check loop --

    report.dispatch_alerts()
    report.print_recap()

    cmt.PERSIST.save()

