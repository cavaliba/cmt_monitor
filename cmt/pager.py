# cavaliba.com - 2021
# pager.py

import requests
import globals as cmt
from logger import logit, debug


# ------------------------------------------------------------
#  TEAMS
# ------------------------------------------------------------

def teams_send(url=None, color="0000FF", title="CMT Alert", message="n/a", origin="n/a"):

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
    }}],
}}
""".format(color, title, origin, message)


    headers = {
        'Content-Type': 'application/json'
    }

    # SEND !
    if cmt.ARGS['devmode']:
        print("DEVMODE : ", url, headers, message)
        return 200
    # real
    try:
        r = requests.post(url, headers=headers, data=message, timeout=cmt.TEAMS_TIMEOUT)
        return r.status_code
    except Exception as e:
        logit("Teams Send Error : {}".format(e))
        return 0


def pager_test():

    pagerconf = cmt.CONF['pagers'].get('test')
    url = pagerconf.get('url')
    debug("pager url :", url)

    origin = cmt.CONF['global']['cmt_group'] + '/' + cmt.CONF['global']['cmt_node']
    color = "0000FF"
    title = "TEST TEST from " + origin
    message = "Test message to Teams. Please ignore."
    if cmt.ARGS['devmode']:
        # DEVMODE to stdout
        print("DEVMODE : url=({}), title=({}), message=({}), color=({}), origin=({})".format(url, title, message, color, origin))
        return
    # REAL
    r = teams_send(url=url, title=title, message=message, color=color, origin=origin)
    logit("Teams test : " + str(r))
