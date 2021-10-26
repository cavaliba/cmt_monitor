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
        self.alert = 0
        self.warn = 0
        self.notice = 0
        self.pager = False
        # new 2.0
        self.severity = cmt.SEVERITY_NONE


    def add_check(self, c):

        self.checks.append(c)
        self.alert += c.alert
        self.warn += c.warn
        self.notice += c.notice

        # new 2.0
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
            return "CRITICAL"
        if self.severity == cmt.SEVERITY_ERROR:
            return "ERROR"
        if self.severity == cmt.SEVERITY_WARNING:
            return "WARNING"
        if self.severity == cmt.SEVERITY_NONE:
            return "NONE"



    def print_recap(self):

        ''' display each alert/warn notice + one line summary'''
        
        print()
        print(bcolors.WHITE + bcolors.BOLD + "Summary" + bcolors.ENDC )
        print(bcolors.WHITE + bcolors.BOLD + "-------" + bcolors.ENDC )
        
        print ("SEVERITY: ", self.get_severity_string() )

        if self.notice == 0:
            #print(bcolors.OKBLUE + bcolors.BOLD + "No notice", bcolors.ENDC)
            print("No Notice.")
        else:
            print(bcolors.CYAN + bcolors.BOLD + "NOTICE", bcolors.ENDC)
            for c in self.checks:
                if c.notice > 0:
                    print("{:15s} : {}".format(c.module, c.get_message_as_str()))
            print()

        if self.warn == 0:
            #print(bcolors.OKGREEN + bcolors.BOLD + "No warnings", bcolors.ENDC)
            print("No Warning.")
        else:
            print(bcolors.WARNING + bcolors.BOLD + "WARNINGS", bcolors.ENDC)
            for c in self.checks:
                if c.warn > 0:
                    print("{:15s} : {}".format(c.module, c.get_message_as_str()))
            print()

        if self.alert == 0:
            #print(bcolors.OKGREEN + bcolors.BOLD + "No alerts", bcolors.ENDC)
            print("No Alert.")
        else:
            print(bcolors.FAIL + bcolors.BOLD + "ALERTS", bcolors.ENDC)
            for c in self.checks:
                if c.alert > 0:
                    print("{:15s} : {}".format(c.module, c.get_message_as_str()))

        # - one line summary

        ck = 0
        alert = 0
        warn = 0
        notice = 0
        for c in self.checks:
            ck += 1
            if c.alert > 0:
                alert += 1
            if c.warn > 0:
                warn += 1
            if c.notice > 0:
                notice += 1
        nok = alert + warn + notice
        ok = ck - nok
        
        print()
        logit("Done - {} checks - {} ok - {} nok - {} alerts - {} warning - {} notice.".format(
              ck, ok, nok, alert, warn, notice))
        print()



