# cavaliba.com - 2021
# main.py


import sys
import time
import signal
import json

# global variables
import globals as cmt
import args
import conf
import map    # needed to init GLOBAL_MAP
import persist
import check
import report
import pager
import metrology

from logger import logit, debug


# -----------------
def timeout_handler(signum, frame):
    # raise Exception("Timed out!")
    print("Timed out ! (max_execution_time)")
    sys.exit()

# ------------
# Main entry
# ------------


if __name__ == "__main__":

    cmt.ARGS = args.parse_arguments(sys.argv[1:])

    if cmt.ARGS["version"]:
        print(cmt.VERSION)
        sys.exit()

    # conf.yml,  conf.d/*.yml
    cmt.CONF = conf.load_conf()

    # Persist
    cmt.PERSIST = persist.Persist(file=cmt.DEFAULT_PERSIST_FILE)
    lastrun = cmt.PERSIST.get_key("cmt_last_run", 0)

    # remote conf (url) or cached conf
    conf.load_conf_remote(cmt.CONF)

    # check master switch / CMT disabled ?
    ts_global_enable = cmt.CONF['global'].get('enable', 'no')
    if not conf.is_timeswitch_on(ts_global_enable):
        logit("CMT globally disabled by conf")
        sys.exit()

    # CLI : check config option ?
    if cmt.ARGS["checkconfig"]:
        print(json.dumps(cmt.CONF, indent=2))
        print("config OK.")
        sys.exit()

    # CLI : Send test message to Teams ?
    if cmt.ARGS["pagertest"]:
        pager.pager_test()
        sys.exit()

    # CLI : List available modules option ?
    if cmt.ARGS["listmodules"]:
        print("Available modules: ")
        for key in cmt.GLOBAL_MODULE_MAP:
            print("  - ", key)
        sys.exit()

    # -----------------
    myreport = report.Report()
    myreport.print_header()

    # set global timer to limit global duration
    maxexec = cmt.CONF['global'].get("max_execution_time", cmt.MAX_EXECUTION_TIME)
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(maxexec)   # seconds

    # main loop
    for modulename in cmt.GLOBAL_MODULE_MAP:
        if modulename in cmt.CONF:
            for checkname in cmt.CONF[modulename]:
                check_result = check.perform_check(checkname, modulename)
                if type(check_result) is str:
                    if check_result == "break":
                        break
                    elif check_result == "continue":
                        continue
                else:
                    # add Check to report
                    myreport.add_check(check_result)
            else: # no break in inner loop
                # called if no break : go on with outer loop 
                continue
            # break from outer for loop
            break

    # -- end of check loop --

    # -- send batch metrology
    if cmt.ARGS['cron'] or cmt.ARGS["pager"]:
        metrology.send_metrology_batch()

    # send alerts to pagers
    myreport.dispatch_alerts()

    # display report recap to CLI
    myreport.print_recap()

    # persist data across runs
    cmt.PERSIST.set_key("cmt_last_run", int(time.time()))
    cmt.PERSIST.save()
