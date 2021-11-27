# cavaliba.com - 2021
# pager.py

import time
import requests
import globals as cmt
from logger import logit, debug
import conf


# ------------------------------------------------------------
#  send_to_pagers
# ------------------------------------------------------------
def sendtest():
    ''' send TEST message to all pagers. '''

    for pager in cmt.CONF['pagers']:

        pagerconf = cmt.CONF['pagers'][pager]
        pagertype = pagerconf.get('type', 'unknown')

        if pagertype == "team_channel" or pagertype =="teams":
            teams_sendtest(pager, pagerconf)

        elif pagertype == "pagerduty":
            pass

        elif pagertype == "smtp":
            pass
        else:
            debug("Unknown pager type in conf for ", pager) 

# -----------------
def sendreal(report):
    ''' Send REAL notifications to all Pagers '''

    # check if alert exists in report (pager set to True)
    if not report.pager:
        debug("Pager : no alerts in report / no pager to be fired")
        return

    # check if Pager enabled globally (global section, master switch)
    tmp = cmt.CONF['global'].get("enable_pager", "no")
    if not conf.is_timeswitch_on(tmp):
        debug("Pager  : disabled/inactive in global config.")
        return

    rate_limit_update = False

    for pager in cmt.CONF['pagers']:

        pagerconf = cmt.CONF['pagers'][pager]
        
        # team_channel/teams, pagerduty, smtp
        pagertype = pagerconf.get('type', 'unknown')
    
        # mode : managed[default], allnotifications
        pagermode = pagerconf.get('mode', 'managed')

        timerange = pagerconf.get("enable", "yes")
        if not conf.is_timeswitch_on(timerange):
            debug("Pager disabled/inactive in conf : ", pager)
            continue

        # rate_limit  : if managed pager, handle rate_limit
        if not cmt.ARGS['no_pager_rate_limit'] and not cmt.ARGS['devmode']:
            if pagermode == "managed":
                pager_rate_limit = int(cmt.CONF['global'].get("pager_rate_limit", 7200))
                t1 = int(cmt.PERSIST.get_key("pager_last_send", 0))
                t2 = int(time.time())
                if t2 - t1 <= pager_rate_limit:
                    waitfor = t1 + pager_rate_limit - t2
                    logit("Pager rate-limit reached ({} sec to wait) for pager {}".format(waitfor, pager))
                    continue

        if pagertype == "team_channel" or pagertype =="teams":
            if teams_sendreal(pager, pagerconf, report):
                debug("Pager fired : ", pager)
                rate_limit_update = True

        elif pagertype == "pagerduty":
            pagerduty_sendreal(pager,pagerconf, report)
            pass

        elif pagertype == "smtp":
            #smtp_sendreal(pager, pagerconf, report)
            pass

        else:
            debug("Unknown pager type in conf for ", pager)            

    # update rate_limit
    if not cmt.ARGS['devmode']:
        cmt.PERSIST.set_key("pager_last_send", time.time() )


# ------------------------------------------------------------
#  TEAMS
# ------------------------------------------------------------
def teams_sendreal(pager, pagerconf, report):

    # get Teams alert channel url
    url = pagerconf.get('url')
    debug("pager url :", url)

    # prepare message
    origin = cmt.CONF['global']['cmt_group'] + '/' + cmt.CONF['global']['cmt_node']
    color = "FF0000"
    title = "CMT ALERT from " + origin

    message = ""
    for c in report.checks:
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

    teams_message = """
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
""".format(color, title, origin, message)

    debug("Pager Message : ", teams_message)

    headers = {
        'Content-Type': 'application/json'
    }
 
    if cmt.ARGS['devmode']:
        print("DEVMODE : ", url, headers, teams_message)


    ssl_verify = pagerconf.get("ssl_verify", False) is True
    http_code = pagerconf.get("http_code", 200)

    # default : use env proxies
    # if "http_proxy:noenv" remove env proxies
    # else use specified proxies
    proxies = {} 
    my_global_http_proxy = cmt.CONF.get('http_proxy',"")
    my_global_https_proxy = cmt.CONF.get('https_proxy',my_global_http_proxy) 
    my_http_proxy = pagerconf.get('http_proxy',my_global_http_proxy)
    my_https_proxy = pagerconf.get('https_proxy',my_global_https_proxy) 
    if my_http_proxy != "":
        proxies["http"] = my_http_proxy
    if my_https_proxy != "":
        proxies["https"] = my_https_proxy
    # if my_http_proxy == "noenv":
    #     cmt.SESSION.trust_env = False
    #     proxies = {}

    else:
        try:
            r = requests.post(
                url, 
                headers=headers, 
                proxies=proxies,
                verify=ssl_verify,
                data=teams_message, 
                timeout=cmt.TEAMS_TIMEOUT)
        except Exception as e:
            logit("Teams Send Error for {} : {}".format(pager, e))
            return False

        if r.status_code != http_code:
            logit("Alert couldn't send to Teams - response  " + str(r))
            return False

    return True

# -------------- 
def teams_sendtest(pager, pagerconf):

    url = pagerconf.get('url')
    debug("pager url :", url)

    origin = cmt.CONF['global']['cmt_group'] + '/' + cmt.CONF['global']['cmt_node']
    title = "TEST TEST from " + origin

    teams_message = """
{{
    "@type": "MessageCard",
    "@context": "http://schema.org/extensions",
    "summary": "Monitoring",
    "themeColor": "0000FF",
    "sections": [{{
        "activityTitle": "{}",
        "activitySubtitle": "{}",
        "activityText": "Test message to Teams. Please ignore",
        "markdown": false
    }}]
}}
""".format(title, origin)

    debug("Pager Message : ", teams_message)

    headers = {
        'Content-Type': 'application/json'
    }

    ssl_verify = pagerconf.get("ssl_verify", False) is True
    http_code = pagerconf.get("http_code", 200)

    # default : use env proxies
    # if "http_proxy:noenv" remove env proxies
    # else use specified proxies
    proxies = {} 
    my_global_http_proxy = cmt.CONF.get('http_proxy',"")
    my_global_https_proxy = cmt.CONF.get('https_proxy',my_global_http_proxy) 
    my_http_proxy = pagerconf.get('http_proxy',my_global_http_proxy)
    my_https_proxy = pagerconf.get('https_proxy',my_global_https_proxy) 
    if my_http_proxy != "":
        proxies["http"] = my_http_proxy
    if my_https_proxy != "":
        proxies["https"] = my_https_proxy
    # if my_http_proxy == "noenv":
    #     cmt.SESSION.trust_env = False
    #     proxies = {}

 
    if cmt.ARGS['devmode']:
        print("DEVMODE : ", url, headers, teams_message)

    else:
        try:
            r = requests.post(
                url, 
                headers=headers,
                proxies=proxies,
                verify=ssl_verify,                
                data=teams_message, 
                timeout=cmt.TEAMS_TIMEOUT)
        except Exception as e:
            logit("Teams Send Error for {} : {}".format(pager, e))
            return False

        if r.status_code != http_code:
            logit("Alert couldn't send to Teams - response  " + str(r))
            return False

    return True


# ------------------------------------------------------------
# PagerDuty
# ------------------------------------------------------------

def pagerduty_sendreal(pager, pagerconf, report):

    # get url
    url = pagerconf.get('url')
    key = pagerconf.get('key')
    debug("pager url :", url)

    # prepare message
    group = cmt.CONF['global']['cmt_group']
    node = cmt.CONF['global']['cmt_node']
    title = "CMT ALERT for {} - {} ".format(group,node)

    dedup = group + "." + node 

    message = ""
    for c in report.checks:
        if c.alert > 0:
            message = c.get_message_as_str()


    pager_message = """
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
""".format(title, node, group, node, message, key, dedup)

    debug("Pager Message : ", pager_message)

    headers = {
        'Content-Type': 'application/json'
    }

    ssl_verify = pagerconf.get("ssl_verify", False) is True
    http_code = pagerconf.get("http_code", 202)

    # default : use env proxies
    # if "http_proxy:noenv" remove env proxies
    # else use specified proxies
    proxies = {} 
    my_global_http_proxy = cmt.CONF.get('http_proxy',"")
    my_global_https_proxy = cmt.CONF.get('https_proxy',my_global_http_proxy) 
    my_http_proxy = pagerconf.get('http_proxy',my_global_http_proxy)
    my_https_proxy = pagerconf.get('https_proxy',my_global_https_proxy) 
    if my_http_proxy != "":
        proxies["http"] = my_http_proxy
    if my_https_proxy != "":
        proxies["https"] = my_https_proxy
    # if my_http_proxy == "noenv":
    #     cmt.SESSION.trust_env = False
    #     proxies = {}
 
    if cmt.ARGS['devmode']:
        print("DEVMODE : ", url, headers, pager_message)

    else:
        try:
            r = requests.post(
                url, 
                headers=headers, 
                proxies=proxies,
                verify=ssl_verify,                 
                data=pager_message, 
                timeout=cmt.PAGERDUTY_TIMEOUT)
        except Exception as e:
            logit("PagerDuty Send Error for {} : {}".format(pager, e))
            return False

        if r.status_code != http_code:
            logit("Alert couldn't send to PagerDuty - response  " + str(r))
            return False

    return True


