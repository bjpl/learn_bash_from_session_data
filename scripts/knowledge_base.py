"""
Comprehensive Bash Command Knowledge Base

This module provides a structured database of bash commands, operators, and concepts
for educational purposes. All content is curated for learning bash from real usage patterns.
"""

from typing import Dict, Set, List, Any

# Command categories with their associated utilities
CATEGORY_MAPPINGS: Dict[str, Set[str]] = {
    "File System": {
        "ls", "cd", "pwd", "mkdir", "rmdir", "rm", "cp", "mv", "touch",
        "cat", "less", "more", "head", "tail", "file", "stat", "ln",
        "readlink", "realpath", "basename", "dirname", "tree", "du", "df",
        "mount", "umount", "fdisk", "mkfs", "fsck", "lsblk", "blkid",
        "find", "locate", "updatedb", "which", "whereis", "type",
    },
    "Text Processing": {
        "grep", "egrep", "fgrep", "sed", "awk", "gawk", "cut", "paste",
        "sort", "uniq", "wc", "tr", "tee", "xargs", "split", "csplit",
        "join", "comm", "diff", "patch", "cmp", "od", "hexdump", "xxd",
        "strings", "expand", "unexpand", "fold", "fmt", "pr", "nl",
        "column", "rev", "shuf", "head", "tail", "tac",
    },
    "Git": {
        "git", "gh", "hub", "tig", "gitk", "git-lfs",
    },
    "Package Management": {
        "apt", "apt-get", "apt-cache", "dpkg", "snap", "flatpak",
        "yum", "dnf", "rpm", "zypper", "pacman", "yay", "paru",
        "brew", "port", "pkg", "apk",
        "npm", "npx", "yarn", "pnpm", "bun",
        "pip", "pip3", "pipx", "conda", "poetry", "uv",
        "cargo", "rustup", "gem", "bundle", "composer", "go",
        "nuget", "dotnet", "mvn", "gradle",
    },
    "Process & System": {
        "ps", "top", "htop", "btop", "atop", "kill", "killall", "pkill",
        "pgrep", "nice", "renice", "nohup", "bg", "fg", "jobs", "disown",
        "screen", "tmux", "byobu", "systemctl", "service", "journalctl",
        "dmesg", "uptime", "free", "vmstat", "iostat", "mpstat", "sar",
        "lsof", "fuser", "strace", "ltrace", "perf", "time", "timeout",
        "watch", "wait", "sleep", "cron", "crontab", "at", "batch",
        "shutdown", "reboot", "halt", "poweroff", "init", "runlevel",
        "uname", "hostname", "hostnamectl", "timedatectl", "localectl",
    },
    "Networking": {
        "curl", "wget", "httpie", "http", "ssh", "scp", "sftp", "rsync",
        "ftp", "tftp", "nc", "netcat", "ncat", "socat", "telnet",
        "ping", "traceroute", "tracepath", "mtr", "dig", "nslookup", "host",
        "ip", "ifconfig", "route", "netstat", "ss", "arp", "arping",
        "iptables", "nft", "ufw", "firewall-cmd", "tcpdump", "wireshark",
        "nmap", "masscan", "nikto", "whois", "openssl", "certbot",
    },
    "Permissions": {
        "chmod", "chown", "chgrp", "umask", "getfacl", "setfacl",
        "sudo", "su", "doas", "chroot", "newgrp", "id", "whoami",
        "groups", "users", "who", "w", "last", "lastlog", "finger",
        "useradd", "userdel", "usermod", "groupadd", "groupdel", "groupmod",
        "passwd", "chpasswd", "pwck", "grpck", "vipw", "vigr",
    },
    "Compression": {
        "tar", "gzip", "gunzip", "bzip2", "bunzip2", "xz", "unxz",
        "zip", "unzip", "7z", "7za", "rar", "unrar", "zstd",
        "compress", "uncompress", "lz4", "lzop", "zcat", "bzcat", "xzcat",
    },
    "Search & Navigation": {
        "find", "locate", "mlocate", "plocate", "updatedb", "which",
        "whereis", "type", "command", "hash", "apropos", "whatis", "man",
        "info", "help", "ag", "rg", "ripgrep", "ack", "fzf", "fd",
        "tree", "exa", "lsd", "broot", "ranger", "mc", "nnn", "lf",
    },
    "Development": {
        "make", "cmake", "ninja", "meson", "autoconf", "automake",
        "gcc", "g++", "clang", "clang++", "cc", "ld", "as", "ar",
        "python", "python3", "python2", "node", "deno", "bun",
        "ruby", "perl", "php", "java", "javac", "kotlin", "scala",
        "go", "rust", "rustc", "cargo", "swift", "swiftc",
        "gdb", "lldb", "valgrind", "objdump", "nm", "readelf", "ldd",
        "docker", "docker-compose", "podman", "kubectl", "helm", "minikube",
        "vagrant", "terraform", "ansible", "puppet", "chef",
        "code", "vim", "nvim", "nano", "emacs", "ed", "ex", "vi",
        "jq", "yq", "xmllint", "xsltproc", "jsonnet",
    },
    "Shell Builtins": {
        "echo", "printf", "read", "source", ".", "exec", "eval", "set",
        "unset", "export", "declare", "local", "readonly", "typeset",
        "alias", "unalias", "builtin", "command", "enable", "hash",
        "cd", "pwd", "pushd", "popd", "dirs", "shopt", "bind",
        "history", "fc", "true", "false", "test", "[", "[[", "exit",
        "return", "break", "continue", "shift", "getopts", "trap",
        "ulimit", "times", "let", ":", "compgen", "complete", "compopt",
    },
}

# Build reverse mapping: command -> category
COMMAND_TO_CATEGORY: Dict[str, str] = {}
for category, commands in CATEGORY_MAPPINGS.items():
    for cmd in commands:
        COMMAND_TO_CATEGORY[cmd] = category

# Operators and special constructs that increase complexity
PIPE_OPERATORS = {"|", "|&"}
REDIRECT_OPERATORS = {">", ">>", "<", "<<", "<<<", "2>", "2>>", "&>", "&>>", "2>&1", ">&2"}
COMPOUND_OPERATORS = {"&&", "||", ";"}
SUBSHELL_MARKERS = {"$(", "`", "(", ")"}
PROCESS_SUBSTITUTION = {"<(", ">("}

# Command patterns that indicate higher complexity
LOOP_KEYWORDS = {"for", "while", "until", "do", "done"}
CONDITIONAL_KEYWORDS = {"if", "then", "else", "elif", "fi", "case", "esac"}
FUNCTION_KEYWORDS = {"function", "()"}

# Common flag patterns by complexity contribution
SIMPLE_FLAGS = {"-h", "--help", "-v", "--version", "-q", "--quiet"}
MODERATE_FLAGS = {"-r", "-R", "--recursive", "-f", "--force", "-a", "--all"}
COMPLEX_FLAGS = {"-e", "--regex", "-P", "--perl-regexp", "-E", "--extended-regexp"}

# Categories ordered by typical learning progression
LEARNING_ORDER: List[str] = [
    "Shell Builtins",
    "File System",
    "Search & Navigation",
    "Text Processing",
    "Permissions",
    "Compression",
    "Process & System",
    "Git",
    "Package Management",
    "Development",
    "Networking",
]

def get_category(command: str) -> str:
    """Get the category for a given base command."""
    return COMMAND_TO_CATEGORY.get(command, "Unknown")

def get_all_categories() -> List[str]:
    """Get all category names in learning order."""
    return LEARNING_ORDER.copy()

def get_commands_in_category(category: str) -> Set[str]:
    """Get all commands in a specific category."""
    return CATEGORY_MAPPINGS.get(category, set()).copy()


# =============================================================================
# COMPREHENSIVE COMMAND DATABASE
# =============================================================================

COMMAND_DB: Dict[str, Dict[str, Any]] = {
    "ls": {
        "description": "List directory contents with various formatting and filtering options",
        "man_url": "https://man7.org/linux/man-pages/man1/ls.1.html",
        "flags": {
            "-l": "Long format with permissions, owner, size, and modification time",
            "-a": "Show all files including hidden (dotfiles)",
            "-A": "Show almost all (exclude . and ..)",
            "-h": "Human-readable sizes (1K, 234M, 2G)",
            "-R": "Recursive listing of subdirectories",
            "-t": "Sort by modification time, newest first",
            "-r": "Reverse sort order",
            "-S": "Sort by file size, largest first",
            "-1": "One file per line",
            "-d": "List directories themselves, not their contents",
        },
        "common_patterns": ["ls -la", "ls -lah", "ls -lt", "ls *.txt", "ls -d */"],
    },
    "cd": {
        "description": "Change the current working directory",
        "man_url": "https://man7.org/linux/man-pages/man1/cd.1p.html",
        "flags": {
            "-": "Change to previous directory ($OLDPWD)",
            "-P": "Use physical directory structure (resolve symlinks)",
            "-L": "Use logical directory structure (follow symlinks, default)",
        },
        "common_patterns": ["cd ~", "cd ..", "cd -", "cd /path/to/dir"],
    },
    "pwd": {
        "description": "Print the current working directory path",
        "man_url": "https://man7.org/linux/man-pages/man1/pwd.1.html",
        "flags": {
            "-L": "Print logical path (with symlinks)",
            "-P": "Print physical path (resolved symlinks)",
        },
        "common_patterns": ["pwd", "echo $(pwd)"],
    },
    "find": {
        "description": "Search for files in directory hierarchy with powerful filtering",
        "man_url": "https://man7.org/linux/man-pages/man1/find.1.html",
        "flags": {
            "-name": "Match filename pattern (case-sensitive)",
            "-iname": "Match filename pattern (case-insensitive)",
            "-type": "File type: f=file, d=directory, l=symlink",
            "-size": "File size (+10M = larger than 10MB)",
            "-mtime": "Modified time in days (-1 = last 24h)",
            "-exec": "Execute command on each match",
            "-delete": "Delete matching files",
            "-maxdepth": "Maximum directory depth to search",
            "-empty": "Match empty files or directories",
            "-print0": "Print with null delimiter (for xargs -0)",
        },
        "common_patterns": [
            "find . -name '*.py'",
            "find . -type f -name '*.log' -delete",
            "find . -mtime -1",
            "find . -size +100M",
            "find . -name '*.txt' -exec grep -l 'pattern' {} \\;",
        ],
    },
    "tree": {
        "description": "Display directory structure as a tree",
        "man_url": "https://linux.die.net/man/1/tree",
        "flags": {
            "-L": "Limit depth of directory tree",
            "-a": "Show all files including hidden",
            "-d": "List directories only",
            "-h": "Print size in human-readable format",
            "-I": "Exclude pattern from listing",
            "--gitignore": "Filter using .gitignore rules",
        },
        "common_patterns": ["tree -L 2", "tree -d", "tree -a -I 'node_modules|.git'"],
    },
    "du": {
        "description": "Estimate file and directory space usage",
        "man_url": "https://man7.org/linux/man-pages/man1/du.1.html",
        "flags": {
            "-h": "Human-readable sizes",
            "-s": "Summary only (total for each argument)",
            "-a": "Show all files, not just directories",
            "-c": "Produce grand total",
            "--max-depth": "Maximum directory depth",
        },
        "common_patterns": ["du -sh *", "du -sh .", "du -h --max-depth=1", "du -sh */ | sort -h"],
    },
    "df": {
        "description": "Report filesystem disk space usage",
        "man_url": "https://man7.org/linux/man-pages/man1/df.1.html",
        "flags": {
            "-h": "Human-readable sizes",
            "-T": "Show filesystem type",
            "-i": "Show inode information instead of block usage",
        },
        "common_patterns": ["df -h", "df -hT", "df -h /"],
    },
    "mkdir": {
        "description": "Create directories",
        "man_url": "https://man7.org/linux/man-pages/man1/mkdir.1.html",
        "flags": {
            "-p": "Create parent directories as needed, no error if exists",
            "-v": "Verbose, print each directory created",
            "-m": "Set permission mode (like chmod)",
        },
        "common_patterns": ["mkdir -p src/components/ui", "mkdir -pv new/nested/dir"],
    },
    "rm": {
        "description": "Remove files or directories",
        "man_url": "https://man7.org/linux/man-pages/man1/rm.1.html",
        "flags": {
            "-r": "Remove directories recursively",
            "-f": "Force, ignore nonexistent files, never prompt",
            "-i": "Interactive, prompt before each removal",
            "-v": "Verbose, explain what is being done",
        },
        "common_patterns": ["rm file.txt", "rm -rf directory/", "rm -i *.log"],
    },
    "cp": {
        "description": "Copy files and directories",
        "man_url": "https://man7.org/linux/man-pages/man1/cp.1.html",
        "flags": {
            "-r": "Copy directories recursively",
            "-a": "Archive mode (preserve all: -dR --preserve=all)",
            "-i": "Interactive, prompt before overwrite",
            "-n": "No clobber, don't overwrite existing",
            "-u": "Update, copy only when source is newer",
            "-v": "Verbose, explain what is being done",
        },
        "common_patterns": ["cp file.txt backup.txt", "cp -r src/ dest/", "cp -a project/ backup/"],
    },
    "mv": {
        "description": "Move or rename files and directories",
        "man_url": "https://man7.org/linux/man-pages/man1/mv.1.html",
        "flags": {
            "-i": "Interactive, prompt before overwrite",
            "-n": "No clobber, don't overwrite existing",
            "-u": "Update, move only when source is newer",
            "-v": "Verbose, explain what is being done",
        },
        "common_patterns": ["mv old.txt new.txt", "mv file.txt directory/", "mv -v *.log archive/"],
    },
    "touch": {
        "description": "Create empty files or update file timestamps",
        "man_url": "https://man7.org/linux/man-pages/man1/touch.1.html",
        "flags": {
            "-a": "Change only access time",
            "-m": "Change only modification time",
            "-c": "Don't create file if it doesn't exist",
            "-d": "Parse string and use instead of current time",
        },
        "common_patterns": ["touch newfile.txt", "touch -c existing.txt"],
    },
    "ln": {
        "description": "Create links between files (hard or symbolic)",
        "man_url": "https://man7.org/linux/man-pages/man1/ln.1.html",
        "flags": {
            "-s": "Create symbolic (soft) link",
            "-f": "Force, remove existing destination files",
            "-r": "Create relative symbolic link",
            "-v": "Verbose, print name of each linked file",
        },
        "common_patterns": ["ln -s /path/to/target linkname", "ln -sf target link"],
    },
    "cat": {
        "description": "Concatenate and display file contents",
        "man_url": "https://man7.org/linux/man-pages/man1/cat.1.html",
        "flags": {
            "-n": "Number all output lines",
            "-b": "Number non-blank output lines",
            "-s": "Squeeze multiple blank lines into one",
            "-A": "Show all (equivalent to -vET)",
        },
        "common_patterns": ["cat file.txt", "cat -n script.sh", "cat file1.txt file2.txt > combined.txt"],
    },
    "grep": {
        "description": "Search for patterns in text using regular expressions",
        "man_url": "https://man7.org/linux/man-pages/man1/grep.1.html",
        "flags": {
            "-i": "Case-insensitive matching",
            "-v": "Invert match (show non-matching lines)",
            "-r": "Recursive search in directories",
            "-l": "List filenames with matches only",
            "-n": "Show line numbers",
            "-c": "Count matching lines",
            "-w": "Match whole words only",
            "-E": "Extended regex (same as egrep)",
            "-o": "Show only matching part of line",
            "-A": "Show N lines after match",
            "-B": "Show N lines before match",
            "-C": "Show N lines of context (before and after)",
            "--include": "Search only files matching pattern",
            "--exclude": "Skip files matching pattern",
        },
        "common_patterns": [
            "grep 'pattern' file.txt",
            "grep -r 'TODO' src/",
            "grep -rn 'function' --include='*.js'",
            "grep -i 'error' log.txt",
            "grep -v '^#' config.txt",
        ],
    },
    "sed": {
        "description": "Stream editor for filtering and transforming text",
        "man_url": "https://man7.org/linux/man-pages/man1/sed.1.html",
        "flags": {
            "-i": "Edit files in place",
            "-e": "Add script/expression to commands",
            "-n": "Suppress automatic printing",
            "-E": "Use extended regular expressions (portable)",
        },
        "common_patterns": [
            "sed 's/old/new/' file.txt",
            "sed 's/old/new/g' file.txt",
            "sed -i 's/old/new/g' file.txt",
            "sed -n '10,20p' file.txt",
            "sed '/pattern/d' file.txt",
        ],
    },
    "awk": {
        "description": "Pattern scanning and text processing language",
        "man_url": "https://man7.org/linux/man-pages/man1/awk.1p.html",
        "flags": {
            "-F": "Set field separator",
            "-v": "Assign variable before execution",
            "-f": "Read program from file",
        },
        "common_patterns": [
            "awk '{print $1}' file.txt",
            "awk -F',' '{print $1, $3}' data.csv",
            "awk '/pattern/ {print}' file.txt",
            "awk '{sum += $1} END {print sum}' numbers.txt",
        ],
    },
    "sort": {
        "description": "Sort lines of text files",
        "man_url": "https://man7.org/linux/man-pages/man1/sort.1.html",
        "flags": {
            "-r": "Reverse sort order",
            "-n": "Numeric sort",
            "-h": "Human numeric sort (2K, 1G)",
            "-k": "Sort by specific field/key",
            "-t": "Field separator",
            "-u": "Output only unique lines",
        },
        "common_patterns": ["sort file.txt", "sort -r file.txt", "sort -n numbers.txt", "du -sh * | sort -h"],
    },
    "uniq": {
        "description": "Report or filter out repeated lines (requires sorted input)",
        "man_url": "https://man7.org/linux/man-pages/man1/uniq.1.html",
        "flags": {
            "-c": "Prefix lines by count of occurrences",
            "-d": "Only print duplicate lines",
            "-u": "Only print unique lines",
            "-i": "Case-insensitive comparison",
        },
        "common_patterns": ["sort file.txt | uniq", "sort file.txt | uniq -c", "sort file.txt | uniq -c | sort -rn"],
    },
    "wc": {
        "description": "Print line, word, and byte counts",
        "man_url": "https://man7.org/linux/man-pages/man1/wc.1.html",
        "flags": {
            "-l": "Print line count only",
            "-w": "Print word count only",
            "-c": "Print byte count only",
            "-m": "Print character count only",
        },
        "common_patterns": ["wc file.txt", "wc -l file.txt", "wc -l *.py"],
    },
    "head": {
        "description": "Output the first part of files",
        "man_url": "https://man7.org/linux/man-pages/man1/head.1.html",
        "flags": {
            "-n": "Print first N lines (or -N for all but last N)",
            "-c": "Print first N bytes",
        },
        "common_patterns": ["head file.txt", "head -n 20 file.txt"],
    },
    "tail": {
        "description": "Output the last part of files",
        "man_url": "https://man7.org/linux/man-pages/man1/tail.1.html",
        "flags": {
            "-n": "Print last N lines (or +N for lines from N onward)",
            "-f": "Follow file as it grows",
            "-F": "Follow with retry (handles log rotation)",
        },
        "common_patterns": ["tail file.txt", "tail -n 50 file.txt", "tail -f logfile.log"],
    },
    "cut": {
        "description": "Remove sections from each line of files",
        "man_url": "https://man7.org/linux/man-pages/man1/cut.1.html",
        "flags": {
            "-d": "Use delimiter instead of TAB",
            "-f": "Select fields (1,3 or 1-3)",
            "-c": "Select characters",
        },
        "common_patterns": ["cut -d',' -f1,3 data.csv", "cut -d':' -f1 /etc/passwd"],
    },
    "tr": {
        "description": "Translate or delete characters",
        "man_url": "https://man7.org/linux/man-pages/man1/tr.1.html",
        "flags": {
            "-d": "Delete characters in SET1",
            "-s": "Squeeze repeated characters",
            "-c": "Use complement of SET1",
        },
        "common_patterns": ["tr 'a-z' 'A-Z'", "tr -d '\\n'", "tr -s ' '"],
    },
    "diff": {
        "description": "Compare files line by line",
        "man_url": "https://man7.org/linux/man-pages/man1/diff.1.html",
        "flags": {
            "-u": "Unified format (most common)",
            "-r": "Recursive directory comparison",
            "-q": "Report only when files differ",
            "-i": "Ignore case differences",
            "--color": "Colorize output",
        },
        "common_patterns": ["diff file1.txt file2.txt", "diff -u original.txt modified.txt"],
    },
    "jq": {
        "description": "Command-line JSON processor",
        "man_url": "https://stedolan.github.io/jq/manual/",
        "flags": {
            "-r": "Raw output (no quotes for strings)",
            "-c": "Compact output (one line)",
            "-s": "Slurp mode (read entire input as array)",
            "-S": "Sort object keys",
            "--arg": "Set variable to string value",
        },
        "common_patterns": [
            "jq '.' file.json",
            "jq '.name' file.json",
            "jq -r '.items[]' file.json",
            "curl -s url | jq '.'",
        ],
    },
    "tee": {
        "description": "Read from stdin and write to stdout and files simultaneously",
        "man_url": "https://man7.org/linux/man-pages/man1/tee.1.html",
        "flags": {
            "-a": "Append to files instead of overwriting",
        },
        "common_patterns": ["echo 'text' | tee file.txt", "command | tee output.log"],
    },
    "xargs": {
        "description": "Build and execute commands from standard input",
        "man_url": "https://man7.org/linux/man-pages/man1/xargs.1.html",
        "flags": {
            "-0": "Input items terminated by null (for find -print0)",
            "-n": "Use at most N arguments per command",
            "-I": "Replace string in command with input",
            "-P": "Run N processes in parallel",
        },
        "common_patterns": [
            "find . -name '*.log' | xargs rm",
            "find . -name '*.txt' -print0 | xargs -0 grep 'pattern'",
            "echo 'a b c' | xargs -n 1 echo",
        ],
    },
    "git": {
        "description": "Distributed version control system",
        "man_url": "https://git-scm.com/docs",
        "flags": {
            "--version": "Print git version",
            "-C": "Run as if started in specified directory",
        },
        "subcommands": {
            "init": "Create empty repository",
            "clone": "Clone repository",
            "add": "Add file contents to staging",
            "commit": "Record changes",
            "status": "Show working tree status",
            "diff": "Show changes",
            "log": "Show commit logs",
            "branch": "Manage branches",
            "checkout": "Switch branches",
            "merge": "Join histories",
            "pull": "Fetch and integrate",
            "push": "Update remote",
            "stash": "Stash changes",
        },
        "common_patterns": [
            "git init",
            "git clone url",
            "git add .",
            "git commit -m 'message'",
            "git status",
            "git log --oneline",
            "git branch -a",
            "git checkout -b new-branch",
            "git pull origin main",
            "git push origin main",
        ],
    },
    "npm": {
        "description": "Node.js package manager",
        "man_url": "https://docs.npmjs.com/cli",
        "flags": {
            "-g": "Install globally",
            "--save-dev": "Save to devDependencies",
            "-D": "Save to devDependencies (shorthand)",
            "-y": "Accept defaults for init",
        },
        "subcommands": {
            "init": "Create package.json",
            "install": "Install dependencies",
            "run": "Run scripts",
            "test": "Run test script",
            "build": "Run build script",
        },
        "common_patterns": [
            "npm init -y",
            "npm install",
            "npm install package-name",
            "npm install -D typescript",
            "npm run build",
        ],
    },
    "npx": {
        "description": "Execute npm package binaries",
        "man_url": "https://docs.npmjs.com/cli/commands/npx",
        "flags": {
            "-y": "Auto-confirm package installation",
            "--no-install": "Error if package not installed",
        },
        "common_patterns": ["npx create-react-app my-app", "npx typescript --init", "npx eslint ."],
    },
    "pip": {
        "description": "Python package installer",
        "man_url": "https://pip.pypa.io/en/stable/",
        "flags": {
            "-r": "Install from requirements file",
            "-e": "Install in editable/development mode",
            "--upgrade": "Upgrade packages",
            "-U": "Upgrade packages (shorthand)",
        },
        "common_patterns": [
            "pip install package-name",
            "pip install -r requirements.txt",
            "pip freeze > requirements.txt",
            "pip list",
        ],
    },
    "apt": {
        "description": "Debian/Ubuntu package manager",
        "man_url": "https://manpages.ubuntu.com/manpages/man8/apt.8.html",
        "flags": {
            "-y": "Automatic yes to prompts",
            "-q": "Quiet output",
        },
        "common_patterns": ["apt update", "apt upgrade -y", "apt install package-name"],
    },
    "brew": {
        "description": "macOS/Linux package manager (Homebrew)",
        "man_url": "https://docs.brew.sh/Manpage",
        "flags": {
            "--cask": "Operate on cask (macOS apps)",
        },
        "common_patterns": ["brew install package-name", "brew update", "brew upgrade"],
    },
    "cargo": {
        "description": "Rust package manager and build tool",
        "man_url": "https://doc.rust-lang.org/cargo/",
        "flags": {
            "--release": "Build in release mode with optimizations",
        },
        "common_patterns": ["cargo new project-name", "cargo build", "cargo run", "cargo test"],
    },
    "ps": {
        "description": "Report process status",
        "man_url": "https://man7.org/linux/man-pages/man1/ps.1.html",
        "flags": {
            "-e": "Select all processes",
            "-f": "Full-format listing",
            "-u": "Select by effective user",
            "aux": "BSD-style all users, detailed",
        },
        "common_patterns": ["ps aux", "ps -ef", "ps aux | grep process-name"],
    },
    "kill": {
        "description": "Send signals to processes",
        "man_url": "https://man7.org/linux/man-pages/man1/kill.1.html",
        "flags": {
            "-9": "SIGKILL - force kill",
            "-15": "SIGTERM - terminate (default)",
            "-l": "List signal names",
        },
        "common_patterns": ["kill PID", "kill -9 PID"],
    },
    "top": {
        "description": "Display and update sorted process information",
        "man_url": "https://man7.org/linux/man-pages/man1/top.1.html",
        "flags": {
            "-b": "Batch mode (for piping output)",
            "-n": "Number of iterations",
            "-u": "Filter by user",
        },
        "common_patterns": ["top", "top -u username"],
    },
    "env": {
        "description": "Display, set, or remove environment variables",
        "man_url": "https://man7.org/linux/man-pages/man1/env.1.html",
        "flags": {
            "-i": "Start with empty environment",
            "-u": "Remove variable from environment",
        },
        "common_patterns": ["env", "env | grep PATH", "env VAR=value command"],
    },
    "export": {
        "description": "Set environment variables for child processes",
        "man_url": "https://www.gnu.org/software/bash/manual/html_node/Bourne-Shell-Builtins.html",
        "flags": {
            "-p": "Display all exported variables",
            "-n": "Remove export property",
        },
        "common_patterns": ["export PATH=$PATH:/new/path", "export NODE_ENV=production"],
    },
    "which": {
        "description": "Locate command executable in PATH",
        "man_url": "https://man7.org/linux/man-pages/man1/which.1.html",
        "flags": {
            "-a": "Print all matches in PATH",
        },
        "common_patterns": ["which python", "which -a python"],
    },
    "curl": {
        "description": "Transfer data with URLs",
        "man_url": "https://curl.se/docs/manpage.html",
        "flags": {
            "-X": "Request method (GET, POST, PUT, DELETE)",
            "-H": "Add header",
            "-d": "Send data in request body",
            "-o": "Write output to file",
            "-O": "Write to file named like remote",
            "-L": "Follow redirects",
            "-s": "Silent mode",
            "-v": "Verbose output",
            "-i": "Include response headers",
            "-I": "Fetch headers only (HEAD request)",
        },
        "common_patterns": [
            "curl https://api.example.com",
            "curl -s https://api.example.com | jq '.'",
            "curl -X POST -H 'Content-Type: application/json' -d '{\"key\":\"value\"}' url",
            "curl -o output.html https://example.com",
            "curl -L https://shortened.url",
        ],
    },
    "wget": {
        "description": "Non-interactive network file downloader",
        "man_url": "https://www.gnu.org/software/wget/manual/wget.html",
        "flags": {
            "-O": "Write to specified file",
            "-q": "Quiet mode",
            "-c": "Continue interrupted download",
            "-r": "Recursive download",
        },
        "common_patterns": ["wget https://example.com/file.zip", "wget -O output.zip url"],
    },
    "ssh": {
        "description": "OpenSSH remote login client",
        "man_url": "https://man.openbsd.org/ssh",
        "flags": {
            "-p": "Port to connect to",
            "-i": "Identity file (private key)",
            "-v": "Verbose mode",
            "-L": "Local port forwarding",
            "-D": "Dynamic port forwarding (SOCKS proxy)",
        },
        "common_patterns": ["ssh user@host", "ssh -p 2222 user@host", "ssh -i ~/.ssh/key.pem user@host"],
    },
    "scp": {
        "description": "Secure copy over SSH",
        "man_url": "https://man.openbsd.org/scp",
        "flags": {
            "-r": "Recursive copy directories",
            "-P": "Port to connect to",
            "-i": "Identity file",
        },
        "common_patterns": ["scp file.txt user@host:/path/", "scp -r directory/ user@host:/path/"],
    },
    "rsync": {
        "description": "Fast, versatile file copying tool for synchronization",
        "man_url": "https://rsync.samba.org/documentation.html",
        "flags": {
            "-a": "Archive mode (preserves everything)",
            "-v": "Verbose output",
            "-z": "Compress during transfer",
            "-n": "Dry run",
            "--delete": "Delete extraneous files from destination",
            "-P": "Show progress and allow resume",
        },
        "common_patterns": ["rsync -av source/ destination/", "rsync -avz source/ user@host:/destination/"],
    },
    "chmod": {
        "description": "Change file mode/permissions",
        "man_url": "https://man7.org/linux/man-pages/man1/chmod.1.html",
        "flags": {
            "-R": "Recursive change",
            "-v": "Verbose, show changes",
        },
        "common_patterns": ["chmod 755 script.sh", "chmod +x script.sh", "chmod -R 644 directory/"],
    },
    "chown": {
        "description": "Change file owner and group",
        "man_url": "https://man7.org/linux/man-pages/man1/chown.1.html",
        "flags": {
            "-R": "Recursive change",
            "-v": "Verbose, show changes",
        },
        "common_patterns": ["chown user file.txt", "chown user:group file.txt", "chown -R user:group directory/"],
    },
    "tar": {
        "description": "Archive files (tape archive)",
        "man_url": "https://man7.org/linux/man-pages/man1/tar.1.html",
        "flags": {
            "-c": "Create archive",
            "-x": "Extract archive",
            "-t": "List archive contents",
            "-f": "Archive filename",
            "-v": "Verbose output",
            "-z": "Filter through gzip",
            "-j": "Filter through bzip2",
            "-C": "Change to directory before operation",
        },
        "common_patterns": [
            "tar -cvf archive.tar directory/",
            "tar -xvf archive.tar",
            "tar -czvf archive.tar.gz directory/",
            "tar -xzvf archive.tar.gz",
        ],
    },
    "gzip": {
        "description": "Compress files with LZ77 algorithm",
        "man_url": "https://man7.org/linux/man-pages/man1/gzip.1.html",
        "flags": {
            "-d": "Decompress",
            "-k": "Keep original file",
            "-v": "Verbose output",
            "-9": "Best compression",
        },
        "common_patterns": ["gzip file.txt", "gzip -d file.txt.gz", "gunzip file.txt.gz"],
    },
    "zip": {
        "description": "Package and compress files",
        "man_url": "https://linux.die.net/man/1/zip",
        "flags": {
            "-r": "Recursive, include directories",
            "-e": "Encrypt with password",
            "-9": "Best compression",
        },
        "common_patterns": ["zip archive.zip file1 file2", "zip -r archive.zip directory/"],
    },
    "unzip": {
        "description": "Extract compressed files from zip archive",
        "man_url": "https://linux.die.net/man/1/unzip",
        "flags": {
            "-l": "List archive contents",
            "-d": "Extract to directory",
            "-o": "Overwrite without prompting",
        },
        "common_patterns": ["unzip archive.zip", "unzip archive.zip -d destination/"],
    },
    "node": {
        "description": "JavaScript runtime built on V8",
        "man_url": "https://nodejs.org/docs/latest/api/cli.html",
        "flags": {
            "-v": "Print Node.js version",
            "-e": "Evaluate script",
            "--inspect": "Enable inspector agent",
        },
        "common_patterns": ["node script.js", "node -e 'console.log(process.version)'"],
    },
    "python": {
        "description": "Python interpreter",
        "man_url": "https://docs.python.org/3/using/cmdline.html",
        "flags": {
            "-V": "Print Python version",
            "-c": "Execute command string",
            "-m": "Run module as script",
        },
        "common_patterns": ["python script.py", "python -m http.server 8000", "python -m venv venv"],
    },
    "docker": {
        "description": "Container management platform",
        "man_url": "https://docs.docker.com/engine/reference/commandline/docker/",
        "flags": {
            "-v": "Bind mount a volume",
            "-p": "Publish port",
            "-d": "Detached mode",
            "-it": "Interactive with TTY",
            "-e": "Set environment variable",
            "--name": "Assign name to container",
            "--rm": "Remove container when stopped",
        },
        "common_patterns": [
            "docker run -it ubuntu bash",
            "docker run -d -p 8080:80 nginx",
            "docker ps",
            "docker images",
            "docker build -t myapp .",
        ],
    },
    "echo": {
        "description": "Display text or variables",
        "man_url": "https://man7.org/linux/man-pages/man1/echo.1.html",
        "flags": {
            "-n": "Don't output trailing newline",
            "-e": "Enable interpretation of backslash escapes",
        },
        "common_patterns": ["echo 'Hello World'", "echo $PATH", "echo -n 'no newline'"],
    },
    "date": {
        "description": "Display or set system date and time",
        "man_url": "https://man7.org/linux/man-pages/man1/date.1.html",
        "flags": {
            "-u": "UTC time",
            "-d": "Display specified date",
            "-I": "ISO 8601 format",
        },
        "common_patterns": ["date", "date +%Y-%m-%d", "date '+%Y-%m-%d %H:%M:%S'"],
    },
    "sleep": {
        "description": "Delay for specified time",
        "man_url": "https://man7.org/linux/man-pages/man1/sleep.1.html",
        "flags": {},
        "common_patterns": ["sleep 5", "sleep 0.5", "sleep 1m"],
    },
    "time": {
        "description": "Measure command execution time",
        "man_url": "https://man7.org/linux/man-pages/man1/time.1.html",
        "flags": {},
        "common_patterns": ["time command", "time ./script.sh"],
    },
    "watch": {
        "description": "Execute command repeatedly and display output",
        "man_url": "https://man7.org/linux/man-pages/man1/watch.1.html",
        "flags": {
            "-n": "Interval in seconds",
            "-d": "Highlight differences",
        },
        "common_patterns": ["watch -n 1 'date'", "watch df -h"],
    },
    "history": {
        "description": "Display command history",
        "man_url": "https://www.gnu.org/software/bash/manual/html_node/Bash-History-Builtins.html",
        "flags": {
            "-c": "Clear history list",
        },
        "common_patterns": ["history", "history | grep pattern"],
    },
    "alias": {
        "description": "Create command aliases",
        "man_url": "https://www.gnu.org/software/bash/manual/html_node/Bash-Builtins.html",
        "flags": {},
        "common_patterns": ["alias", "alias ll='ls -la'", "alias gs='git status'"],
    },
    "test": {
        "description": "Evaluate conditional expression",
        "man_url": "https://man7.org/linux/man-pages/man1/test.1.html",
        "flags": {
            "-e": "File exists",
            "-f": "Is regular file",
            "-d": "Is directory",
            "-r": "Is readable",
            "-w": "Is writable",
            "-x": "Is executable",
            "-z": "String is empty",
            "-n": "String is non-empty",
        },
        "common_patterns": ["test -f file.txt && echo 'exists'", "[ -d dir ] && cd dir"],
    },
    "read": {
        "description": "Read line from stdin into variable",
        "man_url": "https://www.gnu.org/software/bash/manual/html_node/Bash-Builtins.html",
        "flags": {
            "-p": "Prompt string",
            "-r": "Raw input (no backslash escaping)",
            "-s": "Silent mode (for passwords)",
            "-t": "Timeout in seconds",
        },
        "common_patterns": ["read -p 'Enter name: ' name", "read -s -p 'Password: ' pass"],
    },
    "basename": {
        "description": "Strip directory and suffix from filename",
        "man_url": "https://man7.org/linux/man-pages/man1/basename.1.html",
        "flags": {
            "-s": "Remove suffix",
        },
        "common_patterns": ["basename /path/to/file.txt", "basename /path/to/file.txt .txt"],
    },
    "dirname": {
        "description": "Strip last component from filename",
        "man_url": "https://man7.org/linux/man-pages/man1/dirname.1.html",
        "flags": {},
        "common_patterns": ["dirname /path/to/file.txt", "cd $(dirname $0)"],
    },
    "realpath": {
        "description": "Print resolved absolute pathname",
        "man_url": "https://man7.org/linux/man-pages/man1/realpath.1.html",
        "flags": {
            "-e": "All components must exist",
            "-s": "Don't expand symlinks",
        },
        "common_patterns": ["realpath file.txt", "realpath ."],
    },
    "seq": {
        "description": "Print sequence of numbers",
        "man_url": "https://man7.org/linux/man-pages/man1/seq.1.html",
        "flags": {
            "-s": "Separator string",
            "-w": "Equalize width with leading zeros",
        },
        "common_patterns": ["seq 10", "seq 1 10", "seq -w 01 10"],
    },
    "stat": {
        "description": "Display detailed file or filesystem status",
        "man_url": "https://man7.org/linux/man-pages/man1/stat.1.html",
        "flags": {
            "-c": "Use specified FORMAT",
        },
        "common_patterns": ["stat file.txt", "stat -c '%a %n' *"],
    },
    "file": {
        "description": "Determine file type by examining content",
        "man_url": "https://man7.org/linux/man-pages/man1/file.1.html",
        "flags": {
            "-b": "Brief mode (don't print filename)",
            "-i": "Output MIME type strings",
        },
        "common_patterns": ["file *", "file -i document.pdf"],
    },
    "less": {
        "description": "View file contents with scrolling and search",
        "man_url": "https://man7.org/linux/man-pages/man1/less.1.html",
        "flags": {
            "-N": "Show line numbers",
            "-S": "Chop long lines",
            "-R": "Show raw control characters (for colors)",
        },
        "common_patterns": ["less file.txt", "command | less"],
    },
    "more": {
        "description": "View file contents one screen at a time",
        "man_url": "https://man7.org/linux/man-pages/man1/more.1.html",
        "flags": {},
        "common_patterns": ["more file.txt"],
    },
    "clear": {
        "description": "Clear terminal screen",
        "man_url": "https://man7.org/linux/man-pages/man1/clear.1.html",
        "flags": {},
        "common_patterns": ["clear"],
    },
    "man": {
        "description": "Display manual pages for commands",
        "man_url": "https://man7.org/linux/man-pages/man1/man.1.html",
        "flags": {
            "-k": "Search manual page names and descriptions",
        },
        "common_patterns": ["man ls", "man -k keyword"],
    },
    "ping": {
        "description": "Send ICMP ECHO_REQUEST packets to network hosts",
        "man_url": "https://man7.org/linux/man-pages/man8/ping.8.html",
        "flags": {
            "-c": "Stop after N packets",
            "-i": "Interval between packets (seconds)",
        },
        "common_patterns": ["ping google.com", "ping -c 4 google.com"],
    },
    "netstat": {
        "description": "Network statistics and connections",
        "man_url": "https://man7.org/linux/man-pages/man8/netstat.8.html",
        "flags": {
            "-t": "TCP connections",
            "-u": "UDP connections",
            "-l": "Listening sockets only",
            "-p": "Show PID/program name",
            "-n": "Numeric addresses (no DNS)",
        },
        "common_patterns": ["netstat -tlnp", "netstat -an | grep LISTEN"],
    },
    "ss": {
        "description": "Socket statistics (modern netstat replacement)",
        "man_url": "https://man7.org/linux/man-pages/man8/ss.8.html",
        "flags": {
            "-t": "TCP sockets",
            "-u": "UDP sockets",
            "-l": "Listening sockets",
            "-n": "Numeric (no resolve)",
            "-p": "Show processes",
        },
        "common_patterns": ["ss -tlnp", "ss -tulnp"],
    },
    "make": {
        "description": "Build automation tool",
        "man_url": "https://www.gnu.org/software/make/manual/make.html",
        "flags": {
            "-f": "Use specified Makefile",
            "-j": "Parallel jobs",
            "-n": "Dry run",
        },
        "common_patterns": ["make", "make target", "make -j4", "make clean"],
    },
    "tsc": {
        "description": "TypeScript compiler",
        "man_url": "https://www.typescriptlang.org/docs/handbook/compiler-options.html",
        "flags": {
            "-w": "Watch mode",
            "--init": "Create tsconfig.json",
            "--noEmit": "Check without emitting",
        },
        "common_patterns": ["tsc", "tsc --init", "tsc -w"],
    },
    "eslint": {
        "description": "JavaScript/TypeScript linter",
        "man_url": "https://eslint.org/docs/user-guide/command-line-interface",
        "flags": {
            "--fix": "Automatically fix problems",
            "--ext": "File extensions to lint",
        },
        "common_patterns": ["eslint .", "eslint --fix ."],
    },
    "prettier": {
        "description": "Code formatter",
        "man_url": "https://prettier.io/docs/en/cli.html",
        "flags": {
            "--write": "Write changes to file",
            "--check": "Check if files are formatted",
        },
        "common_patterns": ["prettier --write .", "prettier --check ."],
    },
    "pytest": {
        "description": "Python testing framework",
        "man_url": "https://docs.pytest.org/en/stable/reference/reference.html",
        "flags": {
            "-v": "Verbose output",
            "-x": "Stop on first failure",
            "-k": "Filter tests by expression",
            "--cov": "Coverage report",
        },
        "common_patterns": ["pytest", "pytest -v", "pytest --cov=src"],
    },
    "jest": {
        "description": "JavaScript testing framework",
        "man_url": "https://jestjs.io/docs/cli",
        "flags": {
            "--watch": "Watch mode",
            "--coverage": "Collect coverage",
        },
        "common_patterns": ["jest", "jest --watch", "jest --coverage"],
    },
    "killall": {
        "description": "Kill processes by name",
        "man_url": "https://man7.org/linux/man-pages/man1/killall.1.html",
        "flags": {
            "-9": "SIGKILL - force kill",
            "-i": "Interactive, ask before killing",
        },
        "common_patterns": ["killall process-name", "killall -9 hung-process"],
    },
    "pkill": {
        "description": "Signal processes based on pattern matching",
        "man_url": "https://man7.org/linux/man-pages/man1/pkill.1.html",
        "flags": {
            "-f": "Match against full command line",
            "-9": "Send SIGKILL",
        },
        "common_patterns": ["pkill -f 'node server'", "pkill -9 hung-process"],
    },
    "pgrep": {
        "description": "Find processes based on pattern matching",
        "man_url": "https://man7.org/linux/man-pages/man1/pgrep.1.html",
        "flags": {
            "-f": "Match against full command line",
            "-l": "List process name and ID",
        },
        "common_patterns": ["pgrep -f 'node'", "pgrep -l python"],
    },
    "htop": {
        "description": "Interactive process viewer (improved top)",
        "man_url": "https://htop.dev/",
        "flags": {
            "-u": "Show only processes for specified user",
            "-t": "Tree view",
        },
        "common_patterns": ["htop", "htop -u username"],
    },
    "whereis": {
        "description": "Locate binary, source, and manual pages for command",
        "man_url": "https://man7.org/linux/man-pages/man1/whereis.1.html",
        "flags": {
            "-b": "Search for binaries only",
            "-m": "Search for manual pages only",
        },
        "common_patterns": ["whereis python", "whereis -b node"],
    },
    "type": {
        "description": "Describe how command name would be interpreted",
        "man_url": "https://www.gnu.org/software/bash/manual/html_node/Bash-Builtins.html",
        "flags": {
            "-a": "Display all locations",
            "-t": "Print single word (alias, keyword, function, builtin, file)",
        },
        "common_patterns": ["type ls", "type -a python"],
    },
    "printf": {
        "description": "Format and print data",
        "man_url": "https://man7.org/linux/man-pages/man1/printf.1.html",
        "flags": {},
        "common_patterns": ["printf '%s\\n' 'Hello'", "printf '%d\\n' 42"],
    },
    "true": {
        "description": "Return exit status 0 (success)",
        "man_url": "https://man7.org/linux/man-pages/man1/true.1.html",
        "flags": {},
        "common_patterns": ["while true; do command; sleep 1; done"],
    },
    "false": {
        "description": "Return exit status 1 (failure)",
        "man_url": "https://man7.org/linux/man-pages/man1/false.1.html",
        "flags": {},
        "common_patterns": ["false || echo 'command failed'"],
    },
    "umask": {
        "description": "Set default file creation permissions mask",
        "man_url": "https://man7.org/linux/man-pages/man2/umask.2.html",
        "flags": {
            "-S": "Display mask in symbolic form",
        },
        "common_patterns": ["umask", "umask 022", "umask -S"],
    },
    "chgrp": {
        "description": "Change group ownership",
        "man_url": "https://man7.org/linux/man-pages/man1/chgrp.1.html",
        "flags": {
            "-R": "Recursive change",
        },
        "common_patterns": ["chgrp group file.txt", "chgrp -R group directory/"],
    },
    "bzip2": {
        "description": "Block-sorting file compressor",
        "man_url": "https://man7.org/linux/man-pages/man1/bzip2.1.html",
        "flags": {
            "-d": "Decompress",
            "-k": "Keep original file",
            "-9": "Best compression",
        },
        "common_patterns": ["bzip2 file.txt", "bzip2 -d file.txt.bz2"],
    },
    "xz": {
        "description": "High-ratio file compressor using LZMA2",
        "man_url": "https://man7.org/linux/man-pages/man1/xz.1.html",
        "flags": {
            "-d": "Decompress",
            "-k": "Keep original file",
            "-9": "Best compression",
        },
        "common_patterns": ["xz file.txt", "xz -d file.txt.xz"],
    },
    "cal": {
        "description": "Display calendar",
        "man_url": "https://man7.org/linux/man-pages/man1/cal.1.html",
        "flags": {
            "-y": "Display whole year",
            "-3": "Display previous, current, and next month",
        },
        "common_patterns": ["cal", "cal -y", "cal 12 2024"],
    },
    "yes": {
        "description": "Output string repeatedly until killed",
        "man_url": "https://man7.org/linux/man-pages/man1/yes.1.html",
        "flags": {},
        "common_patterns": ["yes | command", "yes n | rm -i *"],
    },
    "shuf": {
        "description": "Shuffle lines randomly",
        "man_url": "https://man7.org/linux/man-pages/man1/shuf.1.html",
        "flags": {
            "-n": "Output at most N lines",
            "-e": "Treat arguments as input lines",
        },
        "common_patterns": ["shuf file.txt", "shuf -n 1 file.txt"],
    },
    "rev": {
        "description": "Reverse lines character by character",
        "man_url": "https://man7.org/linux/man-pages/man1/rev.1.html",
        "flags": {},
        "common_patterns": ["echo 'hello' | rev", "rev file.txt"],
    },
    "tac": {
        "description": "Concatenate and print files in reverse",
        "man_url": "https://man7.org/linux/man-pages/man1/tac.1.html",
        "flags": {},
        "common_patterns": ["tac file.txt"],
    },
    "nl": {
        "description": "Number lines of files",
        "man_url": "https://man7.org/linux/man-pages/man1/nl.1.html",
        "flags": {
            "-b": "Body numbering style (a=all, t=non-empty)",
        },
        "common_patterns": ["nl file.txt", "nl -ba file.txt"],
    },
    "paste": {
        "description": "Merge lines of files",
        "man_url": "https://man7.org/linux/man-pages/man1/paste.1.html",
        "flags": {
            "-d": "Delimiter characters",
            "-s": "Paste one file at a time",
        },
        "common_patterns": ["paste file1.txt file2.txt", "paste -d',' file1.txt file2.txt"],
    },
    "join": {
        "description": "Join lines of two files on common field",
        "man_url": "https://man7.org/linux/man-pages/man1/join.1.html",
        "flags": {
            "-t": "Field separator",
        },
        "common_patterns": ["join file1.txt file2.txt"],
    },
    "comm": {
        "description": "Compare two sorted files line by line",
        "man_url": "https://man7.org/linux/man-pages/man1/comm.1.html",
        "flags": {
            "-1": "Suppress column 1 (lines unique to file1)",
            "-2": "Suppress column 2 (lines unique to file2)",
            "-3": "Suppress column 3 (lines common to both)",
        },
        "common_patterns": ["comm file1.txt file2.txt", "comm -12 file1.txt file2.txt"],
    },
    "split": {
        "description": "Split file into pieces",
        "man_url": "https://man7.org/linux/man-pages/man1/split.1.html",
        "flags": {
            "-l": "Lines per output file",
            "-b": "Bytes per output file",
            "-d": "Use numeric suffixes",
        },
        "common_patterns": ["split -l 1000 file.txt", "split -b 10M file.bin"],
    },
    "column": {
        "description": "Format output into columns",
        "man_url": "https://man7.org/linux/man-pages/man1/column.1.html",
        "flags": {
            "-t": "Create table",
            "-s": "Separator characters",
        },
        "common_patterns": ["column -t file.txt", "mount | column -t"],
    },
}


# =============================================================================
# OPERATORS DATABASE
# =============================================================================

OPERATORS: Dict[str, Dict[str, str]] = {
    "|": {
        "name": "Pipe",
        "description": "Send stdout of left command to stdin of right command",
        "example": "ls -la | grep '.txt'",
        "use_case": "Chain commands together, filtering or transforming output",
    },
    ">": {
        "name": "Redirect stdout (overwrite)",
        "description": "Redirect stdout to file, overwriting existing content",
        "example": "echo 'hello' > file.txt",
        "use_case": "Save command output to file, replacing previous content",
    },
    ">>": {
        "name": "Redirect stdout (append)",
        "description": "Redirect stdout to file, appending to existing content",
        "example": "echo 'new line' >> file.txt",
        "use_case": "Add command output to end of file without losing existing data",
    },
    "2>": {
        "name": "Redirect stderr",
        "description": "Redirect stderr to file",
        "example": "command 2> errors.log",
        "use_case": "Capture error messages separately from normal output",
    },
    "2>&1": {
        "name": "Redirect stderr to stdout",
        "description": "Send stderr to the same destination as stdout",
        "example": "command > output.log 2>&1",
        "use_case": "Capture both normal output and errors in same file/stream",
    },
    "&>": {
        "name": "Redirect both stdout and stderr",
        "description": "Redirect both stdout and stderr to file (bash shorthand)",
        "example": "command &> all_output.log",
        "use_case": "Capture all output in one file (bash 4+ only)",
    },
    "&&": {
        "name": "AND operator",
        "description": "Execute right command only if left command succeeds (exit code 0)",
        "example": "mkdir dir && cd dir",
        "use_case": "Chain dependent commands; second runs only if first succeeds",
    },
    "||": {
        "name": "OR operator",
        "description": "Execute right command only if left command fails (non-zero exit)",
        "example": "git pull || echo 'Pull failed'",
        "use_case": "Provide fallback action when command fails",
    },
    ";": {
        "name": "Command separator",
        "description": "Execute commands sequentially regardless of exit status",
        "example": "cd /tmp; ls; cd -",
        "use_case": "Run multiple commands in sequence, ignoring failures",
    },
    "&": {
        "name": "Background operator",
        "description": "Run command in background, returning control to shell",
        "example": "long_running_command &",
        "use_case": "Start process without waiting for it to complete",
    },
    "$()": {
        "name": "Command substitution",
        "description": "Execute command and substitute its output in place",
        "example": "echo \"Today is $(date)\"",
        "use_case": "Use command output as argument or in string",
    },
    "``": {
        "name": "Command substitution (legacy)",
        "description": "Legacy syntax for command substitution (prefer $())",
        "example": "echo \"Today is `date`\"",
        "use_case": "Same as $() but less readable; avoid in new scripts",
    },
    "<": {
        "name": "Input redirect",
        "description": "Use file as stdin for command",
        "example": "sort < unsorted.txt",
        "use_case": "Feed file content as input to command",
    },
    "<<": {
        "name": "Here document",
        "description": "Multi-line input until delimiter is encountered",
        "example": "cat << EOF\\nline 1\\nline 2\\nEOF",
        "use_case": "Embed multi-line text or create config files in scripts",
    },
    "<<<": {
        "name": "Here string",
        "description": "Pass string as stdin to command",
        "example": "grep 'pattern' <<< 'search in this text'",
        "use_case": "Pass string to command expecting stdin without echo pipe",
    },
    "|&": {
        "name": "Pipe stdout and stderr",
        "description": "Pipe both stdout and stderr to next command",
        "example": "command |& tee output.log",
        "use_case": "Process both output streams together",
    },
}


# =============================================================================
# BASH CONCEPTS
# =============================================================================

CONCEPTS: Dict[str, Dict[str, Any]] = {
    "pipes": {
        "title": "Pipes and Pipelines",
        "description": "Pipes connect the output of one command to the input of another, allowing you to chain commands together into powerful data processing pipelines.",
        "key_points": [
            "Pipes connect stdout to stdin",
            "Data flows left to right through the pipeline",
            "Each command in the pipeline runs in its own process",
            "Exit status is typically that of the last command",
        ],
        "examples": [
            {"code": "cat file.txt | grep 'pattern' | sort | uniq -c", "explanation": "Read file, filter lines, sort, count unique"},
            {"code": "ps aux | grep python | awk '{print $2}'", "explanation": "List processes, filter for python, extract PID"},
        ],
    },
    "redirects": {
        "title": "I/O Redirection",
        "description": "Redirection allows you to control where command input comes from and where output goes.",
        "key_points": [
            "File descriptors: 0=stdin, 1=stdout, 2=stderr",
            "> overwrites file, >> appends to file",
            "< reads from file as stdin",
            "2>&1 redirects stderr to stdout destination",
        ],
        "examples": [
            {"code": "command > output.txt 2>&1", "explanation": "Send both stdout and stderr to output.txt"},
            {"code": "command 2>/dev/null", "explanation": "Discard error messages"},
        ],
    },
    "exit_codes": {
        "title": "Exit Codes and Status",
        "description": "Every command returns an exit status (0-255). By convention, 0 means success and non-zero indicates failure.",
        "key_points": [
            "Exit 0 = success, non-zero = failure",
            "$? contains the exit status of the last command",
            "&& executes next command only if previous succeeded",
            "|| executes next command only if previous failed",
        ],
        "common_codes": {
            0: "Success",
            1: "General error",
            2: "Misuse of shell builtin",
            126: "Command invoked cannot execute",
            127: "Command not found",
            130: "Terminated by Ctrl+C (128+2)",
        },
    },
    "globbing": {
        "title": "Glob Patterns (Wildcards)",
        "description": "Glob patterns allow matching multiple files using wildcards. The shell expands globs before passing arguments to commands.",
        "key_points": [
            "* matches any characters (except leading dot)",
            "? matches exactly one character",
            "[abc] matches any character in brackets",
            "[a-z] matches any character in range",
            "** matches directories recursively (with globstar)",
        ],
        "examples": [
            {"code": "ls *.txt", "explanation": "List all .txt files"},
            {"code": "rm file?.log", "explanation": "Remove file1.log, file2.log, etc."},
        ],
    },
    "quoting": {
        "title": "Quoting and Escaping",
        "description": "Quoting controls how the shell interprets special characters.",
        "key_points": [
            "Single quotes: everything is literal (no expansion)",
            "Double quotes: variables and commands expand, spaces preserved",
            "Backslash: escape single character",
            "Always quote variables: \"$var\" not $var",
        ],
        "examples": [
            {"code": "echo '$HOME'", "explanation": "Prints literal $HOME"},
            {"code": "echo \"$HOME\"", "explanation": "Prints the value of HOME variable"},
        ],
    },
    "variable_expansion": {
        "title": "Variable and Parameter Expansion",
        "description": "Variables store values that can be expanded in commands. Bash provides powerful parameter expansion features.",
        "key_points": [
            "Set: VAR=value (no spaces around =)",
            "Use: $VAR or ${VAR}",
            "Export for child processes: export VAR",
            "Special variables: $?, $#, $@, $*, $$, $!",
        ],
        "expansions": {
            "${VAR:-default}": "Use default if VAR is unset or null",
            "${VAR:=default}": "Set and use default if VAR is unset or null",
            "${#VAR}": "Length of variable value",
            "${VAR%pattern}": "Remove shortest suffix match",
            "${VAR##pattern}": "Remove longest prefix match",
        },
    },
}


# =============================================================================
# CATEGORY DESCRIPTIONS
# =============================================================================

CATEGORY_DESCRIPTIONS: Dict[str, str] = {
    "File System": "Commands for navigating, viewing, creating, and managing files and directories",
    "Text Processing": "Commands for viewing, searching, filtering, and transforming text content",
    "Git": "Version control system commands for tracking changes and collaboration",
    "Package Management": "Package managers for installing, updating, and managing software dependencies",
    "Process & System": "Commands for monitoring, managing, and controlling running processes",
    "Networking": "Commands for network operations, file transfers, and remote access",
    "Permissions": "Commands for managing file ownership and access permissions",
    "Compression": "Commands for compressing, archiving, and extracting files",
    "Development": "Development tools for building, testing, and running code",
    "Shell Builtins": "Built-in shell commands for scripting and interactive use",
    "Search & Navigation": "Commands for finding files and navigating the filesystem",
}


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_command_info(name: str) -> Dict[str, Any] | None:
    """Get comprehensive command information by name."""
    return COMMAND_DB.get(name)


def get_operator(symbol: str) -> Dict[str, str] | None:
    """Get operator information by symbol."""
    return OPERATORS.get(symbol)


def get_concept(name: str) -> Dict[str, Any] | None:
    """Get concept explanation by name."""
    return CONCEPTS.get(name)


def get_flags_for_command(command: str) -> Dict[str, str]:
    """Get all flags for a command."""
    cmd = COMMAND_DB.get(command, {})
    return cmd.get("flags", {})


def get_common_patterns(command: str) -> List[str]:
    """Get common usage patterns for a command."""
    cmd = COMMAND_DB.get(command, {})
    return cmd.get("common_patterns", [])


def search_commands(query: str) -> List[str]:
    """Search commands by name or description."""
    query_lower = query.lower()
    results = []
    for name, info in COMMAND_DB.items():
        if query_lower in name.lower():
            results.append(name)
        elif query_lower in info.get("description", "").lower():
            results.append(name)
    return results


def get_stats() -> Dict[str, int]:
    """Get statistics about the knowledge base."""
    total_flags = sum(len(cmd.get("flags", {})) for cmd in COMMAND_DB.values())
    total_patterns = sum(len(cmd.get("common_patterns", [])) for cmd in COMMAND_DB.values())
    return {
        "total_commands": len(COMMAND_DB),
        "total_operators": len(OPERATORS),
        "total_concepts": len(CONCEPTS),
        "total_categories": len(set(CATEGORY_MAPPINGS.keys())),
        "total_flags": total_flags,
        "total_patterns": total_patterns,
    }


if __name__ == "__main__":
    stats = get_stats()
    print("Knowledge Base Statistics:")
    print(f"  Commands in COMMAND_DB: {stats['total_commands']}")
    print(f"  Operators: {stats['total_operators']}")
    print(f"  Concepts: {stats['total_concepts']}")
    print(f"  Categories: {stats['total_categories']}")
    print(f"  Total flags documented: {stats['total_flags']}")
    print(f"  Total patterns: {stats['total_patterns']}")
