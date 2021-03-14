# check.py

import time
import os

import globals as cmt
import conf
import args

import metrology

from globals import bcolors
from logger import logit, debug


# ----------------------------------------------------------
# Class Check
# ----------------------------------------------------------

class Check():

    '''class Check():
       - Stores multiple CheckItem related to a single Check function run.
       - Each Check is sent as one message to a metrology server like Graylog/Elastic.
       - Count alerts from CheckItem : alert is sent as Yyes/no if any of the checkItem as an alert.
       - Pager alerts are sent globally at the Report level.
    '''

    def __init__(self, module="nomodule", check="noname", conf={}):

        self.group = cmt.CONF['global'].get('cmt_group', 'nogroup')
        self.node = cmt.CONF['global'].get('cmt_node', 'nonode')
        self.node_env = cmt.CONF['global'].get('cmt_node_env', 'noenv')
        self.node_role = cmt.CONF['global'].get('cmt_node_role', 'norole')
        self.node_location = cmt.CONF['global'].get('cmt_node_location', 'nolocation')
        self.module = module
        self.check = check

        self.message = []

        self.alert = 0
        self.warn = 0
        self.notice = 0
        # self.notification = alert + warn + notice
        self.checkitems = []

        # set by framework after Check is performed, if pager_enable and alert>0
        self.pager = False

        # fields from conf
        self.conf = conf

        # persist values from previous run for same get_id()
        id = self.get_id()
        self.persist = cmt.PERSIST.get_key(id, {})

        # compute alert_max_level
        self.alert_max_level = "alert"   # DEFAULT
        
        # at the individual check level ?
        a = conf.get('alert_max_level', '')
        if a in ['alert', 'notice', 'warn', 'none']:
            self.alert_max_level = a
        else:
            # at the module level ?
            b = cmt.CONF['modules'][self.module].get('alert_max_level', '')
            if b in ['alert', 'notice', 'warn', 'none']:
                self.alert_max_level = b
            else:
                # global level ?
                c = cmt.CONF['global'].get('alert_max_level', '')
                if c in ['alert', 'notice', 'warn', 'none']:
                    self.alert_max_level = c

    def add_message(self, m):

        self.message.append(m)

    def add_item(self, item):
        ''' add a CheckItem instance to the Check items list '''
        self.checkitems.append(item)

    def get_id(self):
        ''' Returns unique check id '''
        return "{}.{}.{}.{}".format(self.group, self.node, self.module, self.check)

    def get_notification(self):
        ''' Returns notification has sum of alert + warn + nocive '''
        return int(self.alert + self.warn + self.notice)

    def get_message_as_str(self):

        v = ""
        for mm in self.message:
            if len(v) > 0:
                v = v + " ; "
            v = v + mm
        return v

    def adjust_alert_max_level(self, level=""):

        if level == "":
            level = self.alert_max_level

        debug("adjust alert_max_level to : ", level)

        if level == "alert":
            return

        if level == "warn":
            self.notice = self.warn
            self.warn = self.alert
            self.alert = 0
            return

        if level == "notice":
            self.notice = self.alert
            self.alert = 0
            self.warn = 0

        if level == "none":
            self.notice = 0
            self.alert = 0
            self.warn = 0


    def frequency(self):
        ''' Verify and update run frequency (cron mode).
        Return True/False if allowed/not alloowed to run.
        Update PERSIST() object
        '''
        # last run for this check ?
        freqpersist = cmt.PERSIST.get_key("frequency", {})
        id = self.get_id()
        freqlastrun = freqpersist.get(id, 0)

        # frequency for this specific check ?
        f = self.conf.get('frequency', -1)

        if f == -1:
            debug("Frequency: no Frequency at check level")
            # frequency at the module level ?
            modconf = cmt.CONF['modules'].get(self.module, {})
            f2 = modconf.get('frequency', -1)

            # no frequency specified, return True / no persist
            if f2 == -1:
                debug("Frequency: no Frequency at module level")
                return True
            else:
                f = f2

        # yes, compare value / delta ; update persist if Run
        now = int(time.time())
        delta = int(now - freqlastrun)
        if delta > f:
            freqpersist[id] = now
            cmt.PERSIST.set_key("frequency", freqpersist)
            debug("Frequency: allowed {} > {} (f={}, delta={})".format(now, freqlastrun, f, delta))
            return True

        # too early
        debug("Frequency: not allowed : f={}, delta={}".format(f, delta))
        return False

    # -------------------
    def hysteresis_filter(self):
        ''' Apply Hystereris up/down to alert for this check :
            - consecutive alerts (duration) needed to define real alert
            - consecutire no_alert (idem) needed to define return to noalert
        '''

        # seconds for state transition normal to alert (if alert)
        alert_delay = conf.get_hysteresis(self)

        hystpersist = cmt.PERSIST.get_key("hysteresis", {})
        id = self.get_id()
        hystpersist_item = hystpersist.get(id, {})

        hystlastrun = hystpersist_item.get('lastrun', 0)
        now = int(time.time())
        delta = int(now - hystlastrun)

        duration_alert = hystpersist_item.get('duration_alert', 0)
        oldstate = hystpersist_item.get('state', 'normal')

        newstate = oldstate

        # print("Hysteresis", duration_alert, delta, alert_delay)

        if self.alert > 0:
            if oldstate == "normal":
                duration_alert += delta
                if duration_alert > alert_delay:
                    # transition to up
                    newstate = "alert"
        else:
            newstate = "normal"
            duration_alert = 0

        # not yet a real alert
        if self.alert > 0 and newstate == "normal":
            # adjust to warn ; not a transition
            self.adjust_alert_max_level("warn")

        # write to Persist
        # lastrun
        # BUG
        hystpersist_item['lastrun'] = now
        hystpersist_item['duration_alert'] = duration_alert
        hystpersist_item['state'] = newstate
        hystpersist[id] = hystpersist_item
        cmt.PERSIST.set_key("hysteresis", hystpersist)

    # --------------
    def print_to_cli_short(self):

        head = bcolors.OKGREEN     + "OK     " + bcolors.ENDC

        if self.alert > 0:
            head = bcolors.FAIL    + "NOK    " + bcolors.ENDC
        elif self.warn > 0:
            head = bcolors.WARNING + "WARN   " + bcolors.ENDC
        elif self.notice > 0:
            head = bcolors.OKBLUE  + "NOTICE " + bcolors.ENDC

        # print(head, self.get_message_as_str())
        print("{:12} {:12} {}".format(head, self.module, self.get_message_as_str()))


    def print_to_cli_detail(self):

        print()
        print(bcolors.OKBLUE + bcolors.BOLD + "Check", self.module, bcolors.ENDC)

        for i in self.checkitems:

            v = str(i.value)

            if len(str(i.unit)) > 0:
                v = v + ' ' + str(i.unit) + ' '
            if len(str(i.human())) > 0:
                v = v + ' [' + i.human() + ']'
            if len(i.description) > 0:
                v = v + ' - ' + i.description

            print("cmt_{:20} {}".format(i.name, v))


        head = bcolors.OKGREEN     + "OK     " + bcolors.ENDC

        if self.alert > 0:
            head = bcolors.FAIL    + "NOK    " + bcolors.ENDC
        elif self.warn > 0:
            head = bcolors.WARNING + "WARN   " + bcolors.ENDC
        elif self.notice > 0:
            head = bcolors.OKBLUE  + "NOTICE " + bcolors.ENDC

        print("{:33} {}".format(head, self.get_message_as_str()))


    def send_metrology(self):

        ''' Send Check results (event, multiple CheckItems)
            to metrology servers.
        '''

        graylog_data = metrology.build_gelf_message(self)

        for metro in cmt.CONF['metrology_servers']:


            metroconf = cmt.CONF['metrology_servers'][metro]
            metrotype = metroconf.get('type', 'unknown')

            timerange = metroconf.get("enable", "yes")
            if not conf.is_timeswitch_on(timerange):
                debug("Metrology server disabled in conf : ", metro)
                return

            if metrotype == "graylog_udp_gelf":
                host = metroconf['host']
                port = metroconf['port']
                metrology.graylog_send_udp_gelf(host=host, port=port, data=graylog_data)
                debug("Data sent to metrology server ", metro)

            elif metrotype == "graylog_http_gelf":
                url = metroconf['url']
                metrology.graylog_send_http_gelf(url=url, data=graylog_data)
                debug("Data sent to metrology server ", metro)

            else:
                debug("Unknown metrology server type in conf.")


# --------------------------------------------------------------------------------
# perform a single check
# --------------------------------------------------------------------------------

def perform_check(checkname, modulename):

    debug("Starting check : ", checkname)

    # Is module in GLOBAL MAP ?
    if modulename not in cmt.GLOBAL_MODULE_MAP:
        logit("Unknown module in configuration: ", modulename)
        return "continue"

    # get configuration for this check
    checkconf = cmt.CONF[modulename][checkname]


    # check  enabled in conf ?  (in check or in module)
    ts_check = checkconf.get('enable', 'n/a')
    # no info
    if ts_check == "n/a":
        # module level ?
        if not conf.is_module_active_in_conf(modulename):
            debug("  module disabled in conf")
            return "continue"   # no
    elif not conf.is_timeswitch_on(ts_check):
        debug("  check disabled by conf")
        return "continue"

    # check if module is filtered in ARGS
    if not args.is_module_allowed_in_args(modulename):
        return "continue"

    # check if root privilege is required
    conf_rootreq = checkconf.get('rootrequired', False) is True
    if conf_rootreq:
        if (os.getuid() != 0):
            logit("check %s must run as root." % checkname)
            return "continue"


    # create check object
    check_result = Check(module=modulename, check=checkname, conf=checkconf)

    # verify frequency in cron mode
    if cmt.ARGS['cron']:
        if not check_result.frequency():
            return "continue"

    # HERE / Future : give check_result the needed Module Conf, Global Conf ...

    # TODO : if --available, call diffrent function

    # ---------------
    # perform check !
    # ---------------
    check_result = cmt.GLOBAL_MODULE_MAP[modulename]['check'](check_result)

    if cmt.ARGS["available"]:
        return "break"

    # Hysteresis / alert upd & own
    check_result.hysteresis_filter()

    # apply alert_max_level for this check
    check_result.adjust_alert_max_level()

    # If pager enabled (at check level), and alert exists : set pager True
    if check_result.alert > 0:
        tr = checkconf.get('enable_pager', "no")
        if conf.is_timeswitch_on(tr):
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

    # add Check to report
    return check_result
