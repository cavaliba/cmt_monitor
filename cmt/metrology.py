# cavaliba.com - 2021
# metrology.py

import socket
import time

import globals as cmt
from logger import logit, debug, debug2
import conf

# ------------------------------------------------------------
# Metrology Servers
# ------------------------------------------------------------
# send messages to metrology servers

influxdb_batch = ""


# ------------------------------------------------------------
# Main entry point : send_metrology(check)
# ------------------------------------------------------------

def send_metrology(mycheck):

    ''' Send Check results (event, multiple CheckItems)
        to metrology servers.
        Or add to batch for batch sending at the end of run.
    '''

    influxdb_batched = False

    for metro in cmt.CONF['metrology_servers']:

        metroconf = cmt.CONF['metrology_servers'][metro]
        metrotype = metroconf.get('type', 'unknown')

        timerange = metroconf.get("enable", "yes")
        if not conf.is_timeswitch_on(timerange):
            debug("Metrology server disabled in conf : ", metro)
            continue

        if metrotype == "graylog_udp_gelf":
            gelf_data = build_gelf_message(mycheck)
            host = metroconf['host']
            port = metroconf['port']
            graylog_send_udp_gelf(host=host, port=port, data=gelf_data)
            debug("Data sent to metrology server ", metro)

        elif metrotype == "graylog_http_gelf":
            gelf_data = build_gelf_message(mycheck)
            url = metroconf['url']
            ssl_verify = metroconf.get("ssl_verify", False) is True
            graylog_send_http_gelf(url=url, data=gelf_data, ssl_verify=ssl_verify)
            debug("Data sent to metrology server ", metro)

        elif metrotype == "elastic_http_json":
            json_data = build_json_message(mycheck)
            url = metroconf['url']
            ssl_verify = metroconf.get("ssl_verify", False) is True
            elastic_send_http_json(url=url, data=json_data, ssl_verify=ssl_verify)
            debug("Data sent to metrology server ", metro)

        elif metrotype == "influxdb":
            influxdb_data = build_influxdb_message(mycheck, metroconf)
            url = metroconf['url']
            username = metroconf.get('username','')
            password = metroconf.get('password','')
            token = metroconf.get('token','')
            ssl_verify = metroconf.get("ssl_verify", False) is True
            batch = metroconf.get("batch", True) is True
            if batch:
                if not influxdb_batched:
                    # print("****")
                    influxdb_add_to_batch(influxdb_data)
                    influxdb_batched = True
                    debug("Data batched for influx servers")
            else:
                influxdb_send_http(
                    url, 
                    username=username, 
                    password=password, 
                    token=token, 
                    ssl_verify=ssl_verify,
                    data=influxdb_data)
                debug("Data sent to influx server ", metro)

        else:
            debug("Unknown metrology server type in conf.")


def send_metrology_batch():

    for metro in cmt.CONF['metrology_servers']:

        metroconf = cmt.CONF['metrology_servers'][metro]
        metrotype = metroconf.get('type', 'unknown')        

        if metrotype == "influxdb":
            url = metroconf['url']
            username = metroconf.get('username','')
            password = metroconf.get('password','')
            token = metroconf.get('token','')
            ssl_verify = metroconf.get("ssl_verify", False) is True
            #influxdb_send_http_batch(url, username=username, password=password, data=influxdb_batch)
            # same function for batch / no btch
            influxdb_send_http(
                url, 
                username=username, 
                password=password, 
                token=token, 
                data=influxdb_batch, 
                ssl_verify=ssl_verify)
            debug("Data (batch) sent to metrology server ", metro)

        else:
            pass
            # no batch mode for other metrotype


# ------------------------------------------------------------
# GRAYLOG GELF 
# ------------------------------------------------------------

# GRAYLOG / GELF
def build_gelf_message(check):
    '''Prepare a GELF JSON message suitable to be sent to a Graylog GELF server.'''

    graylog_data = '"version":"1.1"'
    graylog_data += ',"host":"{}_{}"'.format(check.group, check.node)

    # common values
    graylog_data += ',"cmt_group":"{}"'.format(check.group)
    graylog_data += ',"cmt_node":"{}"'.format(check.node)

    graylog_data += ',"cmt_node_env":"{}"'.format(check.node_env)
    graylog_data += ',"cmt_node_role":"{}"'.format(check.node_role)
    graylog_data += ',"cmt_node_location":"{}"'.format(check.node_location)

    graylog_data += ',"cmt_version":"{}"'.format(check.version)

    graylog_data += ',"cmt_module":"{}"'.format(check.module)
    graylog_data += ',"cmt_check":"{}"'.format(check.check)    # deprecated
    graylog_data += ',"cmt_id":"{}"'.format(check.get_id())

    # cmt_message  : Check name + check.message + all items.alert_message
    m = "{} - ".format(check.module)
    m = m + check.get_message_as_str()
    graylog_data += ',"short_message":"{}"'.format(m)
    graylog_data += ',"cmt_message":"{}"'.format(m)

    # check items key/values
    for item in check.checkitems:
        # TODO : improve numerical detection : may cause weird elastic indexing issues
        # if numerical value is the first one for a new field, e.g. after index rotation
        # good enough here for the moment.
        try:
            float(item.value)
            graylog_data += ',"cmt_{}":{}'.format(item.name, item.value)
        except ValueError:
            graylog_data += ',"cmt_{}":"{}"'.format(item.name, item.value)

        debug2("Build gelf data : ", str(item.name), str(item.value))


    # NEW V1.6
    notif = check.get_notification()
    if notif > 0:
        graylog_data += ',"cmt_notification":{}'.format(notif)


    graylog_data = '{' + graylog_data + '}'
    return graylog_data



def graylog_send_http_gelf(url, data="", ssl_verify=False):

    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

    if cmt.GRAYLOG_HTTP_SUSPENDED:
        logit("suspended - HTTP graylog message (http/gelf) not sent to " + str(url))
        return

    if cmt.ARGS['devmode']:
        print("DEVMODE : graylog http : ", url, data, headers)
        return

    try:
        r = cmt.SESSION.post(
            url, 
            data=data, 
            headers=headers, 
            verify=ssl_verify,
            timeout=cmt.GRAYLOG_HTTP_TIMEOUT)
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


# ------------------------------------------------------------
# InfluxDB V1 & V2
# ------------------------------------------------------------
# V1.7+


def build_influxdb_message(check, metroconf):

    ''' Prepare a string with and influxdb protocol formatted message.'''

    influx_data = ''

    # module,cmt_group=XX,cmt_node=XX,cmt_check=XX,cmt_node_env=XX k=v,k=v
    influx_data += 'cmt_' + check.module
    influx_data += ',cmt_group={},cmt_node={},cmt_check={},cmt_node_env={}'.format(
        check.group,
        check.node,
        check.check,
        check.node_env
    )

    # add tags
    send_tags = metroconf.get('send_tags',False) is True
    if send_tags:
        for item in check.checkitems:                
            if item.name.startswith('tag_'):
                float(item.value)
                influx_data += ',cmt_{}={}'.format(item.name, item.value)


    first_item = True
    for item in check.checkitems:

        if item.name.startswith('tag_'):
            continue

        if first_item:
            influx_data += ' '
        else:
            influx_data += ','

        try:
            float(item.value)
            influx_data += 'cmt_{}={}'.format(item.name, item.value)
        except ValueError:
            influx_data += 'cmt_{}="{}"'.format(item.name, item.value)

        first_item = False


    notif = check.get_notification()
    influx_data += ',cmt_notification={}'.format(notif)

    # timestamp in milliseconds
    tsms = round(time.time() * 1000)
    time_format = metroconf.get('time_format','')
    if time_format == 'msec':
        influx_data += " {}".format(tsms)
    elif time_format == 'sec':
        influx_data += " {}".format(round(tsms / 1000))
    elif time_format == 'nsec':
        influx_data += " {}".format(round(tsms) * 1000000)
    else:
        pass    # no timestamp ; provided by influxdb server

    #return "cmt_test,cmt_node=test,cmt_group=test,cmt_check=mytest,cmt_node_env=test cmt_value1=1,cmt_value2=2 time"
    return influx_data


def influxdb_add_to_batch(influxdb_data):

    global influxdb_batch
    influxdb_batch += influxdb_data
    influxdb_batch += "\n"


def influxdb_send_http(url, username="", password="", token="", data="", ssl_verify=False):

    headers = {'Content-type': 'application/x-www-form-urlencoded', 'Accept': '*/*'}

    if cmt.METROLOGY_INFLUXDB_SUSPENDED:
        logit("suspended - INFLUXDB message suspended/not sent to " + str(url))
        return

    #print("********************************",cmt.ARGS['devmode'])
    if cmt.ARGS['devmode']:
        print("DEVMODE : INFLUXDB : ", url)
        print(data)
        return

    try:
        # token authentication (V1/V2)
        # --header "Authorization: Token YOURAUTHTOKEN" \
        if len(token) > 0:   
            headers["Authorization"] = "Token {}".format(token)
            r = cmt.SESSION.post(url, 
                data=data, 
                headers=headers, 
                verify=ssl_verify,
                timeout=cmt.METROLOGY_INFLUXDB_TIMEOUT)        

        # basic authentication
        elif len(username)>0:
            r = cmt.SESSION.post(url, 
                data=data, 
                headers=headers,
                verify=ssl_verify,
                auth=(username, password),
                timeout=cmt.METROLOGY_INFLUXDB_TIMEOUT)

        # no auth / auth in URL ?u=XXX&p=XXX
        else:
            r = cmt.SESSION.post(url, 
                data=data, 
                headers=headers, 
                verify=ssl_verify,
                timeout=cmt.METROLOGY_INFLUXDB_TIMEOUT)        

        debug("Message sent to INFLUXDB ; status = " + str(r.status_code))

    except Exception as e:
        logit("Error - couldn't send INFLUXDB message to {} - {}".format(url, e))
        cmt.METROLOGY_INFLUXDB_SUSPENDED = True


#def influxdb_send_http_batch(url, username="", password="", token="", data=""):
#    pass

# ------------------------------------------------------------
# ElasticSearch
# ------------------------------------------------------------


def build_json_message(check):

    '''Prepare a JSON message suitable to be sent to an Elatic server.'''

    json_data = ''

    # common values
    json_data += '"cmt_group":"{}"'.format(check.group)
    json_data += ',"cmt_node":"{}"'.format(check.node)

    json_data += ',"cmt_node_env":"{}"'.format(check.node_env)
    json_data += ',"cmt_node_role":"{}"'.format(check.node_role)
    json_data += ',"cmt_node_location":"{}"'.format(check.node_location)

    json_data += ',"cmt_version":"{}"'.format(check.version)

    json_data += ',"cmt_module":"{}"'.format(check.module)
    json_data += ',"cmt_check":"{}"'.format(check.check)    # deprecated
    json_data += ',"cmt_id":"{}"'.format(check.get_id())

    # cmt_message  : Check name + check.message + all items.alert_message
    m = "{} - ".format(check.module)
    m = m + check.get_message_as_str()
    json_data += ',"cmt_message":"{}"'.format(m)

    # check items key/values
    for item in check.checkitems:
        # TODO : improve numerical detection : may cause weird elastic indexing issues
        # if numerical value is the first one for a new field, e.g. after index rotation
        # good enough here for the moment.
        try:
            float(item.value)
            json_data += ',"cmt_{}":{}'.format(item.name, item.value)
        except ValueError:
            json_data += ',"cmt_{}":"{}"'.format(item.name, item.value)

        debug2("Build json data : ", str(item.name), str(item.value))


    # NEW V1.6
    # notifications
    notif = check.get_notification()
    if notif > 0:
        json_data += ',"cmt_notification":{}'.format(notif)

    json_data = '{' + json_data + '}'

    return json_data



def elastic_send_http_json(url, data="", ssl_verify=False):

    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

    if cmt.METROLOGY_HTTP_SUSPENDED:
        logit("suspended - HTTP graylog message (http/gelf) not sent to " + str(url))
        return

    if cmt.ARGS['devmode']:
        print("DEVMODE : elastic http : ", url, data, headers)
        return

    try:
        r = cmt.SESSION.post(
            url, 
            data=data, 
            headers=headers, 
            verify=ssl_verify,
            timeout=cmt.METROLOGY_HTTP_TIMEOUT)
        debug("Message sent to elastic(http/json) ; status = " + str(r.status_code))
    except Exception as e:
        logit("Error - couldn't send elastic message (http/json) to {} - {}".format(url, e))
        cmt.METROLOGY_HTTP_SUSPENDED = True




