## Enable the module

### Add a check

    certificate_db:
      module: certificate
      hostname: google.com
      port: 2718                 # defaults to 443 if not specified
      alert_expires_in: 1 week
