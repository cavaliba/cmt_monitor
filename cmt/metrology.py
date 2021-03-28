# cavaliba.com - 2021
# metrology.py

import socket

import globals as cmt
from logger import logit, debug, debug2


# ------------------------------------------------------------
# Metrology Servers
# ------------------------------------------------------------
# send messages to metrology servers


# GRAYLOG / GELF
def build_gelf_message(check):
    '''Prepare a GELF JSON message suitable to be sent to a Graylog GELF server.'''

    graylog_data = '"version":"1.1",'
    graylog_data += '"host":"{}_{}",'.format(check.group, check.node)

    # common values
    graylog_data += '"cmt_group":"{}",'.format(check.group)
    graylog_data += '"cmt_node":"{}",'.format(check.node)

    graylog_data += '"cmt_node_env":"{}",'.format(check.node_env)
    graylog_data += '"cmt_node_role":"{}",'.format(check.node_role)
    graylog_data += '"cmt_node_location":"{}",'.format(check.node_location)

    graylog_data += '"cmt_module":"{}",'.format(check.module)
    graylog_data += '"cmt_check":"{}",'.format(check.check)    # deprecated
    graylog_data += '"cmt_id":"{}",'.format(check.get_id())

    # cmt_message  : Check name + check.message + all items.alert_message
    m = "{} - ".format(check.module)
    m = m + check.get_message_as_str()
    graylog_data += '"short_message":"{}",'.format(m)
    graylog_data += '"cmt_message":"{}",'.format(m)
    # print("ooo    ",m)

    # check items key/values
    for item in check.checkitems:
        # TODO : improve numerical detection : may cause weird elastic indexing issues
        # if numerical value is the first one for a new field, e.g. after index rotation
        # good enough here for the moment.
        try:
            float(item.value)
            graylog_data += '"cmt_{}":{},'.format(item.name, item.value)
        except ValueError:
            graylog_data += '"cmt_{}":"{}",'.format(item.name, item.value)

        debug2("Build gelf data : ", str(item.name), str(item.value))


    # notifications
    graylog_data += '"cmt_notification":{},'.format(check.get_notification())

    # cmt_alert ?
    if check.alert > 0:
        has_alert = "yes"
    else:
        has_alert = "no"
    graylog_data += '"cmt_alert":"{}",'.format(has_alert)

    # cmt_warn ?
    if check.warn > 0:
        has_warn = "yes"
    else:
        has_warn = "no"
    graylog_data += '"cmt_warning":"{}",'.format(has_warn)

    # cmt_notice ?
    if check.notice > 0:
        has_notice = "yes"
    else:
        has_notice = "no"
    graylog_data += '"cmt_notice":"{}"'.format(has_notice)

    graylog_data = '{' + graylog_data + '}'
    return graylog_data



def graylog_send_http_gelf(url, data=""):

    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

    if cmt.GRAYLOG_HTTP_SUSPENDED:
        logit("suspended - HTTP graylog message (http/gelf) not sent to " + str(url))
        return

    if cmt.ARGS['devmode']:
        print("DEVMODE : graylog http : ", url, data, headers)
        return

    try:
        r = cmt.SESSION.post(url, data=data, headers=headers, timeout=cmt.GRAYLOG_HTTP_TIMEOUT)
        debug("Message sent to graylog(http/gelf) ; status = " + str(r.status_code))
    except Exception as e:
        logit("Error - couldn't send graylog message (http/gelf) to {} - {}".format(url, e))
        cmt.GRAYLOG_HTTP_SUSPENDED = True


def graylog_send_udp_gelf(host, port=12201, data=""):

    # data = '"demo":"42"'
    # mess = '{ "version":"1.1", "host":"host-test", "short_message":"CMT gelf test", ' + data + ' }'

    if cmt.ARGS['devmode']:
        print("DEVMODE : graylog udp : ", host, port, data)
        return

    binpayload = bytes(str(data), "utf-8")

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (host, port)

    try:
        sock.sendto(binpayload, server_address)
        sock.close()
        debug("Message sent to graylog(udp/gelf)")
    except Exception as e:
        logit("Error - couldn't send graylod message (udp/gelf) to {} - {}".format(host, e))

# ----


def elastic6_send_http_json(url, data=""):

    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

    if cmt.METROLOGY_HTTP_SUSPENDED:
        logit("suspended - HTTP graylog message (http/gelf) not sent to " + str(url))
        return

    if cmt.ARGS['devmode']:
        print("DEVMODE : elastic6 http : ", url, data, headers)
        return

    try:
        r = cmt.SESSION.post(url, data=data, headers=headers, timeout=cmt.METROLOGY_HTTP_TIMEOUT)
        debug("Message sent to elastic6(http/json) ; status = " + str(r.status_code))
    except Exception as e:
        logit("Error - couldn't send elastic6 message (http/json) to {} - {}".format(url, e))
        cmt.METROLOGY_HTTP_SUSPENDED = True


def build_json_message(check):
    
    '''Prepare a JSON message suitable to be sent to an Elatic server.'''

    json_data = ''

    # common values
    json_data += '"cmt_group":"{}",'.format(check.group)
    json_data += '"cmt_node":"{}",'.format(check.node)

    json_data += '"cmt_node_env":"{}",'.format(check.node_env)
    json_data += '"cmt_node_role":"{}",'.format(check.node_role)
    json_data += '"cmt_node_location":"{}",'.format(check.node_location)

    json_data += '"cmt_module":"{}",'.format(check.module)
    json_data += '"cmt_check":"{}",'.format(check.check)    # deprecated
    json_data += '"cmt_id":"{}",'.format(check.get_id())

    # cmt_message  : Check name + check.message + all items.alert_message
    m = "{} - ".format(check.module)
    m = m + check.get_message_as_str()
    json_data += '"cmt_message":"{}",'.format(m)

    # check items key/values
    for item in check.checkitems:
        # TODO : improve numerical detection : may cause weird elastic indexing issues
        # if numerical value is the first one for a new field, e.g. after index rotation
        # good enough here for the moment.
        try:
            float(item.value)
            json_data += '"cmt_{}":{},'.format(item.name, item.value)
        except ValueError:
            json_data += '"cmt_{}":"{}",'.format(item.name, item.value)

        debug2("Build json data : ", str(item.name), str(item.value))


    # notifications
    json_data += '"cmt_notification":{},'.format(check.get_notification())

    # cmt_alert ?
    if check.alert > 0:
        has_alert = "yes"
    else:
        has_alert = "no"
    json_data += '"cmt_alert":"{}",'.format(has_alert)

    # cmt_warn ?
    if check.warn > 0:
        has_warn = "yes"
    else:
        has_warn = "no"
    json_data += '"cmt_warning":"{}",'.format(has_warn)

    # cmt_notice ?
    if check.notice > 0:
        has_notice = "yes"
    else:
        has_notice = "no"
    json_data += '"cmt_notice":"{}"'.format(has_notice)

    json_data = '{' + json_data + '}'

    # return '{ "cmt_test2" : 45 }' 
    return json_data
