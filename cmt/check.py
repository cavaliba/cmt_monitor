# check.py

import time
import os

import globals as cmt
import conf
import args

import metrology

from globals import bcolors
from logger import logit, debug, debug2
from checkitem import CheckItem


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

    def __init__(self, module="nomodule", check="noname", conf={}, opt={}):

        self.group = cmt.CONF['global'].get('cmt_group', 'nogroup')
        self.node = cmt.CONF['global'].get('cmt_node', 'nonode')
        self.node_env = cmt.CONF['global'].get('cmt_node_env', 'noenv')
        #self.node_role = cmt.CONF['global'].get('cmt_node_role', 'norole')
        #self.node_location = cmt.CONF['global'].get('cmt_node_location', 'nolocation')
        self.module = module
        self.check = check
        self.opt = opt         # opt given at init time by perform_check external creator
        self.result = "ok"     # ok, nok, skip
        self.result_info = ""  # human info about check run
        self.version = cmt.VERSION_NUMBER   # new 1.6.1

        self.message = []

        # new 2.0 - rawdata / multi-events (sendfile, mysqldata)
        self.multievent = []

        # list of individual points of data
        self.checkitems = []
        
        # fields from conf
        self.conf = conf

        # severity : 1=critical, 2=error, 3=warning, 4=notice, 5=none
        # set by modules ; shifted by severity_max configuration
        self.severity = cmt.SEVERITY_NONE    # DEFAULT = nothing wrong  

        # severity_max  ; default = critical
        self.severity_max = cmt.SEVERITY_CRITICAL
        a = conf.get('severity_max', 'critical')
        if a == 'critical':
            self.severity_max = cmt.SEVERITY_CRITICAL
        elif a == 'error':
            self.severity_max = cmt.SEVERITY_ERROR
        elif a == 'warning':
            self.severity_max = cmt.SEVERITY_WARNING
        elif a == 'notice':
            self.severity_max = cmt.SEVERITY_NOTICE
        elif a == 'none':
            self.severity_max = cmt.SEVERITY_NONE
        else:
            logit("Unknown severity_max {} in ({},{}) - default to critical.".format(a,module,check) )

        # events/transition : NEW, ACTIVE, DOWN, NONE - computed (hysteresis, delay)
        self.alert = cmt.ALERT_NONE
        
        # set by framework after Check is performed, if pager_enable and alert ! NONE
        self.pager = False

        # persist values from previous run for same get_id()
        id = self.get_id()
        self.persist = cmt.PERSIST.get_key(id, {})


    def add_message(self, m):

        self.message.append(m)

    def add_item(self, item):
        ''' add a CheckItem instance to the Check items list '''
        self.checkitems.append(item)

    def get_id(self):
        ''' Returns unique check id '''
        return "{}.{}.{}.{}".format(self.group, self.node, self.module, self.check)


    def get_message_as_str(self):

        v = ""
        for mm in self.message:
            if len(v) > 0:
                v = v + " ; "
            v = v + mm
        return v


    def frequency(self):
        ''' 
        Return True/False if allowed/not allowed to run
          - based on frequency configured or not (allow if no frequency)
          - based on previous run (persisted) if frequency configured
        Update PERSIST() object for next run, if  run allowed this time
        '''
        
        # get lastrun timestamp for this check or 0
        freqpersist = cmt.PERSIST.get_key("frequency", {})
        id = self.get_id()
        freqlastrun = freqpersist.get(id, 0)

        # frequency for this specific check ?
        f = self.conf.get('frequency', -1)

        if f == -1:
            debug2("Frequency: no Frequency at check level")
            # allowed to run again
            return True

        # if frequency configured, compare value / delta ; update persist if Run decided
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


    def reverse_severity(self):
        ''' 
        Inverse conditions of severity : negative check. 
        Severity will ne not SEVERITY_NONE  only if check fails
        '''

        a = self.conf.get('reverse_severity', 'not_configured')        
        if a == 'not_configured':
            return

        # perform inversion
        if self.severity != cmt.SEVERITY_NONE:
            # check failed, thus ... normal (inversion)
            self.severity = cmt.SEVERITY_NONE
        else:
            # check OK, but shouldn't (inversion), set new severity
            # get value from config
            if a == 'critical':
                self.severity = cmt.SEVERITY_CRITICAL
            elif a == 'error':
                self.severity = cmt.SEVERITY_ERROR
            elif a == 'warning':
                self.severity = cmt.SEVERITY_WARNING
            elif a == 'notice':
                self.severity = cmt.SEVERITY_NOTICE
            elif a == 'none':
                self.severity = cmt.SEVERITY_NONE
            else:
                logit("Unknown reverse_severity {} in ({}) - default to critical.".format(a,self.check) )

        debug("severity = {} (from reverse_severity)".format(self.severity))
        return




    def adjust_severity(self):
        ''' 
        Cap (reduce) severity for this check  to severity_max
        '''

        if self.severity < self.severity_max:
            self.severity = self.severity_max

        debug("severity = {}".format(self.severity))
        return


    def compute_alert(self):
        '''
        Apply Hystereris up/down to alert for this check :
            - consecutive alerts (duration) needed to define real alert
            - consecutire no_alert (idem) needed to define return to noalert
        '''

        # config : alert_delay : seconds for state transition normal to alert (if alert)
        global_alert_delay = int(cmt.CONF['global'].get("alert_delay", cmt.DEFAULT_HYSTERESIS_ALERT_DELAY ))
        alert_delay = int(self.conf.get("alert_delay", global_alert_delay))

        hystpersist = cmt.PERSIST.get_key("hysteresis", {})
        id = self.get_id()
        hystpersist_item = hystpersist.get(id, {})

        hystlastrun = hystpersist_item.get('lastrun', 0)
        now = int(time.time())
        delta = int(now - hystlastrun)

        duration_alert = hystpersist_item.get('duration_alert', 0)
        oldstate = hystpersist_item.get('state', 'normal')

        newstate = oldstate

        #print("Hysteresis", duration_alert, delta, alert_delay)

        # check NOK - there's a severity  in the check
        if self.severity < cmt.SEVERITY_NONE:
            duration_alert += delta

            if oldstate == "normal":
                if duration_alert > alert_delay:
                    # transition to alert
                    newstate = "alert"
                    self.alert = cmt.ALERT_NEW
                else: 
                    # not yet; stay normal (prealert)
                    newstate = "normal"
                    self.alert = cmt.ALERT_NONE
            else:
                self.alert = cmt.ALERT_ACTIVE

        # check OK - transition or already normal ? (no hystereis in the active to down transition)
        else:         
            # already normal
            if oldstate  =="normal":
                newstate = "normal"
                duration_alert = 0
                self.alert = cmt.ALERT_NONE    
            # transition
            else:
                newstate = "normal"
                duration_alert = 0
                self.alert = cmt.ALERT_DOWN

        # write to Persist
        # lastrun
        hystpersist_item['lastrun'] = now
        hystpersist_item['duration_alert'] = duration_alert
        hystpersist_item['state'] = newstate
        hystpersist[id] = hystpersist_item
        cmt.PERSIST.set_key("hysteresis", hystpersist)


    def compute_pager(self):
        '''
        if there is an ALERT event (transition) and pager is active for this check
        flag pager=TRUE to propagate to Report.
        '''

        # TODO : could be moved to report aggregation level
        
        if self.alert != cmt.ALERT_NONE:
            tr = self.conf.get('enable_pager', "no")
            if conf.is_timeswitch_on(tr):
                debug("pager active for check ", self.get_id())
                self.pager = True



    def print_to_cli_skipped(self):

        alert = ''
        head = bcolors.WHITE  + alert + "SKIPPED" + bcolors.ENDC
        #print('------------------------------------------------------------------')
        print("{:12}  {:12} {} {}".format(head, self.module, self.check, self.result_info))
        #print('------------------------------------------------------------------')

        

    def print_to_cli_short(self):

        alert_symbol = cmt.get_alert_symbol(self.alert)
        severity_label = cmt.get_severity_label(self.severity)
        severity_label += ' ' * (8 - len(severity_label))

        if self.severity == cmt.SEVERITY_CRITICAL:
            head = bcolors.FAIL  + bcolors.BOLD
        elif self.severity == cmt.SEVERITY_ERROR:
            head = bcolors.FAIL
        elif self.severity == cmt.SEVERITY_WARNING:
            head = bcolors.WARNING
        elif self.severity == cmt.SEVERITY_NOTICE:
            head = bcolors.CYAN
        else:
            head = bcolors.OKGREEN

        #head = head + alert_symbol + severity_label + bcolors.ENDC
        head = head + severity_label + bcolors.ENDC
        print("{:12} {:12} {}".format(head, self.module, self.get_message_as_str()))


    def print_to_cli_detail_head(self):

        print('------------------------------------------------------------------')
        print(bcolors.WHITE  + self.module, self.check +  bcolors.ENDC)
        print('------------------------------------------------------------------')


    def print_to_cli_detail(self):

        alert_symbol = cmt.get_alert_symbol(self.alert)
        severity_label = cmt.get_severity_label(self.severity)
        #severity_label += ' ' * (8 - len(severity_label))

        # print('------------------------------------------------------------------')
        # print(bcolors.WHITE  + self.module, self.check +  bcolors.ENDC)
        # print('------------------------------------------------------------------')

        for i in self.checkitems:

            v = str(i.value)

            if len(str(i.unit)) > 0:
                v = v + ' ' + str(i.unit) + ' '
            if len(str(i.human())) > 0:
                v = v + ' [' + i.human() + ']'
            if len(i.description) > 0:
                v = v + ' - ' + i.description

            print("cmt_{:20} {}".format(i.name, v))


        if self.severity == cmt.SEVERITY_CRITICAL:
            head = bcolors.FAIL  + bcolors.BOLD
        elif self.severity == cmt.SEVERITY_ERROR:
            head = bcolors.FAIL
        elif self.severity == cmt.SEVERITY_WARNING:
            head = bcolors.WARNING
        elif self.severity == cmt.SEVERITY_NOTICE:
            head = bcolors.CYAN
        else:
            head = bcolors.OKGREEN

        #head = head  + severity_label + ' ' + alert_symbol + bcolors.ENDC
        head = head  + severity_label + ' ' + bcolors.ENDC

        print("{} : {}".format(head, self.get_message_as_str()))



    def add_tags(self):
        ''' Add checkitems tags from global or check config '''

        # global
        tags = cmt.CONF['global'].get("tags","").split()

        # self.conf
        tags += self.conf.get("tags","").split()

        # parse tags / split if value provided / add check item
        for tag in tags:
            k=''
            v=''
            if '=' in tag:
                (k,v)=tag.split('=')
            else:
                k=tag
                v=1
            #print("tag : ",tag,k,v)
            ci = 'tag_' + k
            self.add_item(CheckItem(ci,v))



# --------------------------------------------------------------------------------
# perform a single check
# --------------------------------------------------------------------------------

def perform_check(checkname, modulename):

    debug2("Starting check : ", checkname)

    # Is module in GLOBAL MAP ?
    if modulename not in cmt.GLOBAL_MODULE_MAP:
        logit("Unknown module in configuration: ", modulename)
        return "continue"

    # get configuration for this check
    checkconf = cmt.CONF[modulename][checkname]

    # check enabled ?
    ts_check = checkconf.get('enable', 'yes')
    if not conf.is_timeswitch_on(ts_check):
        debug("check disabled by conf ",checkname)
        return "continue"

    # check if module is filtered in ARGS
    if not args.is_module_allowed_in_args(modulename):
        #check_result.result = "skip"         
        #check_result.result_info =  "module not requested (args)"
        return "continue"

    # prepare options sent to Module code
    my_opt = {}

    # some checks are exclusive / standalone 
    # Check if it is a standalone check (one module, one check)
    if args.is_module_alone_in_args(modulename):
        my_opt["single_module_run"]=True
    else:
        my_opt["single_module_run"]=False

    # particular checkname requested ? (--check option)
    # NB : several modules can match for the same chechname which is not a PK accross full config
    my_opt["specific_checkname_run"]=False
    if cmt.ARGS["check"]:
        if cmt.ARGS["check"] == checkname:
            debug2("  specific check name : match %s" % checkname)
            my_opt["specific_checkname_run"]=True
        else:
            debug2("  specific check name : skip %s" % checkname)
            return "continue"


    # create check object
    check_result = Check(module=modulename, check=checkname, conf=checkconf, opt=my_opt)

    # Add tags/kv
    check_result.add_tags()

    # print header to CLI
    if cmt.ARGS['cron'] or cmt.ARGS['short']:
        pass
    else:
        check_result.print_to_cli_detail_head()

    # check if root privilege is required
    conf_rootreq = checkconf.get('root_required', False) is True
    if conf_rootreq:
        if (os.getuid() != 0):
            debug("check %s must run as root." % checkname)   
            check_result.result = "skip"         
            check_result.result_info = "must run as root"
            check_result.print_to_cli_skipped()
            return "continue"

    # verify frequency in cron mode
    if cmt.ARGS['cron']:
        if not check_result.frequency():
            check_result.result = "skip"
            check_result.result_info = "check skipped (frequency)"
            check_result.print_to_cli_skipped()
            return "continue"

    # HERE / Future : give check_result the needed Module Conf, Global Conf ...

    # TODO : if --available, call different function


    # *********************************************************
    # **** ACTUAL CHECK IS DONE HERE ****
    # *********************************************************
    check_result = cmt.GLOBAL_MODULE_MAP[modulename]['check'](check_result)
    

    # ---------------
    # process results
    # ---------------

    # option = available => not a real run ; just display discovered target and quit
    if cmt.ARGS["available"]:
        return "break"

    # if check skipped by module itself
    if check_result.result == "skip":
        check_result.resul_info = check_result.message
        check_result.print_to_cli_skipped()
        debug("  skipped in module")
        return "continue"

    # reverse severity if needed (negative condition / inverse check)
    check_result.reverse_severity()

    # adjust severity to severity_max for this check
    check_result.adjust_severity()


    # compute alert transition : NONE, NEW, ACTIVE, DOWN ; hysteresis
    check_result.compute_alert()

    # If pager enabled (at check level), and alert exists : set pager True
    check_result.compute_pager()

    # Print to CLI
    if cmt.ARGS['cron'] or cmt.ARGS['short']:
        check_result.print_to_cli_short()
    else:
        check_result.print_to_cli_detail()
    
    # keep returned Persist structure in check_result
    cmt.PERSIST.set_key(check_result.get_id(), check_result.persist)

    # Metrology
    if cmt.ARGS['cron'] or cmt.ARGS["report"]:
        # check_result.send_metrology()
        metrology.send_metrology(check_result)

    # add Check to report
    return check_result
