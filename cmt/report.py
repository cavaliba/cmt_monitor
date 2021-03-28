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

    def add_check(self, c):

        self.checks.append(c)
        self.alert += c.alert
        self.warn += c.warn
        self.notice += c.notice

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

    def print_recap(self):
        ''' display one line with number of checks, alert, warn, notice.'''
        pass
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

    def dispatch_alerts(self):

        # Alerts : CLI & Pager
        if not cmt.ARGS['cron'] and not cmt.ARGS['short']:
            self.print_alerts_to_cli()
            print()

        if cmt.ARGS['cron'] or cmt.ARGS["pager"]:
            self.send_alerts_to_pager()


    def print_alerts_to_cli(self):
        ''' print pager/alerts to CLI '''

        print()
        print("Notification Summary")
        print("--------------------")
        print()
        if self.notice == 0:
            print(bcolors.OKBLUE + bcolors.BOLD + "No notice", bcolors.ENDC)
        else:
            print(bcolors.OKBLUE + bcolors.BOLD + "Notice", bcolors.ENDC)
            for c in self.checks:
                if c.notice > 0:
                    print("{:15s} : {}".format(c.module, c.get_message_as_str()))

        print()
        if self.warn == 0:
            print(bcolors.OKGREEN + bcolors.BOLD + "No warnings", bcolors.ENDC)
        else:
            print(bcolors.WARNING + bcolors.BOLD + "Warnings", bcolors.ENDC)
            for c in self.checks:
                if c.warn > 0:
                    print("{:15s} : {}".format(c.module, c.get_message_as_str()))
        print()
        if self.alert == 0:
            print(bcolors.OKGREEN + bcolors.BOLD + "No alerts", bcolors.ENDC)
        else:
            print(bcolors.FAIL + bcolors.BOLD + "Alerts", bcolors.ENDC)
            for c in self.checks:
                if c.alert > 0:
                    print("{:15s} : {}".format(c.module, c.get_message_as_str()))
        print()


    def send_alerts_to_pager(self):

        ''' Send alerts to Pagers '''

        # check if alert exists
        if not self.pager:
            debug("Pager : no Pager to be fired")
            return

        # check if Pager enabled globally (global section, master switch)
        tmp = cmt.CONF['global'].get("enable_pager", "no")
        if not conf.is_timeswitch_on(tmp):
            debug("Pager  : disabled/inactive in global config.")
            return

        # Find 'Alert' Pager
        if 'alert' not in cmt.CONF['pagers']:
            debug("No alert pager configured.")
            return

        pagerconf = cmt.CONF['pagers'].get('alert')

        # check if the 'Alert' Pager is enabled
        tmp2 = pagerconf.get("enable", "no")
        if not conf.is_timeswitch_on(tmp2):
            debug("Pager  : alert pager disbled in conf.")
            return

        # check rate_limit
        t1 = int(cmt.PERSIST.get_key("pager_last_send", 0))
        t2 = int(time.time())
        rate = int(cmt.CONF['global'].get("pager_rate_limit", 7200))

        if not cmt.ARGS['no_pager_rate_limit']:
            if t2 - t1 <= rate:
                logit("Alerts : too many alerts (rate-limit) - no alert sent to Pager")
                return

        # get Teams alert channel url
        url = pagerconf.get('url')
        debug("pager url :", url)

        # prepare message
        origin = cmt.CONF['global']['cmt_group'] + '/' + cmt.CONF['global']['cmt_node']
        color = "FF0000"
        title = "ALERT from " + origin

        message = ""
        for c in self.checks:
            if c.alert > 0:
                message += 'ALERT: '
                message += c.get_message_as_str()
                message += '<br>\n'
            if c.warn > 0:
                message += 'WARN: '
                message += c.get_message_as_str()
                message += '<br>\n'
            if c.notice > 0:
                message += 'NOTICE: '
                message += c.get_message_as_str()
                message += '<br>\n'

        debug("Pager Message : ", message)

        # send alert
        r = pager.teams_send(url=url, title=title, message=message, color=color, origin=origin)
        if r == 200:
            logit("Alerts : alert sent to Teams ")
        else:
            logit("Alerts : couldn't send alert to Teams - response  " + str(r))

        # update rate_limit
        cmt.PERSIST.set_key("pager_last_send", t2)
