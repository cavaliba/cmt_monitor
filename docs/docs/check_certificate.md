Opens a socket to `hostname:port` and retrieve certificate information (with
`.getpeercert()`).

### Add a check

    certificate_db:
      module: certificate
      hostname: hostname.com
      port: 2718                 # defaults to 443 if not specified
      alert_expires_in: 1 week


- `hostname`: the hostname
- `port`: the port to connect the socket to
- `alert_expires_in`: [`<duration>`](/docs/duration.md), sends an alert if
  expiry date (`notAfter` field) is less that `<duration>` away.

## Alerts

Sends an alert if a certificate is invalid, that is, one of these condition
matches:

1. `expiry date - now < alert_expires_in`
2. `now < notBefore` (notBefore is the timestamp at which the certificate will
   become valid)
3. No certificate is found
4. The connection to `hostname:port` can't be established.


## Output to ElasticSearch

    cmt_certificate_hostname                 string
    cmt_certificate_port                     int
    certificate_expires_in                   int (seconds)

    certificate_issuer_common_name           string
    certificate_issuer_organization_name     string

    certificate_subject_common_name          string
    certificate_subject_organization_name    string
