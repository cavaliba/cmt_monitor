---
title: check_certificate
---

# Certificate

**Certificate** opens a socket to `hostname:port` and retrieve certificate information (with
[`ssl.SSLSocket.getpeercert()`](https://docs.python.org/3/library/ssl.html#ssl.SSLSocket.getpeercert)).


## Enable the module

Enable de module in the configuration :

    # conf.yml

  Module:
      certificate:
         enable: yes

### Add a check

    a_certificate:
      module: certificate
      hostname: hostname.com
      port: 2718                    # defaults to 443 if not specified
      alert_in:   1 week            # DEFAULT 3 days ; format  X years Y months ... weeks, days, hours"
      warning_in: 1 month           # DEFAULT 2 weeks
      notice_in:  3 months          # DEFAULT 2 months

hostname (string) and port (integer):

    the hostname:port pair to connect the socket to

alert_expires_in ([`duration`](duration.md)):

    sends an alert if expiry date (`notAfter` field) is less that <duration> away.

## Alerts

Sends an alert if a certificate is invalid, that is, one of these conditions
matches:

1. `expiry date - now < alert_expires_in`
2. `now < notBefore` (notBefore is the timestamp at which the certificate
   becomes valid)
3. No certificate is found
4. The connection to `hostname:port` can't be established.


## Output to Metrology Servers

    cmt_certificate_name                     string         # entry name in conf.yml
    cmt_certificate_host                     string         # host:port
    cmt_certificate_seconds                  int (seconds)
    cmt_certificate_days                     int (days)
    cmt_certificate_subject                  string         # domain/subject name
