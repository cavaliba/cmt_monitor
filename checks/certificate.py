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
    threshold = parse_duration(c.conf["alert_expires_in"])
    port = c.conf.get("port", 443)

    c.add_item(CheckItem("certificate_hostname", hostname, "Hostname"))
    c.add_item(CheckItem("certificate_port", port, "Port"))

    cert_infos = get_certificate_infos(hostname, port)

    # certificate dates are in utc. Just reading the warning from the documentation,
    # it seems like Python's datetime modules is pretty bad when it comes to managing
    # timezones correctly. So, keep everything in terms of UTC.
    now = datetime.datetime.now(tz=datetime.timezone.utc)
    if now > cert_infos["notAfter"]:
        c.alert += 1
        c.add_message(
            "hostname: {}:{} - certificate expired by {}".format(
                hostname, port, now - cert_infos["notAfter"]
            )
        )
    elif now < cert_infos["notBefore"]:
        c.alert += 1
        c.add_message(
            "hostname: {}:{} - certificate not yet valid (will be valid in {})".format(
                hostname, port, cert_infos["notBefore"] - now
            )
        )

    expires_in = cert_infos["notAfter"] - now
    if expires_in < threshold:
        c.alert += 1
        c.add_message(
            "hostname: {}:{} - certificate will expire soon (in {})".format(
                hostname, port, expires_in
            )
        )

    c.add_item(
        CheckItem(
            "certificate_expires_in",
            int(round(expires_in.total_seconds())),
            unit="seconds",
        )
    )
    c.add_item(
        CheckItem("certificate_issuer_common_name", cert_infos["issuer"]["commonName"])
    )
    c.add_item(
        CheckItem(
            "certificate_issuer_organization_name",
            cert_infos["issuer"]["organizationName"],
        )
    )
    c.add_item(
        CheckItem(
            "certificate_subject_common_name", cert_infos["subject"]["commonName"]
        )
    )
    c.add_item(
        CheckItem(
            "certificate_subject_organization_name",
            cert_infos["subject"]["organizationName"],
        )
    )

    return c


def get_certificate_infos(hostname, port):
    context = ssl.create_default_context()

    with socket.create_connection((hostname, 443)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            cert = ssock.getpeercert()

    if cert is None:
        raise ValueError(f"no certificate found ({cert})")

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
