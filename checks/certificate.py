# by math2001 - dec 2020

import sys
import ssl
import socket
import datetime

from cmt_shared import Check, CheckItem
from helpers import parse_duration


def check_certificate(c):
    # if this assertion fails, then we have to be even more careful of timezones.
    # ref ssl.cert_time_to_seconds
    assert sys.version_info >= (3, 5), "Python interpreter is too old"

    # get every settings at the start so that we don't crash mid-check if a key
    # is missing

    hostname = c.conf["hostname"]

    # should there be a default value?
    DEFAULT_ALERT   = "4 days"
    DEFAULT_WARNING = "2 weeks"
    DEFAULT_NOTICE  = "2 months"

    threshold_alert = parse_duration(c.conf.get("alert_in", DEFAULT_ALERT))
    threshold_warning = parse_duration(c.conf.get("warning_in", DEFAULT_WARNING))
    threshold_notice = parse_duration(c.conf.get("notice_in", DEFAULT_NOTICE))

    port = c.conf.get("port", 443)

    hostdisplay = "{}:{}".format(hostname,port)

    c.add_item(CheckItem("certificate_name", c.name, unit=""))

    c.add_item(CheckItem("certificate_host", hostdisplay, ""))
    #c.add_item(CheckItem("certificate_port", port, ""))

    try:
        cert_infos = get_certificate_infos(hostname, port)
    except ValueError as e:
        c.alert += 1
        c.add_message("no certificate found for {}".format(hostdisplay))
        #c.add_message("no certificate found for {}:{} - err = {}".format(hostname, port, e))
        return c

    # certificate dates are in utc. Just reading the warning from the documentation,
    # it seems like Python's datetime modules is pretty bad when it comes to managing
    # timezones correctly. So, keep everything in terms of UTC.
    now = datetime.datetime.now(tz=datetime.timezone.utc)
    if now > cert_infos["notAfter"]:
        c.alert += 1
        c.add_message(
            "hostname: {} - certificate expired by {}".format(
                hostdisplay, now - cert_infos["notAfter"]
            )
        )
    elif now < cert_infos["notBefore"]:
        c.alert += 1
        c.add_message(
            "hostname: {} - certificate not yet valid (will be valid in {})".format(
                hostdisplay, cert_infos["notBefore"] - now
            )
        )

    expires_in = cert_infos["notAfter"] - now
    expires_sec = int(round(expires_in.total_seconds()))
    expires_day = int(expires_sec / 86400)

    c.add_item(CheckItem("certificate_seconds", expires_sec, unit="seconds"))
    c.add_item(CheckItem("certificate_days", expires_day, unit="days"))

    if expires_in < threshold_alert:
        c.alert += 1
    elif expires_in < threshold_warning:
        c.warn += 1
    elif expires_in < threshold_notice:
        c.notice += 1        


    # c.add_item(
    #     CheckItem("certificate_issuer_common_name", cert_infos["issuer"]["commonName"])
    # )
    # c.add_item(
    #     CheckItem(
    #         "certificate_issuer_organization_name",
    #         cert_infos["issuer"]["organizationName"],
    #     )
    # )
    c.add_item(
        CheckItem(
            "certificate_subject", cert_infos["subject"]["commonName"]
        )
    )

    # c.add_item(
    #     CheckItem(
    #         "certificate_subject_organization_name",
    #         cert_infos["subject"]["organizationName"],
    #     )
    # )

    c.add_message("{} day(s) left for SSL certificate {}".format(expires_day, hostdisplay))

    return c


def get_certificate_infos(hostname, port):
    context = ssl.create_default_context()

    try:
        with socket.create_connection((hostname, port)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
    except ConnectionRefusedError as e:
        raise ValueError("no connection ({})".format(e))
    except ssl.SSLError as e:
        raise ValueError("no ssl connection ({})".format(e))

    if cert is None:
        raise ValueError("no certificate found")

    todatetime = lambda x: datetime.datetime.fromtimestamp(
        ssl.cert_time_to_seconds(x), tz=datetime.timezone.utc
    )
    return {
        "notAfter": todatetime(cert["notAfter"]),
        "notBefore": todatetime(cert["notBefore"]),
        "issuer": get_source_infos(cert["issuer"]),
        "subject": get_source_infos(cert["subject"]),
    }


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
