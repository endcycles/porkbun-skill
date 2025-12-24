#!/usr/bin/env python3
"""
Porkbun API CLI - Direct API access for Claude Code
Usage: python3 porkbun.py <action> [args...]
"""

import sys
import os
import json
import urllib.request
import urllib.error
from pathlib import Path

# Load .env from skill directory
ENV_FILE = Path(__file__).parent.parent / ".env"

def load_env():
    """Load API keys from .env file"""
    if not ENV_FILE.exists():
        print(f"Error: {ENV_FILE} not found. Copy .env.example to .env and add your API keys.")
        sys.exit(1)

    env = {}
    with open(ENV_FILE) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                key = key.replace('export ', '').strip()
                env[key] = value.strip()
    return env

def api_call(endpoint, data=None):
    """Make API call to Porkbun"""
    env = load_env()

    url = f"https://api.porkbun.com/api/json/v3{endpoint}"
    payload = {
        "apikey": env.get("PORKBUN_API_KEY"),
        "secretapikey": env.get("PORKBUN_SECRET_API_KEY"),
    }
    if data:
        payload.update(data)

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode('utf-8'),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        return {"status": "ERROR", "message": f"HTTP {e.code}: {e.reason}"}
    except Exception as e:
        return {"status": "ERROR", "message": str(e)}

def print_json(data):
    """Pretty print JSON output"""
    print(json.dumps(data, indent=2))

# ============ Commands ============

def cmd_ping():
    """Test API connection"""
    print_json(api_call("/ping"))

def cmd_domains():
    """List all domains"""
    print_json(api_call("/domain/listAll"))

def cmd_check(domain):
    """Check domain availability"""
    print_json(api_call(f"/domain/checkDomain/{domain}"))

def cmd_pricing():
    """Get TLD pricing"""
    print_json(api_call("/pricing/get"))

def cmd_dns_list(domain):
    """List DNS records for domain"""
    print_json(api_call(f"/dns/retrieve/{domain}"))

def cmd_dns_create(domain, record_type, content, name="", ttl="600", prio=None):
    """Create DNS record"""
    data = {"name": name, "type": record_type, "content": content, "ttl": ttl}
    if prio:
        data["prio"] = prio
    print_json(api_call(f"/dns/create/{domain}", data))

def cmd_dns_edit(domain, record_id, record_type, content, name="", ttl="600", prio=None):
    """Edit DNS record by ID"""
    data = {"name": name, "type": record_type, "content": content, "ttl": ttl}
    if prio:
        data["prio"] = prio
    print_json(api_call(f"/dns/edit/{domain}/{record_id}", data))

def cmd_dns_delete(domain, record_id):
    """Delete DNS record by ID"""
    print_json(api_call(f"/dns/delete/{domain}/{record_id}"))

def cmd_dns_delete_by_type(domain, record_type, subdomain=""):
    """Delete DNS records by type and subdomain"""
    endpoint = f"/dns/deleteByNameType/{domain}/{record_type}"
    if subdomain:
        endpoint += f"/{subdomain}"
    print_json(api_call(endpoint))

def cmd_dns_get_by_type(domain, record_type, subdomain=""):
    """Get DNS records by type and subdomain"""
    endpoint = f"/dns/retrieveByNameType/{domain}/{record_type}"
    if subdomain:
        endpoint += f"/{subdomain}"
    print_json(api_call(endpoint))

def cmd_dns_edit_by_type(domain, record_type, content, subdomain="", ttl="600", prio=None):
    """Edit DNS records by type and subdomain"""
    endpoint = f"/dns/editByNameType/{domain}/{record_type}"
    if subdomain:
        endpoint += f"/{subdomain}"
    data = {"content": content, "ttl": ttl}
    if prio:
        data["prio"] = prio
    print_json(api_call(endpoint, data))

def cmd_ns_get(domain):
    """Get nameservers"""
    print_json(api_call(f"/domain/getNs/{domain}"))

def cmd_ns_update(domain, *nameservers):
    """Update nameservers"""
    print_json(api_call(f"/domain/updateNs/{domain}", {"ns": list(nameservers)}))

def cmd_ssl(domain):
    """Get SSL certificate bundle"""
    print_json(api_call(f"/ssl/retrieve/{domain}"))

def cmd_forwards_list(domain):
    """List URL forwards"""
    print_json(api_call(f"/domain/getUrlForwarding/{domain}"))

def cmd_forward_add(domain, location, subdomain="", forward_type="permanent", include_path="no", wildcard="no"):
    """Add URL forward"""
    data = {
        "subdomain": subdomain,
        "location": location,
        "type": forward_type,
        "includePath": include_path,
        "wildcard": wildcard
    }
    print_json(api_call(f"/domain/addUrlForward/{domain}", data))

def cmd_forward_delete(domain, forward_id):
    """Delete URL forward"""
    print_json(api_call(f"/domain/deleteUrlForward/{domain}/{forward_id}"))

def cmd_glue_list(domain):
    """List glue records"""
    print_json(api_call(f"/domain/getGlue/{domain}"))

def cmd_glue_create(domain, subdomain, *ips):
    """Create glue record (supports multiple IPs)"""
    print_json(api_call(f"/domain/createGlue/{domain}/{subdomain}", {"ip": list(ips)}))

def cmd_glue_delete(domain, subdomain):
    """Delete glue record"""
    print_json(api_call(f"/domain/deleteGlue/{domain}/{subdomain}"))

def cmd_glue_update(domain, subdomain, *ips):
    """Update glue record (replaces all IPs)"""
    print_json(api_call(f"/domain/updateGlue/{domain}/{subdomain}", {"ip": list(ips)}))

def cmd_dnssec_list(domain):
    """List DNSSEC records"""
    print_json(api_call(f"/dns/getDnssecRecords/{domain}"))

def cmd_dnssec_create(domain, key_tag, alg, digest_type, digest):
    """Create DNSSEC record"""
    data = {"keyTag": int(key_tag), "alg": int(alg), "digestType": int(digest_type), "digest": digest}
    print_json(api_call(f"/dns/createDnssecRecord/{domain}", data))

def cmd_dnssec_delete(domain, tag):
    """Delete DNSSEC record by key tag"""
    print_json(api_call(f"/dns/deleteDnssecRecord/{domain}/{tag}"))

def cmd_dns_retrieve(domain, record_id):
    """Retrieve single DNS record by ID"""
    print_json(api_call(f"/dns/retrieve/{domain}/{record_id}"))

def show_help():
    print("""
Porkbun API CLI

Usage: python3 porkbun.py <command> [args...]

Commands:
  ping                              Test API connection
  domains                           List all domains
  check <domain>                    Check domain availability
  pricing                           Get TLD pricing

  dns list <domain>                 List all DNS records
  dns get <domain> <id>             Get single DNS record by ID
  dns create <domain> <type> <content> [name] [ttl] [prio]
  dns edit <domain> <id> <type> <content> [name] [ttl] [prio]
  dns delete <domain> <id>          Delete record by ID
  dns get-type <domain> <type> [subdomain]     Get records by type
  dns edit-type <domain> <type> <content> [subdomain] [ttl] [prio]
  dns delete-type <domain> <type> [subdomain]  Delete records by type

  ns get <domain>                   Get nameservers
  ns update <domain> <ns1> <ns2>... Update nameservers

  ssl <domain>                      Get SSL certificate bundle

  forwards list <domain>            List URL forwards
  forward add <domain> <location> [subdomain] [type] [includePath] [wildcard]
  forward delete <domain> <id>

  glue list <domain>                List glue records
  glue create <domain> <subdomain> <ip> [ip2...]
  glue update <domain> <subdomain> <ip> [ip2...]
  glue delete <domain> <subdomain>

  dnssec list <domain>              List DNSSEC records
  dnssec create <domain> <keyTag> <alg> <digestType> <digest>
  dnssec delete <domain> <keyTag>

Examples:
  python3 porkbun.py domains
  python3 porkbun.py dns list example.com
  python3 porkbun.py dns get example.com 123456789
  python3 porkbun.py dns create example.com A 192.168.1.1 www 600
  python3 porkbun.py dns create example.com MX mail.example.com "" 600 10
  python3 porkbun.py dns get-type example.com A www
  python3 porkbun.py forward add example.com https://newsite.com "" permanent
""")

def main():
    if len(sys.argv) < 2:
        show_help()
        sys.exit(1)

    cmd = sys.argv[1].lower()
    args = sys.argv[2:]

    try:
        if cmd == "ping":
            cmd_ping()
        elif cmd == "domains":
            cmd_domains()
        elif cmd == "check" and args:
            cmd_check(args[0])
        elif cmd == "pricing":
            cmd_pricing()
        elif cmd == "dns" and args:
            subcmd = args[0].lower()
            if subcmd == "list" and len(args) > 1:
                cmd_dns_list(args[1])
            elif subcmd == "get" and len(args) >= 3:
                cmd_dns_retrieve(args[1], args[2])
            elif subcmd == "create" and len(args) >= 4:
                cmd_dns_create(args[1], args[2], args[3], *args[4:])
            elif subcmd == "edit" and len(args) >= 5:
                cmd_dns_edit(args[1], args[2], args[3], args[4], *args[5:])
            elif subcmd == "delete" and len(args) >= 3:
                cmd_dns_delete(args[1], args[2])
            elif subcmd == "get-type" and len(args) >= 3:
                cmd_dns_get_by_type(args[1], args[2], args[3] if len(args) > 3 else "")
            elif subcmd == "edit-type" and len(args) >= 4:
                cmd_dns_edit_by_type(args[1], args[2], args[3], *args[4:])
            elif subcmd == "delete-type" and len(args) >= 3:
                cmd_dns_delete_by_type(args[1], args[2], args[3] if len(args) > 3 else "")
            else:
                show_help()
        elif cmd == "ns" and args:
            if args[0] == "get" and len(args) > 1:
                cmd_ns_get(args[1])
            elif args[0] == "update" and len(args) > 2:
                cmd_ns_update(args[1], *args[2:])
            else:
                show_help()
        elif cmd == "ssl" and args:
            cmd_ssl(args[0])
        elif cmd == "forwards" and args:
            if args[0] == "list" and len(args) > 1:
                cmd_forwards_list(args[1])
        elif cmd == "forward" and args:
            if args[0] == "add" and len(args) >= 3:
                cmd_forward_add(args[1], args[2], *args[3:])
            elif args[0] == "delete" and len(args) >= 3:
                cmd_forward_delete(args[1], args[2])
            else:
                show_help()
        elif cmd == "glue" and args:
            if args[0] == "list" and len(args) > 1:
                cmd_glue_list(args[1])
            elif args[0] == "create" and len(args) >= 4:
                cmd_glue_create(args[1], args[2], *args[3:])
            elif args[0] == "update" and len(args) >= 4:
                cmd_glue_update(args[1], args[2], *args[3:])
            elif args[0] == "delete" and len(args) >= 3:
                cmd_glue_delete(args[1], args[2])
            else:
                show_help()
        elif cmd == "dnssec" and args:
            if args[0] == "list" and len(args) > 1:
                cmd_dnssec_list(args[1])
            elif args[0] == "create" and len(args) >= 6:
                cmd_dnssec_create(args[1], args[2], args[3], args[4], args[5])
            elif args[0] == "delete" and len(args) >= 3:
                cmd_dnssec_delete(args[1], args[2])
            else:
                show_help()
        elif cmd in ["help", "-h", "--help"]:
            show_help()
        else:
            show_help()
            sys.exit(1)
    except IndexError:
        show_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
