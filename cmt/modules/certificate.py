# CMT - Cavaliba.com (c) 2022

# module : certificate
# V1 by math2001 - dec 2020
# V2 by cavaliba - jan 2022

import ssl
import socket
import datetime

import globals as cmt
from checkitem import CheckItem

CERT_SOCKET_TIMEOUT = 3

DEFAULT_CERT_WARNING = 7
DEFAULT_CERT_NOTICE  = 30

# severity = NOTICE  if delay < notice_in
# severity = WARNING if delay < warning_in
# severity = CRITICAL if delay  expired




def get_source_infos(rdns):

    infos = {}

    for rdn in rdns:
        for key, value in rdn:
            if key in ("organizationName", "commonName"):
                infos[key] = value

    return {
        "organizationName": infos.get("organizationName", "<no organization name>"),
        "commonName": infos.get("commonName", "<no common name>"),
        }



def check(c):


    hostname = c.conf.get("hostname", "localhost")    # remote network target
    port = c.conf.get("port", 443)                    # remote network port
    name = c.conf.get("name", hostname)               # expected subject name in cert

    # for previous configuration format backward compatibility
    try:
        threshold_warning = int(c.conf.get("warning_in", DEFAULT_CERT_WARNING))
    except:
        threshold_warning = DEFAULT_CERT_WARNING
    try:    
        threshold_notice = int(c.conf.get("notice_in", DEFAULT_CERT_NOTICE))
    except:
        threshold_notice = DEFAULT_CERT_NOTICE

    hostdisplay = "{}:{}".format(hostname,port)
    c.add_item(CheckItem("certificate_host", hostdisplay, "", datapoint=False))
    c.add_item(CheckItem("certificate_name", name, unit="", datapoint=False))


    context = ssl.create_default_context()

    try:
        with socket.create_connection((hostname, port),CERT_SOCKET_TIMEOUT) as sock:
            with context.wrap_socket(sock, server_hostname = name) as ssock:
                cert = ssock.getpeercert()
    except ConnectionRefusedError as e:
        c.severity = cmt.SEVERITY_CRITICAL
        c.add_message("no connection to {}".format(hostdisplay))
        return c
    except ssl.SSLError as e:
        c.severity = cmt.SEVERITY_CRITICAL
        c.add_message("no ssl connection to {}".format(hostdisplay))        
        return c
    except socket.timeout as e: 
        c.severity = cmt.SEVERITY_CRITICAL
        c.add_message("timeout to {}".format(hostdisplay))        
        return c        
    except:
        c.severity = cmt.SEVERITY_CRITICAL
        c.add_message("couldn't get peer cert from {}".format(hostdisplay))        
        return c        

    if cert is None:
        c.severity = cmt.SEVERITY_CRITICAL
        c.add_message("no certificate found for {}".format(hostdisplay))
        #c.add_message("no certificate found for {}:{} - err = {}".format(hostname, port, e))
        return c

    todatetime = lambda x: datetime.datetime.fromtimestamp(
        ssl.cert_time_to_seconds(x), tz=datetime.timezone.utc
    )
    cert_infos = {
        "notAfter": todatetime(cert["notAfter"]),
        "notBefore": todatetime(cert["notBefore"]),
        "issuer": get_source_infos(cert["issuer"]),
        "subject": get_source_infos(cert["subject"]),
    }


    # certificate dates are in utc. Just reading the warning from the documentation,
    # it seems like Python's datetime modules is pretty bad when it comes to managing
    # timezones correctly. So, keep everything in terms of UTC.
    now = datetime.datetime.now(tz=datetime.timezone.utc)

    if now > cert_infos["notAfter"]:
        c.severity = cmt.SEVERITY_CRITICAL
        c.add_message("cert for {} on host {} - certificate expired by {}".format(
                name, hostdisplay, now - cert_infos["notAfter"])
                )
    elif now < cert_infos["notBefore"]:
        c.severity = cmt.SEVERITY_CRITICAL
        c.add_message("cert for {} host {} - certificate not yet valid (will be valid in {})".format(
                name, hostdisplay, cert_infos["notBefore"] - now)
                )

    expires_in = cert_infos["notAfter"] - now
    expires_sec = int(round(expires_in.total_seconds()))
    expires_day = int(expires_sec / 86400)

    #c.add_item(checkitem.CheckItem("certificate_seconds", expires_sec, unit="seconds"))
    c.add_item(CheckItem("certificate_days", expires_day, unit="days"))

    if expires_day < threshold_warning:
        c.severity = cmt.SEVERITY_WARNING

    elif expires_day < threshold_notice:
        c.severity = cmt.SEVERITY_NOTICE

    else:
        c.severity = cmt.SEVERITY_NONE

    #c.add_item(checkitem.CheckItem("certificate_issuer_cn", cert_infos["issuer"]["commonName"]))
    c.add_item(CheckItem("certificate_issuer", cert_infos["issuer"]["organizationName"]))
    c.add_item(CheckItem("certificate_subject", cert_infos["subject"]["commonName"] ))
    c.add_message("{} day(s) left for SSL certificate {} on {} ".format(expires_day, name, hostdisplay))

    return c



