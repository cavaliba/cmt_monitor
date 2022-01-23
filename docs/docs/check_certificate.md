---
title: check_certificate
---

# Certificate

*updated v2.3, 2022/01*

**Certificate** checks the validity for various SSL/TLS certificates. It opens a socket to `hostname:port` and retrieve certificate information  for `name` certificate if provided.

It computes days left before certificate expiry and set a `severity` value accordingly.

It sends certificate informations to metrology server (days left, issuer, subject, severity).

It has a timeout of 3 seconds in case of no response from remote host.


## Configure

    certificate:

        cert_mysite:
            hostname: mysite.com   # remote/network target
            port: 2718             # remote port, defaults to 443 if not specified
            name: mysite.com       # cert name to be looked for ; default to hostname if none
            warning_in: 7          # DEFAULT 7 days
            notice_in:  30         # DEFAULT 30 days
            severity_max: error    # if expired, max severity to raise


        cert_short:
            hostname: www.google.com   # shortest config to check cert at https://www.google.com/



## Alerts

If delay is very short, set a SEVERITY = WARNING ; default 7 days

If delay is a little longuer but short anymay, set a SEVERITY = NOTICE, default 30 days.

If certificate is not valid, set a SEVERITY = CRITICAL (to be filtered with severity_max configuration).


## Output to CLI / metrology

        $ cmt -s certificate

        OK       certificate  56 day(s) left for SSL certificate google.com on google.com:443 
        OK       certificate  56 day(s) left for SSL certificate google.com on 142.250.201.174:443 
        OK       certificate  307 day(s) left for SSL certificate duckduckgo.com on duckduckgo.com:443 
        CRITICAL certificate  no certificate found for duckduckgo.com:80
        OK       certificate  143 day(s) left for SSL certificate yahoo.com on yahoo.com:443 


        $ cmt certificate

        ------------------------------------------------------------------
        certificate duck
        ------------------------------------------------------------------
        cmt_certificate_host     duckduckgo.com:443
        cmt_certificate_name     duckduckgo.com
        cmt_certificate_days     307 days 
        cmt_certificate_issuer   DigiCert Inc
        cmt_certificate_subject  *.duckduckgo.com
        OK  : 307 day(s) left for SSL certificate duckduckgo.com on duckduckgo.com:443 

        ------------------------------------------------------------------
        certificate broken
        ------------------------------------------------------------------
        cmt_certificate_host     duckduckgo.com:80
        cmt_certificate_name     duckduckgo.com
        CRITICAL  : no certificate found for duckduckgo.com:80

        ------------------------------------------------------------------
        certificate cert_ipgoogle
        ------------------------------------------------------------------
        cmt_certificate_host     142.250.201.174:443
        cmt_certificate_name     google.com
        cmt_certificate_days     56 days 
        cmt_certificate_issuer   Google Trust Services LLC
        cmt_certificate_subject  *.google.com
        OK  : 56 day(s) left for SSL certificate google.com on 142.250.201.174:443 

