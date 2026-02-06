"""
Enrichment data for Networking, Process/System, and Permissions commands.

This module provides use_cases, gotchas, man_url, related, difficulty, and
extra_flags for commands that have thin entries in COMMAND_DB.

Usage:
    from scripts.enrichment_netproc import ENRICHMENT_DATA
    # Merge into COMMAND_DB entries as needed.
"""

ENRICHMENT_DATA = {

    # =========================================================================
    # NETWORKING COMMANDS
    # =========================================================================

    "nc": {
        "man_url": "https://man7.org/linux/man-pages/man1/ncat.1.html",
        "use_cases": [
            "Test if a remote port is open with nc -zv host 443 before deploying",
            "Transfer a file between machines: receiver runs nc -l -p 9999 > file.txt, sender runs nc host 9999 < file.txt",
            "Create a quick ad-hoc chat between two terminals for debugging coordination",
            "Pipe data into a network service for scripted testing: echo 'GET / HTTP/1.0\\r\\n\\r\\n' | nc host 80",
        ],
        "gotchas": [
            "There are multiple incompatible netcat implementations (GNU, OpenBSD, ncat) with different flag syntax -- the -p flag behavior and -e support vary between them",
            "The -e flag to execute a program on connection is disabled in many distributions for security reasons; use ncat --exec instead",
            "OpenBSD netcat does not support the -p flag with -l; the port goes directly after -l",
        ],
        "related": ["ncat", "socat", "telnet", "curl"],
        "difficulty": "intermediate",
        "extra_flags": {
            "-k": "Keep listening after client disconnects (accept multiple connections)",
            "-e": "Execute a program after connection (not available in all versions)",
            "-N": "Shutdown the network socket after EOF on stdin",
        },
    },

    "ncat": {
        "man_url": "https://man7.org/linux/man-pages/man1/ncat.1.html",
        "use_cases": [
            "Create an encrypted tunnel with ncat --ssl -l 4444 for secure ad-hoc communication",
            "Set up a simple chat server with ncat -l --chat 8080 for team debugging sessions",
            "Proxy connections through an HTTP proxy to reach internal services with --proxy",
            "Serve a single file over HTTPS by combining --ssl with --exec",
        ],
        "gotchas": [
            "ncat is part of the nmap package and may not be installed by default on minimal systems",
            "The --ssl flag generates a temporary certificate; clients will see certificate warnings unless you provide --ssl-cert and --ssl-key",
        ],
        "related": ["nc", "socat", "openssl", "nmap"],
        "difficulty": "intermediate",
        "extra_flags": {
            "--ssl": "Use SSL/TLS encryption on the connection",
            "--ssl-verify": "Require and verify the server certificate",
            "-k": "Accept multiple connections in listen mode",
            "--broker": "Enable connection brokering between multiple clients",
            "--chat": "Start a simple chat server",
            "-m": "Maximum number of simultaneous connections",
        },
    },

    "netcat": {
        "man_url": "https://man7.org/linux/man-pages/man1/ncat.1.html",
        "use_cases": [
            "Quick port scan of common ports with nc -zv host 20-100",
            "Test SMTP server connectivity by connecting to port 25 and typing HELO commands",
            "Banner grab a service to identify its version: echo '' | nc -w3 host 22",
        ],
        "gotchas": [
            "The netcat command may point to different implementations depending on your distro -- check which version with nc -h or readlink $(which nc)",
            "Port scanning with -z is slow compared to nmap; use nmap for serious scanning work",
        ],
        "related": ["nc", "ncat", "socat", "nmap"],
        "difficulty": "intermediate",
        "extra_flags": {},
    },

    "socat": {
        "man_url": "https://man7.org/linux/man-pages/man1/socat.1.html",
        "use_cases": [
            "Forward a local TCP port to a remote host: socat TCP-LISTEN:8080,fork TCP:remote:80",
            "Create an SSL-encrypted tunnel: socat TCP-LISTEN:443,fork,reuseaddr OPENSSL:target:443",
            "Bridge a Unix socket to a TCP port for remote access to Docker or database sockets",
            "Connect two different socket types, like converting a serial port to a TCP stream",
        ],
        "gotchas": [
            "socat address syntax is powerful but complex -- the learning curve is steep compared to netcat",
            "Forgetting the fork option on a listener means it handles only one connection then exits",
            "The reuseaddr option is often needed to avoid 'address already in use' errors on quick restarts",
        ],
        "related": ["nc", "ncat", "ssh", "openssl"],
        "difficulty": "advanced",
        "extra_flags": {
            "-4": "Use IPv4 only",
            "-6": "Use IPv6 only",
            "-t": "Set EOF timeout in seconds",
            "-T": "Set total inactivity timeout in seconds",
            "-b": "Set data transfer block size (default 8192)",
        },
    },

    "telnet": {
        "man_url": "https://man7.org/linux/man-pages/man1/telnet.1.html",
        "use_cases": [
            "Test if a web server is responding: telnet host 80 then type GET / HTTP/1.0",
            "Debug SMTP mail delivery by connecting to port 25 and issuing EHLO, MAIL FROM, RCPT TO commands",
            "Verify a Redis server is accessible: telnet host 6379 then type PING",
            "Check if a specific port is reachable through a firewall when nc is not installed",
        ],
        "gotchas": [
            "telnet transmits everything including passwords in plain text -- never use it for actual remote login; use SSH instead",
            "telnet is not installed by default on many modern distributions; you may need to install it explicitly",
            "The escape character (default Ctrl-]) is needed to close a telnet session; just closing the terminal may leave the connection open",
        ],
        "related": ["ssh", "nc", "curl", "openssl"],
        "difficulty": "beginner",
        "extra_flags": {},
    },

    "ftp": {
        "man_url": "https://man7.org/linux/man-pages/man1/ftp.1.html",
        "use_cases": [
            "Upload files to a legacy web hosting provider that only supports FTP",
            "Automate file transfers from an FTP server using a script with -n and heredoc commands",
            "Download firmware updates from embedded device FTP servers during maintenance windows",
        ],
        "gotchas": [
            "FTP transmits credentials and data in plain text -- use sftp or scp for anything involving sensitive data",
            "Active mode FTP requires the server to connect back to your machine, which fails behind most NAT/firewalls; use -p for passive mode",
            "Binary mode must be set explicitly with 'binary' command before transferring non-text files, or they will be corrupted",
        ],
        "related": ["sftp", "scp", "rsync", "curl"],
        "difficulty": "beginner",
        "extra_flags": {},
    },

    "tftp": {
        "man_url": "https://man7.org/linux/man-pages/man1/tftp.1.html",
        "use_cases": [
            "Network boot (PXE) servers use TFTP to deliver boot images to diskless clients",
            "Push firmware updates to network switches and routers that support TFTP",
            "Transfer configuration files to embedded devices with minimal network stacks",
        ],
        "gotchas": [
            "TFTP has no authentication whatsoever -- anyone on the network can read or write files if the server allows it",
            "TFTP uses UDP port 69 and has a maximum file size of 32MB in the original protocol (extensions exist but are not universal)",
            "The TFTP server directory must be pre-configured; you cannot browse or list files like FTP",
        ],
        "related": ["ftp", "scp", "curl"],
        "difficulty": "intermediate",
        "extra_flags": {},
    },

    "traceroute": {
        "man_url": "https://man7.org/linux/man-pages/man8/traceroute.8.html",
        "use_cases": [
            "Diagnose where a network path fails when you cannot reach a remote server",
            "Identify which ISP or network segment is causing high latency",
            "Verify that traffic is taking the expected route through your network infrastructure",
        ],
        "gotchas": [
            "Many routers and firewalls block or rate-limit traceroute probes, showing * * * for those hops -- this does not always mean the hop is down",
            "Default UDP-based traceroute may be blocked where ICMP (-I) is allowed, or vice versa; try both methods",
            "traceroute requires root privileges for ICMP mode (-I); use tracepath as a non-root alternative",
        ],
        "related": ["tracepath", "mtr", "ping", "ip"],
        "difficulty": "intermediate",
        "extra_flags": {
            "-T": "Use TCP SYN probes instead of UDP (useful when UDP is firewalled)",
            "-p": "Set the destination port for UDP probes",
            "-q": "Set the number of probe packets per hop (default 3)",
        },
    },

    "tracepath": {
        "man_url": "https://man7.org/linux/man-pages/man8/tracepath.8.html",
        "use_cases": [
            "Trace a network path without root privileges when traceroute is not available",
            "Discover the Path MTU to a destination to diagnose packet fragmentation issues",
            "Quick network path diagnosis on servers where you do not have sudo access",
        ],
        "gotchas": [
            "tracepath does not support all the protocol options that traceroute has (no TCP mode, no ICMP mode)",
            "Path MTU discovery may report incorrect values if ICMP 'need fragmentation' messages are blocked by intermediate firewalls",
        ],
        "related": ["traceroute", "mtr", "ping"],
        "difficulty": "beginner",
        "extra_flags": {},
    },

    "mtr": {
        "man_url": "https://linux.die.net/man/8/mtr",
        "use_cases": [
            "Diagnose intermittent packet loss at a specific network hop that one-shot traceroute misses",
            "Generate a network quality report for an ISP support ticket with mtr -r -c 100 host",
            "Monitor real-time latency to a game server or VoIP endpoint to correlate with quality drops",
            "Test if a firewall is blocking TCP traffic with mtr -T -P 443 host",
        ],
        "gotchas": [
            "Packet loss shown at intermediate hops does not always indicate a problem -- many routers deprioritize ICMP responses causing false loss readings",
            "mtr requires root privileges for raw socket access; some distributions provide a setuid wrapper",
            "The -r report mode sends 10 cycles by default, which may not be enough to catch intermittent issues; use -c 100 or more",
        ],
        "related": ["traceroute", "tracepath", "ping"],
        "difficulty": "intermediate",
        "extra_flags": {
            "-4": "Use IPv4 only",
            "-6": "Use IPv6 only",
            "-s": "Set the packet size in bytes",
            "-i": "Set the interval between ICMP ECHO requests",
            "-e": "Display MPLS information in report mode",
        },
    },

    "dig": {
        "man_url": "https://linux.die.net/man/1/dig",
        "use_cases": [
            "Verify DNS propagation after changing A records: dig @8.8.8.8 example.com A +short",
            "Debug email delivery by checking MX records: dig -t MX example.com",
            "Trace the full DNS delegation chain to find where resolution breaks: dig example.com +trace",
            "Check DNSSEC validation: dig example.com +dnssec",
            "Look up TXT records for SPF/DKIM verification: dig -t TXT example.com",
        ],
        "gotchas": [
            "dig queries your system's default DNS resolver unless you specify one with @server -- results may differ from what the public sees",
            "The +short flag strips all context; when debugging, use the full output to check TTL, authority section, and response flags",
            "dig is part of the bind-utils or dnsutils package and may not be installed on minimal systems; use host as a simpler fallback",
        ],
        "related": ["nslookup", "host", "whois"],
        "difficulty": "intermediate",
        "extra_flags": {
            "+noall +answer": "Show only the answer section for clean output",
            "+dnssec": "Request DNSSEC records",
            "+tcp": "Use TCP instead of UDP for the query",
            "-x": "Perform a reverse DNS lookup on an IP address",
        },
    },

    "nslookup": {
        "man_url": "https://linux.die.net/man/1/nslookup",
        "use_cases": [
            "Quick hostname-to-IP resolution check: nslookup example.com",
            "Query a specific DNS server to test if it has updated records: nslookup example.com 8.8.8.8",
            "Look up MX records for email troubleshooting: nslookup -type=MX example.com",
        ],
        "gotchas": [
            "nslookup is considered deprecated by the ISC (BIND authors) in favor of dig; it may give misleading results in some edge cases",
            "nslookup bypasses the system resolver's /etc/hosts file, so local hostname overrides will not appear",
            "Interactive mode can be confusing -- type 'exit' to quit, not Ctrl-C which just cancels the current query",
        ],
        "related": ["dig", "host", "whois"],
        "difficulty": "beginner",
        "extra_flags": {},
    },

    "host": {
        "man_url": "https://man7.org/linux/man-pages/man1/host.1.html",
        "use_cases": [
            "Quick DNS lookup with clean output: host example.com",
            "Reverse DNS lookup to find hostname for an IP: host 8.8.8.8",
            "Check all record types for a domain: host -a example.com",
        ],
        "gotchas": [
            "host output format varies between versions; scripts should use dig +short for reliable parsing",
            "Like dig, host bypasses /etc/hosts and queries DNS servers directly",
        ],
        "related": ["dig", "nslookup", "whois"],
        "difficulty": "beginner",
        "extra_flags": {},
    },

    "ip": {
        "man_url": "https://man7.org/linux/man-pages/man8/ip.8.html",
        "use_cases": [
            "View all IP addresses assigned to interfaces: ip -br addr (brief, readable format)",
            "Add a static route: ip route add 10.0.0.0/8 via 192.168.1.1",
            "Bring a network interface up or down: ip link set eth0 up/down",
            "View the ARP neighbor cache: ip neigh show",
            "Add a secondary IP address to an interface: ip addr add 192.168.1.100/24 dev eth0",
        ],
        "gotchas": [
            "Changes made with ip are not persistent across reboots -- use netplan, NetworkManager, or /etc/network/interfaces for permanent config",
            "ip replaces ifconfig, route, and arp but uses different syntax for everything; old muscle memory does not transfer",
            "The ip command requires the iproute2 package, which is standard on modern distros but may be missing on very minimal containers",
        ],
        "related": ["ifconfig", "route", "arp", "ss", "netstat"],
        "difficulty": "intermediate",
        "extra_flags": {
            "-s": "Show statistics (packet counts, errors)",
            "-j": "Output in JSON format for scripting",
            "-4": "Show only IPv4",
            "-6": "Show only IPv6",
        },
    },

    "ifconfig": {
        "man_url": "https://man7.org/linux/man-pages/man8/ifconfig.8.html",
        "use_cases": [
            "Quick check of your IP address: ifconfig (or ifconfig eth0 for a specific interface)",
            "Temporarily assign an IP address: ifconfig eth0 192.168.1.100 netmask 255.255.255.0",
            "Bring an interface up or down: ifconfig eth0 up / ifconfig eth0 down",
        ],
        "gotchas": [
            "ifconfig is deprecated in favor of the ip command on modern Linux systems -- it may not be installed by default",
            "ifconfig cannot display or manage multiple IP addresses per interface properly; ip addr handles this correctly",
            "On many modern distros, ifconfig is in /sbin which may not be in a regular user's PATH",
        ],
        "related": ["ip", "route", "netstat"],
        "difficulty": "beginner",
        "extra_flags": {
            "-a": "Display all interfaces including those that are down",
            "-s": "Display a short summary list",
        },
    },

    "route": {
        "man_url": "https://man7.org/linux/man-pages/man8/route.8.html",
        "use_cases": [
            "View the kernel routing table: route -n",
            "Add a default gateway: route add default gw 192.168.1.1",
            "Add a route to a specific network: route add -net 10.0.0.0/8 gw 192.168.1.254",
        ],
        "gotchas": [
            "route is deprecated; use ip route on modern systems for full functionality",
            "Routes added with route are not persistent -- they disappear on reboot unless added to startup scripts",
            "Forgetting -n causes slow output because route tries to reverse-DNS every address",
        ],
        "related": ["ip", "netstat", "traceroute"],
        "difficulty": "intermediate",
        "extra_flags": {},
    },

    "netstat": {
        "man_url": "https://man7.org/linux/man-pages/man8/netstat.8.html",
        "use_cases": [
            "Find which process is using port 8080: netstat -tlnp | grep 8080",
            "Show all established TCP connections: netstat -tn",
            "List all listening services: netstat -tlnp",
        ],
        "gotchas": [
            "netstat is deprecated in favor of ss, which is faster and provides more information",
            "The -p flag requires root privileges to see process names for all sockets, not just your own",
            "netstat may not be installed by default on modern systems; install the net-tools package",
        ],
        "related": ["ss", "lsof", "ip"],
        "difficulty": "intermediate",
        "extra_flags": {
            "-a": "Show all sockets including listening and non-listening",
            "-r": "Display the kernel routing table",
            "-s": "Display summary statistics per protocol",
            "-c": "Continuously refresh the display",
        },
    },

    "ss": {
        "man_url": "https://man7.org/linux/man-pages/man8/ss.8.html",
        "use_cases": [
            "Find which process is listening on port 3000: ss -tlnp | grep 3000",
            "Show all established connections with process info: ss -tnp",
            "Display socket memory usage to debug buffer bloat: ss -tm",
            "Filter connections by state: ss state established '( dport = :443 )'",
            "Display summary statistics for all protocols: ss -s",
        ],
        "gotchas": [
            "The -p flag requires root to show processes for sockets owned by other users",
            "ss filter expressions use a different syntax than netstat grep patterns -- read the man page for the state and address filter syntax",
            "ss output columns differ from netstat; scripts that parse netstat output need rewriting",
        ],
        "related": ["netstat", "lsof", "ip"],
        "difficulty": "intermediate",
        "extra_flags": {
            "-a": "Show both listening and non-listening sockets",
            "-s": "Print summary statistics",
            "-o": "Show timer information",
            "-e": "Show detailed socket information (uid, inode)",
            "-m": "Show socket memory usage",
            "-i": "Show internal TCP information (congestion, RTT)",
            "-K": "Forcibly close a socket",
            "-H": "Suppress header line",
        },
    },

    "arp": {
        "man_url": "https://man7.org/linux/man-pages/man8/arp.8.html",
        "use_cases": [
            "View the ARP cache to see MAC-to-IP mappings on the local network: arp -a",
            "Set a static ARP entry to prevent ARP spoofing for a critical gateway",
            "Diagnose duplicate IP addresses by checking for multiple MAC addresses",
        ],
        "gotchas": [
            "arp is deprecated; use ip neigh on modern systems",
            "The ARP cache has timeouts, so entries may disappear if not recently used",
            "Static ARP entries do not survive reboots unless configured in startup scripts",
        ],
        "related": ["arping", "ip", "ifconfig"],
        "difficulty": "intermediate",
        "extra_flags": {},
    },

    "arping": {
        "man_url": "https://man7.org/linux/man-pages/man8/arping.8.html",
        "use_cases": [
            "Test layer-2 connectivity when ICMP ping is blocked by a firewall",
            "Detect duplicate IP addresses on a network with arping -D",
            "Discover the MAC address of a host on the local network",
        ],
        "gotchas": [
            "arping only works on the local network segment -- it cannot cross routers",
            "Requires root privileges to send raw ARP packets",
            "There are two different arping implementations (Thomas Habets and iputils) with slightly different flags",
        ],
        "related": ["arp", "ping", "ip"],
        "difficulty": "intermediate",
        "extra_flags": {},
    },

    "iptables": {
        "man_url": "https://man7.org/linux/man-pages/man8/iptables.8.html",
        "use_cases": [
            "Block an abusive IP: iptables -A INPUT -s 1.2.3.4 -j DROP",
            "Allow inbound HTTP/HTTPS: iptables -A INPUT -p tcp --dport 80 -j ACCEPT",
            "Set up port forwarding (NAT): iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8080",
            "Log dropped packets for debugging: iptables -A INPUT -j LOG --log-prefix 'DROPPED: '",
            "Save rules to survive reboot: iptables-save > /etc/iptables/rules.v4",
        ],
        "gotchas": [
            "Rules are evaluated in order and first match wins -- a broad ACCEPT at the top can override specific DROP rules below it",
            "iptables rules are lost on reboot unless saved with iptables-save and restored with iptables-restore or a service like netfilter-persistent",
            "Flushing rules with -F on a remote server with default DROP policy will lock you out -- always set -P INPUT ACCEPT before flushing",
            "iptables is being replaced by nftables on newer distributions; new deployments should prefer nft",
        ],
        "related": ["nft", "ufw", "firewall-cmd", "ip"],
        "difficulty": "advanced",
        "extra_flags": {
            "-t": "Specify table (filter, nat, mangle, raw, security)",
            "-s": "Source IP address or range",
            "-d": "Destination IP address or range",
            "-j": "Target action (ACCEPT, DROP, REJECT, LOG)",
            "-p": "Protocol (tcp, udp, icmp)",
            "--dport": "Destination port (requires -p tcp or -p udp)",
            "--sport": "Source port (requires -p tcp or -p udp)",
            "-i": "Input network interface",
            "-o": "Output network interface",
        },
    },

    "nft": {
        "man_url": "https://www.netfilter.org/projects/nftables/manpage.html",
        "use_cases": [
            "List the entire active ruleset: nft list ruleset",
            "Create a basic firewall accepting established connections and dropping others",
            "Replace complex iptables + ip6tables rules with a single unified nft ruleset",
            "Load a firewall configuration from a file: nft -f /etc/nftables.conf",
        ],
        "gotchas": [
            "nftables uses a different syntax from iptables; existing iptables rules cannot be pasted directly",
            "The iptables-translate tool can help convert iptables rules to nft syntax",
            "nft requires root privileges for all operations",
            "Flushing the ruleset on a remote server will lock you out if the default policy is drop",
        ],
        "related": ["iptables", "ufw", "firewall-cmd"],
        "difficulty": "advanced",
        "extra_flags": {
            "-j": "Output in JSON format for programmatic use",
            "-s": "Translate numeric protocols and services to names",
            "-c": "Check command validity without applying changes",
        },
    },

    "ufw": {
        "man_url": "https://manpages.ubuntu.com/manpages/man8/ufw.8.html",
        "use_cases": [
            "Set up a basic server firewall: ufw default deny incoming, ufw allow ssh, ufw allow 80/tcp, ufw enable",
            "Allow connections only from a specific IP: ufw allow from 10.0.0.5 to any port 22",
            "Rate limit SSH to prevent brute force: ufw limit ssh",
            "Check firewall status and rules: ufw status verbose",
        ],
        "gotchas": [
            "Enabling ufw on a remote server without first allowing SSH will lock you out immediately",
            "ufw operates on top of iptables/nftables; direct iptables rules may conflict with ufw rules",
            "ufw does not manage Docker's iptables rules -- Docker bypasses ufw by inserting its own chains",
        ],
        "related": ["iptables", "nft", "firewall-cmd"],
        "difficulty": "beginner",
        "extra_flags": {
            "limit": "Rate limit connections to a port (6 connections in 30 seconds)",
            "logging": "Set logging level (off, low, medium, high, full)",
            "status numbered": "Show rules with numbers for easy deletion",
        },
    },

    "firewall-cmd": {
        "man_url": "https://firewalld.org/documentation/man-pages/firewall-cmd.html",
        "use_cases": [
            "Open HTTP permanently: firewall-cmd --add-service=http --permanent && firewall-cmd --reload",
            "List all allowed services and ports: firewall-cmd --list-all",
            "Temporarily open a port for testing (removed on reload): firewall-cmd --add-port=8080/tcp",
            "Add a rich rule for IP-based access control: firewall-cmd --add-rich-rule='rule family=ipv4 source address=10.0.0.0/24 accept' --permanent",
        ],
        "gotchas": [
            "Changes without --permanent are lost on firewalld restart or reload",
            "After adding --permanent rules, you must --reload for them to take effect immediately",
            "firewall-cmd is specific to RHEL/CentOS/Fedora; Debian/Ubuntu systems use ufw instead",
        ],
        "related": ["iptables", "ufw", "nft"],
        "difficulty": "intermediate",
        "extra_flags": {
            "--get-active-zones": "Show which zones are active and their interfaces",
            "--get-default-zone": "Show the default zone",
            "--set-default-zone": "Change the default zone",
            "--add-rich-rule": "Add a complex rule with source/destination filtering",
        },
    },

    "tcpdump": {
        "man_url": "https://man7.org/linux/man-pages/man8/tcpdump.8.html",
        "use_cases": [
            "Capture HTTP traffic on all interfaces: tcpdump -i any port 80 -A",
            "Save a capture for later analysis in Wireshark: tcpdump -i eth0 -w capture.pcap",
            "Debug DNS resolution issues: tcpdump -i any port 53 -n",
            "Monitor traffic to/from a specific host: tcpdump -i any host 10.0.0.5 -n",
            "Capture only SYN packets to see new connections: tcpdump 'tcp[tcpflags] & tcp-syn != 0'",
        ],
        "gotchas": [
            "tcpdump requires root privileges for packet capture",
            "Capturing on a busy interface without filters generates enormous output -- always use BPF filters to narrow scope",
            "On a server with many connections, -n (no name resolution) is essential to avoid slow output caused by reverse DNS lookups",
            "The -c flag is important in scripts to avoid capturing indefinitely",
        ],
        "related": ["wireshark", "nmap", "ss", "iptables"],
        "difficulty": "advanced",
        "extra_flags": {
            "-s": "Set the snapshot length (bytes to capture per packet; 0 = full packet)",
            "-e": "Print link-layer (MAC) headers",
            "-D": "List available network interfaces for capture",
            "-l": "Line-buffer stdout for real-time piping to grep",
            "-G": "Rotate capture file every N seconds",
        },
    },

    "wireshark": {
        "man_url": "https://www.wireshark.org/docs/man-pages/wireshark.html",
        "use_cases": [
            "Analyze a pcap file captured with tcpdump to visually inspect protocol conversations",
            "Debug TLS handshake failures by examining the Certificate and ServerHello messages",
            "Filter and follow a specific TCP stream to reconstruct an HTTP conversation",
            "Identify network performance issues using the IO graphs and expert information features",
        ],
        "gotchas": [
            "Wireshark's GUI requires a display server (X11/Wayland); use tshark for CLI-based analysis on headless servers",
            "Capturing on a busy network generates massive pcap files quickly -- use capture filters (BPF) to reduce volume",
            "Display filters (applied after capture) use different syntax from capture filters (BPF syntax applied during capture)",
        ],
        "related": ["tcpdump", "nmap", "ss"],
        "difficulty": "advanced",
        "extra_flags": {
            "-T": "Set output format for tshark (fields, json, pdml)",
        },
    },

    "nmap": {
        "man_url": "https://nmap.org/book/man.html",
        "use_cases": [
            "Scan a subnet to discover live hosts: nmap -sn 192.168.1.0/24",
            "Full port scan with service version detection: nmap -sV -p- host",
            "Check if a specific port is open: nmap -p 443 host",
            "Detect the operating system of a remote host: nmap -O host",
            "Run vulnerability scanning scripts: nmap --script vuln host",
        ],
        "gotchas": [
            "Port scanning networks you do not own or have permission to scan is illegal in many jurisdictions",
            "A full port scan (-p-) of 65535 ports is slow; SYN scan (-sS) is faster but requires root",
            "Aggressive scans (-A) are noisy and easily detected by intrusion detection systems",
            "nmap's default scan only covers the top 1000 ports, not all 65535",
        ],
        "related": ["masscan", "nc", "ss", "tcpdump"],
        "difficulty": "advanced",
        "extra_flags": {
            "-sn": "Ping scan only (host discovery, no port scan)",
            "-sU": "UDP port scan (much slower than TCP)",
            "--script": "Run NSE scripts for vulnerability detection",
            "-T": "Set timing template (0-5, higher is faster/noisier)",
            "-oA": "Output in all formats (normal, XML, grepable)",
        },
    },

    "masscan": {
        "man_url": "https://github.com/robertdavidgraham/masscan",
        "use_cases": [
            "Rapidly scan a large IP range for specific open ports: masscan 10.0.0.0/8 -p80,443 --rate=50000",
            "Discover all web servers on a /16 network in minutes",
            "Feed masscan results into nmap for detailed follow-up scanning of discovered hosts",
        ],
        "gotchas": [
            "High scan rates can overwhelm networks, trigger IDS alerts, and crash fragile devices -- start with conservative rates",
            "masscan uses its own TCP stack and does not go through the OS, so firewall rules on the scanning host are bypassed",
            "Results are less accurate than nmap for individual hosts due to the asynchronous scanning approach",
            "Requires root for raw socket access",
        ],
        "related": ["nmap", "nc", "tcpdump"],
        "difficulty": "advanced",
        "extra_flags": {},
    },

    "nikto": {
        "man_url": "https://github.com/sullo/nikto/wiki",
        "use_cases": [
            "Quick web server security audit: nikto -h http://target.com",
            "Scan an HTTPS site: nikto -h target.com -p 443 -ssl",
            "Generate an HTML report for a security assessment: nikto -h target -o report.html -Format htm",
        ],
        "gotchas": [
            "Nikto is extremely noisy and generates hundreds of requests -- it will be detected by any WAF or IDS",
            "Only scan systems you have explicit authorization to test",
            "Nikto checks for known vulnerabilities and misconfigurations; it does not find custom application bugs",
            "Results include many false positives; manual verification is always required",
        ],
        "related": ["nmap", "curl", "openssl"],
        "difficulty": "advanced",
        "extra_flags": {},
    },

    "whois": {
        "man_url": "https://man7.org/linux/man-pages/man1/whois.1.html",
        "use_cases": [
            "Find out who owns a domain: whois example.com",
            "Check domain expiration date before it lapses",
            "Look up the organization responsible for an IP address: whois 8.8.8.8",
            "Determine the registrar and nameservers for a domain",
        ],
        "gotchas": [
            "Many domain registrars now use privacy protection services that hide the real owner information",
            "WHOIS rate limiting may block you if you run too many queries in succession",
            "The output format varies significantly between different TLD registries",
        ],
        "related": ["dig", "nslookup", "host"],
        "difficulty": "beginner",
        "extra_flags": {},
    },

    "openssl": {
        "man_url": "https://www.openssl.org/docs/man3.0/man1/",
        "use_cases": [
            "Test an HTTPS connection and view the certificate chain: openssl s_client -connect host:443",
            "Generate a self-signed certificate for development: openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes",
            "Check certificate expiration: openssl x509 -in cert.pem -noout -enddate",
            "Create a CSR for a production certificate: openssl req -new -key server.key -out server.csr",
            "Generate a random password: openssl rand -base64 32",
        ],
        "gotchas": [
            "The -nodes flag means 'no DES encryption' on the private key, not 'no des' -- it stores the key unencrypted which is a security risk in production",
            "openssl s_client does not verify certificates by default; add -verify_return_error to catch invalid certs",
            "OpenSSL 1.x and 3.x have different default behaviors and deprecated algorithms; check your version with openssl version",
        ],
        "related": ["certbot", "ssh", "curl"],
        "difficulty": "advanced",
        "extra_flags": {
            "rand": "Generate random bytes",
            "speed": "Benchmark cryptographic algorithms",
            "verify": "Verify a certificate chain",
            "pkcs12": "Convert between PFX/PKCS12 and PEM formats",
        },
    },

    "certbot": {
        "man_url": "https://certbot.eff.org/docs/",
        "use_cases": [
            "Get a free HTTPS certificate for Nginx: certbot --nginx -d example.com -d www.example.com",
            "Obtain a certificate without modifying your web server: certbot certonly --standalone -d example.com",
            "Set up automatic certificate renewal: certbot renew (usually in a cron job or systemd timer)",
            "Test the renewal process without actually renewing: certbot renew --dry-run",
        ],
        "gotchas": [
            "Certbot needs port 80 (HTTP) or 443 (HTTPS) accessible from the internet for domain validation",
            "Let's Encrypt certificates are only valid for 90 days -- automated renewal is essential",
            "Rate limits apply: 50 certificates per registered domain per week; use --staging for testing",
            "The standalone mode requires stopping your web server temporarily; use --webroot or --nginx/--apache to avoid downtime",
        ],
        "related": ["openssl", "nginx", "apache"],
        "difficulty": "intermediate",
        "extra_flags": {
            "--agree-tos": "Agree to the terms of service non-interactively",
            "--email": "Set the registration email for expiry notifications",
            "--non-interactive": "Run without any user interaction",
            "certificates": "List all managed certificates and their expiry dates",
            "revoke": "Revoke a certificate",
        },
    },

    "http": {
        "man_url": "https://httpie.io/docs/cli",
        "use_cases": [
            "Quick API testing with readable output: http GET https://api.example.com/users",
            "POST JSON data intuitively: http POST api.example.com/items name=widget price:=9.99",
            "Download a file: http --download https://example.com/file.zip",
            "Debug HTTP by printing full request and response: http --print=HhBb example.com",
        ],
        "gotchas": [
            "HTTPie uses 'http' as the command name, which can conflict with other tools; the package name is 'httpie'",
            "The := syntax sends raw JSON values (numbers, booleans); = sends strings -- mixing them up causes type errors in APIs",
            "HTTPie follows redirects by default (unlike curl), which may hide redirect issues during debugging",
        ],
        "related": ["curl", "wget"],
        "difficulty": "beginner",
        "extra_flags": {
            "--download": "Download the response body to a file",
            "--session": "Create or reuse a named session with persistent headers/cookies",
            "--timeout": "Set the request timeout in seconds",
        },
    },

    "httpie": {
        "man_url": "https://httpie.io/docs/cli",
        "use_cases": [
            "Test REST APIs with human-friendly output formatting and syntax highlighting",
            "Submit forms: http --form POST example.com/login username=admin password=secret",
            "Send authenticated requests: http --auth user:pass GET api.example.com/data",
        ],
        "gotchas": [
            "httpie is the package name; the actual command is 'http' (or 'https' for HTTPS)",
            "HTTPie 3.x changed some defaults from 2.x; check the changelog when upgrading",
        ],
        "related": ["curl", "wget", "http"],
        "difficulty": "beginner",
        "extra_flags": {},
    },

    "ping": {
        "man_url": "https://man7.org/linux/man-pages/man8/ping.8.html",
        "use_cases": [
            "Test basic network connectivity to a host: ping -c 4 google.com",
            "Continuously monitor a connection with timestamps: ping -D host",
            "Test with a specific packet size to check MTU issues: ping -s 1472 host",
            "Quick check if a host is alive in a script: ping -c 1 -W 2 host > /dev/null 2>&1 && echo up",
        ],
        "gotchas": [
            "Many hosts and firewalls block ICMP, so a failed ping does not necessarily mean the host is down -- the service may still be reachable",
            "On Linux, ping runs indefinitely by default; always use -c to limit count in scripts",
            "Flood ping (-f) requires root and can saturate a network link -- use with extreme caution",
            "ping results show round-trip time, not one-way latency; actual one-way delay is roughly half the RTT",
        ],
        "related": ["traceroute", "mtr", "arping"],
        "difficulty": "beginner",
        "extra_flags": {
            "-w": "Deadline timeout: exit after N seconds regardless of packet count",
            "-W": "Timeout waiting for each response in seconds",
            "-s": "Set packet data size in bytes (default 56)",
            "-t": "Set the IP time-to-live",
            "-I": "Specify source interface or address",
            "-f": "Flood ping (requires root, use carefully)",
            "-q": "Quiet output; only show summary at the end",
            "-D": "Print timestamps before each line",
        },
    },

    "scp": {
        "man_url": "https://man.openbsd.org/scp",
        "use_cases": [
            "Copy a file to a remote server: scp file.txt user@host:/remote/path/",
            "Copy a directory recursively: scp -r project/ user@host:/deploy/",
            "Copy between two remote hosts through your local machine: scp user1@host1:file user2@host2:/path/",
            "Use a specific SSH key: scp -i ~/.ssh/deploy_key file.txt user@host:/path/",
        ],
        "gotchas": [
            "scp is considered deprecated by OpenSSH in favor of sftp or rsync -- it has known limitations with filename handling",
            "scp copies the entire file every time; rsync only transfers differences and is much faster for repeated transfers",
            "The -P flag (uppercase) specifies the port, unlike ssh which uses -p (lowercase)",
            "Wildcards in remote paths must be quoted to prevent local shell expansion: scp 'user@host:/path/*.log' .",
        ],
        "related": ["sftp", "rsync", "ssh"],
        "difficulty": "beginner",
        "extra_flags": {
            "-C": "Enable compression during transfer",
            "-l": "Limit bandwidth in Kbit/s",
            "-3": "Copy between two remote hosts through the local machine",
            "-o": "Pass SSH options (e.g., -o StrictHostKeyChecking=no)",
        },
    },

    "sftp": {
        "man_url": "https://man.openbsd.org/sftp",
        "use_cases": [
            "Interactive file transfer session with a remote server: sftp user@host",
            "Batch transfer files from a script: sftp -b commands.txt user@host",
            "Resume interrupted directory uploads with a combination of get -r / put -r",
            "Browse remote files interactively when you are unsure of the exact path",
        ],
        "gotchas": [
            "sftp is not FTP over SSL; it is a completely different protocol that runs over SSH",
            "The -P flag (uppercase) sets the port, matching scp but different from ssh's lowercase -p",
            "Tab completion works in interactive mode but may be slow on high-latency connections",
        ],
        "related": ["scp", "rsync", "ssh", "ftp"],
        "difficulty": "beginner",
        "extra_flags": {
            "-C": "Enable compression",
            "-l": "Limit bandwidth in Kbit/s",
            "-o": "Pass SSH options",
        },
    },

    # =========================================================================
    # PROCESS & SYSTEM COMMANDS
    # =========================================================================

    "top": {
        "man_url": "https://man7.org/linux/man-pages/man1/top.1.html",
        "use_cases": [
            "Monitor CPU and memory usage in real time to find resource-hungry processes",
            "Find the process consuming the most CPU: run top then press P to sort by CPU",
            "Script batch monitoring: top -b -n 1 | head -20 for a snapshot",
            "Filter to a specific user's processes: top -u www-data",
        ],
        "gotchas": [
            "The %CPU column in top shows per-core percentage, so a multithreaded process can show over 100%",
            "Memory readings can be confusing: 'used' includes buffer/cache; check 'avail' for actual available memory",
            "top's interactive keys (P, M, T for sorting, k for kill, 1 for per-CPU) are essential but undiscoverable without reading help (press h)",
        ],
        "related": ["htop", "btop", "ps", "kill"],
        "difficulty": "beginner",
        "extra_flags": {
            "-d": "Set refresh interval in seconds",
            "-p": "Monitor only specific PIDs",
            "-H": "Show individual threads",
            "-c": "Show full command line instead of just the command name",
            "-o": "Sort by a specific field",
        },
    },

    "htop": {
        "man_url": "https://man7.org/linux/man-pages/man1/htop.1.html",
        "use_cases": [
            "Interactively browse and kill processes with a user-friendly color interface",
            "View per-CPU core utilization bars to identify single-threaded bottlenecks",
            "Filter processes by name with / and search incrementally",
            "Show a process tree with F5 to understand parent-child relationships",
        ],
        "gotchas": [
            "htop is not installed by default on most systems; you need to install it from your package manager",
            "htop shows threads by default (unlike top), which can make the process count seem much higher than expected; press H to toggle",
            "Memory bars include shared memory which can overcount total usage when summing process memory",
        ],
        "related": ["top", "btop", "atop", "ps"],
        "difficulty": "beginner",
        "extra_flags": {
            "-d": "Set refresh delay in tenths of seconds",
            "-p": "Monitor specific PIDs only",
            "-s": "Sort by the specified column",
            "-C": "Use monochrome mode",
        },
    },

    "btop": {
        "man_url": "https://github.com/aristocratos/btop",
        "use_cases": [
            "Monitor system resources with a polished dashboard showing CPU, memory, disk, and network simultaneously",
            "Use process tree view to understand hierarchical process relationships",
            "Quick visual triage of system performance issues with color-coded resource graphs",
        ],
        "gotchas": [
            "btop requires a terminal with true color and UTF-8 support; use -lc flag on limited terminals",
            "btop is newer and less commonly available in default repos than htop; may need manual installation",
        ],
        "related": ["htop", "top", "atop"],
        "difficulty": "beginner",
        "extra_flags": {},
    },

    "atop": {
        "man_url": "https://man7.org/linux/man-pages/man1/atop.1.html",
        "use_cases": [
            "Investigate past performance issues by replaying historical logs: atop -r /var/log/atop/atop_20240115",
            "Identify the process that caused a CPU spike last night by scrubbing through recorded data",
            "Monitor disk I/O per process to find which application is thrashing storage",
        ],
        "gotchas": [
            "atop writes to /var/log/atop by default; these log files can grow large and should be rotated",
            "The atop daemon must be running to record historical data; install and enable the atop service",
            "Use t and T keys to navigate forward/backward through time intervals when replaying logs",
        ],
        "related": ["top", "htop", "sar", "iostat"],
        "difficulty": "intermediate",
        "extra_flags": {},
    },

    "kill": {
        "man_url": "https://man7.org/linux/man-pages/man1/kill.1.html",
        "use_cases": [
            "Gracefully stop a process with kill PID which sends SIGTERM and allows cleanup",
            "Force-kill an unresponsive process with kill -9 PID when SIGTERM is ignored",
            "Send a reload signal to a daemon with kill -HUP PID to reload configuration without restarting",
            "Stop a process group: kill -TERM -PGID (negative PID targets the group)",
        ],
        "gotchas": [
            "kill -9 should be a last resort because it prevents the process from cleaning up resources like temp files, database connections, and lock files",
            "kill requires the PID, not the process name -- use pkill or killall to signal processes by name instead",
            "Zombie processes cannot be killed because they are already dead; you need to kill or fix their parent process",
            "Sending signals to PID 1 (init/systemd) has special behavior and should be avoided",
        ],
        "related": ["pkill", "killall", "ps", "pgrep"],
        "difficulty": "beginner",
        "extra_flags": {
            "-L": "List signals in a table format with numbers",
            "-s": "Specify signal by name (e.g., -s TERM)",
            "--timeout": "Send follow-up signal after specified milliseconds if process survives",
        },
    },

    "killall": {
        "man_url": "https://man7.org/linux/man-pages/man1/killall.1.html",
        "use_cases": [
            "Kill all instances of a process by name: killall firefox",
            "Gracefully stop all node processes: killall -TERM node",
            "Force-kill all hung instances: killall -9 frozen-app",
        ],
        "gotchas": [
            "On Solaris, killall kills ALL processes (not by name) -- this Linux-specific behavior does not transfer to other Unix systems",
            "killall requires an exact process name match; use pkill -f for partial or command-line matching",
            "Without -i, killall provides no confirmation before killing multiple matching processes",
        ],
        "related": ["kill", "pkill", "pgrep", "ps"],
        "difficulty": "beginner",
        "extra_flags": {
            "-e": "Require exact match of very long names (over 15 characters)",
            "-u": "Kill only processes owned by the specified user",
            "-w": "Wait for all killed processes to die before returning",
            "-r": "Interpret process name as an extended regular expression",
        },
    },

    "pkill": {
        "man_url": "https://man7.org/linux/man-pages/man1/pkill.1.html",
        "use_cases": [
            "Kill all processes matching a pattern: pkill -f 'node server.js'",
            "Signal all processes of a specific user: pkill -u baduser",
            "Send SIGHUP to reload all nginx workers: pkill -HUP nginx",
        ],
        "gotchas": [
            "Without -f, pkill only matches against the process name (first 15 chars), not the full command line",
            "pkill matches with regex, so special characters in patterns need escaping",
            "pkill returns exit code 1 if no processes matched, which can cause script failures with set -e",
        ],
        "related": ["pgrep", "kill", "killall", "ps"],
        "difficulty": "beginner",
        "extra_flags": {
            "-x": "Require an exact match of the process name",
            "-u": "Match only processes running as the specified user",
            "-t": "Match only processes on the specified terminal",
            "-P": "Match only processes whose parent PID matches",
            "-o": "Select only the oldest (longest-running) matching process",
            "-n": "Select only the newest (most recently started) matching process",
        },
    },

    "pgrep": {
        "man_url": "https://man7.org/linux/man-pages/man1/pgrep.1.html",
        "use_cases": [
            "Find PIDs of all python processes: pgrep python",
            "Check if a specific service is running: pgrep -x nginx && echo running",
            "List processes with their names: pgrep -la node",
            "Find processes belonging to a user: pgrep -u www-data",
        ],
        "gotchas": [
            "pgrep returns exit code 1 when no match is found, which is useful for conditionals but can break set -e scripts",
            "Without -f, pgrep only matches the first 15 characters of the process name",
            "pgrep may match itself if your grep pattern appears in the pgrep command line; -x for exact match helps",
        ],
        "related": ["pkill", "ps", "kill"],
        "difficulty": "beginner",
        "extra_flags": {
            "-a": "List PID and full command line of matching processes",
            "-c": "Count matching processes instead of listing PIDs",
            "-d": "Set the delimiter between PIDs (default newline)",
        },
    },

    "nice": {
        "man_url": "https://man7.org/linux/man-pages/man1/nice.1.html",
        "use_cases": [
            "Run a CPU-intensive build at low priority: nice -n 19 make -j8",
            "Start a backup job without impacting interactive users: nice -n 15 rsync -a /data /backup",
            "Run a high-priority system task (requires root): sudo nice -n -10 critical-task",
        ],
        "gotchas": [
            "Only root can set negative nice values (higher priority); regular users can only lower their priority",
            "Nice values range from -20 (highest priority) to 19 (lowest); the default adjustment is 10",
            "nice affects CPU scheduling priority only, not I/O priority -- use ionice for disk I/O scheduling",
        ],
        "related": ["renice", "ionice", "cpulimit"],
        "difficulty": "intermediate",
        "extra_flags": {},
    },

    "renice": {
        "man_url": "https://man7.org/linux/man-pages/man1/renice.1.html",
        "use_cases": [
            "Lower the priority of a runaway process: renice -n 19 -p 1234",
            "Reprioritize all processes by a specific user: renice -n 10 -u batchuser",
            "Increase priority of a critical running process (root only): sudo renice -n -5 -p 5678",
        ],
        "gotchas": [
            "Regular users can only increase nice values (lower priority), never decrease them",
            "renice changes the priority of already-running processes; use nice to start new processes at a given priority",
        ],
        "related": ["nice", "kill", "top"],
        "difficulty": "intermediate",
        "extra_flags": {},
    },

    "nohup": {
        "man_url": "https://man7.org/linux/man-pages/man1/nohup.1.html",
        "use_cases": [
            "Start a long-running training job that survives SSH disconnection: nohup python train.py > train.log 2>&1 &",
            "Run a server process that persists after logout: nohup ./server &",
            "Launch a batch job on a remote machine before disconnecting: nohup ./process_data.sh &",
        ],
        "gotchas": [
            "nohup appends output to nohup.out by default, which can grow very large; always redirect stdout/stderr explicitly",
            "nohup only ignores SIGHUP; combining with & is required to actually background the process",
            "For interactive or complex scenarios, tmux/screen are better choices than nohup because you can reattach",
        ],
        "related": ["disown", "screen", "tmux", "bg"],
        "difficulty": "beginner",
        "extra_flags": {},
    },

    "bg": {
        "man_url": "https://www.gnu.org/software/bash/manual/html_node/Job-Control-Builtins.html",
        "use_cases": [
            "Resume a suspended job in the background after pressing Ctrl+Z: bg %1",
            "Continue working in your terminal after accidentally starting a long command in the foreground",
        ],
        "gotchas": [
            "bg is a shell builtin and only works with jobs managed by the current shell session",
            "A backgrounded job that tries to read from the terminal will be stopped again with SIGTTIN",
            "bg without arguments resumes the most recently suspended job",
        ],
        "related": ["fg", "jobs", "disown", "nohup"],
        "difficulty": "beginner",
        "extra_flags": {},
    },

    "fg": {
        "man_url": "https://www.gnu.org/software/bash/manual/html_node/Job-Control-Builtins.html",
        "use_cases": [
            "Bring a background process back to the foreground to interact with it: fg %1",
            "Return to a suspended editor session after checking something in the shell",
        ],
        "gotchas": [
            "fg without arguments brings the most recently backgrounded/suspended job to the foreground",
            "If the job has already exited, fg will report an error",
        ],
        "related": ["bg", "jobs", "disown"],
        "difficulty": "beginner",
        "extra_flags": {},
    },

    "jobs": {
        "man_url": "https://www.gnu.org/software/bash/manual/html_node/Job-Control-Builtins.html",
        "use_cases": [
            "List all background and suspended jobs in the current shell: jobs -l",
            "Check if background processes are still running before logging out",
            "Get the PID of a backgrounded job for use with kill: jobs -p",
        ],
        "gotchas": [
            "jobs only shows processes started from the current shell session; it cannot see processes from other terminals",
            "Job numbers (%1, %2) are different from PIDs and are local to the shell session",
        ],
        "related": ["bg", "fg", "disown", "ps"],
        "difficulty": "beginner",
        "extra_flags": {},
    },

    "disown": {
        "man_url": "https://www.gnu.org/software/bash/manual/html_node/Job-Control-Builtins.html",
        "use_cases": [
            "Detach a running background job from the shell so it survives logout: disown %1",
            "Retroactively make a process immune to SIGHUP when you forgot to use nohup",
            "Remove all jobs from the shell's job table before logging out: disown -a",
        ],
        "gotchas": [
            "After disown, you can no longer use fg/bg/jobs to manage the process -- you must use kill with the PID directly",
            "disown only removes the job from the shell's table; it does not redirect output, so the process may still fail if it writes to the closed terminal",
            "disown -h keeps the job in the table but prevents SIGHUP, which is a safer option if you still want to track it",
        ],
        "related": ["nohup", "bg", "fg", "jobs", "screen", "tmux"],
        "difficulty": "intermediate",
        "extra_flags": {},
    },

    "screen": {
        "man_url": "https://man7.org/linux/man-pages/man1/screen.1.html",
        "use_cases": [
            "Keep a long-running process alive after SSH disconnection: screen -S build, run command, then Ctrl-a d to detach",
            "Reattach to a running session after reconnecting: screen -r build",
            "Share a terminal session with another user for pair debugging: screen -x",
        ],
        "gotchas": [
            "screen uses Ctrl-a as its prefix key, which conflicts with the bash shortcut to go to the beginning of the line",
            "Dead sessions (marked as 'dead') must be wiped with screen -wipe before the name can be reused",
            "screen is being superseded by tmux, which has a more scriptable interface and better pane management",
        ],
        "related": ["tmux", "byobu", "nohup", "disown"],
        "difficulty": "intermediate",
        "extra_flags": {
            "-dm": "Start session in detached mode (useful in scripts)",
            "-X": "Send a command to a running session (e.g., screen -S name -X stuff 'command\\n')",
        },
    },

    "tmux": {
        "man_url": "https://man7.org/linux/man-pages/man1/tmux.1.html",
        "use_cases": [
            "Keep long-running processes alive after SSH disconnection: tmux new -s work",
            "Split terminal into multiple panes for monitoring: Ctrl-b % (vertical) and Ctrl-b \" (horizontal)",
            "Share a terminal session with a colleague: tmux new -s pair, then they run tmux attach -t pair",
            "Script complex window layouts for development environments: tmux new-session -d, then send-keys commands",
            "Run multiple parallel tasks visible in one terminal: create panes for logs, servers, and a shell",
        ],
        "gotchas": [
            "tmux uses Ctrl-b as prefix by default (screen uses Ctrl-a) -- muscle memory conflicts are common when switching",
            "The tmux scrollback buffer requires entering copy mode (Ctrl-b [) to scroll; mouse wheel alone does not work without mouse mode enabled",
            "Nested tmux sessions (tmux inside tmux) require pressing the prefix twice to reach the inner session",
            "tmux uses a client-server model; killing the server (tmux kill-server) destroys all sessions",
        ],
        "related": ["screen", "byobu", "nohup", "disown"],
        "difficulty": "intermediate",
        "extra_flags": {
            "new-window": "Create a new window in the current session",
            "split-window": "Split the current pane horizontally or vertically",
            "send-keys": "Send keystrokes to a pane (useful for scripting)",
            "resize-pane": "Resize a pane by a specified number of cells",
            "source-file": "Load tmux configuration from a file",
        },
    },

    "byobu": {
        "man_url": "https://www.byobu.org/documentation",
        "use_cases": [
            "Get a pre-configured tmux experience with status bar and keybindings out of the box",
            "Use function keys (F2 for new window, F3/F4 to switch) instead of memorizing tmux prefix commands",
        ],
        "gotchas": [
            "byobu wraps either tmux or screen depending on configuration; check which backend is active with byobu-select-backend",
            "Function key bindings may conflict with your terminal emulator's shortcuts",
        ],
        "related": ["tmux", "screen"],
        "difficulty": "beginner",
        "extra_flags": {},
    },

    "systemctl": {
        "man_url": "https://man7.org/linux/man-pages/man1/systemctl.1.html",
        "use_cases": [
            "Start and enable a service in one command: systemctl enable --now nginx",
            "Check why a service failed: systemctl status nginx (shows recent logs inline)",
            "List all running services: systemctl list-units --type=service --state=running",
            "Reload service configuration without restarting: systemctl reload nginx",
            "Mask a service to prevent it from starting even manually: systemctl mask dangerous-service",
        ],
        "gotchas": [
            "enable does not start the service; it only configures it to start at boot. Use enable --now to do both",
            "daemon-reload is required after editing a .service unit file before restarting the service",
            "systemctl without arguments lists all loaded units, which can be overwhelming; use --type and --state filters",
            "A masked service cannot be started until unmasked; this is stronger than disable",
        ],
        "related": ["journalctl", "service", "init"],
        "difficulty": "intermediate",
        "extra_flags": {
            "reload": "Reload service configuration without full restart",
            "mask": "Completely prevent a service from being started",
            "unmask": "Remove the mask from a service",
            "is-active": "Check if a service is running (useful in scripts)",
            "is-enabled": "Check if a service is enabled at boot",
            "show": "Show properties of a unit for debugging",
            "--failed": "List only failed units",
            "edit": "Edit or create a unit file override",
        },
    },

    "service": {
        "man_url": "https://man7.org/linux/man-pages/man8/service.8.html",
        "use_cases": [
            "Restart a service on any Linux system (works with both SysVinit and systemd): service nginx restart",
            "Check the status of all services at once: service --status-all",
        ],
        "gotchas": [
            "On systemd systems, service is a compatibility wrapper that redirects to systemctl -- use systemctl directly for full functionality",
            "service --status-all output uses +/- symbols that may not show the full picture on systemd systems",
        ],
        "related": ["systemctl", "init"],
        "difficulty": "beginner",
        "extra_flags": {},
    },

    "journalctl": {
        "man_url": "https://man7.org/linux/man-pages/man1/journalctl.1.html",
        "use_cases": [
            "Follow logs for a specific service in real time: journalctl -u nginx -f",
            "View logs since the last boot: journalctl -b",
            "Find errors from the past hour: journalctl --since '1 hour ago' -p err",
            "Show the last 50 lines of a service log: journalctl -u postgresql -n 50",
            "Export logs in JSON for analysis: journalctl -u myapp -o json --since today",
        ],
        "gotchas": [
            "The journal can consume significant disk space; configure SystemMaxUse in journald.conf to limit it",
            "Without -u, journalctl shows logs from all units, which is noisy; always filter",
            "Timestamps use the system timezone by default; use --utc for UTC output",
            "Regular users may not see all logs; add yourself to the 'systemd-journal' group or use sudo",
        ],
        "related": ["systemctl", "dmesg", "syslog"],
        "difficulty": "intermediate",
        "extra_flags": {
            "-o": "Set output format (short, verbose, json, cat)",
            "--disk-usage": "Show how much disk space the journal uses",
            "--vacuum-size": "Reduce journal disk usage to specified size",
            "--vacuum-time": "Remove entries older than specified time",
            "-k": "Show only kernel messages (like dmesg)",
            "-r": "Show newest entries first (reverse chronological)",
        },
    },

    "dmesg": {
        "man_url": "https://man7.org/linux/man-pages/man1/dmesg.1.html",
        "use_cases": [
            "Check for hardware issues after plugging in a USB device: dmesg -T | tail -20",
            "Diagnose boot problems by reviewing kernel messages: dmesg | less",
            "Watch for new kernel messages in real time: dmesg -T -w",
            "Filter for error-level messages only: dmesg -l err,crit,alert,emerg",
        ],
        "gotchas": [
            "dmesg timestamps are relative to boot by default; use -T for human-readable wall-clock times (note: -T can be inaccurate after suspend/resume)",
            "On newer systems, dmesg may require root or membership in specific groups to read kernel messages",
            "The kernel ring buffer has a fixed size; old messages are overwritten by new ones on busy systems",
        ],
        "related": ["journalctl", "syslog"],
        "difficulty": "intermediate",
        "extra_flags": {},
    },

    "uptime": {
        "man_url": "https://man7.org/linux/man-pages/man1/uptime.1.html",
        "use_cases": [
            "Quick system health check: uptime shows load averages, user count, and time since last boot",
            "Check load averages to determine if a system is overloaded (compare to CPU count)",
        ],
        "gotchas": [
            "Load average numbers greater than your CPU count indicate the system is overloaded with waiting processes",
            "On Linux, load averages include processes waiting for I/O (D state), not just CPU -- so high load does not always mean high CPU usage",
        ],
        "related": ["w", "top", "free"],
        "difficulty": "beginner",
        "extra_flags": {},
    },

    "free": {
        "man_url": "https://man7.org/linux/man-pages/man1/free.1.html",
        "use_cases": [
            "Check available memory: free -h (the 'available' column is what matters)",
            "Monitor memory usage over time: free -h -s 5 (refresh every 5 seconds)",
            "Quickly check swap usage to detect memory pressure",
        ],
        "gotchas": [
            "The 'used' column includes buffer/cache which Linux reclaims on demand -- look at 'available' for actual free memory",
            "High swap usage combined with constant swap activity (check with vmstat) indicates real memory pressure",
            "free shows a snapshot; for historical data use sar -r",
        ],
        "related": ["vmstat", "top", "sar"],
        "difficulty": "beginner",
        "extra_flags": {},
    },

    "vmstat": {
        "man_url": "https://man7.org/linux/man-pages/man8/vmstat.8.html",
        "use_cases": [
            "Quick overview of system performance: vmstat 1 (updates every second)",
            "Check if system is CPU-bound (high us/sy), I/O-bound (high wa), or memory-bound (high si/so swap activity)",
            "Monitor context switches and interrupts: vmstat 1 and watch the cs and in columns",
        ],
        "gotchas": [
            "The first line of vmstat output shows averages since boot, not the current state; ignore it and look at subsequent lines",
            "The si/so columns show swap in/out; consistently non-zero values indicate memory pressure",
            "vmstat's compact format takes practice to read; w flag provides wider, easier-to-read output",
        ],
        "related": ["free", "iostat", "mpstat", "sar"],
        "difficulty": "intermediate",
        "extra_flags": {},
    },

    "iostat": {
        "man_url": "https://man7.org/linux/man-pages/man1/iostat.1.html",
        "use_cases": [
            "Identify disk bottlenecks: iostat -x 1 (watch the %util and await columns)",
            "Monitor disk throughput in human-readable format: iostat -h 1",
            "Determine if slow performance is disk-related by checking average wait times",
        ],
        "gotchas": [
            "iostat is part of the sysstat package and may not be installed by default",
            "Like vmstat, the first report shows averages since boot; subsequent reports show current intervals",
            "%util at 100% does not always mean the disk is saturated (especially for SSDs and RAID arrays that handle concurrent I/O)",
        ],
        "related": ["vmstat", "sar", "iotop"],
        "difficulty": "intermediate",
        "extra_flags": {},
    },

    "mpstat": {
        "man_url": "https://man7.org/linux/man-pages/man1/mpstat.1.html",
        "use_cases": [
            "Check per-CPU utilization to find single-threaded bottlenecks: mpstat -P ALL 1",
            "Identify if workload is evenly distributed across cores",
            "Monitor interrupt distribution: mpstat -I ALL 1",
        ],
        "gotchas": [
            "mpstat is part of the sysstat package and may not be installed by default",
            "If one CPU is at 100% while others are idle, the application likely has a single-threaded bottleneck",
        ],
        "related": ["vmstat", "iostat", "sar", "top"],
        "difficulty": "intermediate",
        "extra_flags": {},
    },

    "sar": {
        "man_url": "https://man7.org/linux/man-pages/man1/sar.1.html",
        "use_cases": [
            "Review CPU usage from yesterday: sar -u -f /var/log/sa/sa$(date -d yesterday +%d)",
            "Check historical memory usage: sar -r",
            "Monitor network throughput: sar -n DEV 1 5",
            "Investigate a performance incident that happened at 3am: sar -u -s 03:00:00 -e 04:00:00",
        ],
        "gotchas": [
            "sar requires the sysstat package and its data collection service (sadc) must be enabled",
            "Data files are stored in /var/log/sa/ and rotate monthly; older data may be overwritten",
            "sar collects data at 10-minute intervals by default; for finer granularity, adjust the cron job",
        ],
        "related": ["vmstat", "iostat", "mpstat", "atop"],
        "difficulty": "advanced",
        "extra_flags": {},
    },

    "lsof": {
        "man_url": "https://man7.org/linux/man-pages/man8/lsof.8.html",
        "use_cases": [
            "Find which process is using port 8080: lsof -i :8080",
            "List all network connections with process info: lsof -i -P -n",
            "Find all open files in a directory (why can't I unmount?): lsof +D /mnt/usb",
            "Get the PID of the process holding a file for scripting: lsof -t /path/to/file",
            "Find all files opened by a specific user: lsof -u www-data",
        ],
        "gotchas": [
            "lsof can be slow on systems with many open files; use specific filters (-i, -p, -u) rather than listing everything",
            "The -P flag prevents port number-to-name conversion, and -n prevents IP-to-hostname conversion; both speed up output significantly",
            "lsof requires root to see files opened by other users' processes",
            "Multiple selection flags are ORed by default; use -a to AND them together",
        ],
        "related": ["fuser", "ss", "netstat", "ps"],
        "difficulty": "intermediate",
        "extra_flags": {
            "-a": "AND selection criteria together (default is OR)",
            "-n": "Do not resolve IP addresses to hostnames",
            "-P": "Do not resolve port numbers to service names",
            "-r": "Repeat the listing every N seconds",
            "-F": "Produce output suitable for parsing by other programs",
        },
    },

    "fuser": {
        "man_url": "https://man7.org/linux/man-pages/man1/fuser.1.html",
        "use_cases": [
            "Find which process is using a file: fuser -v /path/to/file",
            "Kill all processes accessing a stuck mount point: fuser -km /mnt/usb",
            "Find which process is listening on a TCP port: fuser -n tcp 8080",
        ],
        "gotchas": [
            "fuser -k kills ALL processes accessing the file/filesystem -- be very careful with this on system directories",
            "Use -i for interactive confirmation before killing",
        ],
        "related": ["lsof", "kill", "umount"],
        "difficulty": "intermediate",
        "extra_flags": {},
    },

    "strace": {
        "man_url": "https://man7.org/linux/man-pages/man1/strace.1.html",
        "use_cases": [
            "Debug why a program cannot find a config file: strace -e trace=open,openat ./program 2>&1 | grep config",
            "Trace a running process: strace -p PID",
            "Profile system call timing: strace -c ./program",
            "Debug network connectivity: strace -e trace=network ./program",
            "Find why a program hangs: strace -p PID and see which syscall it blocks on",
        ],
        "gotchas": [
            "strace adds significant overhead (10-100x slowdown); do not use in production unless absolutely necessary",
            "strace output goes to stderr by default; use -o to write to a file for analysis",
            "The -s flag controls max string length printed (default 32); increase it to see full filenames and data: -s 256",
            "Attaching to a running process with -p requires root or matching user and ptrace permissions",
        ],
        "related": ["ltrace", "perf", "gdb"],
        "difficulty": "advanced",
        "extra_flags": {
            "-T": "Show time spent in each system call",
            "-r": "Print relative timestamp for each call",
            "-y": "Print paths associated with file descriptor arguments",
            "-e trace=file": "Trace only file-related system calls",
            "-e trace=network": "Trace only network-related system calls",
            "-e trace=process": "Trace only process-related system calls",
        },
    },

    "ltrace": {
        "man_url": "https://man7.org/linux/man-pages/man1/ltrace.1.html",
        "use_cases": [
            "Trace library calls to understand how a program uses libc: ltrace ./program",
            "Profile library call frequency and timing: ltrace -c ./program",
            "Debug dynamic linking issues by watching library function calls",
        ],
        "gotchas": [
            "ltrace does not work with statically linked binaries since there are no dynamic library calls to intercept",
            "ltrace may not work correctly on some architectures or with PIE (position-independent executables)",
            "ltrace has significant overhead; use -e to filter specific functions for performance-sensitive tracing",
        ],
        "related": ["strace", "perf", "gdb", "ldd"],
        "difficulty": "advanced",
        "extra_flags": {},
    },

    "perf": {
        "man_url": "https://man7.org/linux/man-pages/man1/perf.1.html",
        "use_cases": [
            "Count hardware performance events: perf stat ./myprogram",
            "Profile CPU hotspots with stack traces: perf record -g ./myprogram, then perf report",
            "Real-time system-wide profiling like top: perf top",
            "Find cache misses and branch mispredictions: perf stat -e cache-misses,branch-misses ./program",
        ],
        "gotchas": [
            "perf requires root or specific kernel settings (perf_event_paranoid) for most operations",
            "perf record generates perf.data files that can be large; use --call-graph dwarf for accurate stack traces",
            "Kernel symbols require /proc/kallsyms to be readable and debug symbols installed",
        ],
        "related": ["strace", "time", "gprof"],
        "difficulty": "advanced",
        "extra_flags": {
            "annotate": "Show per-line CPU usage of a function in source or assembly",
            "bench": "Run built-in benchmarks for memory, scheduling, etc.",
            "-e": "Select specific events to count or sample",
        },
    },

    "time": {
        "man_url": "https://man7.org/linux/man-pages/man1/time.1.html",
        "use_cases": [
            "Measure how long a build takes: time make -j8",
            "Compare performance of different implementations: time ./version1 vs time ./version2",
            "Identify if a slow command is CPU-bound (high user time) or I/O-bound (real >> user+sys)",
        ],
        "gotchas": [
            "Bash has a built-in 'time' keyword that behaves differently from /usr/bin/time; use \\time or command time to get the external version with more options",
            "The bash builtin 'time' cannot output to a file directly; use { time command; } 2> timing.txt",
            "'real' is wall-clock time, 'user' is CPU time in user space, 'sys' is CPU time in kernel space; real > user+sys indicates I/O waits",
        ],
        "related": ["perf", "strace", "timeout"],
        "difficulty": "beginner",
        "extra_flags": {
            "-v": "Verbose output with detailed resource usage (GNU time only)",
            "-o": "Write output to file (GNU time only)",
            "-f": "Custom output format string (GNU time only)",
        },
    },

    "timeout": {
        "man_url": "https://man7.org/linux/man-pages/man1/timeout.1.html",
        "use_cases": [
            "Prevent a curl request from hanging indefinitely: timeout 30 curl https://slow-api.example.com",
            "Set a hard limit on test execution in CI: timeout -k 10 300 pytest tests/",
            "Kill a process that should complete within a time window: timeout 60 ./batch-job.sh",
        ],
        "gotchas": [
            "timeout sends SIGTERM by default; the process can ignore it. Use -k to send SIGKILL after an additional grace period",
            "Exit code 124 means the command timed out; other exit codes come from the command itself",
            "The duration format supports s (seconds), m (minutes), h (hours), d (days); default is seconds",
        ],
        "related": ["kill", "time", "watch"],
        "difficulty": "beginner",
        "extra_flags": {},
    },

    "watch": {
        "man_url": "https://man7.org/linux/man-pages/man1/watch.1.html",
        "use_cases": [
            "Monitor disk space usage in real time: watch -n 5 df -h",
            "Watch a deployment roll out: watch -n 2 kubectl get pods",
            "Track file changes: watch -d ls -la /path/to/dir",
            "Monitor network connections: watch -n 1 'ss -tn | wc -l'",
        ],
        "gotchas": [
            "The command must be quoted if it contains pipes or special characters: watch 'cmd1 | cmd2'",
            "watch runs the command through sh -c, so bash-specific syntax may not work; use explicit bash -c if needed",
            "The -d flag highlights changes between refreshes, making differences easy to spot",
        ],
        "related": ["tail", "timeout"],
        "difficulty": "beginner",
        "extra_flags": {
            "-t": "Turn off the header showing interval and command",
            "-g": "Exit when the output of the command changes",
            "-e": "Freeze output and exit on command error",
            "-c": "Interpret ANSI color sequences",
            "-x": "Pass command to exec instead of sh -c (avoids shell interpretation)",
        },
    },

    "wait": {
        "man_url": "https://www.gnu.org/software/bash/manual/html_node/Job-Control-Builtins.html",
        "use_cases": [
            "Wait for all background jobs to finish: command1 & command2 & wait",
            "Get the exit status of a specific background process: wait $PID; echo $?",
            "Wait for any one of several background jobs to complete: wait -n",
            "Synchronize parallel tasks in a shell script before proceeding to the next stage",
        ],
        "gotchas": [
            "wait without arguments waits for ALL background children, not just the most recent one",
            "wait only works for child processes of the current shell; it cannot wait for arbitrary PIDs from other sessions",
            "The -n flag (wait for any single job) is a bash 4.3+ feature; it is not available in older bash or POSIX sh",
        ],
        "related": ["bg", "fg", "jobs", "kill"],
        "difficulty": "intermediate",
        "extra_flags": {},
    },

    "sleep": {
        "man_url": "https://man7.org/linux/man-pages/man1/sleep.1.html",
        "use_cases": [
            "Add a delay between retries in a loop: while ! curl -s host; do sleep 5; done",
            "Rate-limit requests in a script: for url in $urls; do curl $url; sleep 1; done",
            "Wait for a service to start: sleep 10 && curl http://localhost:8080/health",
        ],
        "gotchas": [
            "sleep accepts decimal values (sleep 0.5) on GNU/Linux but not on all Unix systems; check portability requirements",
            "sleep supports suffixes: s (seconds, default), m (minutes), h (hours), d (days)",
            "Using sleep in a tight loop wastes time; consider using inotifywait, systemd timers, or polling with exponential backoff instead",
        ],
        "related": ["watch", "timeout", "wait"],
        "difficulty": "beginner",
        "extra_flags": {},
    },

    "cron": {
        "man_url": "https://man7.org/linux/man-pages/man8/cron.8.html",
        "use_cases": [
            "cron is the daemon that runs scheduled jobs defined in crontab files",
            "Ensure cron is running on your system: systemctl status cron",
        ],
        "gotchas": [
            "cron runs commands with a minimal environment; PATH, HOME, and other variables may not be what you expect -- always use full paths in cron jobs",
            "cron has no built-in logging of job output; redirect stdout/stderr in the crontab entry or mail will be sent to the user",
            "cron does not run missed jobs if the system was off during the scheduled time; use anacron for machines that are not always on",
        ],
        "related": ["crontab", "at", "systemctl"],
        "difficulty": "intermediate",
        "extra_flags": {},
    },

    "crontab": {
        "man_url": "https://man7.org/linux/man-pages/man1/crontab.1.html",
        "use_cases": [
            "Edit your crontab: crontab -e",
            "Run a backup every night at 2am: add '0 2 * * * /usr/local/bin/backup.sh >> /var/log/backup.log 2>&1'",
            "List current cron jobs: crontab -l",
            "Remove all cron jobs: crontab -r (use with caution)",
        ],
        "gotchas": [
            "crontab -r removes ALL your cron jobs without confirmation; there is no undo",
            "Cron job environment is minimal -- PATH is typically just /usr/bin:/bin. Always use absolute paths for commands",
            "The cron expression minute field is 0-59; forgetting this and using * means the job runs every minute, not once",
            "Percent signs (%) in crontab lines are treated as newlines; escape them with backslash or put the command in a script",
        ],
        "related": ["cron", "at", "batch"],
        "difficulty": "intermediate",
        "extra_flags": {},
    },

    "at": {
        "man_url": "https://man7.org/linux/man-pages/man1/at.1.html",
        "use_cases": [
            "Schedule a one-time job: echo 'backup.sh' | at 2am",
            "Run a command in one hour: at now + 1 hour -f script.sh",
            "List pending jobs: atq (or at -l)",
        ],
        "gotchas": [
            "at requires the atd daemon to be running",
            "at jobs run with the environment captured at scheduling time, not the environment at execution time",
            "at is for one-time scheduling; use crontab for recurring tasks",
        ],
        "related": ["crontab", "batch", "sleep"],
        "difficulty": "intermediate",
        "extra_flags": {},
    },

    "batch": {
        "man_url": "https://man7.org/linux/man-pages/man1/batch.1.html",
        "use_cases": [
            "Queue a heavy compilation for when the system is idle: echo 'make -j8' | batch",
            "Schedule resource-intensive work to run during low load automatically",
        ],
        "gotchas": [
            "batch executes when load average drops below 1.5 (default); this threshold may never be reached on busy systems",
            "Like at, requires the atd daemon",
        ],
        "related": ["at", "crontab", "nice"],
        "difficulty": "intermediate",
        "extra_flags": {},
    },

    "shutdown": {
        "man_url": "https://man7.org/linux/man-pages/man8/shutdown.8.html",
        "use_cases": [
            "Shut down immediately: shutdown -h now",
            "Schedule a reboot with user warning: shutdown -r +10 'Rebooting for kernel update'",
            "Cancel a pending shutdown: shutdown -c",
        ],
        "gotchas": [
            "shutdown sends wall messages to logged-in users; use --no-wall to suppress in automated scenarios",
            "On systemd systems, 'shutdown +5' creates a transient timer; systemctl status shutdown.target shows the scheduled time",
        ],
        "related": ["reboot", "poweroff", "halt", "systemctl"],
        "difficulty": "beginner",
        "extra_flags": {},
    },

    "reboot": {
        "man_url": "https://man7.org/linux/man-pages/man8/reboot.8.html",
        "use_cases": [
            "Restart the system immediately: sudo reboot",
            "Force reboot a hung system: sudo reboot -f (last resort, may cause data loss)",
        ],
        "gotchas": [
            "reboot -f bypasses normal shutdown procedures and can cause data loss; prefer 'shutdown -r now'",
            "On remote servers, ensure you can access the console before forcing a reboot in case it does not come back",
        ],
        "related": ["shutdown", "poweroff", "halt", "systemctl"],
        "difficulty": "beginner",
        "extra_flags": {},
    },

    "halt": {
        "man_url": "https://man7.org/linux/man-pages/man8/halt.8.html",
        "use_cases": [
            "Stop the system without powering off the hardware: sudo halt",
            "On modern systems, halt usually behaves identically to poweroff",
        ],
        "gotchas": [
            "On modern systemd systems, halt, poweroff, and reboot all redirect to systemctl",
            "halt -f forcibly halts without proper shutdown, risking filesystem corruption",
        ],
        "related": ["shutdown", "poweroff", "reboot"],
        "difficulty": "beginner",
        "extra_flags": {},
    },

    "poweroff": {
        "man_url": "https://man7.org/linux/man-pages/man8/shutdown.8.html",
        "use_cases": [
            "Cleanly power off a server: sudo poweroff",
            "Equivalent to shutdown -h now on modern systems",
        ],
        "gotchas": [
            "poweroff -f bypasses init and can cause filesystem corruption",
        ],
        "related": ["shutdown", "halt", "reboot"],
        "difficulty": "beginner",
        "extra_flags": {},
    },

    "init": {
        "man_url": "https://man7.org/linux/man-pages/man1/init.1.html",
        "use_cases": [
            "Switch to single-user mode for emergency maintenance: sudo init 1",
            "On SysVinit systems, change runlevels to control which services run",
        ],
        "gotchas": [
            "On systemd systems, init is symlinked to systemd; use systemctl isolate instead of init for changing targets",
            "init 0 halts and init 6 reboots; confusing these can be catastrophic on remote servers",
        ],
        "related": ["systemctl", "runlevel", "shutdown"],
        "difficulty": "advanced",
        "extra_flags": {},
    },

    "runlevel": {
        "man_url": "https://man7.org/linux/man-pages/man8/runlevel.8.html",
        "use_cases": [
            "Check the current runlevel on a SysVinit system: runlevel",
        ],
        "gotchas": [
            "runlevel is a SysVinit concept; on systemd systems, use systemctl get-default for the equivalent information",
            "Output shows two values: previous and current runlevel; N means no previous runlevel was recorded",
        ],
        "related": ["init", "systemctl"],
        "difficulty": "intermediate",
        "extra_flags": {},
    },

    "uname": {
        "man_url": "https://man7.org/linux/man-pages/man1/uname.1.html",
        "use_cases": [
            "Print all system information: uname -a",
            "Detect CPU architecture for cross-platform scripts: uname -m",
            "Check kernel version: uname -r",
        ],
        "gotchas": [
            "uname shows the kernel information, not the distribution name; use /etc/os-release or lsb_release for distro info",
            "Inside Docker containers, uname shows the host kernel version, not the container's base image version",
        ],
        "related": ["hostname", "hostnamectl", "lsb_release"],
        "difficulty": "beginner",
        "extra_flags": {},
    },

    "hostname": {
        "man_url": "https://man7.org/linux/man-pages/man1/hostname.1.html",
        "use_cases": [
            "Display the system hostname: hostname",
            "Get all IP addresses of the machine: hostname -I",
            "Get the FQDN: hostname -f",
        ],
        "gotchas": [
            "Setting hostname with the hostname command is temporary; use hostnamectl for persistent changes on systemd systems",
            "hostname -I may show multiple IPs if the machine has multiple interfaces or addresses",
        ],
        "related": ["hostnamectl", "uname"],
        "difficulty": "beginner",
        "extra_flags": {},
    },

    "hostnamectl": {
        "man_url": "https://man7.org/linux/man-pages/man1/hostnamectl.1.html",
        "use_cases": [
            "Permanently set the system hostname: sudo hostnamectl set-hostname webserver01",
            "Display all hostname types and machine info: hostnamectl status",
        ],
        "gotchas": [
            "hostnamectl requires systemd; it does not work on SysVinit systems",
            "Changing the hostname does not update /etc/hosts automatically; update it manually to avoid sudo and other resolution issues",
        ],
        "related": ["hostname", "uname"],
        "difficulty": "beginner",
        "extra_flags": {},
    },

    "timedatectl": {
        "man_url": "https://man7.org/linux/man-pages/man1/timedatectl.1.html",
        "use_cases": [
            "Check current time, timezone, and NTP sync status: timedatectl",
            "Set the timezone: sudo timedatectl set-timezone America/New_York",
            "Enable NTP synchronization: sudo timedatectl set-ntp true",
        ],
        "gotchas": [
            "timedatectl requires systemd and conflicts with running ntpd or chrony in some configurations",
            "Setting time manually with set-time disables NTP; re-enable with set-ntp true afterward",
        ],
        "related": ["date", "hostnamectl", "localectl"],
        "difficulty": "beginner",
        "extra_flags": {},
    },

    "localectl": {
        "man_url": "https://man7.org/linux/man-pages/man1/localectl.1.html",
        "use_cases": [
            "View current locale settings: localectl",
            "Set the system locale: sudo localectl set-locale LANG=en_US.UTF-8",
            "Change the keyboard layout: sudo localectl set-keymap us",
        ],
        "gotchas": [
            "localectl changes are system-wide and require root; they take effect on next login, not the current session",
            "The locale must be generated first (with locale-gen or similar) before it can be set with localectl",
        ],
        "related": ["timedatectl", "hostnamectl"],
        "difficulty": "beginner",
        "extra_flags": {},
    },

    # =========================================================================
    # PERMISSIONS COMMANDS
    # =========================================================================

    "sudo": {
        "man_url": "https://man7.org/linux/man-pages/man8/sudo.8.html",
        "use_cases": [
            "Run a command as root: sudo apt update",
            "Edit a system file with your preferred editor: sudo -e /etc/hosts (uses SUDO_EDITOR or EDITOR)",
            "Run a command as a different user: sudo -u postgres psql",
            "Check what you are allowed to run: sudo -l",
            "Open a root shell: sudo -i (login shell) or sudo -s (non-login shell)",
        ],
        "gotchas": [
            "sudo caches credentials for a short time (typically 15 minutes); use sudo -k to clear the cache if security is a concern",
            "Environment variables are reset by default; use sudo -E to preserve them, or configure env_keep in sudoers",
            "Never edit /etc/sudoers directly; always use visudo which validates syntax and prevents lockouts",
            "sudo !! repeats the last command with sudo -- a common shortcut when you forget to use sudo",
            "Piping with sudo requires careful placement: echo 'text' | sudo tee /etc/file (not sudo echo 'text' > /etc/file which fails)",
        ],
        "related": ["su", "doas", "visudo"],
        "difficulty": "beginner",
        "extra_flags": {
            "-e": "Edit a file with the sudoers-configured editor (sudoedit)",
            "-H": "Set HOME to the target user's home directory",
            "-A": "Use a helper program for password input (SUDO_ASKPASS)",
            "--preserve-env": "More explicit form of -E to preserve environment",
        },
    },

    "su": {
        "man_url": "https://man7.org/linux/man-pages/man1/su.1.html",
        "use_cases": [
            "Switch to root with a full login environment: su - (or su -l root)",
            "Run a single command as another user: su -c 'pg_dump mydb' postgres",
            "Switch to a service account for debugging: su - www-data -s /bin/bash",
        ],
        "gotchas": [
            "su requires the target user's password (not your own like sudo); root password is needed for su -",
            "Without the dash (-), su does not start a login shell and inherits the current environment, which can cause unexpected behavior",
            "Many modern distributions disable the root password by default, making su - fail; use sudo -i instead",
        ],
        "related": ["sudo", "doas", "newgrp"],
        "difficulty": "beginner",
        "extra_flags": {
            "-g": "Set primary group (root only)",
            "-G": "Set supplementary groups (root only)",
            "-P": "Create a pseudo-terminal for the session",
        },
    },

    "doas": {
        "man_url": "https://man.openbsd.org/doas",
        "use_cases": [
            "Run a privileged command with simpler configuration than sudo: doas apt update",
            "Use on OpenBSD systems or Linux systems configured with doas as a sudo alternative",
        ],
        "gotchas": [
            "doas configuration (/etc/doas.conf) uses a completely different syntax from sudoers",
            "doas has fewer features than sudo (no command logging, no group-based sudo, no env editing); it trades features for simplicity and security",
            "doas is not installed by default on most Linux distributions",
        ],
        "related": ["sudo", "su"],
        "difficulty": "intermediate",
        "extra_flags": {},
    },

    "chroot": {
        "man_url": "https://man7.org/linux/man-pages/man1/chroot.1.html",
        "use_cases": [
            "Repair a broken system from a live USB: mount /dev/sda1 /mnt && chroot /mnt /bin/bash",
            "Build packages in a clean environment isolated from the host system",
            "Create a minimal sandbox for running untrusted programs (though containers are preferred now)",
        ],
        "gotchas": [
            "chroot is not a security boundary -- a root process inside a chroot can escape it. Use containers or namespaces for real isolation",
            "The chroot directory must contain all necessary binaries, libraries, and device files; a bare directory will fail immediately",
            "You typically need to mount /proc, /sys, and /dev inside the chroot for many commands to work properly",
        ],
        "related": ["docker", "unshare", "mount"],
        "difficulty": "advanced",
        "extra_flags": {},
    },

    "newgrp": {
        "man_url": "https://man7.org/linux/man-pages/man1/newgrp.1.html",
        "use_cases": [
            "Switch your primary group to create files owned by a different group: newgrp developers",
            "Access a group-restricted resource after being added to a group without logging out: newgrp docker",
        ],
        "gotchas": [
            "newgrp starts a new shell; when you exit, you return to the original shell with the original group",
            "If you were just added to a group, newgrp avoids the need to log out and back in to pick up the new group membership",
        ],
        "related": ["groups", "id", "usermod"],
        "difficulty": "intermediate",
        "extra_flags": {},
    },

    "id": {
        "man_url": "https://man7.org/linux/man-pages/man1/id.1.html",
        "use_cases": [
            "Check your current UID, GID, and all group memberships: id",
            "Verify a user's groups for permission debugging: id username",
            "Get just the username in a script: id -un",
        ],
        "gotchas": [
            "id shows effective UID/GID which may differ from real UID/GID if using setuid programs",
            "Group membership changes from usermod require a new login to take effect; id will show the old groups until then",
        ],
        "related": ["whoami", "groups", "who"],
        "difficulty": "beginner",
        "extra_flags": {},
    },

    "whoami": {
        "man_url": "https://man7.org/linux/man-pages/man1/whoami.1.html",
        "use_cases": [
            "Quick check in a script whether running as root: [ $(whoami) = root ] || exit 1",
            "Embed the username in log messages or file paths",
        ],
        "gotchas": [
            "whoami prints the effective username, which may be different from the login name if you used su or sudo -u",
        ],
        "related": ["id", "who", "logname"],
        "difficulty": "beginner",
        "extra_flags": {},
    },

    "groups": {
        "man_url": "https://man7.org/linux/man-pages/man1/groups.1.html",
        "use_cases": [
            "Check which groups you belong to: groups",
            "Verify a user has the expected group memberships: groups username",
        ],
        "gotchas": [
            "groups shows the groups from the current login session; recently added groups via usermod -aG require a new login to appear",
            "groups is equivalent to id -Gn but with a different output format",
        ],
        "related": ["id", "usermod", "newgrp"],
        "difficulty": "beginner",
        "extra_flags": {},
    },

    "users": {
        "man_url": "https://man7.org/linux/man-pages/man1/users.1.html",
        "use_cases": [
            "Quick list of who is logged in: users",
            "Count logged-in users: users | wc -w",
        ],
        "gotchas": [
            "users shows each login session, so a user logged in multiple times appears multiple times",
        ],
        "related": ["who", "w", "last"],
        "difficulty": "beginner",
        "extra_flags": {},
    },

    "who": {
        "man_url": "https://man7.org/linux/man-pages/man1/who.1.html",
        "use_cases": [
            "See who is logged in and from where: who",
            "Check the last boot time: who -b",
            "Show idle time to find inactive sessions: who -u",
        ],
        "gotchas": [
            "who reads /var/run/utmp which may not include all active sessions (e.g., some GUI sessions may not register)",
            "'who am i' shows the original login name even after su, unlike whoami which shows the effective user",
        ],
        "related": ["w", "users", "last", "whoami"],
        "difficulty": "beginner",
        "extra_flags": {},
    },

    "w": {
        "man_url": "https://man7.org/linux/man-pages/man1/w.1.html",
        "use_cases": [
            "Quick overview of system load and user activity: w",
            "Check what commands active users are running (shown in the WHAT column)",
            "Identify idle user sessions that may need to be terminated",
        ],
        "gotchas": [
            "w shows a combination of who, uptime, and per-user process info -- it is the most information-dense of the who-family commands",
        ],
        "related": ["who", "users", "uptime", "last"],
        "difficulty": "beginner",
        "extra_flags": {},
    },

    "last": {
        "man_url": "https://man7.org/linux/man-pages/man1/last.1.html",
        "use_cases": [
            "View recent login history: last -n 20",
            "Check system reboot history: last reboot",
            "Investigate logins by a specific user: last username",
        ],
        "gotchas": [
            "last reads /var/log/wtmp which may be rotated; historical data beyond the rotation period is lost",
            "On systems with many logins, unfiltered 'last' produces very long output; always use -n or a username filter",
        ],
        "related": ["lastlog", "who", "w"],
        "difficulty": "beginner",
        "extra_flags": {},
    },

    "lastlog": {
        "man_url": "https://man7.org/linux/man-pages/man8/lastlog.8.html",
        "use_cases": [
            "Audit which accounts have been used recently: lastlog",
            "Find stale accounts that have never logged in: lastlog -b 365",
            "Check when a specific user last logged in: lastlog -u username",
        ],
        "gotchas": [
            "Service accounts with /sbin/nologin shell show 'Never logged in' which is expected",
            "On systems with many users, the output can be very long; use -u or -t to filter",
        ],
        "related": ["last", "who"],
        "difficulty": "beginner",
        "extra_flags": {},
    },

    "finger": {
        "man_url": "https://man7.org/linux/man-pages/man1/finger.1.html",
        "use_cases": [
            "Display user account details: finger username",
            "Check a user's real name, login time, and shell",
        ],
        "gotchas": [
            "finger is considered a security risk because it can expose user information remotely; it is often uninstalled or disabled on modern systems",
            "The finger daemon (fingerd) is almost never enabled on production systems",
        ],
        "related": ["id", "who", "w"],
        "difficulty": "beginner",
        "extra_flags": {},
    },

    "useradd": {
        "man_url": "https://man7.org/linux/man-pages/man8/useradd.8.html",
        "use_cases": [
            "Create a regular user with home directory: useradd -m -s /bin/bash newuser",
            "Create a system service account: useradd -r -s /sbin/nologin myservice",
            "Create a user with specific group memberships: useradd -m -G sudo,docker newuser",
        ],
        "gotchas": [
            "useradd without -m does not create a home directory on many distributions -- always use -m for regular users",
            "useradd does not set a password; run passwd username afterward, or the account is locked",
            "On Debian/Ubuntu, adduser is a higher-level wrapper that is more user-friendly than raw useradd",
        ],
        "related": ["userdel", "usermod", "passwd", "groupadd"],
        "difficulty": "intermediate",
        "extra_flags": {},
    },

    "userdel": {
        "man_url": "https://man7.org/linux/man-pages/man8/userdel.8.html",
        "use_cases": [
            "Remove a user and their home directory: userdel -r username",
            "Remove just the account, keeping files for archival: userdel username",
        ],
        "gotchas": [
            "userdel -r permanently deletes the home directory and mail spool; there is no undo",
            "userdel cannot remove a user who is currently logged in unless -f is used",
            "Files owned by the deleted user outside their home directory become orphaned (owned by a numeric UID); find and reassign them",
        ],
        "related": ["useradd", "usermod"],
        "difficulty": "intermediate",
        "extra_flags": {},
    },

    "usermod": {
        "man_url": "https://man7.org/linux/man-pages/man8/usermod.8.html",
        "use_cases": [
            "Add a user to the docker group: usermod -aG docker username",
            "Change a user's login shell: usermod -s /bin/zsh username",
            "Lock a compromised account immediately: usermod -L username",
        ],
        "gotchas": [
            "Using -G without -a REPLACES all supplementary groups, potentially removing the user from sudo and other critical groups; always use -aG",
            "Group changes require the user to log out and back in to take effect",
            "usermod -L locks the password but does not prevent SSH key-based login; for full lockout, also change the shell to /sbin/nologin",
        ],
        "related": ["useradd", "userdel", "passwd", "groups"],
        "difficulty": "intermediate",
        "extra_flags": {},
    },

    "groupadd": {
        "man_url": "https://man7.org/linux/man-pages/man8/groupadd.8.html",
        "use_cases": [
            "Create a group for shared project access: groupadd developers",
            "Create a system group for a daemon: groupadd -r myservice",
        ],
        "gotchas": [
            "Groups are not useful until users are added to them with usermod -aG",
        ],
        "related": ["groupdel", "groupmod", "usermod"],
        "difficulty": "intermediate",
        "extra_flags": {},
    },

    "groupdel": {
        "man_url": "https://man7.org/linux/man-pages/man8/groupdel.8.html",
        "use_cases": [
            "Remove a group that is no longer needed: groupdel oldgroup",
        ],
        "gotchas": [
            "You cannot delete a group that is any user's primary group; change their primary group first",
            "Files owned by the deleted group will show a numeric GID instead of a group name",
        ],
        "related": ["groupadd", "groupmod"],
        "difficulty": "intermediate",
        "extra_flags": {},
    },

    "groupmod": {
        "man_url": "https://man7.org/linux/man-pages/man8/groupmod.8.html",
        "use_cases": [
            "Rename a group: groupmod -n newname oldname",
            "Change a group's GID: groupmod -g 1050 groupname",
        ],
        "gotchas": [
            "Changing a GID does not update file ownership; files will show the old numeric GID. Run find / -gid OLD_GID -exec chgrp NEW_GROUP {} + to fix",
        ],
        "related": ["groupadd", "groupdel"],
        "difficulty": "intermediate",
        "extra_flags": {},
    },

    "passwd": {
        "man_url": "https://man7.org/linux/man-pages/man1/passwd.1.html",
        "use_cases": [
            "Change your own password: passwd",
            "Set a password for a new user (as root): passwd newuser",
            "Lock an account to prevent login: passwd -l username",
            "Force a user to change password at next login: passwd -e username",
        ],
        "gotchas": [
            "passwd enforces password complexity policies; if a password is rejected, check /etc/security/pwquality.conf or PAM settings",
            "passwd -l only locks the password; SSH key auth still works. Use usermod -s /sbin/nologin for a full lockout",
            "passwd -d removes the password entirely, which may allow passwordless login depending on PAM configuration",
        ],
        "related": ["chpasswd", "usermod", "useradd"],
        "difficulty": "beginner",
        "extra_flags": {},
    },

    "chpasswd": {
        "man_url": "https://man7.org/linux/man-pages/man8/chpasswd.8.html",
        "use_cases": [
            "Batch set passwords for multiple users: echo 'user1:pass1\\nuser2:pass2' | chpasswd",
            "Automated user provisioning in scripts: echo 'newuser:temppass' | chpasswd",
        ],
        "gotchas": [
            "Passwords passed on the command line or in files are visible in process listings and shell history; use secure input methods",
            "Without -e, chpasswd expects plain text passwords which it hashes; with -e, it expects pre-hashed passwords",
        ],
        "related": ["passwd", "useradd"],
        "difficulty": "intermediate",
        "extra_flags": {},
    },

    "pwck": {
        "man_url": "https://man7.org/linux/man-pages/man8/pwck.8.html",
        "use_cases": [
            "Verify integrity of /etc/passwd and /etc/shadow after manual edits: pwck",
            "Run a read-only check without fixing anything: pwck -r",
        ],
        "gotchas": [
            "pwck may prompt to delete entries with errors; use -r first to review without changes",
        ],
        "related": ["grpck", "vipw", "passwd"],
        "difficulty": "advanced",
        "extra_flags": {},
    },

    "grpck": {
        "man_url": "https://man7.org/linux/man-pages/man8/grpck.8.html",
        "use_cases": [
            "Verify integrity of /etc/group and /etc/gshadow: grpck",
            "Read-only integrity check: grpck -r",
        ],
        "gotchas": [
            "Like pwck, grpck may prompt to remove invalid entries; use -r first to preview",
        ],
        "related": ["pwck", "vigr", "groupmod"],
        "difficulty": "advanced",
        "extra_flags": {},
    },

    "vipw": {
        "man_url": "https://man7.org/linux/man-pages/man8/vipw.8.html",
        "use_cases": [
            "Safely edit /etc/passwd with file locking: vipw",
            "Edit the shadow file: vipw -s",
        ],
        "gotchas": [
            "Always use vipw instead of directly editing /etc/passwd to prevent file corruption from concurrent access",
            "vipw validates syntax on save; if validation fails, it gives you a chance to fix errors before saving",
        ],
        "related": ["vigr", "pwck", "passwd"],
        "difficulty": "advanced",
        "extra_flags": {},
    },

    "vigr": {
        "man_url": "https://man7.org/linux/man-pages/man8/vigr.8.html",
        "use_cases": [
            "Safely edit /etc/group with file locking: vigr",
            "Edit the shadow group file: vigr -s",
        ],
        "gotchas": [
            "Like vipw, always use vigr instead of directly editing /etc/group",
        ],
        "related": ["vipw", "grpck", "groupmod"],
        "difficulty": "advanced",
        "extra_flags": {},
    },

    "getfacl": {
        "man_url": "https://man7.org/linux/man-pages/man1/getfacl.1.html",
        "use_cases": [
            "View ACL entries on a file: getfacl filename",
            "Audit ACLs recursively on a directory: getfacl -R /shared/",
            "Back up ACLs before making changes: getfacl -R /data > acl-backup.txt",
        ],
        "gotchas": [
            "A + sign in ls -l output after permissions indicates ACLs are set; use getfacl to see them",
            "The filesystem must be mounted with ACL support (most modern filesystems have this by default)",
            "Default ACLs on directories affect new files created inside them, not the directory itself",
        ],
        "related": ["setfacl", "chmod", "chown"],
        "difficulty": "intermediate",
        "extra_flags": {},
    },

    "setfacl": {
        "man_url": "https://man7.org/linux/man-pages/man1/setfacl.1.html",
        "use_cases": [
            "Grant a specific user read access to a file: setfacl -m u:alice:r file.txt",
            "Set a default ACL so new files in a directory inherit permissions: setfacl -d -m g:developers:rwx /shared/",
            "Restore ACLs from a backup: setfacl --restore=acl-backup.txt",
            "Remove all ACLs from a file: setfacl -b file.txt",
        ],
        "gotchas": [
            "ACL entries require a mask entry that limits the effective permissions; use setfacl -m m::rwx to ensure the mask does not restrict your ACL entries",
            "Copying files may not preserve ACLs unless you use cp -a or rsync -A",
            "The ACL mask is recalculated when you add or modify ACL entries, which can inadvertently restrict existing entries",
        ],
        "related": ["getfacl", "chmod", "chown"],
        "difficulty": "intermediate",
        "extra_flags": {},
    },

    "umask": {
        "man_url": "https://man7.org/linux/man-pages/man2/umask.2.html",
        "use_cases": [
            "Check the current umask: umask (octal) or umask -S (symbolic)",
            "Set restrictive default permissions for new files: umask 077 (only owner can read/write/execute)",
            "Set the umask in shell profile for consistent permissions across sessions",
        ],
        "gotchas": [
            "umask subtracts from the maximum permissions (666 for files, 777 for directories); umask 022 means new files get 644 and directories get 755",
            "umask only affects newly created files; it does not change permissions on existing files",
            "umask is per-process and inherited by child processes; setting it in one terminal does not affect others",
        ],
        "related": ["chmod", "getfacl", "setfacl"],
        "difficulty": "intermediate",
        "extra_flags": {},
    },

    "chgrp": {
        "man_url": "https://man7.org/linux/man-pages/man1/chgrp.1.html",
        "use_cases": [
            "Change group ownership of a shared directory: chgrp developers /shared/project/",
            "Recursively change group for all files: chgrp -R webteam /var/www/",
        ],
        "gotchas": [
            "You must be a member of the target group (or root) to change a file's group",
            "chgrp does not change the owner; use chown user:group to change both at once",
        ],
        "related": ["chown", "chmod", "groups"],
        "difficulty": "beginner",
        "extra_flags": {
            "-v": "Verbose output showing each change",
            "--reference": "Set group to match another file",
        },
    },
}
