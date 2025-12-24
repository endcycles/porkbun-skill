---
name: porkbun-dns
description: |
  Manage Porkbun domains and DNS records via API. Use when user asks to:
  - List, check, or manage domains
  - Create/edit/delete DNS records (A, AAAA, CNAME, MX, TXT, NS, SRV)
  - Configure nameservers, glue records, or URL forwarding
  - Retrieve SSL certificates or manage DNSSEC
  - Check domain availability or pricing
  Triggers: "porkbun", "dns record", "domain", "nameserver", "glue record", "A record", "CNAME"
---

# Porkbun DNS Manager

Manage Porkbun domains via direct API calls using curl.

## Authentication

Read credentials from skill directory:
```bash
source ~/.claude/skills/porkbun-dns/.env
```

All API calls use POST with JSON body containing `apikey` and `secretapikey`.

## Base URL

`https://api.porkbun.com/api/json/v3`

## Quick Reference

### Test Connection
```bash
curl -sX POST "https://api.porkbun.com/api/json/v3/ping" \
  -H "Content-Type: application/json" \
  -d "{\"apikey\":\"$PORKBUN_API_KEY\",\"secretapikey\":\"$PORKBUN_SECRET_API_KEY\"}"
```

### List All Domains
```bash
curl -sX POST "https://api.porkbun.com/api/json/v3/domain/listAll" \
  -H "Content-Type: application/json" \
  -d "{\"apikey\":\"$PORKBUN_API_KEY\",\"secretapikey\":\"$PORKBUN_SECRET_API_KEY\"}"
```

### Get DNS Records
```bash
curl -sX POST "https://api.porkbun.com/api/json/v3/dns/retrieve/{domain}" \
  -H "Content-Type: application/json" \
  -d "{\"apikey\":\"$PORKBUN_API_KEY\",\"secretapikey\":\"$PORKBUN_SECRET_API_KEY\"}"
```

### Create DNS Record
```bash
curl -sX POST "https://api.porkbun.com/api/json/v3/dns/create/{domain}" \
  -H "Content-Type: application/json" \
  -d "{
    \"apikey\":\"$PORKBUN_API_KEY\",
    \"secretapikey\":\"$PORKBUN_SECRET_API_KEY\",
    \"name\":\"{subdomain}\",
    \"type\":\"{A|AAAA|CNAME|MX|TXT|NS|SRV}\",
    \"content\":\"{value}\",
    \"ttl\":\"600\"
  }"
```

### Edit DNS Record by ID
```bash
curl -sX POST "https://api.porkbun.com/api/json/v3/dns/edit/{domain}/{id}" \
  -H "Content-Type: application/json" \
  -d "{
    \"apikey\":\"$PORKBUN_API_KEY\",
    \"secretapikey\":\"$PORKBUN_SECRET_API_KEY\",
    \"name\":\"{subdomain}\",
    \"type\":\"{type}\",
    \"content\":\"{value}\",
    \"ttl\":\"600\"
  }"
```

### Delete DNS Record by ID
```bash
curl -sX POST "https://api.porkbun.com/api/json/v3/dns/delete/{domain}/{id}" \
  -H "Content-Type: application/json" \
  -d "{\"apikey\":\"$PORKBUN_API_KEY\",\"secretapikey\":\"$PORKBUN_SECRET_API_KEY\"}"
```

## Detailed Endpoints

See [references/endpoints.md](references/endpoints.md) for complete API reference including:
- Domain management (nameservers, availability, pricing)
- Glue records (for custom nameservers)
- Advanced DNS filtering (by name/type)
- SSL certificate retrieval
- DNSSEC management
- URL forwarding

## Workflow

1. Source credentials: `source ~/.claude/skills/porkbun-dns/.env`
2. Test connection with ping endpoint
3. List domains to confirm access
4. Perform DNS operations as needed
5. Verify changes by retrieving records

## Common Record Types

| Type | Use Case | Content Example |
|------|----------|-----------------|
| A | IPv4 address | `192.168.1.1` |
| AAAA | IPv6 address | `2001:db8::1` |
| CNAME | Alias | `target.example.com` |
| MX | Mail server | `mail.example.com` (set prio) |
| TXT | Verification/SPF | `v=spf1 include:...` |
| NS | Nameserver | `ns1.example.com` |

## Notes

- All endpoints use POST method
- TTL is in seconds (600 = 10 minutes)
- For MX records, include `prio` field
- Subdomain `name` can be empty for root domain (@)
- Response includes `status: "SUCCESS"` or error message
