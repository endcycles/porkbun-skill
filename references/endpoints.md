# Porkbun API Endpoints Reference

Base URL: `https://api.porkbun.com/api/json/v3`

All endpoints use POST with JSON body. Include auth in every request:
```json
{
  "apikey": "$PORKBUN_API_KEY",
  "secretapikey": "$PORKBUN_SECRET_API_KEY"
}
```

## Table of Contents

1. [Authentication & General](#authentication--general)
2. [Domain Management](#domain-management)
3. [Glue Records](#glue-records)
4. [DNS Records](#dns-records)
5. [Advanced DNS Filtering](#advanced-dns-filtering)
6. [SSL Certificates](#ssl-certificates)
7. [DNSSEC](#dnssec)
8. [URL Forwarding](#url-forwarding)

---

## Authentication & General

### Ping (Test Connection)
```
POST /ping
```
Returns your IP address if authentication successful.

### Get TLD Pricing
```
POST /pricing/get
```
No authentication required. Returns pricing for all TLDs.

---

## Domain Management

### List All Domains
```
POST /domain/listAll
```
Optional body params:
- `start` (int): Pagination offset
- `includeLabels` ("yes"): Include domain labels

### Check Domain Availability
```
POST /domain/checkDomain/{domain}
```
Check if a domain is available for registration.

### Get Nameservers
```
POST /domain/getNs/{domain}
```
Returns current nameservers for domain.

### Update Nameservers
```
POST /domain/updateNs/{domain}
```
Body params:
- `ns` (array): List of nameserver hostnames

Example:
```json
{
  "apikey": "...",
  "secretapikey": "...",
  "ns": ["ns1.example.com", "ns2.example.com"]
}
```

---

## Glue Records

Glue records are required when using your own domain as nameservers (e.g., ns1.example.com for example.com).

### Get Glue Records
```
POST /domain/getGlue/{domain}
```
Returns all glue records for domain.

### Create Glue Record
```
POST /domain/createGlue/{domain}/{subdomain}
```
Body params:
- `ip` (array): List of IPv4 addresses for the nameserver

### Update Glue Record
```
POST /domain/updateGlue/{domain}/{subdomain}
```
Body params:
- `ip` (array): New list of IPv4 addresses (replaces existing)

### Delete Glue Record
```
POST /domain/deleteGlue/{domain}/{subdomain}
```
No additional body params required.

---

## DNS Records

### Retrieve All Records
```
POST /dns/retrieve/{domain}
```
Returns all DNS records for domain.

### Retrieve Specific Record
```
POST /dns/retrieve/{domain}/{id}
```
Returns single record by ID.

### Create Record
```
POST /dns/create/{domain}
```
Body params:
- `name` (string): Subdomain (empty for root @)
- `type` (string): A, AAAA, CNAME, MX, TXT, NS, SRV, ALIAS, CAA, HTTPS, SVCB, TLSA
- `content` (string): Record value
- `ttl` (string): Time to live in seconds (default 600)
- `prio` (string): Priority (required for MX, SRV)

### Edit Record by ID
```
POST /dns/edit/{domain}/{id}
```
Body params: Same as create.

### Delete Record by ID
```
POST /dns/delete/{domain}/{id}
```
No additional params.

---

## Advanced DNS Filtering

### Retrieve by Name/Type
```
POST /dns/retrieveByNameType/{domain}/{type}/{subdomain?}
```
- `{type}`: Record type (A, CNAME, etc.)
- `{subdomain}`: Optional, omit for root

### Edit by Name/Type
```
POST /dns/editByNameType/{domain}/{type}/{subdomain?}
```
Body params:
- `content` (string): New value
- `ttl` (string): Time to live
- `prio` (string): Priority (if applicable)

### Delete by Name/Type
```
POST /dns/deleteByNameType/{domain}/{type}/{subdomain?}
```
Deletes all matching records.

---

## SSL Certificates

### Retrieve SSL Bundle
```
POST /ssl/retrieve/{domain}
```
Returns SSL certificate bundle including:
- Certificate chain
- Private key
- Public key

---

## DNSSEC

### Get DNSSEC Records
```
POST /dns/getDnssecRecords/{domain}
```

### Create DNSSEC Record
```
POST /dns/createDnssecRecord/{domain}
```
Body params:
- `keyTag` (int): Key tag
- `alg` (int): Algorithm number
- `digestType` (int): Digest type
- `digest` (string): Digest value

### Delete DNSSEC Record
```
POST /dns/deleteDnssecRecord/{domain}/{tag}
```
- `{tag}`: Key tag to delete

---

## URL Forwarding

### Get URL Forwarding
```
POST /domain/getUrlForwarding/{domain}
```
Returns all URL forwards for domain.

### Add URL Forward
```
POST /domain/addUrlForward/{domain}
```
Body params:
- `subdomain` (string): Subdomain to forward (empty for root)
- `location` (string): Target URL
- `type` (string): "temporary" (302) or "permanent" (301)
- `includePath` (string): "yes" or "no"
- `wildcard` (string): "yes" or "no"

### Delete URL Forward
```
POST /domain/deleteUrlForward/{domain}/{id}
```
- `{id}`: Forward rule ID

---

## Response Format

All endpoints return JSON:

**Success:**
```json
{
  "status": "SUCCESS",
  "yourIp": "1.2.3.4",
  ...
}
```

**Error:**
```json
{
  "status": "ERROR",
  "message": "Error description"
}
```

## Common Errors

| Error | Cause |
|-------|-------|
| Invalid API key | Wrong or missing credentials |
| Domain not found | Domain not in your account |
| API access disabled | Enable API for domain in Porkbun dashboard |
| Rate limit exceeded | Too many requests, wait and retry |
