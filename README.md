# Porkbun Skill

A Claude Code skill for managing Porkbun domains and DNS records.

Inspired by [porkbun-mcp](https://github.com/myroslavtryhubets/porkbun-mcp) - rebuilt as a lightweight skill.

## How It Works

```
You: "Add an A record for www.example.com pointing to 1.2.3.4"
  ↓
Claude Code: Runs Python script with your API keys
  ↓
Porkbun API: Returns success/failure
  ↓
Claude Code: Reports result to you
```

No Docker. No MCP server. No middleware. Just direct API calls.

## Why a Skill Instead of MCP?

| Approach | Token Overhead | Setup |
|----------|----------------|-------|
| **This skill** | ~500 tokens | Just .env file |
| **MCP Server** | 10,000-17,000+ tokens | Docker, process management |

MCP servers consume 10K-17K tokens each for tool definitions. A 5-server setup burns 55K+ tokens before you start - up to 1/3 of Claude's context window.

Skills load only when triggered and have no persistent process.

## Installation

```bash
cd ~/.claude/skills
git clone https://github.com/endcycles/porkbun-skill.git
cd porkbun-skill
cp .env.example .env
```

Edit `.env` with your [Porkbun API credentials](https://porkbun.com/account/api):
```bash
export PORKBUN_API_KEY=pk1_your_api_key_here
export PORKBUN_SECRET_API_KEY=sk1_your_secret_key_here
```

## CLI Reference

Python script with no dependencies - uses standard library only.

```bash
# General
porkbun.py ping                     # Test API connection
porkbun.py domains                  # List all domains
porkbun.py check example.com        # Check availability
porkbun.py pricing                  # Get TLD pricing

# DNS Records
porkbun.py dns list example.com
porkbun.py dns get example.com 123456789
porkbun.py dns create example.com A 1.2.3.4 www 600
porkbun.py dns edit example.com 123456789 A 5.6.7.8 www 600
porkbun.py dns delete example.com 123456789
porkbun.py dns get-type example.com A www
porkbun.py dns edit-type example.com A 5.6.7.8 www 600
porkbun.py dns delete-type example.com A www

# Nameservers
porkbun.py ns get example.com
porkbun.py ns update example.com ns1.cloudflare.com ns2.cloudflare.com

# URL Forwarding
porkbun.py forwards list example.com
porkbun.py forward add example.com https://newsite.com "" permanent
porkbun.py forward delete example.com 123456

# Glue Records (multiple IPs supported)
porkbun.py glue list example.com
porkbun.py glue create example.com ns1 192.168.1.1 192.168.1.2
porkbun.py glue update example.com ns1 10.0.0.1
porkbun.py glue delete example.com ns1

# SSL & DNSSEC
porkbun.py ssl example.com
porkbun.py dnssec list example.com
porkbun.py dnssec create example.com 12345 8 2 abc123...
porkbun.py dnssec delete example.com 12345

# Help
porkbun.py help
```

Full path: `~/.claude/skills/porkbun-skill/scripts/porkbun.py`

## Natural Language Examples

Just ask Claude Code naturally:

```
"List all my Porkbun domains"
"Add an A record for www.example.com pointing to 192.168.1.1"
"Create a CNAME for blog.example.com pointing to my-blog.netlify.app"
"Set up MX records for Google Workspace"
"Delete the A record for old.example.com"
"What nameservers is example.com using?"
"Get the SSL certificate for example.com"
"Check if coolstartup.io is available"
```

## Record Types

| Type | Purpose | Example |
|------|---------|---------|
| A | IPv4 address | `192.168.1.1` |
| AAAA | IPv6 address | `2001:db8::1` |
| CNAME | Alias | `example.github.io` |
| MX | Mail server (needs prio) | `mail.example.com` |
| TXT | SPF, DKIM, verification | `v=spf1 include:...` |
| NS | Nameserver | `ns1.example.com` |

## License

MIT
