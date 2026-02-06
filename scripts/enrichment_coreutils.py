"""
Enrichment data for Coreutils, File Management, User/Group Administration,
Scheduling, Security, and Debugging commands.

This module provides supplemental fields (use_cases, gotchas, man_url, related,
difficulty, extra_flags) for thin entries in the COMMAND_DB knowledge base.

Sources consulted:
  - man7.org Linux man-pages: https://man7.org/linux/man-pages/dir_section_1.html
  - GNU Coreutils documentation: https://www.gnu.org/software/coreutils/manual/
  - Official project documentation (git-scm.com, docs.docker.com, etc.)
  - Greg's Wiki / BashPitfalls: https://mywiki.wooledge.org/BashPitfalls
"""

ENRICHMENT_DATA = {
    # =========================================================================
    # TEXT PROCESSING & FILTERING
    # =========================================================================
    "awk": {
        "man_url": "https://man7.org/linux/man-pages/man1/awk.1p.html",
        "use_cases": [
            "Extract and reformat columns from structured text: awk '{print $1, $3}' file.txt",
            "Compute column sums or averages: awk '{sum+=$2} END{print sum}' data.csv",
            "Filter lines matching a pattern: awk '/ERROR/ {print FILENAME, NR, $0}' *.log",
            "Transform delimited data: awk -F',' '{print $2\": \"$4}' input.csv",
        ],
        "gotchas": [
            "Field separator -F is a regex, so -F'.' splits on every character -- use -F'\\.' for literal dots",
            "Uninitialized variables default to 0 or empty string depending on context, which can mask bugs",
            "POSIX awk and gawk differ significantly -- gawk extensions like FPAT and arrays-of-arrays are not portable",
        ],
        "related": ["sed", "cut", "grep", "gawk"],
        "difficulty": "intermediate",
        "extra_flags": {
            "-v": "Assign a variable before execution begins: awk -v OFS='\\t'",
            "-F": "Set the input field separator (can be a regex)",
            "-f": "Read the awk program from a file instead of the command line",
        },
    },
    "cat": {
        "man_url": "https://man7.org/linux/man-pages/man1/cat.1.html",
        "use_cases": [
            "Display file contents quickly: cat /etc/hostname",
            "Concatenate multiple files: cat part1.txt part2.txt > combined.txt",
            "Create small files with heredoc: cat <<'EOF' > config.yml",
        ],
        "gotchas": [
            "Useless use of cat: prefer redirection over 'cat file | cmd' -- use 'cmd < file' instead",
            "No pagination for large files -- use less or more instead",
        ],
        "related": ["less", "head", "tail", "tac"],
        "difficulty": "beginner",
        "extra_flags": {
            "-A": "Show all non-printing characters including line endings ($) and tabs (^I)",
            "-n": "Number all output lines",
            "-s": "Squeeze multiple adjacent blank lines into one",
        },
    },
    "cut": {
        "man_url": "https://man7.org/linux/man-pages/man1/cut.1.html",
        "use_cases": [
            "Extract specific columns from CSV: cut -d',' -f1,3 data.csv",
            "Pull usernames from /etc/passwd: cut -d: -f1 /etc/passwd",
            "Extract character ranges: cut -c1-10 file.txt",
        ],
        "gotchas": [
            "cut cannot reorder fields -- cut -f3,1 outputs fields in file order (1 then 3), not 3 then 1",
            "cut does not support multi-character delimiters -- use awk for that",
            "Fields beyond the last delimiter are included in the last field, which can give unexpected results",
        ],
        "related": ["awk", "paste", "tr", "sed"],
        "difficulty": "beginner",
        "extra_flags": {
            "-d": "Set the field delimiter (default is TAB)",
            "-f": "Select fields by number or range",
            "--complement": "Invert the selection (print all fields except specified)",
            "--output-delimiter": "Use a different delimiter for output",
        },
    },
    "grep": {
        "man_url": "https://man7.org/linux/man-pages/man1/grep.1.html",
        "use_cases": [
            "Search for patterns in files: grep -rn 'TODO' src/",
            "Filter command output: ps aux | grep nginx",
            "Find files containing a string: grep -rl 'api_key' /etc/",
            "Count occurrences: grep -c 'error' application.log",
        ],
        "gotchas": [
            "grep pattern is BRE by default -- use -E for extended regex or -P for Perl regex",
            "'grep pattern | grep -v grep' is a common antipattern -- use pgrep or brackets: grep '[n]ginx'",
            "Binary file matches are suppressed by default -- use -a to force text mode or --binary-files=text",
        ],
        "related": ["egrep", "fgrep", "sed", "awk"],
        "difficulty": "beginner",
        "extra_flags": {
            "-P": "Use Perl-compatible regex (PCRE) for lookaheads and other advanced patterns",
            "-o": "Print only the matching part of each line",
            "-A": "Print N lines after each match",
            "-B": "Print N lines before each match",
            "-C": "Print N lines of context around each match",
            "--include": "Search only files matching a glob pattern",
        },
    },
    "egrep": {
        "man_url": "https://man7.org/linux/man-pages/man1/grep.1.html",
        "use_cases": [
            "Search with extended regex without escaping: egrep '(error|warning|critical)' log.txt",
            "Match complex patterns: egrep '^[0-9]{1,3}\\.' access.log",
            "Filter with alternation: egrep 'GET|POST|PUT' access.log",
        ],
        "gotchas": [
            "egrep is deprecated -- use grep -E instead for forward compatibility",
            "Some systems may remove egrep in future releases",
        ],
        "related": ["grep", "fgrep", "sed", "awk"],
        "difficulty": "beginner",
    },
    "fgrep": {
        "man_url": "https://man7.org/linux/man-pages/man1/grep.1.html",
        "use_cases": [
            "Search for literal strings with special characters: fgrep 'price=$9.99' orders.txt",
            "Fast multi-pattern search from a file: fgrep -f patterns.txt data.txt",
            "Search for strings containing regex metacharacters without escaping",
        ],
        "gotchas": [
            "fgrep is deprecated -- use grep -F instead for forward compatibility",
            "Cannot use any regex features -- patterns are strictly literal",
        ],
        "related": ["grep", "egrep", "strings", "awk"],
        "difficulty": "beginner",
    },
    "gawk": {
        "man_url": "https://www.gnu.org/software/gawk/manual/gawk.html",
        "use_cases": [
            "Use GNU-specific features like FPAT for CSV parsing: gawk -v FPAT='[^,]*|\"[^\"]*\"'",
            "Process multi-dimensional arrays: gawk '{a[$1][$2]+=$3}'",
            "Use networking with /inet/tcp for simple socket programming",
            "Profile awk scripts with --profile for performance analysis",
        ],
        "gotchas": [
            "gawk extensions are not portable to mawk or nawk -- avoid them in scripts that must run on BSD or macOS",
            "The @include directive and @namespace are gawk-only features",
            "gawk is significantly slower than mawk for simple text processing tasks",
        ],
        "related": ["awk", "sed", "perl", "cut"],
        "difficulty": "intermediate",
        "extra_flags": {
            "--csv": "Enable proper CSV parsing mode (gawk 5.3+)",
            "--sandbox": "Disable I/O redirection and system() for safe execution",
            "-i": "Include a source library (e.g., -i inplace for in-place editing)",
        },
    },
    "head": {
        "man_url": "https://man7.org/linux/man-pages/man1/head.1.html",
        "use_cases": [
            "Preview the first lines of a file: head -n 20 large_file.log",
            "Display all but the last N lines: head -n -5 file.txt",
            "Quickly check CSV headers: head -1 data.csv",
        ],
        "gotchas": [
            "head -n -N (exclude last N lines) requires reading the entire file, so it is slow on huge files",
            "Default is 10 lines, which may not be enough to see the structure of a file",
        ],
        "related": ["tail", "less", "cat", "sed"],
        "difficulty": "beginner",
        "extra_flags": {
            "-c": "Print the first N bytes instead of lines",
            "-q": "Suppress headers when printing multiple files",
        },
    },
    "sed": {
        "man_url": "https://man7.org/linux/man-pages/man1/sed.1.html",
        "use_cases": [
            "Find and replace text in files: sed -i 's/old/new/g' file.txt",
            "Delete lines matching a pattern: sed '/^#/d' config.conf",
            "Extract lines by range: sed -n '10,20p' file.txt",
            "Insert text before or after a line: sed '/pattern/a\\new line' file.txt",
        ],
        "gotchas": [
            "sed -i behaves differently on macOS (BSD) vs Linux (GNU) -- macOS requires -i '' while GNU uses -i alone",
            "The delimiter in s/// can be any character -- use s|old|new| when paths contain slashes",
            "Greedy matching is the default and there is no non-greedy quantifier -- use [^/]* instead of .*",
        ],
        "related": ["awk", "grep", "tr", "perl"],
        "difficulty": "intermediate",
        "extra_flags": {
            "-E": "Use extended regular expressions (ERE) instead of basic (BRE)",
            "-n": "Suppress automatic printing -- only print when explicitly told via p command",
            "-z": "Use NUL as line separator for processing NUL-delimited data",
        },
    },
    "sort": {
        "man_url": "https://man7.org/linux/man-pages/man1/sort.1.html",
        "use_cases": [
            "Sort files alphabetically or numerically: sort -n numbers.txt",
            "Sort by specific column: sort -t',' -k3,3n data.csv",
            "Remove duplicates while sorting: sort -u names.txt",
            "Sort human-readable sizes: du -sh * | sort -h",
        ],
        "gotchas": [
            "Locale affects sort order -- use LC_ALL=C for byte-order sorting and reproducible results",
            "Numeric sort -n only works on leading numbers -- use -k to sort by a specific field",
            "sort -u compares entire lines, not just the sort key -- use sort | uniq for key-based dedup",
        ],
        "related": ["uniq", "cut", "awk", "tsort"],
        "difficulty": "beginner",
        "extra_flags": {
            "-h": "Sort human-readable numbers like 2K, 1G",
            "-V": "Version-number sort (e.g., 1.2 before 1.10)",
            "-S": "Set the main-memory buffer size for large sorts",
            "-t": "Set the field separator character",
            "-k": "Sort by a specific key/field",
            "-s": "Stabilize sort by disabling last-resort comparison",
        },
    },
    "tail": {
        "man_url": "https://man7.org/linux/man-pages/man1/tail.1.html",
        "use_cases": [
            "Follow a log file in real time: tail -f /var/log/syslog",
            "Show the last N lines: tail -n 50 application.log",
            "Skip the first N lines (start from line N+1): tail -n +2 data.csv",
            "Follow multiple log files simultaneously: tail -f *.log",
        ],
        "gotchas": [
            "tail -f does not follow log rotation -- use tail -F (or tail --follow=name) to handle rotated files",
            "tail -n +N starts from line N, not after N lines -- tail -n +1 prints the entire file",
            "Piping tail -f can buffer output -- use --pid to stop when a process exits",
        ],
        "related": ["head", "less", "cat", "multitail"],
        "difficulty": "beginner",
        "extra_flags": {
            "-F": "Follow by name and retry if file is rotated or recreated",
            "-c": "Output the last N bytes instead of lines",
            "--pid": "Terminate after process PID dies (useful with -f)",
        },
    },
    "tee": {
        "man_url": "https://man7.org/linux/man-pages/man1/tee.1.html",
        "use_cases": [
            "Log output while still displaying it: make 2>&1 | tee build.log",
            "Write to a file requiring sudo: echo 'line' | sudo tee /etc/config",
            "Split output to multiple files: cmd | tee file1.txt file2.txt",
        ],
        "gotchas": [
            "tee overwrites by default -- use -a to append instead of truncating",
            "tee buffers output which can delay display -- use stdbuf -oL for line buffering",
            "Exit status reflects tee's success, not the upstream command's",
        ],
        "related": ["cat", "script", "sponge", "redirect"],
        "difficulty": "beginner",
        "extra_flags": {
            "-a": "Append to files instead of overwriting",
            "-p": "Diagnose errors writing to non-pipes (GNU extension)",
        },
    },
    "tr": {
        "man_url": "https://man7.org/linux/man-pages/man1/tr.1.html",
        "use_cases": [
            "Convert case: echo 'hello' | tr 'a-z' 'A-Z'",
            "Delete specific characters: tr -d '\\r' < file.txt (remove carriage returns)",
            "Squeeze repeated characters: tr -s ' ' (collapse multiple spaces)",
        ],
        "gotchas": [
            "tr only works on stdin -- it cannot read files directly, so use redirection: tr 'a' 'b' < file",
            "tr operates on individual characters, not strings -- tr 'abc' 'xyz' maps a->x, b->y, c->z",
            "Character ranges depend on locale -- use LC_ALL=C for consistent behavior",
        ],
        "related": ["sed", "cut", "awk", "iconv"],
        "difficulty": "beginner",
        "extra_flags": {
            "-d": "Delete characters in SET1 from input",
            "-s": "Squeeze repeated characters in the last specified set to a single character",
            "-c": "Complement SET1 (operate on characters NOT in SET1)",
        },
    },
    "uniq": {
        "man_url": "https://man7.org/linux/man-pages/man1/uniq.1.html",
        "use_cases": [
            "Remove adjacent duplicate lines: sort file.txt | uniq",
            "Count occurrences of each line: sort data.txt | uniq -c | sort -rn",
            "Show only duplicate lines: sort names.txt | uniq -d",
        ],
        "gotchas": [
            "uniq only removes ADJACENT duplicates -- input must be sorted first or duplicates will be missed",
            "uniq -c adds leading whitespace to counts, which can break downstream parsing",
            "Field and character skipping (-f, -s) use 1-based indexing",
        ],
        "related": ["sort", "awk", "comm", "wc"],
        "difficulty": "beginner",
        "extra_flags": {
            "-c": "Prefix lines with the count of occurrences",
            "-d": "Only print duplicate lines (one copy each)",
            "-u": "Only print unique lines (lines that are not duplicated)",
            "-i": "Ignore case when comparing lines",
        },
    },
    "wc": {
        "man_url": "https://man7.org/linux/man-pages/man1/wc.1.html",
        "use_cases": [
            "Count lines in a file: wc -l access.log",
            "Count words in a document: wc -w essay.txt",
            "Count files in a directory: ls | wc -l",
        ],
        "gotchas": [
            "wc -l counts newline characters, so a file without a trailing newline reports one fewer line than expected",
            "wc includes the filename in output when given arguments -- use < redirection for just the number",
        ],
        "related": ["cat", "awk", "grep", "sort"],
        "difficulty": "beginner",
        "extra_flags": {
            "-c": "Print byte count",
            "-m": "Print character count (differs from -c for multibyte encodings)",
            "-L": "Print length of the longest line",
        },
    },
    "xargs": {
        "man_url": "https://man7.org/linux/man-pages/man1/xargs.1.html",
        "use_cases": [
            "Delete files found by find: find . -name '*.tmp' -print0 | xargs -0 rm",
            "Run commands in parallel: find . -name '*.png' | xargs -P4 -I{} convert {} {}.webp",
            "Pass grep results as arguments: grep -rl 'TODO' | xargs sed -i 's/TODO/DONE/g'",
        ],
        "gotchas": [
            "Filenames with spaces or special chars break xargs -- always use -0 with find -print0",
            "xargs splits on whitespace and newlines by default, which is unsafe for arbitrary filenames",
            "The -I flag disables parallelism and implies -L1 -- combine with -P for parallel + replacement",
        ],
        "related": ["find", "parallel", "exec", "tee"],
        "difficulty": "intermediate",
        "extra_flags": {
            "-0": "Use NUL as delimiter (pair with find -print0)",
            "-P": "Run up to N processes in parallel",
            "-I": "Replace occurrences of the placeholder with each input line",
            "-n": "Use at most N arguments per command invocation",
            "-t": "Print each command before executing (trace mode)",
        },
    },

    # =========================================================================
    # FILE SYSTEM NAVIGATION & MANAGEMENT
    # =========================================================================
    "cd": {
        "man_url": "https://www.gnu.org/software/bash/manual/bash.html#index-cd",
        "use_cases": [
            "Navigate to a directory: cd /var/log",
            "Return to previous directory: cd -",
            "Go to home directory: cd or cd ~",
        ],
        "gotchas": [
            "cd in a subshell or pipe does not affect the parent shell's working directory",
            "cd without error checking in scripts can cause commands to run in the wrong directory -- always use cd dir || exit 1",
            "Symlinks can make pwd show a different path than expected -- use cd -P to resolve physical paths",
        ],
        "related": ["pwd", "pushd", "popd", "dirs"],
        "difficulty": "beginner",
    },
    "cmp": {
        "man_url": "https://man7.org/linux/man-pages/man1/cmp.1.html",
        "use_cases": [
            "Check if two binary files are identical: cmp file1.bin file2.bin",
            "Find the first differing byte: cmp -l original.bin modified.bin",
            "Silent comparison for scripting: cmp -s a.bin b.bin && echo same",
        ],
        "gotchas": [
            "cmp compares bytes, not lines -- use diff for human-readable text comparison",
            "cmp stops at the first difference by default -- use -l to list all differing bytes",
        ],
        "related": ["diff", "md5sum", "sha256sum", "comm"],
        "difficulty": "beginner",
        "extra_flags": {
            "-s": "Silent mode -- return exit status only, no output",
            "-l": "Print byte number and differing byte values for all differences",
            "-n": "Compare at most N bytes",
        },
    },
    "cp": {
        "man_url": "https://man7.org/linux/man-pages/man1/cp.1.html",
        "use_cases": [
            "Copy files preserving attributes: cp -a source/ dest/",
            "Copy with a progress indicator: cp --verbose largefile.iso /backup/",
            "Create backups before overwriting: cp --backup=numbered file.conf /etc/",
            "Recursively copy directories: cp -r project/ project-backup/",
        ],
        "gotchas": [
            "cp without -r silently skips directories instead of erroring in some versions",
            "cp overwrites destination files without warning unless -i is used",
            "Symlinks are followed by default -- use -a or -d to preserve symlink structure",
        ],
        "related": ["mv", "rsync", "scp", "install"],
        "difficulty": "beginner",
        "extra_flags": {
            "-a": "Archive mode: preserve all attributes, recurse, and copy symlinks",
            "-u": "Copy only when source is newer than destination or destination is missing",
            "--reflink": "Use copy-on-write if supported by the filesystem (instant, space-efficient)",
        },
    },
    "df": {
        "man_url": "https://man7.org/linux/man-pages/man1/df.1.html",
        "use_cases": [
            "Check disk space usage: df -h",
            "Show filesystem type: df -T",
            "Check space on a specific mount: df -h /home",
        ],
        "gotchas": [
            "df shows filesystem-level usage, not directory-level -- use du for directory sizes",
            "Reserved blocks (usually 5%) make df and du totals disagree on ext4 filesystems",
            "Deleted-but-open files still consume space until the file handle is closed",
        ],
        "related": ["du", "lsblk", "mount", "findmnt"],
        "difficulty": "beginner",
        "extra_flags": {
            "-h": "Human-readable sizes (KB, MB, GB)",
            "-i": "Show inode usage instead of block usage",
            "-T": "Show filesystem type",
            "--total": "Show a grand total at the bottom",
        },
    },
    "diff": {
        "man_url": "https://man7.org/linux/man-pages/man1/diff.1.html",
        "use_cases": [
            "Compare two files: diff file1.txt file2.txt",
            "Generate a patch file: diff -u original.c modified.c > fix.patch",
            "Compare directories recursively: diff -r dir1/ dir2/",
            "Side-by-side comparison: diff -y file1.txt file2.txt",
        ],
        "gotchas": [
            "diff exit code 1 means differences found (not an error) -- check for exit code 2 for actual errors",
            "Binary files are reported as differing without details -- use cmp -l for byte-level binary diffs",
            "diff -r on large directory trees can be slow -- consider rsync --dry-run for large comparisons",
        ],
        "related": ["cmp", "patch", "sdiff", "comm"],
        "difficulty": "beginner",
        "extra_flags": {
            "-u": "Unified format (most common for patches)",
            "-r": "Recursively compare subdirectories",
            "-q": "Report only whether files differ, not the details",
            "--color": "Colorize the output for terminal viewing",
        },
    },
    "du": {
        "man_url": "https://man7.org/linux/man-pages/man1/du.1.html",
        "use_cases": [
            "Find the largest directories: du -sh /* 2>/dev/null | sort -h",
            "Check directory size: du -sh /var/log",
            "Show disk usage per subdirectory: du -h --max-depth=1 /home",
        ],
        "gotchas": [
            "du measures disk allocation, not file size -- sparse files show smaller than ls -l reports",
            "Hardlinked files may be counted multiple times unless --count-links is avoided",
            "du without -s shows every subdirectory, producing overwhelming output on deep trees",
        ],
        "related": ["df", "ncdu", "ls", "find"],
        "difficulty": "beginner",
        "extra_flags": {
            "-s": "Show only the total for each argument (summary)",
            "-h": "Human-readable sizes",
            "--max-depth": "Limit directory depth for output",
            "--exclude": "Exclude files matching a pattern",
        },
    },
    "find": {
        "man_url": "https://man7.org/linux/man-pages/man1/find.1.html",
        "use_cases": [
            "Find files by name: find /var -name '*.log' -mtime -7",
            "Delete old temp files: find /tmp -type f -mtime +30 -delete",
            "Find large files: find / -type f -size +100M 2>/dev/null",
            "Execute commands on results: find . -name '*.py' -exec pylint {} +",
        ],
        "gotchas": [
            "find without -maxdepth searches the entire subtree, which can be very slow on large filesystems",
            "-exec {} \\; runs one process per file (slow) -- use -exec {} + or pipe to xargs for batching",
            "The order of predicates matters for performance -- put cheap tests like -name before expensive ones like -exec",
        ],
        "related": ["locate", "fd", "xargs", "ls"],
        "difficulty": "intermediate",
        "extra_flags": {
            "-maxdepth": "Limit search depth",
            "-print0": "Output NUL-delimited results for safe piping to xargs -0",
            "-newer": "Find files newer than a reference file",
            "-empty": "Find empty files or directories",
            "-regextype": "Specify regex dialect for -regex (posix-extended, etc.)",
        },
    },
    "ls": {
        "man_url": "https://man7.org/linux/man-pages/man1/ls.1.html",
        "use_cases": [
            "List files with details: ls -lah",
            "Sort by modification time: ls -lt",
            "Show hidden files: ls -A",
            "Recursively list all files: ls -R",
        ],
        "gotchas": [
            "Parsing ls output is fragile and breaks on filenames with spaces or special characters -- use find or globbing instead",
            "ls -l shows apparent file size, not disk usage -- use du for actual disk allocation",
            "Color output can interfere with piping -- use ls --color=never or \\ls in scripts",
        ],
        "related": ["tree", "find", "stat", "file"],
        "difficulty": "beginner",
        "extra_flags": {
            "-S": "Sort by file size, largest first",
            "-h": "Human-readable sizes with -l",
            "-i": "Show inode numbers",
            "--group-directories-first": "List directories before files",
        },
    },
    "mkdir": {
        "man_url": "https://man7.org/linux/man-pages/man1/mkdir.1.html",
        "use_cases": [
            "Create nested directories: mkdir -p /opt/app/config/ssl",
            "Create with specific permissions: mkdir -m 700 /home/user/.ssh",
            "Create multiple directories at once: mkdir -p src/{lib,bin,tests}",
        ],
        "gotchas": [
            "Without -p, mkdir fails if the parent directory does not exist",
            "mkdir -p silently succeeds if the directory already exists, which can mask logic errors",
        ],
        "related": ["rmdir", "install", "cp", "mv"],
        "difficulty": "beginner",
        "extra_flags": {
            "-p": "Create parent directories as needed, no error if existing",
            "-m": "Set permissions on creation (e.g., -m 755)",
            "-v": "Print each directory as it is created",
        },
    },
    "mv": {
        "man_url": "https://man7.org/linux/man-pages/man1/mv.1.html",
        "use_cases": [
            "Rename files: mv old_name.txt new_name.txt",
            "Move files to a directory: mv *.jpg /photos/",
            "Safely move with backup: mv --backup=numbered config.yml /etc/",
        ],
        "gotchas": [
            "mv across filesystems performs a copy-then-delete, which is slow for large files and not atomic",
            "mv overwrites the destination without warning unless -i (interactive) is used",
            "Moving a directory into itself (mv dir dir/sub) causes an error, but the message can be confusing",
        ],
        "related": ["cp", "rm", "rename", "rsync"],
        "difficulty": "beginner",
        "extra_flags": {
            "-i": "Prompt before overwriting existing files",
            "-n": "Do not overwrite existing files (no-clobber)",
            "-v": "Explain what is being done",
            "-t": "Specify the target directory (useful with xargs)",
        },
    },
    "patch": {
        "man_url": "https://man7.org/linux/man-pages/man1/patch.1.html",
        "use_cases": [
            "Apply a diff/patch file: patch -p1 < fix.patch",
            "Reverse a previously applied patch: patch -R -p1 < fix.patch",
            "Dry-run to test a patch: patch --dry-run -p1 < fix.patch",
        ],
        "gotchas": [
            "The -p (strip) level must match how the patch was created -- -p1 strips the first path component",
            "Patches may fail on files that have been modified since the diff was generated (fuzz/offset warnings)",
            "patch creates .orig backup files by default which can clutter the directory",
        ],
        "related": ["diff", "git", "quilt", "merge"],
        "difficulty": "intermediate",
        "extra_flags": {
            "-p": "Strip N leading path components from filenames in the patch",
            "--dry-run": "Test the patch without applying it",
            "-R": "Reverse the patch (unapply)",
            "-b": "Create backup files (.orig) before patching",
        },
    },
    "pwd": {
        "man_url": "https://man7.org/linux/man-pages/man1/pwd.1.html",
        "use_cases": [
            "Print the current working directory: pwd",
            "Get the physical path resolving symlinks: pwd -P",
            "Store current directory in a variable: DIR=$(pwd)",
        ],
        "gotchas": [
            "pwd without -P shows the logical path including symlinks, which may not be the real filesystem path",
            "The $PWD variable is faster than running the pwd command but may be stale after cd through symlinks",
        ],
        "related": ["cd", "dirname", "basename", "realpath"],
        "difficulty": "beginner",
    },
    "rm": {
        "man_url": "https://man7.org/linux/man-pages/man1/rm.1.html",
        "use_cases": [
            "Remove files: rm unwanted_file.txt",
            "Recursively remove a directory: rm -rf build/",
            "Interactive removal for safety: rm -i important_files*",
        ],
        "gotchas": [
            "rm -rf / or rm -rf $VAR/ where VAR is unset can destroy the entire filesystem -- always quote variables and use set -u",
            "There is no recycle bin -- deleted files are gone unless you have backups or use a trash utility",
            "rm -f suppresses all errors including permission denied, making failures invisible",
        ],
        "related": ["rmdir", "shred", "trash-put", "find"],
        "difficulty": "beginner",
        "extra_flags": {
            "-i": "Prompt before each removal",
            "-I": "Prompt once before removing more than 3 files or recursing",
            "--preserve-root": "Refuse to operate on / (default on modern GNU rm)",
        },
    },
    "tar": {
        "man_url": "https://man7.org/linux/man-pages/man1/tar.1.html",
        "use_cases": [
            "Create a compressed archive: tar czf backup.tar.gz /home/user",
            "Extract an archive: tar xzf archive.tar.gz",
            "List archive contents: tar tzf archive.tar.gz",
            "Extract specific files: tar xzf archive.tar.gz path/to/file",
        ],
        "gotchas": [
            "tar preserves absolute paths by default -- use -C or --strip-components to control extraction location",
            "The order of flags matters in some versions -- put f last since it takes the filename argument",
            "Extracting untrusted archives can overwrite files outside the target directory via path traversal (.. components)",
        ],
        "related": ["gzip", "zip", "rsync", "cpio"],
        "difficulty": "intermediate",
        "extra_flags": {
            "-C": "Change to directory before extracting",
            "--strip-components": "Strip N leading path components on extraction",
            "--exclude": "Exclude files matching a pattern",
            "-j": "Use bzip2 compression instead of gzip",
            "-J": "Use xz compression (best ratio, slower)",
            "--totals": "Print total bytes written after creating archive",
        },
    },
    "tree": {
        "man_url": "https://man7.org/linux/man-pages/man1/tree.1.html",
        "use_cases": [
            "Visualize directory structure: tree -L 2",
            "Show only directories: tree -d",
            "Show files with sizes: tree -sh --du",
        ],
        "gotchas": [
            "tree is not installed by default on many systems -- install it via package manager",
            "Running tree on large directories without -L produces enormous output",
            "tree output is not easily parseable -- use find for scripting",
        ],
        "related": ["ls", "find", "du", "exa"],
        "difficulty": "beginner",
        "extra_flags": {
            "-L": "Limit display depth",
            "-I": "Exclude files matching a pattern (e.g., -I 'node_modules|.git')",
            "-a": "Show hidden files",
            "--gitignore": "Respect .gitignore rules (recent versions)",
        },
    },

    # =========================================================================
    # VERSION CONTROL
    # =========================================================================
    "git": {
        "man_url": "https://git-scm.com/docs",
        "use_cases": [
            "Track and manage source code changes across branches",
            "Collaborate with teams via remotes: git push, pull, fetch",
            "Review history and debug with git log, blame, bisect",
            "Stage selective changes: git add -p for partial commits",
        ],
        "gotchas": [
            "git reset --hard destroys uncommitted changes with no recovery -- use git stash first",
            "Force pushing (git push --force) rewrites shared history and can cause data loss for collaborators",
            "Large binary files bloat the repository permanently -- use git-lfs for binaries",
        ],
        "related": ["diff", "patch", "svn", "hg"],
        "difficulty": "intermediate",
        "extra_flags": {
            "stash": "Temporarily shelve uncommitted changes",
            "bisect": "Binary search through history to find a bug-introducing commit",
            "reflog": "Show log of all ref updates (recovery tool for lost commits)",
            "worktree": "Manage multiple working trees attached to the same repository",
        },
    },

    # =========================================================================
    # CONTAINERS
    # =========================================================================
    "docker": {
        "man_url": "https://docs.docker.com/reference/cli/docker/",
        "use_cases": [
            "Run isolated applications: docker run -d --name web nginx",
            "Build custom images: docker build -t myapp:latest .",
            "Manage multi-container apps with compose: docker compose up -d",
            "Inspect and debug containers: docker logs, exec, inspect",
        ],
        "gotchas": [
            "Containers run as root by default -- use --user or USER in Dockerfile for security",
            "Data is lost when a container is removed unless volumes are used: docker run -v data:/app/data",
            "docker system prune removes all unused images and containers -- add --volumes cautiously",
        ],
        "related": ["podman", "kubectl", "containerd", "docker-compose"],
        "difficulty": "intermediate",
        "extra_flags": {
            "system prune": "Remove all unused data (images, containers, networks)",
            "exec -it": "Open interactive shell in a running container",
            "stats": "Show live resource usage of running containers",
            "inspect": "Return detailed JSON metadata about containers or images",
        },
    },

    # =========================================================================
    # SCHEDULING
    # =========================================================================
    "cron": {
        "man_url": "https://man7.org/linux/man-pages/man8/cron.8.html",
        "use_cases": [
            "Schedule recurring system tasks like log rotation and backups",
            "Run periodic maintenance scripts at off-peak hours",
            "Automate report generation on a daily or weekly schedule",
        ],
        "gotchas": [
            "cron jobs run with a minimal environment -- PATH and other variables may differ from your interactive shell",
            "cron has no dependency tracking -- if a job fails, subsequent dependent jobs still run",
            "Cron emails output to the user by default -- redirect output or set MAILTO to avoid mail buildup",
        ],
        "related": ["crontab", "at", "systemd-timer", "anacron"],
        "difficulty": "intermediate",
    },
    "crontab": {
        "man_url": "https://man7.org/linux/man-pages/man1/crontab.1.html",
        "use_cases": [
            "Edit your cron jobs: crontab -e",
            "List current cron jobs: crontab -l",
            "Install crontab from a file: crontab mycron.txt",
        ],
        "gotchas": [
            "crontab -r removes ALL your cron jobs without confirmation -- use crontab -l > backup first",
            "Cron uses its own minimal PATH -- always use absolute paths for commands in crontab entries",
            "The environment in cron is not your login shell -- source profiles or set variables explicitly",
        ],
        "related": ["cron", "at", "systemctl", "anacron"],
        "difficulty": "intermediate",
        "extra_flags": {
            "-e": "Edit the current user's crontab",
            "-l": "List the current user's crontab entries",
            "-r": "Remove the current user's crontab entirely",
            "-u": "Operate on another user's crontab (requires root)",
        },
    },
    "at": {
        "man_url": "https://man7.org/linux/man-pages/man1/at.1.html",
        "use_cases": [
            "Schedule a one-time job: echo 'backup.sh' | at 2am tomorrow",
            "Run a command after a delay: echo 'reboot' | at now + 5 minutes",
            "List pending jobs: atq",
        ],
        "gotchas": [
            "at requires the atd daemon to be running -- check with systemctl status atd",
            "at jobs inherit the current environment but not terminal -- output goes to mail by default",
            "Time parsing is flexible but can be ambiguous -- always verify with atq after scheduling",
        ],
        "related": ["crontab", "batch", "sleep", "nohup"],
        "difficulty": "intermediate",
        "extra_flags": {
            "-m": "Send mail even if the job produces no output",
            "-f": "Read commands from a file instead of stdin",
            "-l": "List pending jobs (alias for atq)",
            "-d": "Delete a job by number (alias for atrm)",
        },
    },
    "batch": {
        "man_url": "https://man7.org/linux/man-pages/man1/batch.1.html",
        "use_cases": [
            "Run a CPU-intensive job when system load drops: echo './compile.sh' | batch",
            "Queue multiple jobs to run sequentially during idle time",
            "Schedule resource-heavy tasks without impacting interactive users",
        ],
        "gotchas": [
            "batch waits until load average drops below 0.8 (or configured threshold) -- jobs may wait indefinitely on busy systems",
            "Like at, batch requires the atd daemon to be running",
            "Output is mailed to the user unless redirected -- check mail or redirect in the script",
        ],
        "related": ["at", "nice", "nohup", "crontab"],
        "difficulty": "intermediate",
    },

    # =========================================================================
    # USER & GROUP ADMINISTRATION
    # =========================================================================
    "chgrp": {
        "man_url": "https://man7.org/linux/man-pages/man1/chgrp.1.html",
        "use_cases": [
            "Change file group ownership: chgrp developers project/",
            "Recursively change group: chgrp -R www-data /var/www",
            "Change group using a reference file: chgrp --reference=ref.txt target.txt",
        ],
        "gotchas": [
            "Non-root users can only change to groups they belong to",
            "chgrp follows symlinks by default -- use -h to change the symlink itself",
        ],
        "related": ["chown", "chmod", "groups", "newgrp"],
        "difficulty": "intermediate",
        "extra_flags": {
            "-R": "Operate recursively on directories",
            "-h": "Change the symlink itself rather than the file it points to",
            "--reference": "Use the group of a reference file",
        },
    },
    "chmod": {
        "man_url": "https://man7.org/linux/man-pages/man1/chmod.1.html",
        "use_cases": [
            "Make a script executable: chmod +x script.sh",
            "Set specific permissions: chmod 644 config.yml",
            "Recursively fix directory permissions: chmod -R u=rwX,go=rX /var/www",
        ],
        "gotchas": [
            "chmod 777 is almost never correct -- it allows anyone to read, write, and execute",
            "The X (capital) permission sets execute only on directories and already-executable files -- useful for recursive operations",
            "setuid/setgid bits (chmod u+s, g+s) are security-sensitive and often ignored on scripts",
        ],
        "related": ["chown", "chgrp", "umask", "setfacl"],
        "difficulty": "intermediate",
        "extra_flags": {
            "-R": "Change permissions recursively",
            "--reference": "Copy permissions from a reference file",
            "-v": "Output a diagnostic for every file processed",
        },
    },
    "chown": {
        "man_url": "https://man7.org/linux/man-pages/man1/chown.1.html",
        "use_cases": [
            "Change file owner: chown user:group file.txt",
            "Recursively change ownership: chown -R www-data:www-data /var/www",
            "Change only the user, preserving group: chown newuser file.txt",
        ],
        "gotchas": [
            "Only root can change file ownership -- non-root users get 'Operation not permitted'",
            "chown follows symlinks by default -- use -h to change the symlink itself",
            "Recursive chown on /etc or /var can break system services if done incorrectly",
        ],
        "related": ["chmod", "chgrp", "stat", "id"],
        "difficulty": "intermediate",
        "extra_flags": {
            "-R": "Operate recursively on directories",
            "-h": "Change the symlink itself rather than the dereferenced file",
            "--from": "Only change ownership if current owner:group matches",
            "--reference": "Use the owner/group of a reference file",
        },
    },
    "chpasswd": {
        "man_url": "https://man7.org/linux/man-pages/man8/chpasswd.8.html",
        "use_cases": [
            "Batch-set passwords from a file: echo 'user:newpass' | chpasswd",
            "Set encrypted passwords: chpasswd -e < hashed_passwords.txt",
            "Automate user provisioning in scripts",
        ],
        "gotchas": [
            "Passwords on stdin are in cleartext unless -e is used -- secure the input source",
            "Must be run as root",
            "Input format is strictly username:password, one per line",
        ],
        "related": ["passwd", "useradd", "usermod", "openssl"],
        "difficulty": "advanced",
    },
    "chroot": {
        "man_url": "https://man7.org/linux/man-pages/man1/chroot.1.html",
        "use_cases": [
            "Run a command in an isolated root filesystem: chroot /mnt/sysimage /bin/bash",
            "Repair a broken system from a live CD by chrooting into the installed root",
            "Create a minimal sandbox for building or testing software",
        ],
        "gotchas": [
            "chroot is NOT a security sandbox -- processes can escape with root access; use namespaces or containers instead",
            "The chroot environment needs all required libraries and binaries (use ldd to check dependencies)",
            "Must be run as root and requires a functional filesystem tree at the target path",
        ],
        "related": ["unshare", "nsenter", "docker", "pivot_root"],
        "difficulty": "advanced",
        "extra_flags": {
            "--userspec": "Run as specified USER:GROUP inside the chroot",
        },
    },
    "doas": {
        "man_url": "https://man.openbsd.org/doas",
        "use_cases": [
            "Run a command as root: doas apt update",
            "Execute as another user: doas -u postgres psql",
            "Simpler alternative to sudo with a minimal config file",
        ],
        "gotchas": [
            "doas is not installed by default on most Linux distros -- it must be installed and configured",
            "Configuration file is /etc/doas.conf with different syntax than sudoers",
            "Fewer features than sudo -- no command logging, session caching is limited",
        ],
        "related": ["sudo", "su", "pkexec", "runuser"],
        "difficulty": "intermediate",
    },
    "getfacl": {
        "man_url": "https://man7.org/linux/man-pages/man1/getfacl.1.html",
        "use_cases": [
            "View access control lists on a file: getfacl /shared/project",
            "Backup ACLs for restoration: getfacl -R /data > acl_backup.txt",
            "Audit fine-grained permissions beyond standard Unix owner/group/other",
        ],
        "gotchas": [
            "ACLs require filesystem support (ext4, xfs) and must be mounted with acl option",
            "cp and mv may not preserve ACLs by default -- use cp -a or rsync -A",
            "ACL mask can restrict effective permissions below what individual entries grant",
        ],
        "related": ["setfacl", "chmod", "chown", "ls"],
        "difficulty": "advanced",
    },
    "groupadd": {
        "man_url": "https://man7.org/linux/man-pages/man8/groupadd.8.html",
        "use_cases": [
            "Create a new group: groupadd developers",
            "Create a system group: groupadd -r appservice",
            "Create with specific GID: groupadd -g 1500 team",
        ],
        "gotchas": [
            "Requires root privileges",
            "Does not automatically add any users to the new group -- use usermod -aG",
            "System groups (-r) use GIDs from the system range defined in /etc/login.defs",
        ],
        "related": ["groupdel", "groupmod", "useradd", "usermod"],
        "difficulty": "intermediate",
    },
    "groupdel": {
        "man_url": "https://man7.org/linux/man-pages/man8/groupdel.8.html",
        "use_cases": [
            "Remove a group: groupdel oldteam",
            "Clean up groups after project decommissioning",
            "Remove groups as part of user offboarding automation",
        ],
        "gotchas": [
            "Cannot delete a group that is any user's primary group -- change the user's primary group first",
            "Files owned by the deleted group will show a numeric GID instead of a group name",
        ],
        "related": ["groupadd", "groupmod", "userdel", "find"],
        "difficulty": "intermediate",
    },
    "groupmod": {
        "man_url": "https://man7.org/linux/man-pages/man8/groupmod.8.html",
        "use_cases": [
            "Rename a group: groupmod -n newname oldname",
            "Change a group's GID: groupmod -g 2000 developers",
            "Modify group properties during organizational changes",
        ],
        "gotchas": [
            "Changing GID does not update file ownership -- run find / -gid OLD_GID -exec chgrp NEW_GID {} +",
            "Renaming a group does not update references in sudoers or other config files",
        ],
        "related": ["groupadd", "groupdel", "usermod", "chgrp"],
        "difficulty": "intermediate",
    },
    "groups": {
        "man_url": "https://man7.org/linux/man-pages/man1/groups.1.html",
        "use_cases": [
            "List groups for the current user: groups",
            "Check another user's groups: groups username",
            "Verify group membership after usermod changes",
        ],
        "gotchas": [
            "Group changes from usermod -aG do not take effect until the user logs out and back in (or uses newgrp)",
            "The first group listed is the primary group; others are supplementary",
        ],
        "related": ["id", "newgrp", "usermod", "getent"],
        "difficulty": "beginner",
    },
    "grpck": {
        "man_url": "https://man7.org/linux/man-pages/man8/grpck.8.html",
        "use_cases": [
            "Verify integrity of /etc/group and /etc/gshadow: grpck",
            "Fix inconsistencies in group databases: grpck -r (read-only check)",
            "Run as part of system health audits",
        ],
        "gotchas": [
            "Must be run as root to modify files; use -r for read-only checks as non-root",
            "Interactive prompts for fixes can be disruptive in automated scripts -- review changes carefully",
        ],
        "related": ["pwck", "groupmod", "vigr", "getent"],
        "difficulty": "advanced",
    },
    "id": {
        "man_url": "https://man7.org/linux/man-pages/man1/id.1.html",
        "use_cases": [
            "Display current user's UID, GID, and groups: id",
            "Check another user's identity: id username",
            "Get just the numeric UID for scripting: id -u",
        ],
        "gotchas": [
            "id shows effective IDs, which may differ from real IDs when setuid programs are involved",
            "Supplementary groups listed by id may not match groups if group membership was recently changed",
        ],
        "related": ["whoami", "groups", "who", "w"],
        "difficulty": "beginner",
        "extra_flags": {
            "-u": "Print only the effective user ID",
            "-g": "Print only the effective group ID",
            "-G": "Print all group IDs (supplementary groups)",
            "-n": "Print names instead of numbers (use with -u, -g, or -G)",
        },
    },
    "last": {
        "man_url": "https://man7.org/linux/man-pages/man1/last.1.html",
        "use_cases": [
            "View recent login history: last",
            "Check logins for a specific user: last username",
            "View reboot history: last reboot",
        ],
        "gotchas": [
            "last reads /var/log/wtmp which may be rotated -- old entries are lost after rotation",
            "Still-logged-in sessions show 'still logged in' with no duration",
            "System clock changes can make timestamps inaccurate in the log",
        ],
        "related": ["lastlog", "w", "who", "utmpdump"],
        "difficulty": "beginner",
        "extra_flags": {
            "-n": "Show only the last N entries",
            "-x": "Show system shutdown and runlevel changes",
            "-F": "Show full login and logout times",
        },
    },
    "lastlog": {
        "man_url": "https://man7.org/linux/man-pages/man8/lastlog.8.html",
        "use_cases": [
            "Show last login time for all users: lastlog",
            "Check when a specific user last logged in: lastlog -u username",
            "Find accounts that have never logged in: lastlog | grep 'Never'",
        ],
        "gotchas": [
            "lastlog reads /var/log/lastlog which uses a sparse file indexed by UID -- very high UIDs can make this file large",
            "Service accounts show 'Never logged in' which is expected, not a problem",
        ],
        "related": ["last", "who", "w", "faillog"],
        "difficulty": "beginner",
        "extra_flags": {
            "-u": "Show information for a specific user",
            "-b": "Show users who have not logged in for N days",
        },
    },
    "newgrp": {
        "man_url": "https://man7.org/linux/man-pages/man1/newgrp.1.html",
        "use_cases": [
            "Switch active group without logging out: newgrp docker",
            "Activate a newly assigned supplementary group in the current session",
            "Create files with a specific group ownership by switching first",
        ],
        "gotchas": [
            "newgrp starts a new shell -- exit to return to the original shell with original groups",
            "If a group password is set and the user is not a member, newgrp prompts for it",
        ],
        "related": ["groups", "id", "usermod", "sg"],
        "difficulty": "intermediate",
    },
    "passwd": {
        "man_url": "https://man7.org/linux/man-pages/man1/passwd.1.html",
        "use_cases": [
            "Change your own password: passwd",
            "Change another user's password (root): passwd username",
            "Lock a user account: passwd -l username",
            "Set password expiration: passwd -x 90 username",
        ],
        "gotchas": [
            "Password complexity rules are enforced by PAM -- they may reject passwords that seem fine to you",
            "passwd -l locks the account but does not disable SSH key authentication",
            "Expired passwords may lock users out of automated services that cannot handle interactive password changes",
        ],
        "related": ["chpasswd", "usermod", "chage", "pwck"],
        "difficulty": "beginner",
        "extra_flags": {
            "-l": "Lock the account (prefix hash with !)",
            "-u": "Unlock a locked account",
            "-S": "Show password status (locked, set, etc.)",
            "-e": "Force password change at next login",
        },
    },
    "pwck": {
        "man_url": "https://man7.org/linux/man-pages/man8/pwck.8.html",
        "use_cases": [
            "Verify integrity of /etc/passwd and /etc/shadow: pwck",
            "Read-only check without modifications: pwck -r",
            "Part of routine system integrity audits",
        ],
        "gotchas": [
            "Must be run as root to modify files; use -r for safe read-only checking",
            "May prompt to fix issues interactively -- not suitable for fully unattended automation without -r",
        ],
        "related": ["grpck", "vipw", "passwd", "useradd"],
        "difficulty": "advanced",
    },
    "setfacl": {
        "man_url": "https://man7.org/linux/man-pages/man1/setfacl.1.html",
        "use_cases": [
            "Grant a specific user access: setfacl -m u:bob:rwx /shared/project",
            "Set default ACL for new files in a directory: setfacl -d -m g:dev:rw /shared",
            "Remove all ACLs: setfacl -b /shared/project",
        ],
        "gotchas": [
            "The ACL mask limits effective permissions for named users and groups -- set mask explicitly if needed",
            "Default ACLs only apply to newly created files, not existing ones",
            "Some backup tools (tar without --acls) do not preserve ACLs",
        ],
        "related": ["getfacl", "chmod", "chown", "umask"],
        "difficulty": "advanced",
        "extra_flags": {
            "-m": "Modify ACL entries",
            "-x": "Remove specific ACL entries",
            "-b": "Remove all ACL entries",
            "-R": "Apply recursively",
            "-d": "Set default ACL (for directories, applied to new files)",
        },
    },
    "su": {
        "man_url": "https://man7.org/linux/man-pages/man1/su.1.html",
        "use_cases": [
            "Switch to root: su -",
            "Run a command as another user: su -c 'whoami' postgres",
            "Open a login shell as another user: su - deploy",
        ],
        "gotchas": [
            "su without - does not set a login environment -- PATH and other variables remain from the original user",
            "su requires the target user's password, while sudo requires your own password",
            "su to root leaves no audit trail of which user invoked it -- sudo provides better accountability",
        ],
        "related": ["sudo", "doas", "runuser", "newgrp"],
        "difficulty": "intermediate",
        "extra_flags": {
            "-": "Start a login shell (full environment reset)",
            "-c": "Run a single command and return",
            "-s": "Use a specific shell instead of the target user's default",
        },
    },
    "sudo": {
        "man_url": "https://man7.org/linux/man-pages/man8/sudo.8.html",
        "use_cases": [
            "Run a command as root: sudo apt update",
            "Edit a protected file: sudo -e /etc/hosts (uses sudoedit)",
            "Run as another user: sudo -u postgres psql",
            "List allowed commands: sudo -l",
        ],
        "gotchas": [
            "sudo caches credentials for a timeout period -- use sudo -k to invalidate the cache",
            "Environment variables are reset by default -- use sudo -E or specific env_keep in sudoers to preserve them",
            "Piping with sudo fails: 'sudo echo x > /etc/file' -- use 'echo x | sudo tee /etc/file' instead",
        ],
        "related": ["su", "doas", "visudo", "pkexec"],
        "difficulty": "intermediate",
        "extra_flags": {
            "-u": "Run as a specified user instead of root",
            "-E": "Preserve the user's environment variables",
            "-l": "List commands the user is allowed to run",
            "-k": "Invalidate the cached credentials",
            "-i": "Start a login shell as root",
        },
    },
    "umask": {
        "man_url": "https://www.gnu.org/software/bash/manual/bash.html#index-umask",
        "use_cases": [
            "Check current umask: umask",
            "Set restrictive default permissions: umask 077 (owner-only access)",
            "Set permissive defaults for shared directories: umask 002",
        ],
        "gotchas": [
            "umask is a mask (inverted) -- umask 022 means files get 644, not 022",
            "umask only affects new file creation, not existing files",
            "Different shells and login methods may set different default umasks -- check /etc/profile and PAM config",
        ],
        "related": ["chmod", "mkdir", "touch", "install"],
        "difficulty": "intermediate",
    },
    "updatedb": {
        "man_url": "https://man7.org/linux/man-pages/man8/updatedb.8.html",
        "use_cases": [
            "Refresh the locate database: sudo updatedb",
            "Update with specific paths excluded: updatedb --prunepaths='/tmp /proc'",
            "Schedule via cron for daily index updates",
        ],
        "gotchas": [
            "updatedb can be slow on large filesystems and generates significant I/O",
            "The database is stale between updates -- newly created files won't appear until next updatedb run",
            "By default only indexes paths accessible to the user running updatedb",
        ],
        "related": ["locate", "mlocate", "plocate", "find"],
        "difficulty": "intermediate",
    },
    "mlocate": {
        "man_url": "https://man7.org/linux/man-pages/man1/locate.1.html",
        "use_cases": [
            "Find files by name quickly: locate nginx.conf",
            "Search with regex: locate -r '/etc/.*\\.conf$'",
            "Count matches: locate -c '*.py'",
        ],
        "gotchas": [
            "Results may be stale -- run updatedb to refresh the database",
            "mlocate checks file permissions so users only see files they can access, unlike older locate",
            "Many distros have replaced mlocate with plocate for better performance",
        ],
        "related": ["plocate", "updatedb", "find", "fd"],
        "difficulty": "beginner",
    },
    "plocate": {
        "man_url": "https://man7.org/linux/man-pages/man1/plocate.1.html",
        "use_cases": [
            "Fast file search by name: plocate config.yaml",
            "Case-insensitive search: plocate -i README",
            "Drop-in replacement for mlocate with significantly faster queries",
        ],
        "gotchas": [
            "Still requires updatedb to be run (typically via cron) -- results lag behind filesystem changes",
            "Database format is incompatible with mlocate -- migration creates a new database",
        ],
        "related": ["mlocate", "updatedb", "find", "fd"],
        "difficulty": "beginner",
    },
    "useradd": {
        "man_url": "https://man7.org/linux/man-pages/man8/useradd.8.html",
        "use_cases": [
            "Create a new user with home directory: useradd -m -s /bin/bash newuser",
            "Create a system user for a service: useradd -r -s /usr/sbin/nologin appuser",
            "Create user with specific UID and groups: useradd -u 1500 -G docker,dev newuser",
        ],
        "gotchas": [
            "useradd does not create a home directory by default on many distros -- always use -m explicitly",
            "useradd does not set a password -- run passwd username afterward",
            "Debian/Ubuntu adduser is a friendlier wrapper -- useradd is the low-level tool",
        ],
        "related": ["userdel", "usermod", "passwd", "adduser"],
        "difficulty": "intermediate",
        "extra_flags": {
            "-m": "Create the user's home directory",
            "-s": "Set the login shell",
            "-G": "Add to supplementary groups (comma-separated)",
            "-r": "Create a system account (no home, low UID)",
            "-e": "Set account expiration date (YYYY-MM-DD)",
        },
    },
    "userdel": {
        "man_url": "https://man7.org/linux/man-pages/man8/userdel.8.html",
        "use_cases": [
            "Remove a user account: userdel olduser",
            "Remove user and their home directory: userdel -r olduser",
            "Clean up deactivated accounts during offboarding",
        ],
        "gotchas": [
            "userdel without -r leaves the home directory and mail spool behind -- orphaned files remain",
            "Cannot delete a user who is currently logged in -- use kill or loginctl to terminate sessions first",
            "Files owned by the deleted UID outside /home will show a numeric UID in ls -l",
        ],
        "related": ["useradd", "usermod", "passwd", "find"],
        "difficulty": "intermediate",
        "extra_flags": {
            "-r": "Remove home directory and mail spool",
            "-f": "Force removal even if user is logged in (dangerous)",
        },
    },
    "usermod": {
        "man_url": "https://man7.org/linux/man-pages/man8/usermod.8.html",
        "use_cases": [
            "Add user to a group: usermod -aG docker username",
            "Change login shell: usermod -s /bin/zsh username",
            "Lock an account: usermod -L username",
            "Rename a user: usermod -l newname oldname",
        ],
        "gotchas": [
            "usermod -G WITHOUT -a replaces all supplementary groups -- always use -aG to append",
            "Changes to groups do not take effect until the user logs out and back in",
            "Renaming a user (-l) does not rename the home directory -- use -d -m to move it",
        ],
        "related": ["useradd", "userdel", "passwd", "groups"],
        "difficulty": "intermediate",
        "extra_flags": {
            "-aG": "Append to supplementary groups without removing existing ones",
            "-L": "Lock the user account (disable password login)",
            "-U": "Unlock a locked user account",
            "-l": "Change the login name",
            "-d": "Change the home directory (use -m to move files)",
        },
    },
    "users": {
        "man_url": "https://man7.org/linux/man-pages/man1/users.1.html",
        "use_cases": [
            "List currently logged-in usernames: users",
            "Quick check if anyone is logged in: users | wc -w",
            "Simple alternative to who when you only need usernames",
        ],
        "gotchas": [
            "users reads /var/run/utmp which may not include all sessions (e.g., tmux/screen sub-sessions)",
            "Duplicate names appear if a user has multiple sessions",
        ],
        "related": ["who", "w", "last", "id"],
        "difficulty": "beginner",
    },
    "vigr": {
        "man_url": "https://man7.org/linux/man-pages/man8/vigr.8.html",
        "use_cases": [
            "Safely edit /etc/group with locking: vigr",
            "Edit /etc/gshadow: vigr -s",
            "Prevent concurrent edits to group files by multiple admins",
        ],
        "gotchas": [
            "Must be run as root",
            "Uses the $EDITOR or $VISUAL environment variable -- set these to your preferred editor",
            "Always run grpck after manual edits to verify file integrity",
        ],
        "related": ["vipw", "grpck", "groupmod", "groupadd"],
        "difficulty": "advanced",
    },
    "vipw": {
        "man_url": "https://man7.org/linux/man-pages/man8/vipw.8.html",
        "use_cases": [
            "Safely edit /etc/passwd with locking: vipw",
            "Edit /etc/shadow: vipw -s",
            "Prevent corruption from concurrent edits to password files",
        ],
        "gotchas": [
            "Must be run as root",
            "Always run pwck after manual edits to verify file integrity",
            "Syntax errors in /etc/passwd can lock all users out -- be very careful",
        ],
        "related": ["vigr", "pwck", "passwd", "usermod"],
        "difficulty": "advanced",
    },
    "w": {
        "man_url": "https://man7.org/linux/man-pages/man1/w.1.html",
        "use_cases": [
            "See who is logged in and what they are doing: w",
            "Check system load and uptime at a glance",
            "Monitor idle times to find inactive sessions",
        ],
        "gotchas": [
            "The WHAT column shows the current foreground process, which may not represent what the user is actually doing",
            "IDLE time resets on any terminal activity including background output",
        ],
        "related": ["who", "uptime", "last", "users"],
        "difficulty": "beginner",
    },
    "wait": {
        "man_url": "https://www.gnu.org/software/bash/manual/bash.html#index-wait",
        "use_cases": [
            "Wait for all background jobs to finish: wait",
            "Wait for a specific PID: wait $pid",
            "Capture exit status of a background process: wait $pid; echo $?",
        ],
        "gotchas": [
            "wait only works for children of the current shell -- it cannot wait for arbitrary PIDs from other processes",
            "In pipelines, $! gives the PID of the last command only -- store PIDs explicitly for multiple background jobs",
            "wait returns immediately with an error for PIDs that are not children of the current shell",
        ],
        "related": ["jobs", "bg", "fg", "kill"],
        "difficulty": "intermediate",
    },
    "who": {
        "man_url": "https://man7.org/linux/man-pages/man1/who.1.html",
        "use_cases": [
            "List logged-in users with terminal info: who",
            "Show current user and terminal: who am i",
            "Check system boot time: who -b",
        ],
        "gotchas": [
            "who reads utmp, which may not include pseudo-terminals from screen/tmux on all systems",
            "who am i may show nothing if not connected via a real login session (e.g., in a script)",
        ],
        "related": ["w", "users", "last", "id"],
        "difficulty": "beginner",
        "extra_flags": {
            "-b": "Show time of last system boot",
            "-q": "Quick mode: show only usernames and count",
            "-H": "Print column headers",
        },
    },

    # =========================================================================
    # SECURITY & TLS
    # =========================================================================
    "certbot": {
        "man_url": "https://eff-certbot.readthedocs.io/en/latest/",
        "use_cases": [
            "Obtain a free TLS certificate: certbot --nginx -d example.com",
            "Renew all certificates: certbot renew",
            "Test renewal without changing anything: certbot renew --dry-run",
        ],
        "gotchas": [
            "Certificates expire every 90 days -- set up auto-renewal via cron or systemd timer",
            "Port 80 or 443 must be accessible for HTTP-01 or TLS-ALPN-01 validation",
            "Rate limits apply -- avoid repeated requests for the same domain during testing (use --staging)",
        ],
        "related": ["openssl", "nginx", "apache2", "acme.sh"],
        "difficulty": "intermediate",
        "extra_flags": {
            "--nginx": "Use the Nginx plugin for automatic configuration",
            "--apache": "Use the Apache plugin for automatic configuration",
            "--standalone": "Run a temporary web server for validation",
            "--dry-run": "Test without saving certificates",
            "--staging": "Use the staging server to avoid rate limits during testing",
        },
    },

    # =========================================================================
    # PYTHON RUNTIMES
    # =========================================================================
    "python2": {
        "man_url": "https://docs.python.org/2/using/cmdline.html",
        "use_cases": [
            "Run legacy Python 2 scripts: python2 legacy_script.py",
            "Check if Python 2 is still installed: python2 --version",
            "Maintain compatibility during Python 2 to 3 migration",
        ],
        "gotchas": [
            "Python 2 reached end-of-life on January 1, 2020 -- no security patches are issued",
            "print is a statement in Python 2 (print 'x') but a function in Python 3 (print('x'))",
            "Integer division in Python 2 truncates: 3/2 == 1, not 1.5",
        ],
        "related": ["python3", "pip", "virtualenv", "2to3"],
        "difficulty": "intermediate",
    },
    "python3": {
        "man_url": "https://docs.python.org/3/using/cmdline.html",
        "use_cases": [
            "Run Python scripts: python3 script.py",
            "Quick one-liner: python3 -c 'import json; print(json.dumps({\"a\":1}))'",
            "Start a simple HTTP server: python3 -m http.server 8080",
            "Create virtual environments: python3 -m venv .venv",
        ],
        "gotchas": [
            "python may point to python2 or python3 depending on the system -- always use python3 explicitly",
            "pip install without --user or a venv may require sudo and can break system packages",
            "The GIL limits true parallelism for CPU-bound threads -- use multiprocessing for CPU-heavy work",
        ],
        "related": ["pip", "venv", "ipython", "python2"],
        "difficulty": "beginner",
        "extra_flags": {
            "-m": "Run a module as a script (e.g., -m venv, -m http.server)",
            "-c": "Execute a command string",
            "-u": "Unbuffered stdout/stderr (useful in containers and pipes)",
            "-B": "Do not write .pyc bytecode cache files",
        },
    },

    # =========================================================================
    # DEBUGGING & TRACING
    # =========================================================================
    "strace": {
        "man_url": "https://man7.org/linux/man-pages/man1/strace.1.html",
        "use_cases": [
            "Trace system calls of a process: strace -f ./program",
            "Debug why a program fails to open a file: strace -e trace=openat ./prog",
            "Measure syscall timing: strace -T -c ./program",
            "Attach to a running process: strace -p PID",
        ],
        "gotchas": [
            "strace significantly slows down the traced process -- do not use on production without caution",
            "Output is very verbose by default -- use -e to filter specific syscall categories",
            "strace requires ptrace permissions -- seccomp or Yama may block it on hardened systems",
        ],
        "related": ["ltrace", "perf", "gdb", "dmesg"],
        "difficulty": "advanced",
        "extra_flags": {
            "-f": "Follow child processes (fork/clone)",
            "-e": "Filter by syscall name or category (e.g., -e trace=network)",
            "-p": "Attach to a running process by PID",
            "-c": "Summarize syscall counts and times at exit",
            "-o": "Write trace output to a file instead of stderr",
            "-T": "Show time spent in each syscall",
        },
    },
    "ltrace": {
        "man_url": "https://man7.org/linux/man-pages/man1/ltrace.1.html",
        "use_cases": [
            "Trace library calls: ltrace ./program",
            "Debug shared library loading issues: ltrace -e dlopen ./prog",
            "Compare library call patterns between program versions",
        ],
        "gotchas": [
            "ltrace does not work with statically linked binaries -- only dynamic libraries are traced",
            "Significant performance overhead, similar to strace",
            "May not be installed by default on minimal systems",
        ],
        "related": ["strace", "ldd", "nm", "objdump"],
        "difficulty": "advanced",
        "extra_flags": {
            "-e": "Filter by library function name",
            "-p": "Attach to a running process by PID",
            "-c": "Summarize call counts and times",
            "-S": "Also trace system calls (like strace)",
        },
    },
    "perf": {
        "man_url": "https://man7.org/linux/man-pages/man1/perf.1.html",
        "use_cases": [
            "Profile CPU usage: perf record -g ./program && perf report",
            "Count hardware events: perf stat ./program",
            "Find performance hotspots: perf top",
            "Trace specific events: perf trace -e syscalls:sys_enter_write",
        ],
        "gotchas": [
            "perf requires kernel support and may need kernel debug symbols for full stack traces",
            "Permission restrictions (perf_event_paranoid) may require root or sysctl tuning",
            "perf record files can grow very large for long-running programs -- use -F to lower sample frequency",
        ],
        "related": ["strace", "valgrind", "gprof", "flamegraph"],
        "difficulty": "advanced",
        "extra_flags": {
            "record": "Collect performance data into perf.data",
            "report": "Display the recorded performance data",
            "stat": "Run a program and show event counters",
            "top": "Live system-wide profiling (like top for CPU events)",
            "-g": "Enable call graph (stack trace) recording",
        },
    },
}
