# args.py

import argparse

import globals as cmt
from logger import debug, debug2


class BlankLinesHelpFormatter(argparse.HelpFormatter):
   def _split_lines(self, text, width):
        return super()._split_lines(text, width) + ['']

# process args on CLI

def parse_arguments(myargs):

    parser = argparse.ArgumentParser(description='CMT - Cavaliba Monitoring', formatter_class = BlankLinesHelpFormatter)

    # parser.add_argument('--conf', dest="config_file", type=str ,help="configuration file")

    parser.add_argument('--version', '-v', help='display current version',
                        action='store_true', required=False)

    parser.add_argument('--short', '-s', help='CLI - short compact output',
                        action='store_true', required=False)

    parser.add_argument('--cron', help='equiv to report, pager_enable, persist, short output',
                        action='store_true', required=False)

    parser.add_argument('modules', nargs='*',
                        action='append', help='modules to check (all by default)')

    parser.add_argument('--check', help='check name for single check run',
                        action='store', required=False)

    parser.add_argument('--conf', help='specify alternate yaml config file',
                        action='store', required=False)



    parser.add_argument('--report', help='send events to Metrology servers (default in cron)',
                        action='store_true', required=False)

    parser.add_argument('--persist', help='persist data accross CMT runs (default in cron)',
                        action='store_true', required=False)


    # pager
    parser.add_argument('--listmodules', help='display available modules',
                        action='store_true', required=False)
    parser.add_argument('--available', help='display available entries for modules (cli)',
                        action='store_true', required=False)

    parser.add_argument('--pager_enable', help='send alerts to Pagers (default in cron)',
                        action='store_true', required=False)
    parser.add_argument('--pager_test', help='send a test message to pagers and exit',
                        action='store_true', required=False)
    parser.add_argument('--no-pager-rate-limit', help='disable pager rate limit',
                        action='store_true', required=False)
    parser.add_argument('--pager', nargs='*',
                        action='append', help='limit to specified pagers')


    parser.add_argument('--nopersist', help='dont load previous run infos',
                        action='store_true', required=False)

    parser.add_argument('--checkconfig', help='checkconfig and exit',
                        action='store_true', required=False)
    parser.add_argument('--debug', help='verbose/debug output',
                        action='store_true', required=False)
    parser.add_argument('--debug2', help='more debug',
                        action='store_true', required=False)
    parser.add_argument('--devmode', help='dev mode, no pager, no remote metrology',
                        action='store_true', required=False)



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
