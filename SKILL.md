---
name: porkbun-skill
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

Manage Porkbun domains via the `porkbun.py` script.

## Script Location

```
~/.claude/skills/porkbun-skill/scripts/porkbun.py
```

Credentials are loaded automatically from `~/.claude/skills/porkbun-skill/.env`

## Quick Reference

### Test Connection
```bash
python3 ~/.claude/skills/porkbun-skill/scripts/porkbun.py ping
```

### List All Domains
```bash
python3 ~/.claude/skills/porkbun-skill/scripts/porkbun.py domains
```

### Check Domain Availability
```bash
python3 ~/.claude/skills/porkbun-skill/scripts/porkbun.py check example.com
```

### List DNS Records
```bash
python3 ~/.claude/skills/porkbun-skill/scripts/porkbun.py dns list example.com
```

### Create DNS Record
```bash
python3 ~/.claude/skills/porkbun-skill/scripts/porkbun.py dns create <domain> <type> <content> [name] [ttl] [prio]

# Examples:
python3 ~/.claude/skills/porkbun-skill/scripts/porkbun.py dns create example.com A 192.168.1.1 www 600
python3 ~/.claude/skills/porkbun-skill/scripts/porkbun.py dns create example.com CNAME target.com blog 600
python3 ~/.claude/skills/porkbun-skill/scripts/porkbun.py dns create example.com MX mail.example.com "" 600 10
python3 ~/.claude/skills/porkbun-skill/scripts/porkbun.py dns create example.com TXT "v=spf1 include:_spf.google.com ~all" "" 600
```

### Edit DNS Record
```bash
python3 ~/.claude/skills/porkbun-skill/scripts/porkbun.py dns edit <domain> <id> <type> <content> [name] [ttl] [prio]
```

### Get DNS Record by ID
```bash
python3 ~/.claude/skills/porkbun-skill/scripts/porkbun.py dns get example.com 123456789
```

### Get/Edit/Delete DNS Records by Type
```bash
python3 ~/.claude/skills/porkbun-skill/scripts/porkbun.py dns get-type example.com A www
python3 ~/.claude/skills/porkbun-skill/scripts/porkbun.py dns edit-type example.com A 1.2.3.4 www 600
python3 ~/.claude/skills/porkbun-skill/scripts/porkbun.py dns delete-type example.com A www
```

### Delete DNS Record by ID
```bash
python3 ~/.claude/skills/porkbun-skill/scripts/porkbun.py dns delete example.com 123456789
```

### Nameservers
```bash
python3 ~/.claude/skills/porkbun-skill/scripts/porkbun.py ns get example.com
python3 ~/.claude/skills/porkbun-skill/scripts/porkbun.py ns update example.com ns1.cloudflare.com ns2.cloudflare.com
```

### URL Forwarding
```bash
python3 ~/.claude/skills/porkbun-skill/scripts/porkbun.py forwards list example.com
python3 ~/.claude/skills/porkbun-skill/scripts/porkbun.py forward add example.com https://newsite.com "" permanent
python3 ~/.claude/skills/porkbun-skill/scripts/porkbun.py forward delete example.com 123456
```

### SSL Certificate
```bash
python3 ~/.claude/skills/porkbun-skill/scripts/porkbun.py ssl example.com
```

### Glue Records
```bash
python3 ~/.claude/skills/porkbun-skill/scripts/porkbun.py glue list example.com
python3 ~/.claude/skills/porkbun-skill/scripts/porkbun.py glue create example.com ns1 192.168.1.1 192.168.1.2
python3 ~/.claude/skills/porkbun-skill/scripts/porkbun.py glue update example.com ns1 10.0.0.1
python3 ~/.claude/skills/porkbun-skill/scripts/porkbun.py glue delete example.com ns1
```

### DNSSEC
```bash
python3 ~/.claude/skills/porkbun-skill/scripts/porkbun.py dnssec list example.com
python3 ~/.claude/skills/porkbun-skill/scripts/porkbun.py dnssec create example.com 12345 8 2 abc123...
python3 ~/.claude/skills/porkbun-skill/scripts/porkbun.py dnssec delete example.com 12345
```

### Help
```bash
python3 ~/.claude/skills/porkbun-skill/scripts/porkbun.py help
```

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

- Script loads .env automatically - no need to source
- TTL is in seconds (600 = 10 minutes)
- For MX records, set name to "" and add prio as last argument
- Response is JSON with `status: "SUCCESS"` or `status: "ERROR"`
