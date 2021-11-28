# cavaliba.com - 2021
# report.py

import time

import globals as cmt
import conf
import pager

from globals import bcolors
from logger import logit, debug


# ----------------------------------------------------------
# Class Report
# ----------------------------------------------------------

class Report():
    '''A Report stores all the Checks from a single run of CMT.
       Pager alerts are sent to Pager targets at the end of the run.
    '''

    def __init__(self):

        self.checks = []
        self.severity = cmt.SEVERITY_NONE
        self.pager = False

    def add_check(self, c):

        self.checks.append(c)
        # keep most critical severity (minimal value)
        self.severity = min (self.severity, c.severity)
        # propagate Pager from check to report
        if c.pager:
            self.pager = True


    def print_header(self):

        if cmt.ARGS['cron']:
            print("-" * 60)
            logit("Starting ...")
            print()
        else:
            print('-' * 60)
            print(cmt.VERSION)
            print('-' * 60)
            print("cmt_group      : ", cmt.CONF['global']['cmt_group'])
            print("cmt_node       : ", cmt.CONF['global']['cmt_node'])
            print("config file    : ", cmt.CONF['__config_file'])
            print()

    def get_severity_string(self):

        if self.severity == cmt.SEVERITY_CRITICAL:
            return bcolors.FAIL + bcolors.BOLD + "CRITICAL" + bcolors.ENDC
        if self.severity == cmt.SEVERITY_ERROR:
            return bcolors.FAIL + bcolors.BOLD + "ERROR"  + bcolors.ENDC
        if self.severity == cmt.SEVERITY_WARNING:
            return bcolors.WARNING + bcolors.BOLD + "WARNING" + bcolors.ENDC
        if self.severity == cmt.SEVERITY_NOTICE:
            return bcolors.CYAN + bcolors.BOLD + "NOTICE" + bcolors.ENDC
        if self.severity == cmt.SEVERITY_NONE:
            return bcolors.WHITE + bcolors.BOLD + "NONE" + bcolors.ENDC


    def print_line_summary(self):
        ''' Print a one-line summary.'''

        ck = 0
        ok = 0 
        nok = 0
        critical = 0
        error = 0
        warning = 0
        notice = 0
        for c in self.checks:
            ck += 1
            if c.severity == cmt.SEVERITY_CRITICAL:
                critical += 1
            elif c.severity == cmt.SEVERITY_ERROR:
                error += 1
            elif c.severity == cmt.SEVERITY_WARNING:
                warning += 1
            elif c.severity == cmt.SEVERITY_NOTICE:
                notice += 1
            else:
                ok += 1

        nok = ck - ok
        
        percent = int(100*ok/ck)

        print()
        logit("SEVERITY={} - {}/{} OK ({} %) - {} NOK : {} criticial - {} error - {} warning - {} notice.".format(
              self.get_severity_string(), ok, ck, percent, nok, critical, error, warning, notice))
        print()
