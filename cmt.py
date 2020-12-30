#!/usr/bin/python3
# cavaliba.com - 2020 - CMT_monitor - cmt.py

import os
import sys
import time
import signal
import json

# global variables
import cmt_globals as cmt

# shared functions and class
from cmt_shared import perform_check
from cmt_shared import debug, debug2
from cmt_shared import parse_arguments
from cmt_shared import load_conf, load_conf_remote
from cmt_shared import display_version, display_modules
from cmt_shared import pager_test

from cmt_shared import Report
from cmt_shared import Persist

from cmt_helper import timeout_handler
from cmt_helper import bcolors
from cmt_helper import logit, abort
from cmt_helper import is_timeswitch_on

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

    # Persist
    cmt.PERSIST = Persist(file=cmt.DEFAULT_PERSIST_FILE)
    lastrun = cmt.PERSIST.get_key("cmt_last_run", 0)


    # remote conf / cached conf
    load_conf_remote(cmt.CONF)
    

    # check config option
    if cmt.ARGS["checkconfig"]:
        print(json.dumps(cmt.CONF, indent=2))
        print("config OK.")
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


    maxexec = cmt.CONF['global'].get("max_execution_time", cmt.MAX_EXECUTION_TIME)
    # set global timer to limit global duration
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(maxexec)   #  seconds


    # FIRST LOOP : all individual checks entries in CONF
    #  => must contain an module parameter
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

    # SECOND LOOP : alternate configuration
    # checks are below each modulename entries in CONF

    for modulename in cmt.GLOBAL_MODULE_MAP:
        if modulename in cmt.CONF:
            for checkname in cmt.CONF[modulename]:
                check_result = perform_check(checkname, modulename)
                if type(check_result) is str:
                    if check_result == "break":
                        break
                    elif check_result == "continue":
                        continue
                else:
                    # add Check to report
                    report.add_check(check_result)
            # break outer loop as well ; called if inner loop didnt break
            else:
                continue
            break


    # -- end of check loop --

    report.dispatch_alerts()
    report.print_recap()

    cmt.PERSIST.set_key("cmt_last_run",int(time.time()))
    cmt.PERSIST.save()

