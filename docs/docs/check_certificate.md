---
title: check_certificate
---

# Certificate

**Certificate** checks the validity left of various SSL/TLS certificates.
It opens a socket to `hostname:port` and retrieve certificate information (with
[`ssl.SSLSocket.getpeercert()`](https://docs.python.org/3/library/ssl.html#ssl.SSLSocket.getpeercert)).


## Enable the module

Enable de module in the configuration :

    # conf.yml

    modules:
      certificate:
         enable: yes

## Add a check in the configuration

    certificate:

      mysite
        hostname: mysite.com
        port: 2718             # defaults to 443 if not specified
        alert_in:   1 week     # DEFAULT 3 days ;  X years Y months Z weeks D days H hours
        warning_in: 1 month    # DEFAULT 2 weeks
        notice_in:  3 months   # DEFAULT 2 months


hostname (string) and port (integer):

    the hostname:port pair to connect the socket to

`alert_in` ([`duration`](duration.md)) raise an alert if expiry date (`notAfter` field) is less that <duration> away.

Use `warning_in` and `notice_in` for lower grade alerts.


## Alerts

Sends an alert if a certificate is invalid, that is, one of these conditions
matches:

1. `expiry date - now < alert_in`
2. `now < notBefore` (notBefore is the timestamp at which the certificate
   becomes valid)
3. No certificate is found
4. The connection to `hostname:port` can't be established.


## Output to Metrology Servers

    cmt_certificate_name                     string         # entry name in conf.yml
    cmt_certificate_host                     string         # host:port
    cmt_certificate_seconds                  int (seconds)  # seconds left before certificate expirry
    cmt_certificate_days                     int (days)     # days left
    cmt_certificate_subject                  string         # domain/subject name
