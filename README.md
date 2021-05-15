# Dynamic PowerDNS Updater

Dynamically updates/inserts DNS records on PowerDNS server for Docker containers.


Set `svc.dns.name` label for your running container and the *pdns-updater* service would update DNS record periodically.

For each server, the only one pdns-updater service would be enough.

Basic usage requires only `svc.dns.name` label to be set. (e.g. `myhost.yourdomain.com`)

PowerDNS requires zone creation for domain records, pdns-updater handles zone creation on the fly. It tries to guess the domain name from given `svc.dns.name` by taking the last two parts of dot separated domain name (for `myhost.yourdomain.com`, `yourdomain.com`). If you want to define something complex (e.g. wildcard domain) you can define `svc.dns.domain` label additionally.

Different usage examples can found at `docker-compose.yml`.

## Docker Image

Docker images for several platforms (armv7, arm64, amd64) are available at Docker Hub([dcagatay/pdns-updater](https://hub.docker.com/r/dcagatay/pdns-updater)).

## Environment Variables

- `HOST_IP`: IP address of the host that the docker daemon is running. Services will be declared to DNS server with IP address. *No defaults, required to be set*
- `PDNS_API_URL`: PowerDNS server REST API URL. You need to enable webserver feature on PowerDNS server. Default: *http://pdns:8081/api/v1*
- `PDNS_API_KEY`: PowerDNS REST API KEY. Default: *changeme*
- `UPDATE_PERIOD_SECONDS`: DNS record update period. Docker will be checked and DNS records will be updated every period seconds. Default: *30*

## docker-compose Example

A basic docker-compose.yml example can be constructed as follows.

```yml
version: "3"
services:

  pdns-updater:
    image: dcagatay/pdns-updater:latest
    environment:
      HOST_IP: "10.35.23.90"
      PDNS_API_URL: "http://pdns:8081/api/v1"
      PDNS_API_KEY: "changeme"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    restart: unless-stopped

  whoami:
    image: containous/whoami
    ports:
      - 8182:80
    labels:
      - "svc.dns.name=whoami.yourdomain.com"
```

