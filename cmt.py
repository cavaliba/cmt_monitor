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

# ------------
# Timeout stop
# ------------
def signal_handler(signum, frame):
    #raise Exception("Timed out!")
    print("Timed out ! (max_execution_time)")
    sys.exit()

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
    signal.signal(signal.SIGALRM, signal_handler)
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


    # -----------------

    if cmt.ARGS['cron']:
        print("-" * 60)    
        logit("Starting ...")    
    
    else:
        print('-' * 60)
        display_version()
        print('-' * 60)
        print("cmt_group      : ", cmt.CONF['global']['cmt_group'])
        print("cmt_node       : ", cmt.CONF['global']['cmt_node'])
        print()
    

    report = Report()

    # check master switch / CMT disabled ?
    ts_global_enable = cmt.CONF['global'].get('enable', 'no')
    if not is_timeswitch_on(ts_global_enable):
        logit("CMT globally disabled by conf")
        sys.exit()

    # LOOP over each individual check in CONF

    for checkname in cmt.CONF['checks']:

        debug("Starting check : ", checkname)

        # get conf for this check
        checkconf = cmt.CONF['checks'][checkname]

        # get module for this check
        modulename = checkconf.get('module', "unknown")
        debug("  module : ", modulename)

        #Is module in GLOBAL MAP ?
        if not modulename in cmt.GLOBAL_MODULE_MAP:
            debug("  unknown module in MAP: ", modulename)
            continue

        # check  enabled in conf ?  (in check or in module)
        ts_check = checkconf.get('enable', 'n/a')
        # no info
        if ts_check == "n/a":
            # module level ?
            if not is_module_active_in_conf(modulename):
                debug("  module disabled in conf")
                continue #no
        elif not is_timeswitch_on(ts_check):
            debug("  check disabled by conf")
            continue

        # check if module is filtered in ARGS
        if not is_module_allowed_in_args(modulename):
            continue

        # TODO : verify frequency

        # create check object
        check_result = Check(module=modulename, name=checkname, conf = checkconf)

        # HERE / Future : give check_result the needed Module Conf, Global Conf ...

        # TODO : if --available, call diffrent function

        # ---------------
        # perform check !
        # ---------------
        check_result = cmt.GLOBAL_MODULE_MAP[modulename]['check'](check_result)

        if cmt.ARGS["available"]:
            break

        # Hysteresis / alert upd & own
        check_result.hysteresis_filter()

        # apply alert_max_level for this check
        check_result.adjust_alert_max_level()

        # If pager enabled (at check level), and alert exists : set pager True
        if check_result.alert > 0:
            tr =  checkconf.get('enable_pager', "no")
            if is_timeswitch_on(tr):
                debug("pager for check ", check_result.get_id())
                check_result.pager = True


        # keep returned Persist structure in check_result
        cmt.PERSIST.set_key(check_result.get_id(), check_result.persist)

        # Print to CLI
        if cmt.ARGS['cron'] or cmt.ARGS['short']:
            check_result.print_to_cli_short()
        else:
            check_result.print_to_cli_detail()

        # Metrology
        if cmt.ARGS['cron'] or cmt.ARGS["report"]:
            check_result.send_metrology()


        # add Check to report
        report.add_check(check_result)


    # -- end of check loop --

    # Alerts : CLI & Pager
    if not cmt.ARGS['cron'] and not cmt.ARGS['short']:
        report.print_alerts_to_cli()
        print()

    if cmt.ARGS['cron'] or cmt.ARGS["pager"]:
        report.send_alerts_to_pager()

    # Save Persistance
    if cmt.ARGS['persist']:
        cmt.PERSIST.set_key("cmt_last_run",int(time.time()))
        cmt.PERSIST.save()
        debug2("Persist saved")
    else:
        debug2("Persist: save disabled")

    
    report.print_recap()
