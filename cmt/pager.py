# cavaliba.com - 2021
# pager.py

import time
import requests

import globals as cmt
from logger import logit, debug
import conf


# ------------------------------------------------------------
#  SEND TO PAGERS - entry point
# ------------------------------------------------------------
def send_test():
    ''' send TEST alert to all pagers. '''


    for pager in cmt.CONF['pagers']:
        
        if cmt.ARGS["pager"]:
            if pager not in cmt.ARGS["pager"][0]:
                continue
        
        pagerconf = cmt.CONF['pagers'][pager]
        pagertype = pagerconf.get('type', 'unknown')

        if pagertype == "team_channel" or pagertype =="teams":
            message, content = teams_build_test_message()
            r = teams_send_message(message=message, pagerconf=pagerconf)
            if r:
                logit("Pager Teams <{}> : test OK".format(pager))
            else:
                logit("Pager Teams <{}> : test FAILED".format(pager))

        elif pagertype == "pagerduty":
            message, content = pagerduty_build_test_message(pagerconf=pagerconf)
            r = pagerduty_send_message(message=message, pagerconf=pagerconf)
            if r:
                logit("Pager PagerDuty {} : test OK".format(pager))
            else:
                logit("Pager PagerDuty {} : test FAILED".format(pager))            

        elif pagertype == "smtp":
            pass

        else:
            debug("Unknown pager type in conf for ", pager) 

# -----------------
def send_real(report):
    ''' Send REAL alerts to all Pagers '''

    # global : Pager enabled  (global section, master switch) ?
    tmp = cmt.CONF['global'].get("enable_pager", "no")
    if not conf.is_timeswitch_on(tmp):
        debug("Pager  : disabled/inactive in global config.")
        return

    # check if alert exists in report (report.pager set to True)
    if not report.pager:
        debug("Pager : no alerts in report / no pager to be fired")
        return

    count_pager_fired = 0
    persist_last_timestamps = cmt.PERSIST.get_key("pager_last_timestamps", {})

    for pager in cmt.CONF['pagers']:

        if cmt.ARGS["pager"]:
            if pager not in cmt.ARGS["pager"][0]:
                continue

        debug("Processing pager {}".format(pager))
        pagerconf = cmt.CONF['pagers'][pager]        
        pagertype = pagerconf.get('type', 'unknown')         # team_channel/teams, pagerduty, smtp
        pager_rate_limit = int(pagerconf.get("rate_limit", 7200))
        timerange = pagerconf.get("enable", "yes")
        pagermode = pagerconf.get('mode', 'managed')

        # is this pager active ?
        if not conf.is_timeswitch_on(timerange):
            debug("Pager disabled/inactive in conf : ", pager)
            continue

        # which mode ?  managed[default], allnotifications
        selected_alerts = [cmt.ALERT_NEW]
        if pagermode == "allnotifications":
            selected_alerts = [cmt.ALERT_NEW, cmt.ALERT_ACTIVE, cmt.ALERT_DOWN]
        #print(pagerconf, pagermode, selected_alerts)

        # per pager rate_limit  : if managed, handle rate_limit
        if not cmt.ARGS['no_pager_rate_limit'] and not cmt.ARGS['devmode']:
            if pagermode == "managed":
                t1 = persist_last_timestamps.get(pager, 0)
                t2 = int(time.time())
                if t2 - t1 <= pager_rate_limit:
                    waitfor = t1 + pager_rate_limit - t2
                    logit("Pager rate-limit reached ({} sec to wait) for pager {}".format(waitfor, pager))
                    continue
                else:
                    persist_last_timestamps[pager] = t2
            else:
                # not managed : no rate-limit
                pass

        # build and send messages
        # ------------------------
        # teams
        if pagertype == "team_channel" or pagertype =="teams":
            message, content = teams_build_message(report, selected_alerts=selected_alerts)
            if len(content)>0:
                r = teams_send_message(message=message, pagerconf=pagerconf)
                if r:
                    logit("Pager Teams {} : OK".format(pager))
                    count_pager_fired += 1
                else:
                    logit("Pager Teams {} : FAILED".format(pager))
            else:
                # nothing to send
                pass

        # pagerduty
        elif pagertype == "pagerduty":
            message,content = pagerduty_build_message(report, pagerconf=pagerconf, selected_alerts=selected_alerts)
            if len(content)>0:
                r = pagerduty_send_message(message=message, pagerconf=pagerconf)
                if r:
                    logit("Pager PagerDuty {} : OK".format(pager))
                    count_pager_fired += 1
                else:
                    logit("Pager PagerDuty {} : FAILED".format(pager)) 
            else:
                # nothing to send
                pass

        # smtp
        elif pagertype == "smtp":
            #smtp_sendreal(pager, pagerconf, report)
            pass

        #unknown
        else:
            debug("Unknown pager type in conf for ", pager)            


    if count_pager_fired > 0:
        logit("Pager fired : {}".format(count_pager_fired))
    else:
        logit("No pager fired.")


    # update rate_limit
    if not cmt.ARGS['devmode']:
        cmt.PERSIST.set_key("pager_last_timestamps", persist_last_timestamps)



# =========================================================================
#  TEAMS
# =========================================================================
def teams_build_test_message():

    origin = cmt.CONF['global']['cmt_group'] + '/' + cmt.CONF['global']['cmt_node']
    title = "TEST from " + origin

    message = """
    {{
    "@type": "MessageCard",
    "@context": "http://schema.org/extensions",
    "summary": "Monitoring",
    "themeColor": "0000FF",
    "sections": [{{
        "activityTitle": "{}",
        "activitySubtitle": "{}",
        "activityText": "Test message to Teams. Please ignore.",
        "markdown": false
    }}]
    }}
    """.format(title, origin)

    return message, title


def teams_build_message(report, selected_alerts=[]):

    origin = cmt.CONF['global']['cmt_group'] + '/' + cmt.CONF['global']['cmt_node']
    title = "CMT ALERT from " + origin
    color = "FF0000"

    content = ""
    for c in report.checks:
        # no pager requested for this check results
        if not c.pager:
            continue
        # kind of event transition  for this pager ?
        if c.alert in selected_alerts:
            content += c.get_alert_symbol() + ' ' + c.get_alert_label() + ' - '
            content += c.get_message_as_str()
            content += '<br>\n'

    message = """
    {{
    "@type": "MessageCard",
    "@context": "http://schema.org/extensions",
    "summary": "Monitoring",
    "themeColor": "{}",
    "sections": [{{
        "activityTitle": "{}",
        "activitySubtitle": "{}",
        "activityText": "{}",
        "markdown": false
    }}]
    }}
    """.format(color, title, origin, content)

    return message, content



def teams_send_message(pagerconf={}, message=""):

    headers = {'Content-Type': 'application/json'}

    url = pagerconf.get('url','http://localhost/')
    ssl_verify = pagerconf.get("ssl_verify", True) is True
    http_code = pagerconf.get("http_code", 200)
    proxies, proxy_noenv = conf.get_proxies(pagerconf)

    if proxy_noenv:
        cmt.SESSION.trust_env = False
        proxies={}

    if cmt.ARGS['devmode']:
        print("DEVMODE : ", url, headers, message)
        return True

    try:
        r = cmt.SESSION.post(
            url, 
            headers=headers, 
            proxies=proxies,
            verify=ssl_verify,
            data=message, 
            timeout=cmt.TEAMS_TIMEOUT)
        debug("Teams - message sent ; status = {}".format(str(r.status_code)))
    except Exception as e:
        debug("Teams - FAILED to send message: {}".format(e))
        return False

    if r.status_code != http_code:
        debug("Teams - FAILED to send - bad response  " + str(r))
        return False

    return True


# =========================================================================
# PagerDuty
# =========================================================================
def pagerduty_build_test_message(pagerconf={}):

    group = cmt.CONF['global']['cmt_group']
    node = cmt.CONF['global']['cmt_node']
    key = pagerconf.get('key')
    dedup = group + "." + node + "." + "test" + "." + str(int(time.time() / 10))

    title = "TEST TEST from  {} - {} - please ignore".format(group,node)
    cmt_message = "This is a test from CMT. Please ignore. dedup=" + dedup

    message = """
    {{
      "payload": {{
        "summary": "{}",
        "source": "{}",
        "severity": "critical",
        "group": "{}",
        "class": "{}",
        "custom_details": {{
          "cmt_message": "{}"
        }}
      }},
      "routing_key": "{}",
      "dedup_key": "{}",
      "event_action": "trigger"
    }}
    """.format(title, node, group, node, cmt_message, key, dedup)    

    return message, title


def pagerduty_build_message(report, pagerconf={}, selected_alerts=[]):

    group = cmt.CONF['global']['cmt_group']
    node = cmt.CONF['global']['cmt_node']
    title = "CMT ALERT for {} - {} ".format(group,node)
    dedup = group + "." + node 
    key = pagerconf.get('key')

    content = ""
    for c in report.checks:
        # no pager requested for this check results
        if not c.pager:
            continue
        # kind of event transition  for this pager ?
        if c.alert in selected_alerts:
            content += c.get_alert_symbol() + ' ' + c.get_alert_label() + ' - '
            content += c.get_message_as_str()
            content += ' ; '


    message = """
    {{
      "payload": {{
        "summary": "{}",
        "source": "{}",
        "severity": "critical",
        "group": "{}",
        "class": "{}",
        "custom_details": {{
          "cmt_message": "{}"
        }}
      }},
      "routing_key": "{}",
      "dedup_key": "{}",
      "event_action": "trigger"
    }}
    """.format(title, node, group, node, content, key, dedup)

    return message, content


def pagerduty_send_message(pagerconf={}, message=""):

    headers = {'Content-Type': 'application/json' }
    url = pagerconf.get('url')
    ssl_verify = pagerconf.get("ssl_verify", False) is True
    http_code = pagerconf.get("http_code", 202)
    proxies, proxy_noenv = conf.get_proxies(pagerconf)

    if cmt.ARGS['devmode']:
        print("DEVMODE : ", url, headers, message)
        return True

    try:
        r = requests.post(
            url, 
            headers=headers, 
            proxies=proxies,
            verify=ssl_verify,                 
            data=message, 
            timeout=cmt.PAGERDUTY_TIMEOUT)
        debug("PagerDuty - message sent ; status = {}".format(str(r.status_code)))
    except Exception as e:
        debug("PagerDuty FAILED  - errror: {}".format(e))
        return False

    if r.status_code != http_code:
        debug("PagerDuty FAILED - bad response: " + str(r))
        return False

    return True

