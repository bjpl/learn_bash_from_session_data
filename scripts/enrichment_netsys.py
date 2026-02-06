"""
Enrichment data for Networking, System Administration, and Process Management commands.

This module provides additional educational metadata (use_cases, gotchas,
related commands, difficulty, and supplementary flags) for commands that
exist in COMMAND_DB but are missing these fields.

Sources:
  - man7.org Linux man-pages: https://man7.org/linux/man-pages/dir_section_1.html
  - man7.org section 8: https://man7.org/linux/man-pages/dir_section_8.html
  - nmap.org: https://nmap.org/book/man.html
  - OpenSSH: https://www.openssh.com/manual.html
  - curl docs: https://curl.se/docs/manpage.html
"""

ENRICHMENT_DATA = {
    # =========================================================================
    # NETWORKING - DNS & LOOKUP
    # =========================================================================

    "dig": {
        "man_url": "https://man7.org/linux/man-pages/man1/dig.1.html",
        "use_cases": [
            "Query DNS records for a domain: dig example.com A",
            "Look up MX records for mail troubleshooting: dig example.com MX",
            "Trace the full DNS resolution path: dig +trace example.com",
        ],
        "gotchas": [
            "Output is verbose by default; use +short for just the answer",
            "dig uses system resolvers unless you specify @server explicitly",
        ],
        "related": ["nslookup", "host", "whois"],
        "difficulty": "intermediate",
        "extra_flags": {
            "+short": "Show only the answer, no headers or authority sections",
            "+trace": "Trace the delegation path from root servers",
            "@server": "Query a specific DNS server instead of system default",
        },
    },

    "nslookup": {
        "man_url": "https://man7.org/linux/man-pages/man1/nslookup.1.html",
        "use_cases": [
            "Quick DNS lookup for a hostname: nslookup example.com",
            "Reverse DNS lookup from an IP address: nslookup 8.8.8.8",
            "Query a specific DNS server: nslookup example.com 8.8.8.8",
        ],
        "gotchas": [
            "nslookup is considered deprecated in favor of dig on many systems",
            "Interactive mode behaves differently from command-line mode",
        ],
        "related": ["dig", "host", "whois"],
        "difficulty": "beginner",
    },

    "host": {
        "man_url": "https://man7.org/linux/man-pages/man1/host.1.html",
        "use_cases": [
            "Simple DNS lookup: host example.com",
            "Reverse DNS lookup: host 192.168.1.1",
            "Find mail servers for a domain: host -t MX example.com",
        ],
        "gotchas": [
            "Output format differs significantly from dig and nslookup",
            "Less detailed than dig; not ideal for advanced DNS debugging",
        ],
        "related": ["dig", "nslookup", "whois"],
        "difficulty": "beginner",
    },

    "whois": {
        "man_url": "https://man7.org/linux/man-pages/man1/whois.1.html",
        "use_cases": [
            "Look up domain registration details: whois example.com",
            "Check IP address ownership and ASN info: whois 8.8.8.8",
            "Verify domain expiration dates for renewal planning",
        ],
        "gotchas": [
            "Many registrars now redact personal info due to GDPR/privacy policies",
            "Output format varies wildly between different TLD registries",
        ],
        "related": ["dig", "nslookup", "host"],
        "difficulty": "beginner",
    },

    # =========================================================================
    # NETWORKING - CONNECTIVITY & TRANSFER
    # =========================================================================

    "ping": {
        "man_url": "https://man7.org/linux/man-pages/man8/ping.8.html",
        "use_cases": [
            "Test basic network connectivity to a host: ping 8.8.8.8",
            "Check if a server is reachable and measure round-trip latency",
            "Send a specific number of pings: ping -c 5 example.com",
        ],
        "gotchas": [
            "Many firewalls block ICMP, so no reply does not always mean host is down",
            "On Linux ping runs forever by default; use -c to limit count",
        ],
        "related": ["traceroute", "mtr", "tracepath"],
        "difficulty": "beginner",
        "extra_flags": {
            "-c": "Stop after sending N packets",
            "-i": "Set interval between packets in seconds",
            "-W": "Set timeout for each reply in seconds",
        },
    },

    "traceroute": {
        "man_url": "https://man7.org/linux/man-pages/man8/traceroute.8.html",
        "use_cases": [
            "Map the network path to a destination host",
            "Identify where packet loss or high latency occurs in a route",
            "Debug routing issues between networks",
        ],
        "gotchas": [
            "Uses UDP by default on Linux; some firewalls block it, use -I for ICMP or -T for TCP",
            "Asterisks (*) mean the hop did not respond, not necessarily that it is down",
        ],
        "related": ["mtr", "tracepath", "ping"],
        "difficulty": "intermediate",
        "extra_flags": {
            "-I": "Use ICMP ECHO instead of UDP",
            "-T": "Use TCP SYN for probes (useful through firewalls)",
            "-n": "Do not resolve IP addresses to hostnames",
        },
    },

    "tracepath": {
        "man_url": "https://man7.org/linux/man-pages/man8/tracepath.8.html",
        "use_cases": [
            "Trace the path to a host without requiring root privileges",
            "Discover the MTU along the path to a destination",
            "Lightweight alternative to traceroute for quick diagnostics",
        ],
        "gotchas": [
            "Does not support as many options as traceroute",
            "May not be installed by default on all distributions",
        ],
        "related": ["traceroute", "mtr", "ping"],
        "difficulty": "beginner",
    },

    "mtr": {
        "man_url": "https://man7.org/linux/man-pages/man8/mtr.8.html",
        "use_cases": [
            "Continuously monitor network path quality combining ping and traceroute",
            "Identify intermittent packet loss on specific hops",
            "Generate a report of network path statistics: mtr --report example.com",
        ],
        "gotchas": [
            "Requires root/sudo for ICMP mode; use --udp for unprivileged operation",
            "Interactive TUI mode can confuse new users; use --report for one-shot output",
        ],
        "related": ["traceroute", "ping", "tracepath"],
        "difficulty": "intermediate",
        "extra_flags": {
            "--report": "Run in report mode and exit after N cycles",
            "--udp": "Use UDP instead of ICMP",
            "-c": "Number of pings to send per hop",
        },
    },

    "curl": {
        "man_url": "https://curl.se/docs/manpage.html",
        "use_cases": [
            "Download files from URLs: curl -O https://example.com/file.tar.gz",
            "Test REST API endpoints: curl -X POST -d '{\"key\":\"val\"}' URL",
            "Send form data or upload files to web services",
            "Follow redirects and inspect HTTP headers: curl -LI URL",
        ],
        "gotchas": [
            "Use -f to fail silently on HTTP errors instead of saving the error page",
            "Quote URLs containing special characters like & or ? in the shell",
            "Without -L, curl will not follow HTTP redirects",
        ],
        "related": ["wget", "http", "httpie"],
        "difficulty": "intermediate",
        "extra_flags": {
            "-k": "Allow insecure SSL connections (skip certificate verification)",
            "-L": "Follow HTTP redirects",
            "-o": "Write output to a specific file instead of stdout",
            "-s": "Silent mode; suppress progress meter and errors",
            "-H": "Add a custom HTTP header to the request",
        },
    },

    "wget": {
        "man_url": "https://man7.org/linux/man-pages/man1/wget.1.html",
        "use_cases": [
            "Download a file from the web: wget https://example.com/file.tar.gz",
            "Mirror an entire website recursively: wget -m https://example.com",
            "Resume an interrupted download: wget -c URL",
            "Download files listed in a text file: wget -i urls.txt",
        ],
        "gotchas": [
            "Recursive downloads (-r) without depth limits can consume enormous disk space",
            "wget saves to files by default while curl prints to stdout by default",
            "Use --no-check-certificate cautiously; it disables SSL verification",
        ],
        "related": ["curl", "rsync", "scp"],
        "difficulty": "beginner",
        "extra_flags": {
            "-c": "Continue a partially downloaded file",
            "-q": "Quiet mode; suppress output",
            "-b": "Run in background after startup",
            "--mirror": "Shortcut for -r -N -l inf --no-remove-listing",
        },
    },

    "http": {
        "man_url": "https://httpie.io/docs/cli",
        "use_cases": [
            "Human-friendly HTTP requests: http GET example.com",
            "Send JSON data easily: http POST api.example.com name=value",
            "Inspect response headers with colorized output",
        ],
        "gotchas": [
            "The command may be named 'http' or 'httpie' depending on installation",
            "Sends JSON by default unlike curl which sends form-encoded data",
        ],
        "related": ["curl", "wget", "httpie"],
        "difficulty": "beginner",
    },

    "httpie": {
        "man_url": "https://httpie.io/docs/cli",
        "use_cases": [
            "User-friendly HTTP client with syntax highlighting",
            "Quick API testing with intuitive syntax: httpie POST url key=val",
            "Download files with progress bar and formatted output",
        ],
        "gotchas": [
            "Not installed by default on most systems; install via pip or package manager",
            "The actual command name is usually 'http', not 'httpie'",
        ],
        "related": ["curl", "wget", "http"],
        "difficulty": "beginner",
    },

    "rsync": {
        "man_url": "https://man7.org/linux/man-pages/man1/rsync.1.html",
        "use_cases": [
            "Sync files between local and remote systems efficiently",
            "Create incremental backups: rsync -av --delete /src/ /backup/",
            "Transfer large directories with compression: rsync -avz src/ host:/dest/",
            "Resume interrupted transfers without re-sending completed files",
        ],
        "gotchas": [
            "Trailing slash on source directory matters: dir/ syncs contents, dir syncs the directory itself",
            "--delete removes files in destination that do not exist in source; use with caution",
            "Permissions and ownership preservation requires running as root or using --no-perms",
        ],
        "related": ["scp", "sftp", "cp"],
        "difficulty": "intermediate",
        "extra_flags": {
            "-a": "Archive mode; preserves permissions, timestamps, symlinks, etc.",
            "-z": "Compress data during transfer",
            "--progress": "Show progress during transfer",
            "--dry-run": "Show what would be transferred without actually doing it",
        },
    },

    "scp": {
        "man_url": "https://man7.org/linux/man-pages/man1/scp.1.html",
        "use_cases": [
            "Copy files to a remote server: scp file.txt user@host:/path/",
            "Copy files from a remote server to local machine",
            "Recursively copy directories: scp -r dir/ user@host:/path/",
        ],
        "gotchas": [
            "scp is considered deprecated in favor of sftp or rsync by OpenSSH",
            "Does not support resuming interrupted transfers; use rsync -P instead",
        ],
        "related": ["rsync", "sftp", "ssh"],
        "difficulty": "intermediate",
        "extra_flags": {
            "-r": "Recursively copy entire directories",
            "-P": "Specify an alternate SSH port",
            "-C": "Enable compression during transfer",
        },
    },

    "sftp": {
        "man_url": "https://man7.org/linux/man-pages/man1/sftp.1.html",
        "use_cases": [
            "Interactive secure file transfer session: sftp user@host",
            "Transfer files securely as a replacement for FTP",
            "Batch file transfers using -b option with a command file",
        ],
        "gotchas": [
            "Uses SSH protocol, not FTP; firewall rules differ from traditional FTP",
            "Interactive commands (get, put, ls) differ slightly from local shell commands",
        ],
        "related": ["scp", "rsync", "ftp", "ssh"],
        "difficulty": "intermediate",
    },

    "ftp": {
        "man_url": "https://man7.org/linux/man-pages/man1/ftp.1.html",
        "use_cases": [
            "Connect to legacy FTP servers for file transfer",
            "Upload/download files on systems that only support FTP",
            "Automate FTP transfers with scripted commands",
        ],
        "gotchas": [
            "FTP transmits credentials in plain text; always prefer sftp or scp",
            "Active mode FTP requires firewall rules for data connections on dynamic ports",
        ],
        "related": ["sftp", "scp", "curl", "wget"],
        "difficulty": "beginner",
    },

    "tftp": {
        "man_url": "https://man7.org/linux/man-pages/man1/tftp.1.html",
        "use_cases": [
            "Boot network devices (PXE) that use TFTP for firmware loading",
            "Transfer small configuration files to embedded devices",
            "Simple file transfers in environments where FTP is unavailable",
        ],
        "gotchas": [
            "No authentication or encryption; only use on trusted networks",
            "Limited to small files; no directory listing or resume support",
        ],
        "related": ["ftp", "sftp", "scp"],
        "difficulty": "intermediate",
    },

    "telnet": {
        "man_url": "https://man7.org/linux/man-pages/man1/telnet.1.html",
        "use_cases": [
            "Test if a TCP port is open on a remote host: telnet host 80",
            "Debug text-based protocols like SMTP or HTTP manually",
            "Quick connectivity test when nc is not available",
        ],
        "gotchas": [
            "Never use telnet for remote login; it sends everything in plain text",
            "Many modern systems do not have telnet installed by default",
        ],
        "related": ["ssh", "nc", "ncat"],
        "difficulty": "beginner",
    },

    "ssh": {
        "man_url": "https://man7.org/linux/man-pages/man1/ssh.1.html",
        "use_cases": [
            "Securely log into a remote machine: ssh user@host",
            "Run a command on a remote server: ssh user@host 'ls /var/log'",
            "Create SSH tunnels for port forwarding: ssh -L 8080:localhost:80 host",
            "Use as a SOCKS proxy: ssh -D 1080 user@host",
        ],
        "gotchas": [
            "Strict host key checking will reject changed host keys; update known_hosts if the server was legitimately reinstalled",
            "Agent forwarding (-A) can be a security risk on untrusted intermediate hosts",
            "Idle SSH connections may be killed by firewalls; use ServerAliveInterval in config",
        ],
        "related": ["scp", "sftp", "rsync", "ssh-keygen"],
        "difficulty": "intermediate",
        "extra_flags": {
            "-L": "Local port forwarding: -L local_port:remote_host:remote_port",
            "-R": "Remote port forwarding",
            "-D": "Dynamic SOCKS proxy on local port",
            "-N": "Do not execute a remote command (useful for tunnels only)",
            "-J": "Jump host (proxy jump) for connecting through a bastion",
        },
    },

    # =========================================================================
    # NETWORKING - INTERFACES & ROUTING
    # =========================================================================

    "ip": {
        "man_url": "https://man7.org/linux/man-pages/man8/ip.8.html",
        "use_cases": [
            "Show all network interfaces and addresses: ip addr show",
            "Add or remove IP addresses from interfaces: ip addr add 10.0.0.1/24 dev eth0",
            "Display and manipulate the routing table: ip route show",
            "Bring interfaces up or down: ip link set eth0 up",
        ],
        "gotchas": [
            "ip replaces the deprecated ifconfig, route, and arp commands",
            "Changes made with ip are not persistent across reboots; use network config files",
            "Subcommands can be abbreviated: ip a, ip r, ip l",
        ],
        "related": ["ifconfig", "route", "ss", "arp"],
        "difficulty": "intermediate",
        "extra_flags": {
            "-br": "Brief output mode for concise display",
            "-c": "Colorize output",
            "-s": "Show statistics",
        },
    },

    "ifconfig": {
        "man_url": "https://man7.org/linux/man-pages/man8/ifconfig.8.html",
        "use_cases": [
            "Display all network interface configurations",
            "Assign an IP address to an interface: ifconfig eth0 192.168.1.10",
            "Enable or disable a network interface: ifconfig eth0 up/down",
        ],
        "gotchas": [
            "Deprecated in favor of the ip command on modern Linux systems",
            "May not be installed by default; part of net-tools package",
        ],
        "related": ["ip", "route", "netstat"],
        "difficulty": "beginner",
    },

    "route": {
        "man_url": "https://man7.org/linux/man-pages/man8/route.8.html",
        "use_cases": [
            "Display the kernel routing table: route -n",
            "Add a default gateway: route add default gw 192.168.1.1",
            "Add a static route to a specific network",
        ],
        "gotchas": [
            "Deprecated in favor of ip route on modern Linux systems",
            "Changes are not persistent; configure routes in network config files",
        ],
        "related": ["ip", "ifconfig", "netstat", "traceroute"],
        "difficulty": "intermediate",
    },

    "arp": {
        "man_url": "https://man7.org/linux/man-pages/man8/arp.8.html",
        "use_cases": [
            "Display the ARP cache showing IP-to-MAC mappings: arp -a",
            "Manually add a static ARP entry for a host",
            "Delete an ARP cache entry to force re-resolution",
        ],
        "gotchas": [
            "Deprecated in favor of ip neigh on modern systems",
            "ARP cache entries expire; stale entries can cause connectivity issues",
        ],
        "related": ["ip", "arping", "ifconfig", "ping"],
        "difficulty": "intermediate",
    },

    "arping": {
        "man_url": "https://man7.org/linux/man-pages/man8/arping.8.html",
        "use_cases": [
            "Check if an IP address is already in use on the local network",
            "Resolve an IP address to a MAC address at layer 2",
            "Detect duplicate IP addresses on a LAN segment",
        ],
        "gotchas": [
            "Only works on the local network segment; cannot cross routers",
            "Requires root privileges to send raw ARP packets",
        ],
        "related": ["arp", "ping", "ip", "nmap"],
        "difficulty": "intermediate",
    },

    # =========================================================================
    # NETWORKING - SOCKETS & PORT SCANNING
    # =========================================================================

    "ss": {
        "man_url": "https://man7.org/linux/man-pages/man8/ss.8.html",
        "use_cases": [
            "List all listening TCP ports: ss -tlnp",
            "Show established connections with process info: ss -tp",
            "Filter connections by port or state: ss state established dport = :443",
        ],
        "gotchas": [
            "Replaces the deprecated netstat command; syntax differs significantly",
            "Process info (-p) requires root to see processes owned by other users",
        ],
        "related": ["netstat", "lsof", "ip"],
        "difficulty": "intermediate",
        "extra_flags": {
            "-t": "Show TCP sockets only",
            "-u": "Show UDP sockets only",
            "-l": "Show only listening sockets",
            "-n": "Show numeric addresses instead of resolving names",
            "-p": "Show the process using each socket",
        },
    },

    "netstat": {
        "man_url": "https://man7.org/linux/man-pages/man8/netstat.8.html",
        "use_cases": [
            "List all listening ports: netstat -tlnp",
            "Show network connections and their states",
            "Display routing table: netstat -rn",
        ],
        "gotchas": [
            "Deprecated in favor of ss on modern Linux; part of net-tools",
            "Output can be very long on busy systems; use grep to filter",
        ],
        "related": ["ss", "lsof", "ip", "route"],
        "difficulty": "intermediate",
    },

    "nc": {
        "man_url": "https://man7.org/linux/man-pages/man1/nc.1.html",
        "use_cases": [
            "Test if a TCP port is open: nc -zv host 80",
            "Create a simple TCP server: nc -l -p 8080",
            "Transfer files between machines over the network",
            "Debug network protocols by sending raw data",
        ],
        "gotchas": [
            "Multiple implementations exist (GNU, OpenBSD, ncat); flags differ between them",
            "No encryption by default; use ncat --ssl or socat for encrypted connections",
        ],
        "related": ["ncat", "netcat", "socat", "telnet"],
        "difficulty": "intermediate",
        "extra_flags": {
            "-z": "Scan mode; report connection status without sending data",
            "-v": "Verbose output",
            "-l": "Listen mode; act as a server",
            "-u": "Use UDP instead of TCP",
        },
    },

    "ncat": {
        "man_url": "https://nmap.org/ncat/guide/",
        "use_cases": [
            "Improved netcat with SSL support: ncat --ssl host 443",
            "Create a persistent backdoor listener for authorized testing",
            "Broker connections between multiple clients: ncat --broker",
        ],
        "gotchas": [
            "Part of the nmap suite; not installed by default on all systems",
            "Different from traditional nc/netcat; some flags are incompatible",
        ],
        "related": ["nc", "netcat", "socat", "nmap"],
        "difficulty": "intermediate",
    },

    "netcat": {
        "man_url": "https://man7.org/linux/man-pages/man1/nc.1.html",
        "use_cases": [
            "Often an alias for nc; used for ad-hoc TCP/UDP connections",
            "Port scanning and banner grabbing on remote hosts",
            "Pipe data between processes over the network",
        ],
        "gotchas": [
            "The actual binary and flags depend on which netcat variant is installed",
            "On some systems, netcat and nc are different implementations",
        ],
        "related": ["nc", "ncat", "socat", "telnet"],
        "difficulty": "intermediate",
    },

    "socat": {
        "man_url": "https://man7.org/linux/man-pages/man1/socat.1.html",
        "use_cases": [
            "Relay data between two bidirectional byte streams",
            "Create encrypted tunnels: socat TCP-LISTEN:8080 OPENSSL:host:443",
            "Forward Unix sockets to TCP or vice versa",
            "Advanced port forwarding and protocol bridging",
        ],
        "gotchas": [
            "Syntax is complex with many address types; steep learning curve",
            "Not installed by default on most distributions",
        ],
        "related": ["nc", "ncat", "ssh", "stunnel"],
        "difficulty": "advanced",
    },

    "lsof": {
        "man_url": "https://man7.org/linux/man-pages/man8/lsof.8.html",
        "use_cases": [
            "Find which process is using a specific port: lsof -i :80",
            "List all open files for a process: lsof -p PID",
            "Find processes using a specific file: lsof /var/log/syslog",
            "List all network connections: lsof -i",
        ],
        "gotchas": [
            "Requires root to see files opened by other users' processes",
            "Can be slow on systems with many open file descriptors",
        ],
        "related": ["ss", "fuser", "ps", "netstat"],
        "difficulty": "intermediate",
        "extra_flags": {
            "-i": "List network connections (optionally filter by port or protocol)",
            "-p": "Filter by process ID",
            "-u": "Filter by username",
            "+D": "Recursively list open files in a directory",
        },
    },

    "fuser": {
        "man_url": "https://man7.org/linux/man-pages/man1/fuser.1.html",
        "use_cases": [
            "Find which process is using a file or directory: fuser /mnt/usb",
            "Kill all processes using a specific file: fuser -k /path/to/file",
            "Check which process holds a port: fuser 80/tcp",
        ],
        "gotchas": [
            "fuser -k sends SIGKILL by default which cannot be caught; use -signal to specify",
            "Requires root to see processes from other users",
        ],
        "related": ["lsof", "ps", "kill", "ss"],
        "difficulty": "intermediate",
    },

    # =========================================================================
    # NETWORKING - SECURITY & SCANNING
    # =========================================================================

    "nmap": {
        "man_url": "https://nmap.org/book/man.html",
        "use_cases": [
            "Scan a host for open ports: nmap 192.168.1.1",
            "Detect services and versions: nmap -sV host",
            "Perform OS detection: nmap -O host",
            "Scan an entire subnet: nmap 192.168.1.0/24",
        ],
        "gotchas": [
            "Scanning without authorization may be illegal; always get written permission",
            "SYN scans (-sS) require root privileges",
            "Aggressive scans (-A) are noisy and easily detected by IDS",
        ],
        "related": ["masscan", "nc", "ss", "nikto"],
        "difficulty": "advanced",
        "extra_flags": {
            "-sS": "TCP SYN scan (stealth scan, requires root)",
            "-sV": "Probe open ports to determine service/version info",
            "-O": "Enable OS detection",
            "-A": "Aggressive scan: OS detection, version, scripts, traceroute",
            "-p": "Specify port range: -p 1-1000 or -p- for all ports",
        },
    },

    "masscan": {
        "man_url": "https://github.com/robertdavidgraham/masscan",
        "use_cases": [
            "Rapidly scan large IP ranges for open ports at scale",
            "Internet-wide surveys of specific services",
            "Fast alternative to nmap for initial port discovery",
        ],
        "gotchas": [
            "Extremely fast scanning can overwhelm networks and trigger IDS alerts",
            "Does not do service version detection; pair with nmap for follow-up",
            "Requires root and uses its own TCP stack bypassing the kernel",
        ],
        "related": ["nmap", "nc", "ss"],
        "difficulty": "advanced",
    },

    "nikto": {
        "man_url": "https://github.com/sullo/nikto/wiki",
        "use_cases": [
            "Scan web servers for known vulnerabilities and misconfigurations",
            "Check for outdated server software and dangerous default files",
            "Automated web security assessment during penetration tests",
        ],
        "gotchas": [
            "Very noisy; easily detected by IDS/WAF and logged by web servers",
            "Only use against systems you have explicit permission to test",
        ],
        "related": ["nmap", "curl", "openssl"],
        "difficulty": "advanced",
    },

    "openssl": {
        "man_url": "https://man7.org/linux/man-pages/man1/openssl.1ssl.html",
        "use_cases": [
            "Test SSL/TLS connections: openssl s_client -connect host:443",
            "Generate self-signed certificates for development",
            "Check certificate expiration dates and details",
            "Encrypt/decrypt files: openssl enc -aes-256-cbc -in file -out file.enc",
        ],
        "gotchas": [
            "The command-line interface has many subcommands with inconsistent syntax",
            "Default cipher choices may be weak in older versions; specify explicitly",
            "s_client does not verify server certificates by default; use -verify_return_error",
        ],
        "related": ["ssh", "curl", "nc"],
        "difficulty": "advanced",
        "extra_flags": {
            "s_client": "Test SSL/TLS client connections",
            "req": "Create certificate signing requests",
            "x509": "Display and manipulate X.509 certificates",
            "genrsa": "Generate RSA private keys",
        },
    },

    # =========================================================================
    # NETWORKING - FIREWALLS
    # =========================================================================

    "iptables": {
        "man_url": "https://man7.org/linux/man-pages/man8/iptables.8.html",
        "use_cases": [
            "List current firewall rules: iptables -L -n -v",
            "Block an IP address: iptables -A INPUT -s IP -j DROP",
            "Allow traffic on a specific port: iptables -A INPUT -p tcp --dport 80 -j ACCEPT",
            "Set up NAT/masquerading for network address translation",
        ],
        "gotchas": [
            "Rules are evaluated in order; a DROP before an ACCEPT will block matching traffic",
            "Rules are lost on reboot unless saved with iptables-save or a persistence mechanism",
            "Locking yourself out is easy on remote servers; always allow SSH first",
        ],
        "related": ["nft", "ufw", "firewall-cmd"],
        "difficulty": "advanced",
        "extra_flags": {
            "-A": "Append a rule to the end of a chain",
            "-D": "Delete a rule from a chain",
            "-I": "Insert a rule at a specific position in a chain",
            "-F": "Flush (delete) all rules in a chain",
        },
    },

    "nft": {
        "man_url": "https://man7.org/linux/man-pages/man8/nft.8.html",
        "use_cases": [
            "Modern replacement for iptables using nftables framework",
            "List all rules: nft list ruleset",
            "Create firewall rules with a cleaner syntax than iptables",
        ],
        "gotchas": [
            "Syntax is different from iptables; existing scripts need rewriting",
            "Not all distributions default to nftables yet; check which backend is active",
        ],
        "related": ["iptables", "ufw", "firewall-cmd"],
        "difficulty": "advanced",
    },

    "ufw": {
        "man_url": "https://man7.org/linux/man-pages/man8/ufw.8.html",
        "use_cases": [
            "Simple firewall management: ufw allow 22/tcp",
            "Enable/disable firewall quickly: ufw enable / ufw disable",
            "Check firewall status and rules: ufw status verbose",
        ],
        "gotchas": [
            "ufw is a frontend to iptables; raw iptables rules may conflict",
            "Enabling ufw on a remote server without allowing SSH first will lock you out",
        ],
        "related": ["iptables", "nft", "firewall-cmd"],
        "difficulty": "beginner",
    },

    "firewall-cmd": {
        "man_url": "https://firewalld.org/documentation/man-pages/firewall-cmd.html",
        "use_cases": [
            "Manage firewalld zones and services on RHEL/CentOS/Fedora",
            "Open a port permanently: firewall-cmd --permanent --add-port=80/tcp",
            "List active rules: firewall-cmd --list-all",
        ],
        "gotchas": [
            "Changes without --permanent are lost on reload or reboot",
            "Must run firewall-cmd --reload after permanent changes to activate them",
        ],
        "related": ["iptables", "ufw", "nft"],
        "difficulty": "intermediate",
    },

    # =========================================================================
    # NETWORKING - PACKET CAPTURE & ANALYSIS
    # =========================================================================

    "tcpdump": {
        "man_url": "https://man7.org/linux/man-pages/man8/tcpdump.8.html",
        "use_cases": [
            "Capture packets on an interface: tcpdump -i eth0",
            "Filter traffic by host or port: tcpdump host 10.0.0.1 and port 80",
            "Save capture to file for analysis: tcpdump -w capture.pcap",
            "Debug network connectivity and protocol issues in real time",
        ],
        "gotchas": [
            "Requires root privileges to capture packets",
            "High-traffic captures can fill disk quickly; use -c to limit packet count",
            "Output can be overwhelming; use specific filters to narrow down traffic",
        ],
        "related": ["wireshark", "nmap", "ss", "nc"],
        "difficulty": "advanced",
        "extra_flags": {
            "-i": "Specify the network interface to capture on",
            "-w": "Write raw packets to a file (pcap format)",
            "-r": "Read packets from a previously saved file",
            "-c": "Capture only N packets then stop",
            "-n": "Do not resolve hostnames",
        },
    },

    "wireshark": {
        "man_url": "https://www.wireshark.org/docs/man-pages/wireshark.html",
        "use_cases": [
            "Analyze network traffic with a graphical interface",
            "Inspect packet details and protocol dissection",
            "Open pcap files captured by tcpdump for deeper analysis",
        ],
        "gotchas": [
            "GUI application; use tshark for command-line packet analysis",
            "Capturing on remote servers requires SSH tunneling or tshark",
        ],
        "related": ["tcpdump", "nmap", "ss"],
        "difficulty": "advanced",
    },

    # =========================================================================
    # PROCESS MANAGEMENT
    # =========================================================================

    "ps": {
        "man_url": "https://man7.org/linux/man-pages/man1/ps.1.html",
        "use_cases": [
            "List all running processes: ps aux",
            "Show process tree: ps auxf or ps --forest",
            "Find a specific process: ps aux | grep nginx",
        ],
        "gotchas": [
            "BSD-style (aux) and UNIX-style (-ef) options produce different output formats",
            "ps shows a snapshot; use top or htop for real-time monitoring",
        ],
        "related": ["top", "htop", "kill", "pgrep"],
        "difficulty": "beginner",
        "extra_flags": {
            "aux": "Show all processes with user-oriented format (BSD style)",
            "-ef": "Show all processes with full format (UNIX style)",
            "--forest": "Show process tree hierarchy",
            "-o": "Custom output format: ps -o pid,user,%cpu,%mem,cmd",
        },
    },

    "top": {
        "man_url": "https://man7.org/linux/man-pages/man1/top.1.html",
        "use_cases": [
            "Monitor system resource usage in real time",
            "Identify processes consuming the most CPU or memory",
            "Batch mode for scripting: top -bn1 | head -20",
        ],
        "gotchas": [
            "Default refresh rate can cause high CPU use on slow systems; press d to change interval",
            "Memory values shown may be misleading; RES is actual RAM used, VIRT includes mapped files",
        ],
        "related": ["htop", "btop", "atop", "ps"],
        "difficulty": "beginner",
        "extra_flags": {
            "-b": "Batch mode; useful for piping output to other commands",
            "-n": "Number of iterations in batch mode",
            "-p": "Monitor only specific PIDs",
            "-u": "Show only processes owned by a specific user",
        },
    },

    "htop": {
        "man_url": "https://man7.org/linux/man-pages/man1/htop.1.html",
        "use_cases": [
            "Interactive process viewer with color and mouse support",
            "Sort processes by CPU, memory, or other fields interactively",
            "Send signals to processes directly from the interface",
        ],
        "gotchas": [
            "Not installed by default on all systems; install via package manager",
            "Tree view (F5) can be confusing if processes reparent frequently",
        ],
        "related": ["top", "btop", "atop", "ps"],
        "difficulty": "beginner",
    },

    "btop": {
        "man_url": "https://github.com/aristocratos/btop",
        "use_cases": [
            "Modern resource monitor with rich TUI showing CPU, memory, disks, and network",
            "Visual process management with graphs and detailed stats",
            "Monitor system performance with a clean, colorful interface",
        ],
        "gotchas": [
            "Requires a terminal with true color support for full visual fidelity",
            "Not installed by default; must be installed separately",
        ],
        "related": ["htop", "top", "atop", "vmstat"],
        "difficulty": "beginner",
    },

    "atop": {
        "man_url": "https://man7.org/linux/man-pages/man1/atop.1.html",
        "use_cases": [
            "Advanced system and process monitor with historical logging",
            "Analyze past system performance from atop log files",
            "Monitor disk I/O, network, and CPU at the process level",
        ],
        "gotchas": [
            "Logging daemon must be running to capture historical data",
            "Output is dense; takes time to learn which metrics matter",
        ],
        "related": ["top", "htop", "sar", "vmstat"],
        "difficulty": "intermediate",
    },

    "kill": {
        "man_url": "https://man7.org/linux/man-pages/man1/kill.1.html",
        "use_cases": [
            "Terminate a process by PID: kill 1234",
            "Send a specific signal: kill -9 PID (SIGKILL) or kill -HUP PID",
            "Gracefully stop a process: kill -TERM PID",
        ],
        "gotchas": [
            "kill without a signal sends SIGTERM (15), not SIGKILL (9); the process can catch it",
            "SIGKILL (-9) cannot be caught or ignored and may leave resources in a bad state",
            "You can only kill processes you own unless you are root",
        ],
        "related": ["killall", "pkill", "pgrep", "ps"],
        "difficulty": "beginner",
        "extra_flags": {
            "-9": "Send SIGKILL (force kill, cannot be caught)",
            "-15": "Send SIGTERM (graceful termination, default)",
            "-l": "List all available signal names",
            "-HUP": "Send SIGHUP (often used to reload configuration)",
        },
    },

    "killall": {
        "man_url": "https://man7.org/linux/man-pages/man1/killall.1.html",
        "use_cases": [
            "Kill all processes by name: killall nginx",
            "Send a signal to all instances of a program: killall -HUP sshd",
            "Interactively confirm before killing: killall -i processname",
        ],
        "gotchas": [
            "On Solaris, killall without args kills ALL processes; Linux version is safe",
            "Matches by exact process name; use pkill for partial or regex matching",
        ],
        "related": ["kill", "pkill", "pgrep", "ps"],
        "difficulty": "beginner",
    },

    "pgrep": {
        "man_url": "https://man7.org/linux/man-pages/man1/pgrep.1.html",
        "use_cases": [
            "Find PIDs matching a process name: pgrep nginx",
            "List processes by user: pgrep -u www-data",
            "Show full command line of matched processes: pgrep -a sshd",
        ],
        "gotchas": [
            "Matches against process name by default, not the full command line; use -f for full match",
            "Returns exit code 1 if no processes match, useful for scripting",
        ],
        "related": ["pkill", "kill", "ps", "pidof"],
        "difficulty": "beginner",
    },

    "pkill": {
        "man_url": "https://man7.org/linux/man-pages/man1/pkill.1.html",
        "use_cases": [
            "Kill processes by name pattern: pkill -f 'python my_script'",
            "Send signals to processes matching a pattern: pkill -HUP nginx",
            "Kill all processes for a specific user: pkill -u username",
        ],
        "gotchas": [
            "Without -f, matches only the process name, not arguments",
            "Be careful with broad patterns; pkill java kills ALL Java processes",
        ],
        "related": ["pgrep", "kill", "killall", "ps"],
        "difficulty": "beginner",
    },

    "nice": {
        "man_url": "https://man7.org/linux/man-pages/man1/nice.1.html",
        "use_cases": [
            "Start a process with lower priority: nice -n 19 long_task",
            "Run CPU-intensive tasks without impacting interactive performance",
            "Launch background jobs at reduced scheduling priority",
        ],
        "gotchas": [
            "Only root can set negative nice values (higher priority)",
            "Nice values range from -20 (highest priority) to 19 (lowest priority)",
        ],
        "related": ["renice", "ps", "top", "ionice"],
        "difficulty": "intermediate",
    },

    "renice": {
        "man_url": "https://man7.org/linux/man-pages/man1/renice.1.html",
        "use_cases": [
            "Change the priority of a running process: renice 10 -p PID",
            "Lower priority of a CPU-hogging process without restarting it",
            "Adjust priority for all processes of a user: renice 5 -u username",
        ],
        "gotchas": [
            "Non-root users can only increase nice value (lower priority), never decrease it",
            "Affects CPU scheduling only; for I/O priority use ionice",
        ],
        "related": ["nice", "kill", "top", "ps"],
        "difficulty": "intermediate",
    },

    # =========================================================================
    # JOB CONTROL
    # =========================================================================

    "jobs": {
        "man_url": "https://man7.org/linux/man-pages/man1/jobs.1p.html",
        "use_cases": [
            "List all background and suspended jobs in the current shell",
            "Check the status of a backgrounded process: jobs -l",
            "Identify job numbers for use with fg and bg commands",
        ],
        "gotchas": [
            "Jobs are per-shell; you cannot see jobs from other terminal sessions",
            "Job numbers (%1, %2) are different from PIDs",
        ],
        "related": ["bg", "fg", "disown", "nohup"],
        "difficulty": "beginner",
    },

    "bg": {
        "man_url": "https://man7.org/linux/man-pages/man1/bg.1p.html",
        "use_cases": [
            "Resume a suspended job in the background: bg %1",
            "Continue a Ctrl+Z stopped process without bringing it to the foreground",
            "Convert an accidentally foreground process to background execution",
        ],
        "gotchas": [
            "The process will still be killed if the terminal closes; use disown or nohup",
            "If the background job tries to read from the terminal, it will be stopped again",
        ],
        "related": ["fg", "jobs", "disown", "nohup"],
        "difficulty": "beginner",
    },

    "fg": {
        "man_url": "https://man7.org/linux/man-pages/man1/fg.1p.html",
        "use_cases": [
            "Bring a background job to the foreground: fg %1",
            "Resume interaction with a previously backgrounded process",
            "Switch between multiple running jobs in a shell session",
        ],
        "gotchas": [
            "Without arguments, fg brings the most recently backgrounded job forward",
            "If the job has finished, fg will report an error",
        ],
        "related": ["bg", "jobs", "disown", "kill"],
        "difficulty": "beginner",
    },

    "disown": {
        "man_url": "https://www.gnu.org/software/bash/manual/html_node/Job-Control-Builtins.html",
        "use_cases": [
            "Detach a background job from the shell so it survives logout: disown %1",
            "Prevent SIGHUP from killing background processes when closing the terminal",
            "Remove a job from the shell's job table: disown -h %1",
        ],
        "gotchas": [
            "disown is a bash built-in; not available in all shells",
            "The process output still goes to the terminal unless redirected",
        ],
        "related": ["nohup", "bg", "jobs", "screen"],
        "difficulty": "intermediate",
    },

    "nohup": {
        "man_url": "https://man7.org/linux/man-pages/man1/nohup.1.html",
        "use_cases": [
            "Run a command immune to hangups: nohup ./script.sh &",
            "Start a long-running process that survives terminal disconnection",
            "Redirect output to nohup.out automatically for later review",
        ],
        "gotchas": [
            "Output goes to nohup.out in the current directory if stdout is a terminal",
            "nohup does not background the process; append & to do so",
        ],
        "related": ["disown", "screen", "tmux", "bg"],
        "difficulty": "beginner",
    },

    "timeout": {
        "man_url": "https://man7.org/linux/man-pages/man1/timeout.1.html",
        "use_cases": [
            "Run a command with a time limit: timeout 30s wget URL",
            "Prevent hung processes in scripts: timeout 5m backup.sh",
            "Set a hard kill after a grace period: timeout --kill-after=10s 60s cmd",
        ],
        "gotchas": [
            "Sends SIGTERM by default; the process might catch it and not exit",
            "Exit status is 124 when the command times out, which can be checked in scripts",
        ],
        "related": ["kill", "watch", "sleep"],
        "difficulty": "beginner",
    },

    # =========================================================================
    # TERMINAL MULTIPLEXERS
    # =========================================================================

    "tmux": {
        "man_url": "https://man7.org/linux/man-pages/man1/tmux.1.html",
        "use_cases": [
            "Persist terminal sessions across SSH disconnections",
            "Split the terminal into multiple panes: tmux split-window",
            "Manage multiple terminal windows in a single connection",
            "Share a terminal session with another user for pair programming",
        ],
        "gotchas": [
            "Prefix key is Ctrl+b by default; many users remap it to Ctrl+a",
            "Nested tmux sessions can cause confusing prefix key behavior",
            "Copy mode uses different keybindings depending on vi/emacs setting",
        ],
        "related": ["screen", "byobu", "nohup"],
        "difficulty": "intermediate",
        "extra_flags": {
            "new -s": "Create a new named session: tmux new -s mysession",
            "attach -t": "Attach to an existing session: tmux attach -t mysession",
            "ls": "List all active sessions",
            "kill-session -t": "Kill a specific session",
        },
    },

    "screen": {
        "man_url": "https://man7.org/linux/man-pages/man1/screen.1.html",
        "use_cases": [
            "Keep processes running after SSH disconnection: screen -S session_name",
            "Reattach to a detached session: screen -r session_name",
            "Run long-running tasks on remote servers safely",
        ],
        "gotchas": [
            "Prefix key is Ctrl+a which conflicts with readline beginning-of-line",
            "screen is being replaced by tmux on many systems but remains widely available",
        ],
        "related": ["tmux", "byobu", "nohup"],
        "difficulty": "intermediate",
    },

    "byobu": {
        "man_url": "https://www.byobu.org/documentation",
        "use_cases": [
            "User-friendly wrapper around tmux/screen with status bar",
            "Enhanced terminal multiplexer with keybinding help (F1-F12)",
            "Easy session management with sensible defaults",
        ],
        "gotchas": [
            "Uses tmux or screen as backend; behavior depends on which is configured",
            "F-key bindings may conflict with other applications or terminal emulators",
        ],
        "related": ["tmux", "screen", "nohup"],
        "difficulty": "beginner",
    },

    # =========================================================================
    # SYSTEM MONITORING & PERFORMANCE
    # =========================================================================

    "vmstat": {
        "man_url": "https://man7.org/linux/man-pages/man8/vmstat.8.html",
        "use_cases": [
            "Report virtual memory statistics: vmstat 1 5 (every 1s, 5 times)",
            "Check for memory pressure, swapping, and CPU utilization",
            "Monitor system performance trends over short intervals",
        ],
        "gotchas": [
            "First line of output shows averages since boot, not current values",
            "High si/so (swap in/out) values indicate memory pressure",
        ],
        "related": ["iostat", "mpstat", "sar", "free"],
        "difficulty": "intermediate",
    },

    "iostat": {
        "man_url": "https://man7.org/linux/man-pages/man1/iostat.1.html",
        "use_cases": [
            "Monitor disk I/O statistics: iostat -x 1",
            "Identify disk bottlenecks by checking utilization and wait times",
            "Report CPU utilization alongside disk activity",
        ],
        "gotchas": [
            "First report shows statistics since boot; subsequent reports show interval data",
            "Part of the sysstat package; may need to be installed separately",
        ],
        "related": ["vmstat", "mpstat", "sar", "iotop"],
        "difficulty": "intermediate",
    },

    "mpstat": {
        "man_url": "https://man7.org/linux/man-pages/man1/mpstat.1.html",
        "use_cases": [
            "Show per-CPU utilization: mpstat -P ALL 1",
            "Identify CPU imbalance in multi-core systems",
            "Monitor interrupt and softirq distribution across CPUs",
        ],
        "gotchas": [
            "Part of the sysstat package; not installed by default on all systems",
            "First report shows averages since boot like vmstat and iostat",
        ],
        "related": ["vmstat", "iostat", "sar", "top"],
        "difficulty": "intermediate",
    },

    "sar": {
        "man_url": "https://man7.org/linux/man-pages/man1/sar.1.html",
        "use_cases": [
            "Collect and report system activity data over time",
            "Review historical CPU/memory/disk usage: sar -u -f /var/log/sysstat/sa01",
            "Generate reports for capacity planning: sar -r (memory), sar -b (I/O)",
        ],
        "gotchas": [
            "Requires sysstat data collection daemon (sadc) to be enabled for historical data",
            "Without -f, sar shows today's data; archived data is in /var/log/sysstat/",
        ],
        "related": ["vmstat", "iostat", "mpstat", "atop"],
        "difficulty": "advanced",
    },

    "dmesg": {
        "man_url": "https://man7.org/linux/man-pages/man1/dmesg.1.html",
        "use_cases": [
            "View kernel ring buffer messages: dmesg | tail",
            "Diagnose hardware issues and driver errors after boot",
            "Check for disk errors, USB device events, or OOM killer activity",
        ],
        "gotchas": [
            "Requires root on some systems due to dmesg_restrict sysctl setting",
            "Ring buffer has a fixed size; old messages are overwritten on busy systems",
        ],
        "related": ["journalctl", "syslog", "lsblk"],
        "difficulty": "intermediate",
        "extra_flags": {
            "-T": "Show human-readable timestamps instead of seconds since boot",
            "-w": "Follow new messages in real time (like tail -f)",
            "--level": "Filter by log level: --level=err,warn",
        },
    },

    "journalctl": {
        "man_url": "https://man7.org/linux/man-pages/man1/journalctl.1.html",
        "use_cases": [
            "View systemd journal logs: journalctl -xe",
            "Follow logs in real time: journalctl -f",
            "Filter logs by service: journalctl -u nginx.service",
            "View logs since last boot: journalctl -b",
        ],
        "gotchas": [
            "Journal may not persist across reboots unless /var/log/journal/ directory exists",
            "Non-root users may only see their own logs depending on configuration",
        ],
        "related": ["systemctl", "dmesg", "service"],
        "difficulty": "intermediate",
        "extra_flags": {
            "-f": "Follow new log entries in real time",
            "-u": "Show logs for a specific systemd unit",
            "-b": "Show logs from current boot only",
            "--since": "Show logs since a timestamp: --since '2024-01-01 00:00'",
            "-p": "Filter by priority level (emerg, alert, crit, err, warning, notice, info, debug)",
        },
    },

    # =========================================================================
    # SYSTEM SERVICES & INIT
    # =========================================================================

    "systemctl": {
        "man_url": "https://man7.org/linux/man-pages/man1/systemctl.1.html",
        "use_cases": [
            "Start/stop/restart services: systemctl restart nginx",
            "Enable a service to start at boot: systemctl enable sshd",
            "Check service status: systemctl status nginx",
            "List all active services: systemctl list-units --type=service",
        ],
        "gotchas": [
            "enable does not start the service immediately; use enable --now for both",
            "Masking a service (systemctl mask) prevents it from starting even manually",
            "User services use --user flag and run in user scope, not system scope",
        ],
        "related": ["service", "journalctl", "init"],
        "difficulty": "intermediate",
        "extra_flags": {
            "enable --now": "Enable and start a service in one command",
            "is-active": "Check if a service is running (useful in scripts)",
            "daemon-reload": "Reload systemd after editing unit files",
            "list-timers": "Show all active systemd timers",
        },
    },

    "service": {
        "man_url": "https://man7.org/linux/man-pages/man8/service.8.html",
        "use_cases": [
            "Start/stop/restart services on SysV init systems: service nginx restart",
            "Check service status: service sshd status",
            "Compatibility wrapper that works on both SysV and systemd systems",
        ],
        "gotchas": [
            "On systemd systems, service redirects to systemctl; use systemctl directly",
            "Does not support enable/disable; use chkconfig (SysV) or systemctl (systemd)",
        ],
        "related": ["systemctl", "init", "journalctl"],
        "difficulty": "beginner",
    },

    "init": {
        "man_url": "https://man7.org/linux/man-pages/man1/init.1.html",
        "use_cases": [
            "The first process started by the kernel (PID 1)",
            "Change runlevel on SysV systems: init 3 (multi-user), init 5 (graphical)",
            "Halt the system: init 0, or reboot: init 6",
        ],
        "gotchas": [
            "On systemd systems, init is symlinked to systemd; runlevel commands still work",
            "Directly calling init to change runlevel is disruptive; prefer systemctl",
        ],
        "related": ["systemctl", "runlevel", "shutdown", "reboot"],
        "difficulty": "advanced",
    },

    "runlevel": {
        "man_url": "https://man7.org/linux/man-pages/man8/runlevel.8.html",
        "use_cases": [
            "Display the current and previous system runlevel",
            "Verify the system is in the expected runlevel for troubleshooting",
            "Script checks for runlevel-dependent behavior",
        ],
        "gotchas": [
            "On systemd systems, runlevel is a compatibility wrapper; use systemctl get-default",
            "Output format is 'previous current' where N means no previous runlevel known",
        ],
        "related": ["init", "systemctl", "shutdown"],
        "difficulty": "intermediate",
    },

    # =========================================================================
    # SYSTEM - HOSTNAME & LOCALE & TIME
    # =========================================================================

    "hostnamectl": {
        "man_url": "https://man7.org/linux/man-pages/man1/hostnamectl.1.html",
        "use_cases": [
            "View current hostname and OS info: hostnamectl status",
            "Set the system hostname: hostnamectl set-hostname myserver",
            "Check machine ID, boot ID, and virtualization type",
        ],
        "gotchas": [
            "Only works on systemd-based systems",
            "Setting hostname may not update /etc/hosts; update it manually",
        ],
        "related": ["timedatectl", "localectl", "systemctl"],
        "difficulty": "beginner",
    },

    "localectl": {
        "man_url": "https://man7.org/linux/man-pages/man1/localectl.1.html",
        "use_cases": [
            "View current locale settings: localectl status",
            "Set system locale: localectl set-locale LANG=en_US.UTF-8",
            "Configure keyboard layout: localectl set-keymap us",
        ],
        "gotchas": [
            "Changes may require re-login or service restart to take effect",
            "Only works on systemd-based systems",
        ],
        "related": ["hostnamectl", "timedatectl", "systemctl"],
        "difficulty": "beginner",
    },

    "timedatectl": {
        "man_url": "https://man7.org/linux/man-pages/man1/timedatectl.1.html",
        "use_cases": [
            "View current time and timezone: timedatectl status",
            "Set the system timezone: timedatectl set-timezone America/New_York",
            "Enable/disable NTP synchronization: timedatectl set-ntp true",
        ],
        "gotchas": [
            "Only works on systemd-based systems; use date/hwclock on others",
            "Changing timezone does not change the hardware clock (UTC by default)",
        ],
        "related": ["hostnamectl", "localectl", "systemctl"],
        "difficulty": "beginner",
    },

    # =========================================================================
    # SYSTEM - POWER & SHUTDOWN
    # =========================================================================

    "shutdown": {
        "man_url": "https://man7.org/linux/man-pages/man8/shutdown.8.html",
        "use_cases": [
            "Schedule system shutdown: shutdown -h +10 (in 10 minutes)",
            "Shutdown immediately: shutdown -h now",
            "Reboot the system: shutdown -r now",
            "Cancel a pending shutdown: shutdown -c",
        ],
        "gotchas": [
            "Without a time argument, shutdown defaults to +1 (one minute), not immediately",
            "Sends wall message to all logged-in users before shutting down",
        ],
        "related": ["reboot", "halt", "poweroff", "init"],
        "difficulty": "beginner",
    },

    "reboot": {
        "man_url": "https://man7.org/linux/man-pages/man8/reboot.8.html",
        "use_cases": [
            "Reboot the system immediately: reboot",
            "Force an immediate reboot without syncing: reboot -f",
            "Schedule a reboot via shutdown -r for a specific time",
        ],
        "gotchas": [
            "reboot -f skips shutdown scripts and can cause data loss",
            "Requires root privileges; non-root users must use sudo",
        ],
        "related": ["shutdown", "halt", "poweroff", "systemctl"],
        "difficulty": "beginner",
    },

    "halt": {
        "man_url": "https://man7.org/linux/man-pages/man8/halt.8.html",
        "use_cases": [
            "Halt the system (stop the CPU but may not power off)",
            "Used in scripts for clean system shutdown procedures",
            "On systemd systems, equivalent to systemctl halt",
        ],
        "gotchas": [
            "halt stops the system but may not power off the machine; use poweroff instead",
            "Behavior varies between SysV init and systemd systems",
        ],
        "related": ["poweroff", "shutdown", "reboot", "init"],
        "difficulty": "beginner",
    },

    "poweroff": {
        "man_url": "https://man7.org/linux/man-pages/man8/poweroff.8.html",
        "use_cases": [
            "Power off the machine immediately",
            "Clean shutdown with power-off: equivalent to shutdown -h now",
            "Used in automated scripts to power down systems",
        ],
        "gotchas": [
            "Requires root; non-root users need sudo or polkit authorization",
            "On systemd, equivalent to systemctl poweroff",
        ],
        "related": ["halt", "shutdown", "reboot", "init"],
        "difficulty": "beginner",
    },

    # =========================================================================
    # DISK & FILESYSTEM
    # =========================================================================

    "mount": {
        "man_url": "https://man7.org/linux/man-pages/man8/mount.8.html",
        "use_cases": [
            "Mount a filesystem: mount /dev/sdb1 /mnt/usb",
            "List all mounted filesystems: mount | column -t",
            "Mount with specific options: mount -o ro,noexec /dev/sda1 /mnt",
        ],
        "gotchas": [
            "Mounting requires root unless the filesystem is listed in /etc/fstab with user option",
            "Mount points must be empty directories; existing contents are hidden while mounted",
        ],
        "related": ["umount", "lsblk", "fdisk", "blkid"],
        "difficulty": "intermediate",
        "extra_flags": {
            "-o": "Mount options (ro, rw, noexec, nosuid, etc.)",
            "-t": "Specify filesystem type (ext4, ntfs, vfat, etc.)",
            "-a": "Mount all filesystems listed in /etc/fstab",
        },
    },

    "umount": {
        "man_url": "https://man7.org/linux/man-pages/man8/umount.8.html",
        "use_cases": [
            "Unmount a filesystem: umount /mnt/usb",
            "Force unmount a busy filesystem: umount -f /mnt/stuck",
            "Lazy unmount that detaches when no longer busy: umount -l /mnt/busy",
        ],
        "gotchas": [
            "Cannot unmount if any process has open files on it; use lsof or fuser to find them",
            "Lazy unmount (-l) hides the mount immediately but data may not be flushed yet",
        ],
        "related": ["mount", "lsof", "fuser", "lsblk"],
        "difficulty": "intermediate",
    },

    "lsblk": {
        "man_url": "https://man7.org/linux/man-pages/man8/lsblk.8.html",
        "use_cases": [
            "List all block devices and their mount points: lsblk",
            "Show filesystem type and size: lsblk -f",
            "Identify disk partitions and their hierarchy",
        ],
        "gotchas": [
            "Does not show unpartitioned space; use fdisk -l for that",
            "Loop devices from snap packages can clutter the output",
        ],
        "related": ["blkid", "fdisk", "mount", "df"],
        "difficulty": "beginner",
    },

    "blkid": {
        "man_url": "https://man7.org/linux/man-pages/man8/blkid.8.html",
        "use_cases": [
            "Show UUIDs and filesystem types for all block devices: blkid",
            "Find the UUID of a partition for use in /etc/fstab",
            "Identify filesystem type on a specific device: blkid /dev/sda1",
        ],
        "gotchas": [
            "Requires root to probe all devices; non-root sees limited info",
            "Cached results may be stale; use -p to force fresh probing",
        ],
        "related": ["lsblk", "fdisk", "mount"],
        "difficulty": "intermediate",
    },

    "fdisk": {
        "man_url": "https://man7.org/linux/man-pages/man8/fdisk.8.html",
        "use_cases": [
            "List all disk partitions: fdisk -l",
            "Create, delete, and modify disk partitions interactively",
            "View partition table details for a specific disk: fdisk -l /dev/sda",
        ],
        "gotchas": [
            "Destructive operations; wrong disk selection can destroy all data",
            "Changes are not written until you explicitly press 'w' in interactive mode",
            "Does not support GPT well; use gdisk or parted for GPT disks",
        ],
        "related": ["lsblk", "blkid", "mkfs", "mount"],
        "difficulty": "advanced",
    },

    "mkfs": {
        "man_url": "https://man7.org/linux/man-pages/man8/mkfs.8.html",
        "use_cases": [
            "Create a new filesystem: mkfs.ext4 /dev/sdb1",
            "Format a USB drive: mkfs.vfat /dev/sdc1",
            "Initialize a partition with a specific filesystem type",
        ],
        "gotchas": [
            "Destroys all data on the target partition; double-check the device name",
            "Use mkfs.TYPE (e.g., mkfs.ext4, mkfs.xfs) for specific filesystem types",
        ],
        "related": ["fdisk", "mount", "lsblk", "fsck"],
        "difficulty": "advanced",
    },

    "fsck": {
        "man_url": "https://man7.org/linux/man-pages/man8/fsck.8.html",
        "use_cases": [
            "Check and repair a filesystem: fsck /dev/sda1",
            "Force check even if filesystem appears clean: fsck -f /dev/sda1",
            "Automatically fix errors: fsck -y /dev/sda1",
        ],
        "gotchas": [
            "Never run fsck on a mounted filesystem; it can cause data corruption",
            "Running fsck on the root filesystem requires booting into recovery mode",
        ],
        "related": ["mkfs", "mount", "lsblk", "fdisk"],
        "difficulty": "advanced",
    },

    # =========================================================================
    # SYSTEM - MISCELLANEOUS
    # =========================================================================

    "sort": {
        "man_url": "https://man7.org/linux/man-pages/man1/sort.1.html",
        "use_cases": [
            "Sort file contents alphabetically: sort file.txt",
            "Sort numerically: sort -n numbers.txt",
            "Sort by a specific column: sort -k2 -t: /etc/passwd",
            "Remove duplicate lines while sorting: sort -u file.txt",
        ],
        "gotchas": [
            "Default sort is lexicographic; use -n for numeric, -V for version strings",
            "Locale affects sort order; use LC_ALL=C for byte-value sorting",
        ],
        "related": ["uniq", "cut", "awk", "wc"],
        "difficulty": "beginner",
        "extra_flags": {
            "-n": "Sort numerically instead of lexicographically",
            "-r": "Reverse the sort order",
            "-k": "Sort by a specific field/column",
            "-u": "Output only unique lines (like sort | uniq)",
            "-h": "Sort human-readable numbers (1K, 2M, 3G)",
        },
    },

    "plocate": {
        "man_url": "https://man7.org/linux/man-pages/man1/plocate.1.html",
        "use_cases": [
            "Find files by name instantly using a pre-built database: plocate myfile.txt",
            "Much faster than find for filename searches across the whole filesystem",
            "Search with patterns: plocate '*.conf'",
        ],
        "gotchas": [
            "Database must be updated regularly (updatedb) to find newly created files",
            "Does not find files created since the last database update",
        ],
        "related": ["find", "locate", "which", "whereis"],
        "difficulty": "beginner",
    },

    "finger": {
        "man_url": "https://man7.org/linux/man-pages/man1/finger.1.html",
        "use_cases": [
            "Display user information: finger username",
            "Show who is logged in and their idle time",
            "View a user's plan and project files (.plan, .project)",
        ],
        "gotchas": [
            "finger daemon is a security risk and disabled on most modern systems",
            "Remote finger queries (finger @host) are rarely supported anymore",
        ],
        "related": ["who", "w", "last", "id"],
        "difficulty": "beginner",
    },
}
