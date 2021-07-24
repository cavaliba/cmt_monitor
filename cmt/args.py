# args.py

import argparse

import globals as cmt
from logger import debug, debug2


# process args on CLI

def parse_arguments(myargs):

    parser = argparse.ArgumentParser(description='CMT - Cavaliba Monitoring')

    # parser.add_argument('--conf', dest="config_file", type=str ,help="configuration file")

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

    parser.add_argument('--short', '-s', help='short compact cli output',
                        action='store_true', required=False)

    parser.add_argument('--check', help='check name for single check run',
                        action='store', required=False)



    r = parser.parse_args(myargs)
    return vars(r)
    

# ------------------
def is_module_allowed_in_args(name):
    modules = cmt.ARGS['modules'][0]
    if name in modules or len(modules) == 0:
        return True
    debug2(name, "module not in ARGS")
    return False

# ------------------
def is_module_alone_in_args(name):
    modules = cmt.ARGS['modules'][0]
    if name in modules and len(modules) == 1:
        return True
    debug2(name, "module not alone or not in ARGS")
    return False

# -------------------
# check if all module names exist
def get_invalid_modules_in_args():
    err =[]
    modules = cmt.ARGS['modules'][0]
    for modulename in modules:
        if modulename not in cmt.GLOBAL_MODULE_MAP:
            err.append(modulename)
    return err
