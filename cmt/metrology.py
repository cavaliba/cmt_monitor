# cavaliba.com - 2021
# metrology.py

import socket
import time
#import json

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

    # avoid sending to bach multiple times(if multiple metrology servers)
    influxdb_already_batched = False

    for metro in cmt.CONF['metrology_servers']:

        metroconf = cmt.CONF['metrology_servers'][metro]
        metrotype = metroconf.get('type', 'unknown')

        send_rawdata = metroconf.get("send_rawdata", True) is True                    
        rawdata_prefix = metroconf.get("rawdata_prefix", "raw_")

        timerange = metroconf.get("enable", "yes")
        if not conf.is_timeswitch_on(timerange):
            debug("Metrology server disabled in conf : ", metro)

        if metrotype == "graylog_udp_gelf":
            gelf_data = build_gelf_message(mycheck)
            graylog_send_udp_gelf(metroconf=metroconf, data=gelf_data)
            debug("Data sent to metrology server ", metro)
            if send_rawdata:
                for index, val in enumerate(mycheck.multievent):
                    gelf_data_multi = build_gelf_message(mycheck, index, rawdata_prefix=rawdata_prefix)
                    graylog_send_udp_gelf(metroconf=metroconf, data=gelf_data_multi)
                    debug2("Data sent to metrology server (multievent)", metro)

        elif metrotype == "graylog_http_gelf":
            gelf_data = build_gelf_message(mycheck)
            graylog_send_http_gelf(metroconf=metroconf, data=gelf_data)
            debug("Data sent to metrology server ", metro)
            if send_rawdata:
                for index, val in enumerate(mycheck.multievent):
                    gelf_data_multi = build_gelf_message(mycheck, index, rawdata_prefix=rawdata_prefix)
                    graylog_send_http_gelf(metroconf=metroconf, data=gelf_data_multi)
                    debug2("Data sent to metrology server (multievent)", metro)

        elif metrotype == "elastic_http_json":
            json_data = build_json_message(mycheck)
            elastic_send_http_json(metroconf=metroconf, data=json_data)
            debug("Data sent to metrology server ", metro)
            if send_rawdata:
                for index, val in enumerate(mycheck.multievent):
                    json_data_multi = build_json_message(mycheck, index, rawdata_prefix=rawdata_prefix)
                    elastic_send_http_json(metroconf=metroconf, data=json_data_multi)

        elif metrotype == "influxdb":
            influxdb_data = build_influxdb_message(mycheck, metroconf)
            batch = metroconf.get("batch", True) is True
            if batch:
                if not influxdb_already_batched:
                    influxdb_add_to_batch(influxdb_data)
                    influxdb_already_batched = True
                    debug("Data batched for influx servers")
                    if send_rawdata:
                        for index, val in enumerate(mycheck.multievent):
                            influxdb_data_multi = build_influxdb_message(mycheck, metroconf, index=index)
                            influxdb_add_to_batch(influxdb_data_multi)
                else:
                    # already batched by another influx server
                    pass
            else:
                # immediate send
                influxdb_send_http(metroconf=metroconf, data=influxdb_data)
                debug("Data sent to influx server ", metro)
                if send_rawdata:
                    for index, val in enumerate(mycheck.multievent):
                        influxdb_data_multi = build_influxdb_message(mycheck, metroconf, index=index)
                        influxdb_send_http(metrconf=metroconf, data=influxdb_data_multi)
        else:
            debug("Unknown metrology server type in conf.")


def send_metrology_batch():

    for metro in cmt.CONF['metrology_servers']:

        metroconf = cmt.CONF['metrology_servers'][metro]
        metrotype = metroconf.get('type', 'unknown')        

        if metrotype == "influxdb":
            # same function for batch / no batch
            influxdb_send_http(metroconf=metroconf,data=influxdb_batch)
            debug("Data (batch) sent to metrology server ", metro)

        else:
            pass
            # no batch mode for other metrotype


def get_proxies(metroconf):
    ''' 
    Get global and local (check) proxies configuration. Local overrides Global.
    Use noenv http_proxy option to ignore OS/ENV proxies  and use direct access.
    '''
    proxies = {} 
    my_global_http_proxy = cmt.CONF.get('http_proxy',"")
    my_global_https_proxy = cmt.CONF.get('https_proxy',my_global_http_proxy) 
    my_http_proxy = metroconf.get('http_proxy',my_global_http_proxy)
    my_https_proxy = metroconf.get('https_proxy',my_global_https_proxy) 
    if my_http_proxy != "":
        proxies["http"] = my_http_proxy
    if my_https_proxy != "":
        proxies["https"] = my_https_proxy
    noenv = False
    if my_http_proxy == "noenv":
        noenv = True
    #     cmt.SESSION.trust_env = False
    return proxies, noenv    

# ------------------------------------------------------------
# GRAYLOG GELF 
# ------------------------------------------------------------

# GRAYLOG / GELF
def build_gelf_message(check, index=None, rawdata_prefix='raw'):
    '''Prepare a GELF JSON message suitable to be sent to a Graylog GELF server.'''

    graylog_data = '"version":"1.1"'
    graylog_data += ',"host":"{}_{}"'.format(check.group, check.node)

    # common values
    graylog_data += ',"cmt_group":"{}"'.format(check.group)
    graylog_data += ',"cmt_node":"{}"'.format(check.node)

    graylog_data += ',"cmt_node_env":"{}"'.format(check.node_env)
    #graylog_data += ',"cmt_node_role":"{}"'.format(check.node_role)
    #graylog_data += ',"cmt_node_location":"{}"'.format(check.node_location)

    graylog_data += ',"cmt_version":"{}"'.format(check.version)

    graylog_data += ',"cmt_module":"{}"'.format(check.module)
    graylog_data += ',"cmt_check":"{}"'.format(check.check)    # deprecated
    graylog_data += ',"cmt_id":"{}"'.format(check.get_id())


    # rawdata / multi-event part
    if index is not None:
        graylog_data += ',"cmt_raw_id":{}'.format(index)
        event = check.multievent[index]
        m = "{}".format(check.check)
        for k,v in event.items():
            m = m + " ; {}={}".format(k,v)
        #QUOTES BUG : m = m + json.dumps(event)
        graylog_data += ',"short_message":"{}"'.format(m)
        graylog_data += ',"cmt_message":"{}"'.format(m)
        for k,v in event.items():
            try:
                float(v)
                graylog_data += ',"{}_{}_{}":{}'.format(rawdata_prefix, check.check, k, v)
            except Exception as e:
                graylog_data += ',"{}_{}_{}":"{}"'.format(rawdata_prefix, check.check, k, v)

            debug2("Build gelf rawdata multievent: ", str(k), str(v))

    # main / standard event
    else:

        # cmt_message  : Check name + check.message + all items.alert_message
        m = "{} - ".format(check.module)
        m = m + check.get_message_as_str()
        graylog_data += ',"short_message":"{}"'.format(m)
        graylog_data += ',"cmt_message":"{}"'.format(m)

        # check items key/values
        for item in check.checkitems:
            try:
                float(item.value)
                graylog_data += ',"cmt_{}":{}'.format(item.name, item.value)
            except ValueError:
                graylog_data += ',"cmt_{}":"{}"'.format(item.name, item.value)
            debug2("Build gelf data : ", str(item.name), str(item.value))


        # graylog_data += ',"cmt_alert":{}'.format(check.alert)
        # graylog_data += ',"cmt_severity":{}'.format(check.severity)
        graylog_data += ',"alert":"{}"'.format(cmt.get_alert_label(check.alert))
        graylog_data += ',"severity":"{}"'.format(cmt.get_severity_label(check.severity))


    # all messages
    graylog_data = '{' + graylog_data + '}'
    return graylog_data


def graylog_send_udp_gelf(metroconf={}, data=""):

    # data = '"demo":"42"'
    # mess = '{ "version":"1.1", "host":"host-test", "short_message":"CMT gelf test", ' + data + ' }'

    host = metroconf.get('host','localhost')
    port = metroconf.get('port', 12201)


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



def graylog_send_http_gelf(metroconf={}, data=""):

    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

    url = metroconf.get('url','http://localhost/')
    ssl_verify = metroconf.get("ssl_verify", True) is True
    http_code = metroconf.get("http_code", 202)
    proxies, proxy_noenv = get_proxies(metroconf)

    if proxy_noenv:
        cmt.SESSION.trust_env = False
        proxies={}

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
            proxies=proxies,
            timeout=cmt.GRAYLOG_HTTP_TIMEOUT)
        debug("Message sent to graylog(http/gelf) ; status = " + str(r.status_code))
    except Exception as e:
        logit("Error - couldn't send graylog message (http/gelf) to {} - {}".format(url, e))
        cmt.GRAYLOG_HTTP_SUSPENDED = True
        return

    if http_code>0:
        if r.status_code != http_code:
            logit("Alert couldn't send to Graylog HTTP - bad response: " + str(r))
            return

    return

# ------------------------------------------------------------
# ElasticSearch
# ------------------------------------------------------------


def build_json_message(check, index=None, rawdata_prefix='raw'):

    '''Prepare a JSON message suitable to be sent to an Elatic server.'''

    json_data = ''

    # common values
    json_data += '"cmt_group":"{}"'.format(check.group)
    json_data += ',"cmt_node":"{}"'.format(check.node)

    json_data += ',"cmt_node_env":"{}"'.format(check.node_env)
    #json_data += ',"cmt_node_role":"{}"'.format(check.node_role)
    #json_data += ',"cmt_node_location":"{}"'.format(check.node_location)

    json_data += ',"cmt_version":"{}"'.format(check.version)

    json_data += ',"cmt_module":"{}"'.format(check.module)
    json_data += ',"cmt_check":"{}"'.format(check.check)    # deprecated
    json_data += ',"cmt_id":"{}"'.format(check.get_id())


    # rawadata / multi-event part
    if index is not None:
        json_data += ',"cmt_raw_id":{}'.format(index)
        event = check.multievent[index]
        m = "{} ".format(check.check)
        for k,v in event.items():
            m = m + "; {}={}".format(k,v)
        #QUOTES BUG : m = m + json.dumps(event)
        json_data += ',"short_message":"{}"'.format(m)
        json_data += ',"cmt_message":"{}"'.format(m)
        for k,v in event.items():
            try:
                float(v)
                json_data += ',"{}_{}_{}":{}'.format(rawdata_prefix, check.check, k, v)
            except Exception as e:
                json_data += ',"{}_{}_{}":"{}"'.format(rawdata_prefix, check.check, k, v)

            debug2("Build json data rawdata multievent: ", str(k), str(v))

    # main / standard event
    else:
        # cmt_message  : Check name + check.message + all items.alert_message
        m = "{} - ".format(check.module)
        m = m + check.get_message_as_str()
        json_data += ',"cmt_message":"{}"'.format(m)

        # check items key/values
        for item in check.checkitems:


            value2 = item.value
            
            if item.multiline:
                #print("********************************** multi")
                # not suitable for elastic line protocol    
                value2 = value2.replace('\n', ' ; ')
                value2 = value2.replace('\r', ' ')
                # value2 = '["a","b","c"]'
                # json_data += ',"cmt_{}":{}'.format(item.name, value2)
                # continue 

            try:
                float(value2)
                json_data += ',"cmt_{}":{}'.format(item.name, value2)
            except ValueError:
                json_data += ',"cmt_{}":"{}"'.format(item.name, value2)

            debug2("Build json data : ", str(item.name), str(value2))


        # json_data += ',"cmt_alert":{}'.format(check.alert)
        # json_data += ',"cmt_severity":{}'.format(check.severity)
        json_data += ',"alert":"{}"'.format(cmt.get_alert_label(check.alert))
        json_data += ',"severity":"{}"'.format(cmt.get_severity_label(check.severity))

    json_data = '{' + json_data + '}'
    return json_data



def elastic_send_http_json(metroconf={}, data=""):

    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

    url = metroconf.get('url','http://localhost/')
    ssl_verify = metroconf.get("ssl_verify", True) is True
    http_code = metroconf.get("http_code", 201)
    proxies, proxy_noenv = get_proxies(metroconf)

    if proxy_noenv:
        cmt.SESSION.trust_env = False
        proxies={}

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
            proxies=proxies,
            timeout=cmt.METROLOGY_HTTP_TIMEOUT)
        debug("Message sent to elastic(http/json) ; status = " + str(r.status_code))
    except Exception as e:
        logit("Error - couldn't send elastic message (http/json) to {} - {}".format(url, e))
        cmt.METROLOGY_HTTP_SUSPENDED = True
        return

    if http_code>0:
        if r.status_code != http_code:
            logit("Alert couldn't send to Elastic - bad response: " + str(r))
            return

    return

# ------------------------------------------------------------
# InfluxDB V1 & V2
# ------------------------------------------------------------
# CMT V1.7+


def build_influxdb_message(check, metroconf, index=None):

    ''' Prepare a string with and influxdb protocol formatted message.'''

    time_format = metroconf.get('time_format','')
    rawdata_prefix = metroconf.get("rawdata_prefix", "raw_")
    single_measurement = metroconf.get('single_measurement',True) is True
    send_tags = metroconf.get('send_tags',False) is True

    influx_data = ''

    # measurement section
    # -------------------
    # cmt,cmt_module=XX,cmt_group=XX,cmt_node=XX,cmt_check=XX,cmt_node_env=XX k=v,k=v
    # cmt_{module},cmt_group=XX,cmt_node=XX,cmt_check=XX,cmt_node_env=XX k=v,k=v
    if single_measurement:
        influx_data += 'cmt,cmt_module=' + check.module
    else:
        influx_data += 'cmt_' + check.module

    # tag section
    # ------------

    # global tags
    influx_data += ',cmt_group={},cmt_node={},cmt_check={},cmt_node_env={}'.format(
        check.group,
        check.node,
        check.check,
        check.node_env)

    # none datapoint checkitems tags
    for item in check.checkitems:
        if item.datapoint:
            # skip items to be  inserted in the influx field section of line protocol
            continue
        # add as a tag in the influx tag section
        influx_data += ','
        try:
            float(item.value)
            influx_data += 'cmt_{}={}'.format(item.name, item.value)
        except ValueError:
            influx_data += 'cmt_{}="{}"'.format(item.name, item.value)

    # cmt conf tags
    if send_tags:
        for item in check.checkitems:                
            if item.name.startswith('tag_'):
                #float(item.value)
                influx_data += ',cmt_{}="{}"'.format(item.name, item.value)

    # severity, alert
    # influx_data += ',cmt_alert={}'.format(check.alert)
    # influx_data += ',cmt_severity={}'.format(check.severity)
    influx_data += ',alert="{}"'.format(cmt.get_alert_label(check.alert))
    influx_data += ',severity="{}"'.format(cmt.get_severity_label(check.severity))


    # field section
    # ------------

    # rawdata multi-event part
    if index is not None:
        influx_data += ' cmt_raw_id={}'.format(index)
        event = check.multievent[index]
        for k,v in event.items():
            try:
                float(v)
                influx_data += ',{}_{}_{}={}'.format(rawdata_prefix, check.check, k, v)
            except ValueError:
                influx_data += ',{}_{}_{}="{}"'.format(rawdata_prefix, check.check, k, v)

    # main / standard event
    else:
        influx_data += ' '
        first_item = True

        for item in check.checkitems:

            if item.name.startswith('tag_'):
                continue

            if not item.datapoint:
                # skip items already inserted in the influx tag section of line protocol
                continue

            if item.multiline:
                # not suitable for influx line protocol
                continue

            if not first_item:        
                influx_data += ','

            try:
                float(item.value)
                influx_data += 'cmt_{}={}'.format(item.name, item.value)
            except ValueError:
                influx_data += 'cmt_{}="{}"'.format(item.name, item.value)

            first_item = False

        # also add severity, alert as field/value items in the influx line protocol
        if not first_item:        
            influx_data += ','
        # influx_data += 'cmt_alert={}'.format(check.alert)
        # influx_data += ',cmt_severity={}'.format(check.severity)
        influx_data += ',alert="{}"'.format(cmt.get_alert_label(check.alert))
        influx_data += ',severity="{}"'.format(cmt.get_severity_label(check.severity))


    # timestamp section
    # -----------------

    # timestamp in milliseconds
    tsms = round(time.time() * 1000)
    if time_format == 'msec':
        influx_data += " {}".format(tsms)
    elif time_format == 'sec':
        influx_data += " {}".format(round(tsms / 1000))
    elif time_format == 'nsec':
        influx_data += " {}".format(round(tsms) * 1000000)
    else:
        pass    # no timestamp ; will be provided by influxdb server

    return influx_data


def influxdb_add_to_batch(influxdb_data):

    global influxdb_batch
    influxdb_batch += influxdb_data
    influxdb_batch += "\n"


def influxdb_send_http(metroconf={}, data=""):

    headers = {'Content-type': 'application/x-www-form-urlencoded', 'Accept': '*/*'}

    url = metroconf.get('url', 'http://localhost/')
    username = metroconf.get('username','')
    password = metroconf.get('password','')
    token = metroconf.get('token','')
    ssl_verify = metroconf.get("ssl_verify", True) is True
    http_code = metroconf.get("http_code", 204)
    proxies, proxy_noenv = get_proxies(metroconf)

    if proxy_noenv:
        cmt.SESSION.trust_env = False
        proxies={}

    if cmt.METROLOGY_INFLUXDB_SUSPENDED:
        logit("suspended - INFLUXDB message suspended/not sent to " + str(url))
        return

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
                proxies=proxies,
                timeout=cmt.METROLOGY_INFLUXDB_TIMEOUT)        

        # basic authentication
        elif len(username)>0:
            r = cmt.SESSION.post(url, 
                data=data, 
                headers=headers,
                verify=ssl_verify,
                proxies=proxies,
                auth=(username, password),
                timeout=cmt.METROLOGY_INFLUXDB_TIMEOUT)

        # no auth / auth in URL ?u=XXX&p=XXX
        else:
            r = cmt.SESSION.post(url, 
                data=data, 
                headers=headers, 
                verify=ssl_verify,
                proxies=proxies,
                timeout=cmt.METROLOGY_INFLUXDB_TIMEOUT)        

        debug("Message sent to INFLUXDB ; status = " + str(r.status_code))

    except Exception as e:
        logit("Error - couldn't send INFLUXDB message to {} - {}".format(url, e))
        cmt.METROLOGY_INFLUXDB_SUSPENDED = True
        return

    if http_code>0:
        if r.status_code != http_code:
            logit("Alert couldn't send to InfluxDB - bad response: " + str(r))
            return

    return

