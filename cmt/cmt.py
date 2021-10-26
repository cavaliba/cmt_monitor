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

    if not sys.version_info >= (3, 6):
        print ("Should use Python >= 3.6")
        sys.exit()

    cmt.ARGS = args.parse_arguments(sys.argv[1:])

    if cmt.ARGS["version"]:
        print(cmt.VERSION)
        sys.exit()

    err = args.get_invalid_modules_in_args()
    if len(err) > 0:
        print ("ERR - Unknow module(s)  : " + ','.join(err))
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

    # CLI : Send test message to Pagers ?
    if cmt.ARGS["pagertest"]:
        pager.sendtest()
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

    # display report recap to CLI
    if cmt.ARGS['short']:
        myreport.print_line_summary()
    else:
        myreport.print_recap()
        myreport.print_line_summary()

    # send batch metrology if needed
    if cmt.ARGS['cron'] or cmt.ARGS["report"]:
        metrology.send_metrology_batch()

    # send alerts to pagers
    if cmt.ARGS['cron'] or cmt.ARGS["pager"]:
        pager.sendreal(myreport)

    # persist data across runs
    cmt.PERSIST.set_key("cmt_last_run", int(time.time()))
    cmt.PERSIST.save()
