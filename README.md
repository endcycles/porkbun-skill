# Porkbun Skill

A Claude Code skill for managing Porkbun domains and DNS records.

Inspired by [porkbun-mcp](https://github.com/myroslavtryhubets/porkbun-mcp) - rebuilt as a lightweight skill.

## How It Works

```
You: "Add an A record for www.example.com pointing to 1.2.3.4"
  ↓
Claude Code: Reads your API keys from .env
  ↓
Claude Code: Executes curl request to Porkbun API
  ↓
Porkbun API: Returns success/failure
  ↓
Claude Code: Reports result to you
```

No Docker. No MCP server. No middleware. Just direct API calls via Python script.

## Why a Skill Instead of MCP?

| Approach | Token Overhead | Setup |
|----------|----------------|-------|
| **This skill** | ~500 tokens | Just .env file |
| **MCP Server** | 10,000-17,000+ tokens | Docker, process management |

MCP servers add significant token overhead:
- Each server consumes **10K-17K tokens** for tool definitions
- A 5-server setup burns **55K+ tokens** before you start
- That's up to 1/3 of Claude's context window gone immediately

Direct API calls via curl are leaner:
- SKILL.md loads only when triggered
- No persistent process running
- No tool definitions eating context
- Curl runs, returns result, done

**Use MCP for:** Complex stateful integrations (browser automation, databases)

**Use Skills for:** Simple REST APIs like Porkbun

Sources: [Anthropic Engineering](https://www.anthropic.com/engineering/claude-code-best-practices), [MCP Context Optimization](https://scottspence.com/posts/optimising-mcp-server-context-usage-in-claude-code)

## Requirements

- [Claude Code](https://claude.ai/download) CLI
- Porkbun account with API access enabled
- API keys from [porkbun.com/account/api](https://porkbun.com/account/api)

## Installation

```bash
cd ~/.claude/skills
git clone https://github.com/endcycles/porkbun-skill.git
cd porkbun-skill
cp .env.example .env
```

Edit `.env` with your Porkbun API credentials:
```bash
export PORKBUN_API_KEY=pk1_your_api_key_here
export PORKBUN_SECRET_API_KEY=sk1_your_secret_key_here
```

## CLI Script

The skill includes a Python CLI (`scripts/porkbun.py`) that handles authentication automatically:

```bash
# Test connection
python3 ~/.claude/skills/porkbun-skill/scripts/porkbun.py ping

# List domains
python3 ~/.claude/skills/porkbun-skill/scripts/porkbun.py domains

# DNS operations
python3 ~/.claude/skills/porkbun-skill/scripts/porkbun.py dns list example.com
python3 ~/.claude/skills/porkbun-skill/scripts/porkbun.py dns create example.com A 1.2.3.4 www 600
python3 ~/.claude/skills/porkbun-skill/scripts/porkbun.py dns get-type example.com A www
python3 ~/.claude/skills/porkbun-skill/scripts/porkbun.py dns edit-type example.com A 5.6.7.8 www
python3 ~/.claude/skills/porkbun-skill/scripts/porkbun.py dns delete example.com 123456789

# Glue records (multiple IPs supported)
python3 ~/.claude/skills/porkbun-skill/scripts/porkbun.py glue list example.com
python3 ~/.claude/skills/porkbun-skill/scripts/porkbun.py glue create example.com ns1 192.168.1.1 192.168.1.2

# Full help
python3 ~/.claude/skills/porkbun-skill/scripts/porkbun.py help
```

No dependencies required - uses Python standard library only.

## Usage Examples

Once installed, ask Claude Code to manage your Porkbun domains naturally:

### Domain Management
```
"List all my Porkbun domains"
"Check if coolstartup.io is available"
"What nameservers is example.com using?"
"Update example.com to use Cloudflare nameservers"
```

### DNS Records
```
"Show all DNS records for example.com"
"Add an A record for www.example.com pointing to 192.168.1.1"
"Create a CNAME record pointing blog.example.com to my-blog.netlify.app"
"Set up MX records for example.com to use Google Workspace"
"Add a TXT record for domain verification: google-site-verification=abc123"
"Delete the A record for old.example.com"
"Change the IP for api.example.com to 10.0.0.5"
```

### Batch Operations
```
"Set up DNS for my new site: A record for @ pointing to 1.2.3.4, CNAME for www pointing to @, and MX records for Google"
"Add A records for app, api, and cdn subdomains all pointing to 192.168.1.100"
"Delete all TXT records for example.com"
"Show me all CNAME records across all my domains"
```

### Email Setup
```
"Configure example.com for Google Workspace email"
"Add SPF and DKIM records for example.com"
"Set up MX records with priority 10 for mail.example.com"
```

### SSL & Security
```
"Get the SSL certificate for example.com"
"Show DNSSEC status for example.com"
"Enable DNSSEC for example.com"
```

### URL Forwarding
```
"Redirect old-domain.com to new-domain.com permanently"
"Set up a 302 redirect from promo.example.com to example.com/summer-sale"
"Forward all subdomains of redirect.example.com to example.com"
"List all URL forwards for example.com"
```

### Glue Records (Custom Nameservers)
```
"Set up glue records for ns1.example.com and ns2.example.com"
"Update the IP for ns1.example.com to 10.0.0.1"
"Show glue records for example.com"
```

### Investigation & Audit
```
"What's the TTL on all my A records for example.com?"
"Find all records pointing to 192.168.1.1 across my domains"
"List all domains expiring in the next 30 days"
"Compare DNS records between example.com and example.net"
```

## API Endpoints & Example Commands

All commands use the Porkbun API v3. Base URL: `https://api.porkbun.com/api/json/v3`

### Authentication

```bash
source ~/.claude/skills/porkbun-skill/.env
```

---

### General

#### Test Connection
```bash
curl -sX POST "https://api.porkbun.com/api/json/v3/ping" \
  -H "Content-Type: application/json" \
  -d "{\"apikey\":\"$PORKBUN_API_KEY\",\"secretapikey\":\"$PORKBUN_SECRET_API_KEY\"}"
```

#### Get TLD Pricing (no auth required)
```bash
curl -sX POST "https://api.porkbun.com/api/json/v3/pricing/get" \
  -H "Content-Type: application/json" -d "{}"
```

---

### Domain Management

#### List All Domains
```bash
curl -sX POST "https://api.porkbun.com/api/json/v3/domain/listAll" \
  -H "Content-Type: application/json" \
  -d "{\"apikey\":\"$PORKBUN_API_KEY\",\"secretapikey\":\"$PORKBUN_SECRET_API_KEY\"}"
```

#### Check Domain Availability
```bash
curl -sX POST "https://api.porkbun.com/api/json/v3/domain/checkDomain/example.com" \
  -H "Content-Type: application/json" \
  -d "{\"apikey\":\"$PORKBUN_API_KEY\",\"secretapikey\":\"$PORKBUN_SECRET_API_KEY\"}"
```

#### Get Nameservers
```bash
curl -sX POST "https://api.porkbun.com/api/json/v3/domain/getNs/example.com" \
  -H "Content-Type: application/json" \
  -d "{\"apikey\":\"$PORKBUN_API_KEY\",\"secretapikey\":\"$PORKBUN_SECRET_API_KEY\"}"
```

#### Update Nameservers
```bash
curl -sX POST "https://api.porkbun.com/api/json/v3/domain/updateNs/example.com" \
  -H "Content-Type: application/json" \
  -d "{
    \"apikey\":\"$PORKBUN_API_KEY\",
    \"secretapikey\":\"$PORKBUN_SECRET_API_KEY\",
    \"ns\":[\"ns1.example.com\",\"ns2.example.com\"]
  }"
```

---

### Glue Records

Glue records are required when using your own domain's nameservers (e.g., ns1.example.com for example.com).

#### Get Glue Records
```bash
curl -sX POST "https://api.porkbun.com/api/json/v3/domain/getGlue/example.com" \
  -H "Content-Type: application/json" \
  -d "{\"apikey\":\"$PORKBUN_API_KEY\",\"secretapikey\":\"$PORKBUN_SECRET_API_KEY\"}"
```

#### Create Glue Record
```bash
curl -sX POST "https://api.porkbun.com/api/json/v3/domain/createGlue/example.com/ns1" \
  -H "Content-Type: application/json" \
  -d "{
    \"apikey\":\"$PORKBUN_API_KEY\",
    \"secretapikey\":\"$PORKBUN_SECRET_API_KEY\",
    \"ip\":[\"192.168.1.1\",\"192.168.1.2\"]
  }"
```

#### Update Glue Record
```bash
curl -sX POST "https://api.porkbun.com/api/json/v3/domain/updateGlue/example.com/ns1" \
  -H "Content-Type: application/json" \
  -d "{
    \"apikey\":\"$PORKBUN_API_KEY\",
    \"secretapikey\":\"$PORKBUN_SECRET_API_KEY\",
    \"ip\":[\"10.0.0.1\"]
  }"
```

#### Delete Glue Record
```bash
curl -sX POST "https://api.porkbun.com/api/json/v3/domain/deleteGlue/example.com/ns1" \
  -H "Content-Type: application/json" \
  -d "{\"apikey\":\"$PORKBUN_API_KEY\",\"secretapikey\":\"$PORKBUN_SECRET_API_KEY\"}"
```

---

### DNS Records

#### Retrieve All DNS Records
```bash
curl -sX POST "https://api.porkbun.com/api/json/v3/dns/retrieve/example.com" \
  -H "Content-Type: application/json" \
  -d "{\"apikey\":\"$PORKBUN_API_KEY\",\"secretapikey\":\"$PORKBUN_SECRET_API_KEY\"}"
```

#### Retrieve Record by ID
```bash
curl -sX POST "https://api.porkbun.com/api/json/v3/dns/retrieve/example.com/123456789" \
  -H "Content-Type: application/json" \
  -d "{\"apikey\":\"$PORKBUN_API_KEY\",\"secretapikey\":\"$PORKBUN_SECRET_API_KEY\"}"
```

#### Create A Record
```bash
curl -sX POST "https://api.porkbun.com/api/json/v3/dns/create/example.com" \
  -H "Content-Type: application/json" \
  -d "{
    \"apikey\":\"$PORKBUN_API_KEY\",
    \"secretapikey\":\"$PORKBUN_SECRET_API_KEY\",
    \"name\":\"www\",
    \"type\":\"A\",
    \"content\":\"192.168.1.1\",
    \"ttl\":\"600\"
  }"
```

#### Create AAAA Record (IPv6)
```bash
curl -sX POST "https://api.porkbun.com/api/json/v3/dns/create/example.com" \
  -H "Content-Type: application/json" \
  -d "{
    \"apikey\":\"$PORKBUN_API_KEY\",
    \"secretapikey\":\"$PORKBUN_SECRET_API_KEY\",
    \"name\":\"www\",
    \"type\":\"AAAA\",
    \"content\":\"2001:db8::1\",
    \"ttl\":\"600\"
  }"
```

#### Create CNAME Record
```bash
curl -sX POST "https://api.porkbun.com/api/json/v3/dns/create/example.com" \
  -H "Content-Type: application/json" \
  -d "{
    \"apikey\":\"$PORKBUN_API_KEY\",
    \"secretapikey\":\"$PORKBUN_SECRET_API_KEY\",
    \"name\":\"blog\",
    \"type\":\"CNAME\",
    \"content\":\"example.github.io\",
    \"ttl\":\"600\"
  }"
```

#### Create MX Record
```bash
curl -sX POST "https://api.porkbun.com/api/json/v3/dns/create/example.com" \
  -H "Content-Type: application/json" \
  -d "{
    \"apikey\":\"$PORKBUN_API_KEY\",
    \"secretapikey\":\"$PORKBUN_SECRET_API_KEY\",
    \"name\":\"\",
    \"type\":\"MX\",
    \"content\":\"mail.example.com\",
    \"ttl\":\"600\",
    \"prio\":\"10\"
  }"
```

#### Create TXT Record
```bash
curl -sX POST "https://api.porkbun.com/api/json/v3/dns/create/example.com" \
  -H "Content-Type: application/json" \
  -d "{
    \"apikey\":\"$PORKBUN_API_KEY\",
    \"secretapikey\":\"$PORKBUN_SECRET_API_KEY\",
    \"name\":\"\",
    \"type\":\"TXT\",
    \"content\":\"v=spf1 include:_spf.google.com ~all\",
    \"ttl\":\"600\"
  }"
```

#### Create NS Record
```bash
curl -sX POST "https://api.porkbun.com/api/json/v3/dns/create/example.com" \
  -H "Content-Type: application/json" \
  -d "{
    \"apikey\":\"$PORKBUN_API_KEY\",
    \"secretapikey\":\"$PORKBUN_SECRET_API_KEY\",
    \"name\":\"sub\",
    \"type\":\"NS\",
    \"content\":\"ns1.otherdns.com\",
    \"ttl\":\"600\"
  }"
```

#### Create SRV Record
```bash
curl -sX POST "https://api.porkbun.com/api/json/v3/dns/create/example.com" \
  -H "Content-Type: application/json" \
  -d "{
    \"apikey\":\"$PORKBUN_API_KEY\",
    \"secretapikey\":\"$PORKBUN_SECRET_API_KEY\",
    \"name\":\"_sip._tcp\",
    \"type\":\"SRV\",
    \"content\":\"sipserver.example.com\",
    \"ttl\":\"600\",
    \"prio\":\"10\"
  }"
```

#### Edit Record by ID
```bash
curl -sX POST "https://api.porkbun.com/api/json/v3/dns/edit/example.com/123456789" \
  -H "Content-Type: application/json" \
  -d "{
    \"apikey\":\"$PORKBUN_API_KEY\",
    \"secretapikey\":\"$PORKBUN_SECRET_API_KEY\",
    \"name\":\"www\",
    \"type\":\"A\",
    \"content\":\"192.168.1.2\",
    \"ttl\":\"600\"
  }"
```

#### Delete Record by ID
```bash
curl -sX POST "https://api.porkbun.com/api/json/v3/dns/delete/example.com/123456789" \
  -H "Content-Type: application/json" \
  -d "{\"apikey\":\"$PORKBUN_API_KEY\",\"secretapikey\":\"$PORKBUN_SECRET_API_KEY\"}"
```

---

### Advanced DNS Filtering

#### Retrieve by Name and Type
```bash
# Get all A records for "www" subdomain
curl -sX POST "https://api.porkbun.com/api/json/v3/dns/retrieveByNameType/example.com/A/www" \
  -H "Content-Type: application/json" \
  -d "{\"apikey\":\"$PORKBUN_API_KEY\",\"secretapikey\":\"$PORKBUN_SECRET_API_KEY\"}"

# Get all MX records for root domain (omit subdomain)
curl -sX POST "https://api.porkbun.com/api/json/v3/dns/retrieveByNameType/example.com/MX" \
  -H "Content-Type: application/json" \
  -d "{\"apikey\":\"$PORKBUN_API_KEY\",\"secretapikey\":\"$PORKBUN_SECRET_API_KEY\"}"
```

#### Edit by Name and Type
```bash
curl -sX POST "https://api.porkbun.com/api/json/v3/dns/editByNameType/example.com/A/www" \
  -H "Content-Type: application/json" \
  -d "{
    \"apikey\":\"$PORKBUN_API_KEY\",
    \"secretapikey\":\"$PORKBUN_SECRET_API_KEY\",
    \"content\":\"192.168.1.100\",
    \"ttl\":\"300\"
  }"
```

#### Delete by Name and Type
```bash
curl -sX POST "https://api.porkbun.com/api/json/v3/dns/deleteByNameType/example.com/A/www" \
  -H "Content-Type: application/json" \
  -d "{\"apikey\":\"$PORKBUN_API_KEY\",\"secretapikey\":\"$PORKBUN_SECRET_API_KEY\"}"
```

---

### SSL Certificates

#### Retrieve SSL Bundle
```bash
curl -sX POST "https://api.porkbun.com/api/json/v3/ssl/retrieve/example.com" \
  -H "Content-Type: application/json" \
  -d "{\"apikey\":\"$PORKBUN_API_KEY\",\"secretapikey\":\"$PORKBUN_SECRET_API_KEY\"}"
```

---

### DNSSEC

#### Get DNSSEC Records
```bash
curl -sX POST "https://api.porkbun.com/api/json/v3/dns/getDnssecRecords/example.com" \
  -H "Content-Type: application/json" \
  -d "{\"apikey\":\"$PORKBUN_API_KEY\",\"secretapikey\":\"$PORKBUN_SECRET_API_KEY\"}"
```

#### Create DNSSEC Record
```bash
curl -sX POST "https://api.porkbun.com/api/json/v3/dns/createDnssecRecord/example.com" \
  -H "Content-Type: application/json" \
  -d "{
    \"apikey\":\"$PORKBUN_API_KEY\",
    \"secretapikey\":\"$PORKBUN_SECRET_API_KEY\",
    \"keyTag\":12345,
    \"alg\":13,
    \"digestType\":2,
    \"digest\":\"your_digest_here\"
  }"
```

#### Delete DNSSEC Record
```bash
curl -sX POST "https://api.porkbun.com/api/json/v3/dns/deleteDnssecRecord/example.com/12345" \
  -H "Content-Type: application/json" \
  -d "{\"apikey\":\"$PORKBUN_API_KEY\",\"secretapikey\":\"$PORKBUN_SECRET_API_KEY\"}"
```

---

### URL Forwarding

#### Get URL Forwarding Rules
```bash
curl -sX POST "https://api.porkbun.com/api/json/v3/domain/getUrlForwarding/example.com" \
  -H "Content-Type: application/json" \
  -d "{\"apikey\":\"$PORKBUN_API_KEY\",\"secretapikey\":\"$PORKBUN_SECRET_API_KEY\"}"
```

#### Add URL Forward (301 Permanent)
```bash
curl -sX POST "https://api.porkbun.com/api/json/v3/domain/addUrlForward/example.com" \
  -H "Content-Type: application/json" \
  -d "{
    \"apikey\":\"$PORKBUN_API_KEY\",
    \"secretapikey\":\"$PORKBUN_SECRET_API_KEY\",
    \"subdomain\":\"old\",
    \"location\":\"https://newsite.com\",
    \"type\":\"permanent\",
    \"includePath\":\"yes\",
    \"wildcard\":\"no\"
  }"
```

#### Add URL Forward (302 Temporary)
```bash
curl -sX POST "https://api.porkbun.com/api/json/v3/domain/addUrlForward/example.com" \
  -H "Content-Type: application/json" \
  -d "{
    \"apikey\":\"$PORKBUN_API_KEY\",
    \"secretapikey\":\"$PORKBUN_SECRET_API_KEY\",
    \"subdomain\":\"\",
    \"location\":\"https://tempsite.com\",
    \"type\":\"temporary\",
    \"includePath\":\"no\",
    \"wildcard\":\"yes\"
  }"
```

#### Delete URL Forward
```bash
curl -sX POST "https://api.porkbun.com/api/json/v3/domain/deleteUrlForward/example.com/123456" \
  -H "Content-Type: application/json" \
  -d "{\"apikey\":\"$PORKBUN_API_KEY\",\"secretapikey\":\"$PORKBUN_SECRET_API_KEY\"}"
```

---

## Record Types Reference

| Type | Purpose | Example Content |
|------|---------|-----------------|
| A | IPv4 address | `192.168.1.1` |
| AAAA | IPv6 address | `2001:db8::1` |
| CNAME | Alias to another domain | `example.github.io` |
| MX | Mail server (requires prio) | `mail.example.com` |
| TXT | Text record (SPF, DKIM, etc) | `v=spf1 include:...` |
| NS | Nameserver delegation | `ns1.example.com` |
| SRV | Service record (requires prio) | `sipserver.example.com` |
| CAA | Certificate authority auth | `0 issue "letsencrypt.org"` |
| ALIAS | Root domain alias | `example.herokudns.com` |

## Notes

- All endpoints use POST method
- TTL is in seconds (600 = 10 minutes, 300 = 5 minutes)
- For MX and SRV records, include `prio` field
- Subdomain `name` can be empty string `""` for root domain (@)
- Response includes `status: "SUCCESS"` or `status: "ERROR"` with message

## License

MIT
