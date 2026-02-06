"""
Enrichment data for Text Processing, Search/Navigation, and Development commands.

This module provides supplemental fields (use_cases, gotchas, man_url, related,
difficulty, extra_flags) for thin entries in the COMMAND_DB knowledge base.

Sources consulted:
  - man7.org Linux man-pages
  - GNU Coreutils documentation (gnu.org)
  - Official project documentation (gcc.gnu.org, docs.docker.com, kubernetes.io, etc.)
  - GitHub project pages for modern CLI tools (fzf, fd, ripgrep, exa, etc.)
"""

ENRICHMENT_DATA = {
    # =========================================================================
    # TEXT PROCESSING
    # =========================================================================
    "paste": {
        "man_url": "https://man7.org/linux/man-pages/man1/paste.1.html",
        "use_cases": [
            "Merge two column files side by side with paste file1.txt file2.txt to create a combined table",
            "Convert a single-column list into a comma-separated line with paste -sd',' file.txt",
            "Interleave lines from stdin into columns with seq 6 | paste - - - to create 3-column output",
        ],
        "gotchas": [
            "The default delimiter is TAB, which may not be visible -- use -d to set an explicit delimiter if you need commas or other separators",
            "The -s flag fundamentally changes behavior from parallel merging (side by side) to serial (one file at a time concatenated horizontally) -- confusing these modes produces unexpected output",
            "When using - for stdin, each - consumes successive lines, so paste - - reads two lines at a time into two columns",
        ],
        "related": ["join", "column", "pr", "cut"],
        "difficulty": "intermediate",
        "extra_flags": {
            "-z": "Use NUL as line delimiter instead of newline",
        },
    },
    "join": {
        "man_url": "https://man7.org/linux/man-pages/man1/join.1.html",
        "use_cases": [
            "Perform a relational join of two CSV files on a shared key with join -t',' file1.csv file2.csv",
            "Find unmatched lines between two sorted files with join -v 1 sorted1.txt sorted2.txt",
            "Join files on a non-first field with join -1 2 -2 3 file1.txt file2.txt",
        ],
        "gotchas": [
            "Both input files MUST be sorted on the join field before running join -- unsorted input silently produces wrong results rather than an error",
            "By default join matches on the first field with whitespace as separator -- use -t to set the actual delimiter for CSV or TSV data",
            "Lines that do not match are silently dropped unless you use -a or -v to include unpaired lines from one or both files",
        ],
        "related": ["paste", "comm", "sort", "awk"],
        "difficulty": "intermediate",
        "extra_flags": {
            "-a": "Also print unpairable lines from the specified file (1 or 2)",
            "-e": "Replace missing input fields with this string",
            "-i": "Ignore case when comparing join fields",
            "-v": "Print only unpairable lines from the specified file",
            "-o": "Specify output format using FILENUM.FIELD notation",
            "-1": "Join on this field of file 1",
            "-2": "Join on this field of file 2",
            "--header": "Treat first line of each file as a header",
        },
    },
    "comm": {
        "man_url": "https://man7.org/linux/man-pages/man1/comm.1.html",
        "use_cases": [
            "Find lines common to two sorted files with comm -12 file1.txt file2.txt",
            "Find lines unique to the first file with comm -23 file1.txt file2.txt for set-difference operations",
            "Compare two sorted package lists to find newly installed packages with comm -13 old_pkgs.txt new_pkgs.txt",
        ],
        "gotchas": [
            "Both files MUST be sorted -- comm on unsorted files produces garbage output without any warning",
            "The three columns are: lines only in file1, lines only in file2, lines in both -- the -1 -2 -3 flags SUPPRESS columns, so -12 shows column 3 (common lines)",
            "Column numbering is unintuitive: -12 does not mean columns 1 and 2, it means suppress columns 1 and 2, showing only column 3",
        ],
        "related": ["diff", "join", "sort", "uniq"],
        "difficulty": "intermediate",
        "extra_flags": {
            "--check-order": "Check that input is correctly sorted",
            "--nocheck-order": "Do not check input sort order",
            "--output-delimiter": "Separate columns with this string",
            "-z": "Use NUL as line delimiter instead of newline",
        },
    },
    "csplit": {
        "man_url": "https://man7.org/linux/man-pages/man1/csplit.1.html",
        "use_cases": [
            "Split a log file at each date header with csplit access.log '/^2024-/' '{*}'",
            "Split a document at chapter markers with csplit book.txt '/^Chapter/' '{*}'",
            "Extract the section between two patterns by splitting at both boundaries",
        ],
        "gotchas": [
            "Without -k, if a pattern is not found csplit removes ALL output files it already created -- use -k to keep partial results on error",
            "The '{*}' repeat specifier means repeat as many times as possible -- without it csplit only splits at the first match",
            "Output files are named xx00, xx01, etc. by default -- use -f to set a meaningful prefix and -n to control digit count",
        ],
        "related": ["split", "awk", "grep", "sed"],
        "difficulty": "intermediate",
        "extra_flags": {
            "-b": "Use sprintf-style suffix format instead of default %02d",
            "--suppress-matched": "Suppress the lines matching the pattern in output",
        },
    },
    "split": {
        "man_url": "https://man7.org/linux/man-pages/man1/split.1.html",
        "use_cases": [
            "Break a large CSV file into manageable chunks with split -l 10000 data.csv chunk_ for parallel processing",
            "Split a large backup file into pieces that fit on removable media with split -b 4G backup.tar part_",
            "Create numbered output files with split -d -l 500 log.txt log_ for easier sorting",
        ],
        "gotchas": [
            "Output files are named xaa, xab, etc. by default -- use a PREFIX argument and -d for numeric suffixes to get readable names",
            "split does not add headers to subsequent chunks -- when splitting CSV files, the header row only appears in the first piece",
            "The -n flag splits into N equal-sized pieces but can split mid-line unless you use -n l/N for line-boundary splits",
        ],
        "related": ["csplit", "cat", "head", "tail"],
        "difficulty": "beginner",
        "extra_flags": {
            "-n": "Split into N chunks (use l/N for line-aligned chunks)",
            "-a": "Set the length of the generated suffix (default 2)",
            "--filter": "Write to a shell command instead of files",
            "--additional-suffix": "Append an extra suffix to output filenames",
        },
    },
    "column": {
        "man_url": "https://man7.org/linux/man-pages/man1/column.1.html",
        "use_cases": [
            "Format command output into a clean table with mount | column -t",
            "Display CSV data as an aligned table with column -t -s',' data.csv",
            "Create readable side-by-side output from tab-delimited data for reports",
        ],
        "gotchas": [
            "The -s flag sets the INPUT separator, not the output separator -- the output is always space-padded for alignment",
            "On older Linux systems (util-linux < 2.30), column -t does not support -s with multi-character separators -- only single character delimiters work",
            "The newer util-linux column supports -N for named headers and -J for JSON output, but these are not available on macOS or older systems",
        ],
        "related": ["paste", "pr", "printf", "awk"],
        "difficulty": "beginner",
        "extra_flags": {
            "-o": "Set output separator string (util-linux 2.30+)",
            "-N": "Set comma-separated list of column names for headers",
            "-J": "Output as JSON with column names from -N",
            "-c": "Set output width in characters",
        },
    },
    "rev": {
        "man_url": "https://man7.org/linux/man-pages/man1/rev.1.html",
        "use_cases": [
            "Reverse each line to extract file extensions with rev | cut -d. -f1 | rev",
            "Check for palindromes in a word list by comparing input with reversed output",
            "Get the last field of a variable-length delimited line when you cannot predict field count",
        ],
        "gotchas": [
            "rev reverses characters within each line, not the order of lines -- use tac to reverse line order",
            "Multi-byte UTF-8 characters may not reverse correctly on all implementations -- test with your locale",
        ],
        "related": ["tac", "cut", "awk"],
        "difficulty": "beginner",
        "extra_flags": {},
    },
    "shuf": {
        "man_url": "https://man7.org/linux/man-pages/man1/shuf.1.html",
        "use_cases": [
            "Select a random line from a file with shuf -n 1 quotes.txt for random quote display",
            "Randomize the order of a playlist or test data with shuf playlist.m3u > shuffled.m3u",
            "Generate random numbers in a range with shuf -i 1-100 -n 10 for sampling",
        ],
        "gotchas": [
            "shuf loads the entire input into memory -- for very large files this can exhaust RAM",
            "The randomness comes from /dev/urandom by default -- for reproducible shuffles use --random-source with a fixed seed file",
        ],
        "related": ["sort", "head", "seq"],
        "difficulty": "beginner",
        "extra_flags": {
            "-i": "Generate integers from LO to HI range instead of reading input",
            "-o": "Write output to a file instead of stdout",
            "-r": "Allow output lines to repeat (sample with replacement)",
            "-z": "Use NUL as line delimiter instead of newline",
        },
    },
    "nl": {
        "man_url": "https://man7.org/linux/man-pages/man1/nl.1.html",
        "use_cases": [
            "Number all lines including blanks with nl -ba script.sh for code review",
            "Add right-justified zero-padded line numbers with nl -nrz -w4 file.txt",
            "Number only lines matching a pattern with nl -bp'^function' file.sh",
        ],
        "gotchas": [
            "By default nl only numbers non-empty lines (style t) -- use -ba to number ALL lines including blanks",
            "nl treats lines starting with \\:\\:\\: as page section delimiters (header/body/footer) which can cause unexpected behavior if your data contains these patterns",
            "Line numbers reset at each logical page by default -- use -p to prevent renumbering across sections",
        ],
        "related": ["cat", "pr", "grep"],
        "difficulty": "beginner",
        "extra_flags": {
            "-n": "Number format: ln (left justified), rn (right justified), rz (right justified with zeros)",
            "-w": "Set number width (default 6)",
            "-s": "Set separator string between number and line (default TAB)",
            "-i": "Line number increment (default 1)",
            "-v": "Starting line number (default 1)",
            "-p": "Do not reset line numbers at logical page boundaries",
        },
    },
    "fold": {
        "man_url": "https://man7.org/linux/man-pages/man1/fold.1.html",
        "use_cases": [
            "Wrap long lines for terminal display with fold -s -w 80 readme.txt",
            "Prepare text for systems with fixed line-length limits like email with fold -w 76",
            "Break base64-encoded data into fixed-width lines with fold -w 76 encoded.txt",
        ],
        "gotchas": [
            "Without -s, fold breaks lines at the exact column count even mid-word -- always use -s for human-readable text to break at spaces",
            "fold counts display columns by default, not bytes -- use -b for byte counting which matters for multi-byte encodings",
            "Unlike fmt, fold does not join short lines or reflow paragraphs -- it only breaks long lines",
        ],
        "related": ["fmt", "pr", "column"],
        "difficulty": "beginner",
        "extra_flags": {},
    },
    "fmt": {
        "man_url": "https://man7.org/linux/man-pages/man1/fmt.1.html",
        "use_cases": [
            "Reflow a paragraph to 72 columns for email formatting with fmt -w 72 message.txt",
            "Clean up ragged text from copy-paste with fmt -u file.txt for uniform spacing",
            "Wrap only long lines without joining short ones with fmt -s -w 80 code_comments.txt",
        ],
        "gotchas": [
            "fmt joins short lines into paragraphs by default -- use -s if you only want to split long lines without merging short ones",
            "Indented lines are treated as paragraph boundaries, so fmt preserves code indentation but may reflow comments unexpectedly",
            "The default width is 75, not 80 -- explicitly set -w 80 if you want standard terminal width",
        ],
        "related": ["fold", "pr", "par"],
        "difficulty": "beginner",
        "extra_flags": {
            "-p": "Only reformat lines starting with this prefix string",
            "-t": "Indent like the first line, subsequent lines like the second",
        },
    },
    "pr": {
        "man_url": "https://man7.org/linux/man-pages/man1/pr.1.html",
        "use_cases": [
            "Add headers and page numbers to a file for printing with pr -h 'Report' data.txt | lpr",
            "Display two files side by side with pr -m -t file1.txt file2.txt for comparison",
            "Format output into multiple columns with pr -3 -t wordlist.txt",
        ],
        "gotchas": [
            "By default pr adds 5-line headers and trailers on each page -- use -t to suppress them for pipeline use",
            "The default page length is 66 lines (standard US letter at 6 lines/inch) -- adjust with -l for other formats",
            "pr paginates output with form feeds -- pipe to head or less if you want continuous output",
        ],
        "related": ["column", "nl", "fmt", "fold"],
        "difficulty": "intermediate",
        "extra_flags": {
            "-t": "Suppress headers and trailers",
            "-T": "Suppress headers, trailers, and form feeds",
            "-W": "Set page width including margin (overrides -w)",
            "-J": "Merge full lines, overriding -W truncation",
        },
    },
    "expand": {
        "man_url": "https://man7.org/linux/man-pages/man1/expand.1.html",
        "use_cases": [
            "Convert tabs to 4 spaces for consistent indentation with expand -t 4 file.c > file_spaces.c",
            "Normalize mixed tab/space files before diffing with expand -t 4 file.txt",
            "Convert only leading tabs (preserve alignment tabs) with expand -i -t 4 source.py",
        ],
        "gotchas": [
            "The default tab stop is 8, not 4 -- always specify -t with your project's indentation width",
            "expand processes all tabs by default including those inside strings -- use -i to limit conversion to leading whitespace only",
            "Pipe through expand before diff to avoid false differences caused by mixed tabs and spaces",
        ],
        "related": ["unexpand", "sed", "tr"],
        "difficulty": "beginner",
        "extra_flags": {},
    },
    "unexpand": {
        "man_url": "https://man7.org/linux/man-pages/man1/unexpand.1.html",
        "use_cases": [
            "Convert spaces to tabs for Makefiles that require tab indentation with unexpand -t 4 --first-only file",
            "Reduce file size of heavily indented files by converting space runs to tabs",
            "Convert all space sequences (not just leading) with unexpand -a -t 4 file.txt",
        ],
        "gotchas": [
            "By default unexpand only converts leading spaces to tabs -- use -a to convert all sequences of spaces",
            "Makefiles REQUIRE literal tab characters for recipe lines -- unexpand can help fix spaces-only Makefiles",
            "The tab stop must match the original indentation width or the conversion will misalign content",
        ],
        "related": ["expand", "sed", "tr"],
        "difficulty": "beginner",
        "extra_flags": {},
    },
    "od": {
        "man_url": "https://man7.org/linux/man-pages/man1/od.1.html",
        "use_cases": [
            "Debug encoding issues by viewing raw bytes with od -c file.txt to see newline types (\\r\\n vs \\n)",
            "Inspect binary file headers to identify file format with od -A x -t x1z -N 32 mystery_file",
            "Examine network packet captures at the byte level for protocol debugging",
        ],
        "gotchas": [
            "od collapses repeated identical lines with an asterisk (*) by default -- this hides data in repetitive binary files",
            "The default output format is octal, which is rarely what you want -- use -t x1 for hex bytes or -c for character display",
            "od uses the system byte order for multi-byte formats -- -t x2 shows 2-byte hex in host endianness which may confuse cross-platform work",
        ],
        "related": ["hexdump", "xxd", "strings"],
        "difficulty": "intermediate",
        "extra_flags": {
            "-j": "Skip this many bytes from the beginning of input",
            "-v": "Display all data without collapsing duplicate lines",
            "-w": "Set output width in bytes per line",
        },
    },
    "hexdump": {
        "man_url": "https://man7.org/linux/man-pages/man1/hexdump.1.html",
        "use_cases": [
            "View binary files with the canonical hex+ASCII display with hexdump -C file.bin",
            "Inspect the first 512 bytes of a disk for boot sector analysis with hexdump -C -n 512 /dev/sda",
            "Debug character encoding by checking actual byte values with echo -n 'text' | hexdump -C",
        ],
        "gotchas": [
            "Without -v, hexdump suppresses duplicate lines with asterisks -- use -v to see all data",
            "hexdump without -C shows little-endian 16-bit words which reverses byte pairs -- always use -C for byte-level inspection",
            "The -e flag for custom format strings uses a confusing printf-like syntax that differs from standard printf",
        ],
        "related": ["xxd", "od", "strings"],
        "difficulty": "intermediate",
        "extra_flags": {
            "-e": "Specify custom format string for output",
        },
    },
    "xxd": {
        "man_url": "https://man7.org/linux/man-pages/man1/xxd.1.html",
        "use_cases": [
            "Create a hex dump for inclusion in C source with xxd -i data.bin > data.h",
            "Patch a binary file by editing hex then converting back with xxd file | edit | xxd -r > patched",
            "Get a plain hex string of a file with xxd -p file.bin for checksums or embedding",
        ],
        "gotchas": [
            "xxd -r requires the EXACT same format that xxd produces -- manually edited hex dumps must preserve the offset column format",
            "The -r flag reads hex dump from stdin, not a file argument -- pipe or redirect your edited dump",
            "xxd is bundled with vim, not coreutils -- it may not be available on minimal systems without vim installed",
        ],
        "related": ["hexdump", "od", "vim"],
        "difficulty": "intermediate",
        "extra_flags": {},
    },
    "strings": {
        "man_url": "https://man7.org/linux/man-pages/man1/strings.1.html",
        "use_cases": [
            "Find embedded URLs or file paths in a compiled binary with strings binary | grep -i 'http'",
            "Identify the compiler and libraries used to build an executable with strings program | grep -i gcc",
            "Extract readable text from a corrupted document or firmware image for forensic analysis",
        ],
        "gotchas": [
            "strings only shows sequences of 4+ printable characters by default -- short strings like 2-character error codes are hidden unless you lower -n",
            "strings may show misleading output from random byte sequences that happen to look like text -- not every match is meaningful",
            "On ELF binaries, strings only scans loadable sections by default -- use -a to scan the entire file including debug sections",
        ],
        "related": ["od", "hexdump", "file", "readelf"],
        "difficulty": "beginner",
        "extra_flags": {
            "-e": "Select character encoding (s=7-bit, S=8-bit, b=16-bit big-endian, l=16-bit little-endian)",
        },
    },
    "tac": {
        "man_url": "https://man7.org/linux/man-pages/man1/tac.1.html",
        "use_cases": [
            "View log files with newest entries first with tac /var/log/syslog | head -20",
            "Reverse the order of lines in a file for bottom-up processing with tac input.txt > reversed.txt",
            "Process records separated by blank lines in reverse with tac -s '' data.txt",
        ],
        "gotchas": [
            "tac reverses LINE ORDER, not characters within lines -- use rev to reverse characters",
            "tac reads the entire file into memory for processing -- for very large files consider tail -r on BSD or other approaches",
            "tac is a GNU coreutils command not available on macOS by default -- install via brew install coreutils and use gtac",
        ],
        "related": ["rev", "tail", "sort", "head"],
        "difficulty": "beginner",
        "extra_flags": {
            "-b": "Attach separator before instead of after each record",
            "-r": "Interpret separator as a regular expression",
            "-s": "Use STRING as the record separator instead of newline",
        },
    },

    # =========================================================================
    # SEARCH & NAVIGATION
    # =========================================================================
    "locate": {
        "man_url": "https://man7.org/linux/man-pages/man1/locate.1.html",
        "use_cases": [
            "Instantly find a configuration file by name with locate nginx.conf instead of slow find /",
            "Count how many Python files exist system-wide with locate -c '*.py'",
            "Find recently installed binaries after updating the database with sudo updatedb && locate new_tool",
        ],
        "gotchas": [
            "The database is updated periodically (usually daily via cron) -- recently created files will not appear until you run sudo updatedb",
            "locate shows ALL matches including deleted files still in the database -- verify results exist with locate -e",
            "On modern systems mlocate or plocate may be installed instead of the original locate -- they are CLI-compatible but use different database formats",
        ],
        "related": ["find", "updatedb", "mlocate", "plocate", "fd"],
        "difficulty": "beginner",
        "extra_flags": {
            "-e": "Print only entries for files that currently exist on disk",
            "-b": "Match only against the basename, not the full path",
        },
    },
    "ag": {
        "man_url": "https://github.com/ggreer/the_silver_searcher",
        "use_cases": [
            "Search a codebase for a function definition with ag 'def process_data' --python",
            "Find TODO comments across a project with ag TODO --ignore-dir=node_modules",
            "Search for a pattern only in specific file types with ag -G '\\.jsx?$' 'useState'",
        ],
        "gotchas": [
            "ag respects .gitignore by default -- files ignored by git will not appear in search results unless you use -u (unrestricted)",
            "ag uses PCRE regex by default, not basic regex -- metacharacters like ( and | work without escaping unlike grep",
            "ag has been largely superseded by ripgrep (rg) which is faster in most benchmarks -- consider rg for new workflows",
        ],
        "related": ["rg", "grep", "ack", "fzf"],
        "difficulty": "beginner",
        "extra_flags": {
            "-u": "Search all files, ignoring .gitignore and .ignore rules",
            "-U": "Search all files including binary files",
            "--stats": "Print stats about matches at the end",
        },
    },
    "rg": {
        "man_url": "https://github.com/BurntSushi/ripgrep/blob/master/GUIDE.md",
        "use_cases": [
            "Search for a pattern in only Python files with rg -t py 'import requests'",
            "Find all TODO and FIXME comments with rg -i 'todo|fixme' --glob '!vendor/'",
            "Search with context lines for code review with rg -C 3 'panic!' src/",
            "List only files containing matches for piping to other tools with rg -l 'deprecated' | xargs sed -i 's/deprecated/new_api/g'",
        ],
        "gotchas": [
            "rg skips .gitignore-listed files, hidden files, and binary files by default -- use --no-ignore --hidden -a to search everything",
            "rg uses Rust regex syntax which does not support backreferences or lookahead -- for those patterns use grep -P or ag instead",
            "The -t flag uses built-in type definitions (rg --type-list to see them) -- custom file extensions need --glob or --type-add",
            "rg returns exit code 1 when no matches are found, which can break set -e scripts -- handle it explicitly",
        ],
        "related": ["grep", "ag", "ack", "fd", "fzf"],
        "difficulty": "beginner",
        "extra_flags": {
            "-M": "Set max line length to display (suppress very long lines)",
            "--json": "Output results in JSON format for programmatic consumption",
            "-U": "Enable multiline matching across line boundaries",
            "-S": "Smart case: case-insensitive if all lowercase, sensitive if any uppercase",
            "-e": "Specify multiple patterns (each with its own -e flag)",
            "--sort": "Sort results by path, modified time, accessed time, or created time",
        },
    },
    "ripgrep": {
        "man_url": "https://github.com/BurntSushi/ripgrep/blob/master/GUIDE.md",
        "use_cases": [
            "Search for a pattern in only Python files with rg -t py 'import requests'",
            "Find all TODO and FIXME comments with rg -i 'todo|fixme' --glob '!vendor/'",
            "List only files containing matches with rg -l 'deprecated' for batch processing",
        ],
        "gotchas": [
            "ripgrep skips .gitignore-listed files, hidden files, and binary files by default -- use --no-ignore --hidden to override",
            "ripgrep uses Rust regex syntax which does not support backreferences or lookahead",
            "Typically invoked as rg, not ripgrep -- the binary name is rg",
        ],
        "related": ["grep", "ag", "ack", "fd"],
        "difficulty": "beginner",
        "extra_flags": {},
    },
    "ack": {
        "man_url": "https://beyondgrep.com/documentation/",
        "use_cases": [
            "Search only in Python files with ack --python 'class.*Model'",
            "Find all files of a specific type with ack -f --perl to list Perl source files",
            "Search for a literal string containing regex metacharacters with ack -Q 'array[0]'",
        ],
        "gotchas": [
            "ack uses Perl-compatible regex by default -- regex like \\d, \\w, and lookahead work out of the box",
            "ack is slower than ripgrep (rg) for large codebases -- it remains useful for its Perl regex support and --type system",
            "ack ignores backup files, core dumps, and VCS directories by default -- use --noignore-directory to override",
        ],
        "related": ["rg", "ag", "grep", "fzf"],
        "difficulty": "beginner",
        "extra_flags": {
            "-f": "List all files that would be searched (no pattern required)",
            "--sort-files": "Sort output by filename",
            "--color-match": "Set the color for matched text",
        },
    },
    "fzf": {
        "man_url": "https://github.com/junegunn/fzf",
        "use_cases": [
            "Open a file in your editor with interactive search with vim $(fzf --preview 'head -50 {}')",
            "Interactively search and checkout a git branch with git checkout $(git branch | fzf)",
            "Kill a process interactively with kill -9 $(ps aux | fzf | awk '{print $2}')",
            "Search command history with Ctrl+R integration (enabled via fzf --bash or fzf --zsh setup)",
        ],
        "gotchas": [
            "fzf reads from stdin by default -- if no input is piped, it uses a file finder (find or fd) which may be slow on large directory trees",
            "Key bindings (Ctrl+R, Ctrl+T, Alt+C) require shell integration setup -- run eval \"$(fzf --bash)\" in your .bashrc",
            "fzf returns exit code 130 when the user presses Escape to cancel -- handle this in scripts with || true",
            "The FZF_DEFAULT_COMMAND environment variable controls what command generates the file list -- set it to fd or rg --files for better performance",
        ],
        "related": ["fd", "rg", "find", "grep"],
        "difficulty": "intermediate",
        "extra_flags": {
            "--bind": "Set custom key bindings for actions within fzf",
            "--header": "Display a fixed header line above the match list",
            "--delimiter": "Set field delimiter for --with-nth and --nth",
            "--nth": "Restrict matching to specific fields",
            "--tac": "Reverse input order",
            "--no-sort": "Do not sort the results",
        },
    },
    "fd": {
        "man_url": "https://github.com/sharkdp/fd",
        "use_cases": [
            "Find all Python files in a project with fd -e py",
            "Find and delete all .DS_Store files with fd -H '.DS_Store' -x rm",
            "Find large files with fd -e log -x ls -lh {} to inspect file sizes",
            "Find recently modified files with fd --changed-within 1d",
        ],
        "gotchas": [
            "fd ignores .gitignore patterns and hidden files by default -- use -H for hidden files and -I to skip .gitignore filtering",
            "fd uses regex patterns by default, not glob -- use -g to switch to glob matching for patterns like '*.py'",
            "On some Linux distributions fd is installed as fdfind to avoid conflict with another package -- create an alias if needed",
        ],
        "related": ["find", "fzf", "rg", "locate"],
        "difficulty": "beginner",
        "extra_flags": {
            "--changed-within": "Filter to files modified within a time duration",
            "--changed-before": "Filter to files modified before a time duration",
            "--size": "Filter by file size (e.g., +1m for files over 1MB)",
            "-0": "Separate results with NUL for xargs -0",
            "-L": "Follow symbolic links",
            "-p": "Match against the full path, not just the filename",
        },
    },
    "exa": {
        "man_url": "https://github.com/ogham/exa",
        "use_cases": [
            "List files with git status indicators with exa -la --git",
            "View a directory tree with file sizes with exa -T -L 3 --icons -s size",
            "List files sorted by modification time with exa -la -s modified --reverse",
        ],
        "gotchas": [
            "exa is no longer maintained as of 2023 -- the community fork eza is the actively maintained successor",
            "The --icons flag requires a Nerd Font installed and configured in your terminal -- without it you get garbled characters",
            "exa uses different flags than ls -- muscle memory for ls -ltr will not work (exa uses -s modified --reverse instead of -t -r)",
        ],
        "related": ["ls", "lsd", "eza", "tree"],
        "difficulty": "beginner",
        "extra_flags": {
            "-d": "List directories themselves, not their contents",
            "--no-permissions": "Suppress the permissions column",
            "--time-style": "Set time display format (default, iso, long-iso, full-iso)",
        },
    },
    "lsd": {
        "man_url": "https://github.com/lsd-rs/lsd",
        "use_cases": [
            "Get a visually rich directory listing with lsd -la for quick file inspection",
            "View a colorful directory tree with lsd --tree --depth 2",
            "Sort files by size to find large files with lsd -lS",
        ],
        "gotchas": [
            "lsd requires a Nerd Font for icons to render correctly -- without it icons appear as broken characters",
            "lsd's flag compatibility with ls is intentional but not 100% -- some obscure ls flags may not work",
            "Color output is on by default which can interfere with pipe processing -- use --color never for scripts",
        ],
        "related": ["ls", "exa", "tree"],
        "difficulty": "beginner",
        "extra_flags": {
            "--blocks": "Configure which metadata blocks to show",
            "--date": "Set date format (date, relative, +format-string)",
            "--group-directories-first": "List directories before files",
            "--no-symlink": "Do not follow symbolic links",
        },
    },
    "broot": {
        "man_url": "https://dystroy.org/broot/",
        "use_cases": [
            "Explore a large codebase interactively by typing to fuzzy-filter the tree view",
            "Find and navigate to deeply nested files without typing full paths",
            "View disk usage in a tree with broot -w to identify large directories",
        ],
        "gotchas": [
            "broot requires a shell function (br) for cd-on-quit behavior -- run broot --install to set it up, then use br instead of broot",
            "First launch creates a configuration file at ~/.config/broot/conf.hjson -- customize verbs and key bindings there",
            "broot may appear unfamiliar at first -- type text to filter, use arrow keys to navigate, and press Enter to open or Alt+Enter to cd",
        ],
        "related": ["tree", "ranger", "nnn", "fzf"],
        "difficulty": "intermediate",
        "extra_flags": {
            "-g": "Show git status for files",
            "--sort-by-date": "Sort entries by modification date",
            "--sort-by-size": "Sort entries by size",
        },
    },
    "ranger": {
        "man_url": "https://github.com/ranger/ranger",
        "use_cases": [
            "Navigate and preview files visually in a three-column Miller layout",
            "Perform bulk file operations (rename, move, copy) with vi keybindings",
            "Preview images in terminal with ranger (requires w3m or ueberzug for image support)",
        ],
        "gotchas": [
            "ranger uses vi keybindings by default -- j/k to move, h to go up, l to enter directories",
            "To cd to the last ranger directory on quit, you must use the shell function: add source ranger-cd to your shell config",
            "ranger can be slow on very large directories because it stats every file for preview -- use nnn or lf for large directory trees",
        ],
        "related": ["nnn", "mc", "lf", "broot"],
        "difficulty": "intermediate",
        "extra_flags": {
            "--copy-config": "Create a copy of the default config files for customization",
        },
    },
    "mc": {
        "man_url": "https://midnight-commander.org/",
        "use_cases": [
            "Manage files across two directories simultaneously with a dual-pane view",
            "Connect to remote servers via SFTP/FTP with mc's built-in virtual filesystem",
            "Edit files with the built-in editor mcedit which supports syntax highlighting",
        ],
        "gotchas": [
            "mc captures the F-keys which may conflict with terminal or tmux key bindings -- use Esc+number as an alternative",
            "mc's FTP/SFTP panel (accessed via cd sh://user@host) can be slow on high-latency connections",
            "The mouse support can interfere with terminal copy-paste -- hold Shift while selecting to use the terminal's native selection",
        ],
        "related": ["ranger", "nnn", "lf"],
        "difficulty": "intermediate",
        "extra_flags": {
            "-s": "Run in slow terminal mode for better compatibility",
            "-u": "Disable concurrent shell (use subshell only if needed)",
        },
    },
    "nnn": {
        "man_url": "https://github.com/jarun/nnn",
        "use_cases": [
            "Navigate large directory trees quickly with minimal resource usage",
            "Use plugins for previewing files, opening in editors, or batch renaming with nnn -P preview",
            "Select multiple files for batch operations with nnn -p /tmp/sel and process the selection file",
        ],
        "gotchas": [
            "nnn does not cd on quit by default -- you must configure the shell function (n) using the nnn-quitcd setup",
            "nnn uses single-key shortcuts that are case-sensitive -- capital letters do different things than lowercase",
            "nnn requires the NNN_PLUG environment variable to be set for plugins to work",
        ],
        "related": ["ranger", "lf", "mc", "broot"],
        "difficulty": "intermediate",
        "extra_flags": {
            "-c": "Set NNN_FCOLORS environment for 8-color scheme",
            "-e": "Open text files in $VISUAL or $EDITOR on Enter",
            "-o": "Open files with only a single click in navigation",
            "-x": "Enable various system notifications and copy path to clipboard",
        },
    },
    "lf": {
        "man_url": "https://github.com/gokcehan/lf",
        "use_cases": [
            "Navigate files with a ranger-like interface but faster startup due to Go implementation",
            "Configure custom file openers and previews through the lfrc configuration file",
            "Use with fzf for fuzzy file search within the file manager",
        ],
        "gotchas": [
            "lf configuration uses its own command language, not shell script -- refer to lf -doc for syntax",
            "Like nnn and ranger, cd-on-quit requires a shell wrapper function -- use the lfcd function from the documentation",
            "lf defaults to a single-column view unlike ranger's three-column layout -- customize with set ratios",
        ],
        "related": ["ranger", "nnn", "mc", "broot"],
        "difficulty": "intermediate",
        "extra_flags": {},
    },
    "apropos": {
        "man_url": "https://man7.org/linux/man-pages/man1/apropos.1.html",
        "use_cases": [
            "Find commands related to a concept with apropos compress to discover compression tools",
            "Search for disk-related commands with apropos partition to find fdisk, parted, etc.",
            "Discover all commands in a specific man section with apropos -s 8 network for admin network tools",
        ],
        "gotchas": [
            "apropos searches the whatis database which must be built first -- run sudo mandb if you get no results",
            "Results can be noisy -- use apropos -e for exact matches or combine with grep to narrow results",
            "apropos is equivalent to man -k -- they use the same database and return the same results",
        ],
        "related": ["whatis", "man", "info", "help"],
        "difficulty": "beginner",
        "extra_flags": {},
    },
    "whatis": {
        "man_url": "https://man7.org/linux/man-pages/man1/whatis.1.html",
        "use_cases": [
            "Quickly check what a command does with whatis tar before reading the full man page",
            "Get one-line descriptions of multiple commands at once with whatis ls cp mv rm",
            "Verify which man page section a command belongs to with whatis printf to see both the shell builtin and C library versions",
        ],
        "gotchas": [
            "whatis requires the man database to be built -- if it returns nothing, run sudo mandb",
            "whatis only shows exact name matches by default -- use apropos (man -k) for keyword searches across descriptions",
        ],
        "related": ["apropos", "man", "help", "info"],
        "difficulty": "beginner",
        "extra_flags": {},
    },
    "help": {
        "man_url": "https://www.gnu.org/software/bash/manual/html_node/Bash-Builtins.html",
        "use_cases": [
            "Look up syntax for a shell builtin with help test or help [[ when man page is unavailable",
            "Get a quick list of all builtins with help -d '*'",
            "View man-page-style formatted help with help -m export",
        ],
        "gotchas": [
            "help only works for bash builtins -- external commands like grep or find need man instead",
            "help is itself a builtin and is not available in sh or dash -- it is bash-specific",
            "Some builtins have both a help entry and a man page -- the help version covers the bash-specific behavior",
        ],
        "related": ["man", "whatis", "apropos", "info"],
        "difficulty": "beginner",
        "extra_flags": {},
    },
    "info": {
        "man_url": "https://www.gnu.org/software/texinfo/manual/info-stnd/info-stnd.html",
        "use_cases": [
            "Read detailed GNU coreutils documentation with info coreutils for comprehensive examples",
            "Navigate directly to a specific topic with info bash 'Shell Expansions'",
            "Read info pages that contain more detail than their man page counterparts, especially for GNU tools",
        ],
        "gotchas": [
            "info uses Emacs-style navigation by default (Ctrl+F forward, Ctrl+B back, Tab for links) -- use --vi-keys for vi-style",
            "Not all commands have info pages -- if no info page exists, info falls back to displaying the man page",
            "The info reader is separate from man -- info coreutils has a full tutorial that man pages lack",
        ],
        "related": ["man", "help", "whatis", "apropos"],
        "difficulty": "beginner",
        "extra_flags": {},
    },

    # =========================================================================
    # DEVELOPMENT - BUILD SYSTEMS
    # =========================================================================
    "make": {
        "man_url": "https://www.gnu.org/software/make/manual/make.html",
        "use_cases": [
            "Build a C project with make all or just make to run the default target",
            "Clean build artifacts with make clean before a fresh rebuild",
            "Run a parallel build on all cores with make -j$(nproc) for faster compilation",
            "Perform a dry run to see what commands would execute with make -n before committing",
        ],
        "gotchas": [
            "Makefiles require actual TAB characters for recipe indentation -- spaces cause 'missing separator' errors and this is the single most common Makefile problem",
            "Variables set on the command line (make VAR=val) override values set in the Makefile -- use override directive in the Makefile to prevent this",
            "make -j without a number spawns unlimited parallel jobs which can overwhelm the system -- always specify a count like -j4 or -j$(nproc)",
            "make only rebuilds targets whose dependencies have changed -- if timestamps are wrong (e.g., after a timezone change or git checkout), use make -B to force rebuild",
        ],
        "related": ["cmake", "ninja", "gcc", "autoconf"],
        "difficulty": "intermediate",
        "extra_flags": {
            "-B": "Unconditionally make all targets (force rebuild)",
            "-C": "Change to directory before reading Makefile",
            "-k": "Keep going when some targets cannot be made",
            "-s": "Silent mode, do not echo recipes",
            "-w": "Print working directory info (useful for recursive make)",
            "-q": "Question mode: exit 0 if target is up to date, 1 if not",
            "-p": "Print the database of rules and variables (debug)",
        },
    },
    "cmake": {
        "man_url": "https://cmake.org/cmake/help/latest/manual/cmake.1.html",
        "use_cases": [
            "Configure an out-of-source build with cmake -S . -B build to keep source tree clean",
            "Build a release configuration with cmake -DCMAKE_BUILD_TYPE=Release -S . -B build",
            "Build the project after configuration with cmake --build build -j$(nproc)",
            "Install after building with cmake --install build --prefix /usr/local",
        ],
        "gotchas": [
            "CMake generates build files but does not build -- you need to run the generated build system (make, ninja) or use cmake --build",
            "CMake caches variables in CMakeCache.txt -- if you change a -D option and it does not take effect, delete the cache or the build directory",
            "The minimum CMake version in cmake_minimum_required affects available features -- old minimum versions may disable modern CMake features",
            "Prefer cmake --build build over cd build && make because it works regardless of the generator (Make, Ninja, VS)",
        ],
        "related": ["make", "ninja", "gcc", "clang"],
        "difficulty": "intermediate",
        "extra_flags": {
            "--preset": "Use a named preset from CMakePresets.json",
            "-Wdev": "Enable developer warnings",
            "--fresh": "Configure a fresh build tree, removing any existing cache",
        },
    },
    "ninja": {
        "man_url": "https://ninja-build.org/manual.html",
        "use_cases": [
            "Build a CMake project faster by generating Ninja files with cmake -G Ninja -S . -B build && ninja -C build",
            "Build with verbose output to debug compilation issues with ninja -v",
            "Clean build artifacts with ninja -t clean",
        ],
        "gotchas": [
            "Ninja is not designed to be written by hand -- use CMake or Meson to generate build.ninja files",
            "Ninja defaults to parallel builds using all available cores -- unlike make, you rarely need -j",
            "Ninja does not support pattern rules or includes like Makefiles -- it is intentionally minimal and relies on a generator",
        ],
        "related": ["cmake", "meson", "make"],
        "difficulty": "intermediate",
        "extra_flags": {},
    },
    "meson": {
        "man_url": "https://mesonbuild.com/Reference-manual.html",
        "use_cases": [
            "Set up a new C/C++ project build with meson setup builddir",
            "Create a release build with meson setup --buildtype=release builddir",
            "Run project tests after building with meson test -C builddir",
        ],
        "gotchas": [
            "Meson requires a separate build directory -- in-source builds are not supported",
            "Meson uses Python-like syntax in meson.build files but is not actually Python -- it is a custom DSL",
            "Build options can only be changed with meson configure, not by editing the build directory -- regenerate with meson setup --reconfigure if needed",
        ],
        "related": ["ninja", "cmake", "make"],
        "difficulty": "intermediate",
        "extra_flags": {
            "--reconfigure": "Regenerate build configuration without clearing the build directory",
            "--wipe": "Clear the build directory and reconfigure from scratch",
        },
    },
    "autoconf": {
        "man_url": "https://www.gnu.org/software/autoconf/manual/autoconf.html",
        "use_cases": [
            "Generate a configure script from configure.ac with autoreconf --install",
            "Regenerate all autotools files after modifying configure.ac with autoreconf -fiv",
            "Create a portable build system for distributable open-source packages",
        ],
        "gotchas": [
            "autoconf is typically used through autoreconf which runs autoconf, automake, aclocal, and other tools in the correct order",
            "configure.ac uses M4 macro language which has unusual quoting rules -- use [ ] for quoting, not single or double quotes",
            "The autotools toolchain (autoconf + automake + libtool) has a steep learning curve -- CMake or Meson are simpler alternatives for new projects",
        ],
        "related": ["automake", "make", "cmake", "meson"],
        "difficulty": "advanced",
        "extra_flags": {},
    },
    "automake": {
        "man_url": "https://www.gnu.org/software/automake/manual/automake.html",
        "use_cases": [
            "Generate Makefile.in templates from Makefile.am files with automake --add-missing",
            "Set up the standard GNU build system with aclocal && automake --add-missing && autoconf",
            "Create a distribution tarball with make dist after automake setup",
        ],
        "gotchas": [
            "Makefile.am files use a special syntax that is not regular Makefile syntax -- variables like bin_PROGRAMS and _SOURCES follow automake naming conventions",
            "automake --foreign relaxes GNU strictness requirements -- without it, automake expects NEWS, README, AUTHORS, ChangeLog files to exist",
            "automake must be run after aclocal and before autoconf -- the order matters and is why autoreconf exists",
        ],
        "related": ["autoconf", "make", "cmake"],
        "difficulty": "advanced",
        "extra_flags": {},
    },

    # =========================================================================
    # DEVELOPMENT - COMPILERS & LINKERS
    # =========================================================================
    "gcc": {
        "man_url": "https://gcc.gnu.org/onlinedocs/gcc/Invoking-GCC.html",
        "use_cases": [
            "Compile a C program with warnings and debug info with gcc -Wall -Wextra -g -o program main.c",
            "Build an optimized release binary with gcc -O2 -o fast_program main.c",
            "Compile multiple source files and link with a library with gcc -o app main.c utils.c -lm -lpthread",
            "Generate only the object file for later linking with gcc -c -o module.o module.c",
        ],
        "gotchas": [
            "Order matters for -l flags: libraries must come AFTER the object files that reference them -- gcc main.c -lm works but gcc -lm main.c may fail with undefined references",
            "-O2 is generally safe for production but -O3 can occasionally produce different floating-point results or expose latent bugs in code with undefined behavior",
            "Without -Wall -Wextra many real bugs go unreported -- always enable warnings and consider -Werror in CI",
            "gcc and g++ are different frontends -- use g++ for C++ code, gcc for C, even though gcc can sometimes compile C++",
        ],
        "related": ["g++", "clang", "make", "gdb", "ld"],
        "difficulty": "intermediate",
        "extra_flags": {
            "-Wextra": "Enable extra warnings beyond -Wall",
            "-pedantic": "Issue warnings demanded by strict ISO C compliance",
            "-fsanitize": "Enable runtime sanitizers (address, undefined, thread, memory)",
            "-D": "Define a preprocessor macro",
            "-S": "Compile to assembly instead of object code",
            "-E": "Preprocess only, do not compile",
            "-pie": "Create a position-independent executable",
            "-shared": "Create a shared library",
        },
    },
    "g++": {
        "man_url": "https://gcc.gnu.org/onlinedocs/gcc/Invoking-GCC.html",
        "use_cases": [
            "Compile a C++17 program with g++ -std=c++17 -Wall -o app main.cpp",
            "Build with AddressSanitizer for memory bug detection with g++ -fsanitize=address -g -o test test.cpp",
            "Compile and link with pthread support with g++ -o server server.cpp -lpthread",
        ],
        "gotchas": [
            "g++ links the C++ standard library automatically unlike gcc -- use g++ (not gcc) for C++ code to avoid linker errors",
            "The default C++ standard varies by GCC version -- always specify -std=c++17 or -std=c++20 explicitly for portability",
            "Template errors produce notoriously long error messages -- read from the bottom up to find the actual source of the error",
        ],
        "related": ["gcc", "clang++", "make", "gdb"],
        "difficulty": "intermediate",
        "extra_flags": {},
    },
    "clang": {
        "man_url": "https://clang.llvm.org/docs/ClangCommandLineReference.html",
        "use_cases": [
            "Compile with AddressSanitizer for catching buffer overflows with clang -fsanitize=address -g -o test test.c",
            "Get detailed error messages with clang -Wall -Wextra -std=c17 -o app main.c",
            "Cross-compile for a different target with clang --target=aarch64-linux-gnu -o app main.c",
        ],
        "gotchas": [
            "clang error messages are generally more readable than gcc's -- clang is often preferred for development even if gcc is used for release builds",
            "clang's ABI is compatible with gcc on Linux but some edge cases differ -- test with both compilers in CI",
            "On macOS, the cc and gcc commands are actually clang in disguise -- check with cc --version",
        ],
        "related": ["clang++", "gcc", "lldb", "make"],
        "difficulty": "intermediate",
        "extra_flags": {},
    },
    "clang++": {
        "man_url": "https://clang.llvm.org/docs/ClangCommandLineReference.html",
        "use_cases": [
            "Compile modern C++20 code with clang++ -std=c++20 -Wall -o app main.cpp",
            "Use clang++ with libc++ instead of libstdc++ with clang++ -stdlib=libc++ -o app main.cpp",
            "Run UndefinedBehaviorSanitizer to catch UB at runtime with clang++ -fsanitize=undefined -g -o test test.cpp",
        ],
        "gotchas": [
            "clang++ defaults to libstdc++ on Linux but libc++ on macOS -- this can cause ABI incompatibility when mixing libraries compiled with different standard libraries",
            "clang++ may produce different warnings than g++ -- enable both in CI for maximum bug detection",
        ],
        "related": ["clang", "g++", "lldb", "cmake"],
        "difficulty": "intermediate",
        "extra_flags": {},
    },
    "cc": {
        "man_url": "https://man7.org/linux/man-pages/man1/cc.1p.html",
        "use_cases": [
            "Compile a portable C program with cc -o program main.c as a system-agnostic compiler invocation",
            "Use in Makefiles and configure scripts as the default compiler name that works on any Unix system",
        ],
        "gotchas": [
            "cc is a symlink to the system default C compiler -- it may be gcc, clang, or another compiler depending on the OS",
            "On macOS cc points to clang, on most Linux systems cc points to gcc -- check with cc --version",
            "Using cc instead of gcc or clang in build scripts improves portability across Unix-like systems",
        ],
        "related": ["gcc", "clang", "make"],
        "difficulty": "beginner",
        "extra_flags": {},
    },
    "ld": {
        "man_url": "https://sourceware.org/binutils/docs/ld/",
        "use_cases": [
            "Link object files into an executable with ld -o program main.o utils.o -lc",
            "Create a shared library with ld -shared -o libfoo.so foo.o",
            "Use a custom linker script for embedded firmware with ld -T linker.ld -o firmware.elf startup.o main.o",
        ],
        "gotchas": [
            "ld is usually invoked indirectly through gcc or clang which add necessary startup files and library paths -- calling ld directly requires specifying crt0.o and other platform files",
            "Library order matters: ld processes libraries left to right and only includes symbols needed at that point -- put -l flags after the .o files that need them",
            "ld uses the system default linker script unless -T is specified -- this controls memory layout and is critical for embedded/OS development",
        ],
        "related": ["gcc", "as", "ar", "nm", "ldd"],
        "difficulty": "advanced",
        "extra_flags": {
            "-static": "Do not link against shared libraries",
            "-pie": "Create a position-independent executable",
            "--as-needed": "Only link libraries that resolve undefined symbols",
        },
    },
    "as": {
        "man_url": "https://sourceware.org/binutils/docs/as/",
        "use_cases": [
            "Assemble an x86 assembly file with as -o output.o source.s",
            "Generate a listing file alongside assembly with as -ahlms=listing.lst source.s",
            "Assemble with debug information for gdb with as --gstabs -o debug.o source.s",
        ],
        "gotchas": [
            "as uses AT&T syntax by default on x86 where source comes before destination -- this is opposite to Intel/NASM syntax",
            "The assembler is architecture-specific -- cross-assembling requires a cross-compilation toolchain (e.g., aarch64-linux-gnu-as)",
            "as is usually invoked automatically by gcc when compiling .s or .S files -- direct use is mainly for OS development and embedded work",
        ],
        "related": ["gcc", "ld", "objdump", "gdb"],
        "difficulty": "advanced",
        "extra_flags": {},
    },
    "ar": {
        "man_url": "https://sourceware.org/binutils/docs/binutils/ar.html",
        "use_cases": [
            "Create a static library from object files with ar rcs libmylib.a obj1.o obj2.o",
            "List contents of a static library with ar t libmylib.a",
            "Extract a specific object file from a library with ar x libmylib.a module.o",
        ],
        "gotchas": [
            "Always use 's' with 'r' (ar rcs) to create/update the symbol index -- without it the linker may not find symbols",
            "ar creates static libraries (.a) not shared libraries (.so) -- use gcc -shared for shared libraries",
            "The r flag replaces files in the archive, c suppresses the creation warning, and s creates the index -- rcs is the standard combination",
        ],
        "related": ["gcc", "ld", "nm", "ranlib"],
        "difficulty": "intermediate",
        "extra_flags": {},
    },

    # =========================================================================
    # DEVELOPMENT - DEBUGGERS & ANALYSIS
    # =========================================================================
    "gdb": {
        "man_url": "https://sourceware.org/gdb/current/onlinedocs/gdb/",
        "use_cases": [
            "Debug a segfault by running gdb ./program then typing run, and bt (backtrace) after the crash",
            "Set a breakpoint and inspect variables with gdb -ex 'break main' -ex 'run' ./program",
            "Examine a core dump with gdb ./program core to see where a crash occurred post-mortem",
            "Debug with source display using gdb -tui ./program for a visual split-screen interface",
        ],
        "gotchas": [
            "Programs must be compiled with -g for meaningful debug output -- without it gdb shows only assembly and hex addresses",
            "Optimized code (-O2, -O3) confuses gdb because variables are optimized out and code is reordered -- debug with -O0 -g",
            "gdb prints variables in the current scope only -- if a variable shows as 'optimized out' try compiling with -O0",
            "Use -ex to pass commands non-interactively: gdb -batch -ex run -ex bt --args ./program for automated crash analysis",
        ],
        "related": ["lldb", "valgrind", "gcc", "objdump"],
        "difficulty": "intermediate",
        "extra_flags": {
            "-batch": "Run in batch mode (exit after processing -ex commands)",
            "-p": "Attach to running process by PID",
            "-core": "Load a core dump file for post-mortem debugging",
            "-x": "Execute GDB commands from a file",
        },
    },
    "lldb": {
        "man_url": "https://lldb.llvm.org/use/tutorial.html",
        "use_cases": [
            "Debug a program on macOS with lldb ./program (lldb is the default macOS debugger)",
            "Attach to a running process with lldb -p $(pgrep myapp)",
            "Analyze a core dump with lldb -c core ./program for post-mortem debugging",
        ],
        "gotchas": [
            "lldb commands differ from gdb: use 'thread backtrace' instead of 'bt', 'breakpoint set -n main' instead of 'break main'",
            "On macOS, codesigning is required to debug other processes -- lldb shipped with Xcode has the proper entitlements",
            "lldb uses the LLVM expression parser which can evaluate C++ and Swift but has quirks with complex template expressions",
        ],
        "related": ["gdb", "clang", "valgrind"],
        "difficulty": "intermediate",
        "extra_flags": {},
    },
    "valgrind": {
        "man_url": "https://valgrind.org/docs/manual/manual.html",
        "use_cases": [
            "Check for memory leaks with valgrind --leak-check=full --track-origins=yes ./program",
            "Profile cache usage with valgrind --tool=cachegrind ./program",
            "Generate a call graph for profiling with valgrind --tool=callgrind ./program then view with kcachegrind",
        ],
        "gotchas": [
            "Programs run 10-30x slower under valgrind -- reduce input sizes for testing or it may take hours",
            "Compile with -g -O0 for accurate line numbers -- optimized code (-O2+) causes valgrind to report false positives for uninitialized values",
            "Valgrind doubles memory usage (1.25x allocation + ~120 bytes overhead per malloc) -- you may need to reduce parallel workers or input sizes",
            "Valgrind only works on Linux and macOS x86_64 -- it does not support ARM64 on macOS (Apple Silicon) natively",
            "Use --suppressions to ignore known false positives from system libraries",
        ],
        "related": ["gdb", "gcc", "clang"],
        "difficulty": "intermediate",
        "extra_flags": {
            "-v": "Verbose mode with more details about each error",
            "--gen-suppressions": "Generate suppression entries for each error (all or yes)",
            "--vgdb": "Enable gdb to connect to valgrind for interactive debugging",
        },
    },
    "objdump": {
        "man_url": "https://sourceware.org/binutils/docs/binutils/objdump.html",
        "use_cases": [
            "Disassemble a binary to view assembly with objdump -d program",
            "View disassembly interleaved with source code with objdump -d -S -l program (requires -g)",
            "Inspect section headers and sizes with objdump -h program to understand binary layout",
        ],
        "gotchas": [
            "objdump -d only disassembles executable sections -- use -D to disassemble ALL sections including data",
            "Source interleaving with -S requires the binary to be compiled with -g debug info",
            "objdump uses AT&T syntax by default on x86 -- use -M intel for Intel syntax if you prefer it",
        ],
        "related": ["nm", "readelf", "gdb", "strings"],
        "difficulty": "advanced",
        "extra_flags": {
            "-M": "Pass disassembler options (e.g., -M intel for Intel syntax)",
            "-j": "Disassemble only the specified section",
        },
    },
    "nm": {
        "man_url": "https://sourceware.org/binutils/docs/binutils/nm.html",
        "use_cases": [
            "List all exported symbols in a shared library with nm -gD libfoo.so",
            "Find undefined symbols that need resolving with nm -u program.o",
            "Demangle C++ symbols for readability with nm -C libcpp.so",
        ],
        "gotchas": [
            "nm cannot read stripped binaries -- if nm shows no symbols, the binary was stripped with strip",
            "For shared libraries, use -D to show dynamic symbols -- regular nm may show nothing for .so files",
            "Symbol types: T=text/code, D=data, U=undefined, B=BSS -- U symbols are what the linker needs to resolve",
        ],
        "related": ["objdump", "readelf", "ldd", "ar"],
        "difficulty": "advanced",
        "extra_flags": {},
    },
    "readelf": {
        "man_url": "https://sourceware.org/binutils/docs/binutils/readelf.html",
        "use_cases": [
            "Inspect ELF headers to determine architecture with readelf -h binary",
            "List dynamic library dependencies with readelf -d binary | grep NEEDED",
            "View all symbols including their types and sizes with readelf -s --wide program",
        ],
        "gotchas": [
            "readelf only works on ELF binaries (Linux/Unix) -- it cannot read Mach-O (macOS) or PE (Windows) binaries",
            "Use -W (wide) to prevent long symbol names from being truncated in output",
            "readelf -d shows dynamic section including NEEDED (shared library dependencies) and RPATH -- useful for diagnosing library loading issues",
        ],
        "related": ["objdump", "nm", "ldd", "file"],
        "difficulty": "advanced",
        "extra_flags": {
            "-n": "Display the note segments (build ID, etc.)",
            "-V": "Display the version sections",
        },
    },
    "ldd": {
        "man_url": "https://man7.org/linux/man-pages/man1/ldd.1.html",
        "use_cases": [
            "Find all shared library dependencies of a binary with ldd ./myapp",
            "Diagnose 'cannot open shared object file' errors by checking which libraries are missing",
            "Verify that a binary links to the expected version of a library with ldd -v ./myapp",
        ],
        "gotchas": [
            "NEVER run ldd on untrusted binaries -- ldd can execute the binary's code to resolve dependencies, which is a security risk. Use objdump -p or readelf -d instead",
            "ldd shows the resolved paths at the current moment -- results depend on LD_LIBRARY_PATH and ldconfig cache",
            "If ldd shows 'not found' for a library, the library is either not installed or not in the linker search path -- fix with ldconfig or LD_LIBRARY_PATH",
        ],
        "related": ["readelf", "nm", "ldconfig", "objdump"],
        "difficulty": "intermediate",
        "extra_flags": {},
    },

    # =========================================================================
    # DEVELOPMENT - CONTAINERS & INFRASTRUCTURE
    # =========================================================================
    "docker-compose": {
        "man_url": "https://docs.docker.com/compose/reference/",
        "use_cases": [
            "Start a full application stack in the background with docker-compose up -d",
            "View real-time logs from all services with docker-compose logs -f",
            "Rebuild images after code changes with docker-compose up --build -d",
            "Scale a specific service with docker-compose up -d --scale worker=3",
        ],
        "gotchas": [
            "docker-compose (V1, Python) is deprecated -- use docker compose (V2, Go plugin) which is now built into Docker CLI",
            "V2 uses hyphens in container names (myproject-svc-1) instead of V1's underscores (myproject_svc_1) -- this can break scripts that parse container names",
            "The top-level version: field in docker-compose.yml is ignored by V2 -- it uses the Compose Specification directly",
            "docker-compose down removes containers but not volumes -- add -v to also remove named volumes, or data persists between restarts",
        ],
        "related": ["docker", "podman", "kubectl"],
        "difficulty": "intermediate",
        "extra_flags": {
            "--env-file": "Specify an alternate .env file for environment variable substitution",
            "--profile": "Specify a profile to enable optional services",
            "--scale": "Scale a service to N instances",
        },
    },
    "podman": {
        "man_url": "https://docs.podman.io/en/latest/",
        "use_cases": [
            "Run containers without root privileges with podman run --rm -it ubuntu bash",
            "Use as a drop-in Docker replacement with alias docker=podman in your shell config",
            "Build OCI images with podman build -t myapp . using the same Dockerfile syntax",
        ],
        "gotchas": [
            "Podman is daemonless -- there is no background service to start, which means podman ps only shows your containers not other users'",
            "Rootless podman uses user namespaces which can cause UID mapping issues -- files created inside containers may appear as 'nobody' on the host",
            "podman-compose exists but is less mature than docker compose -- for complex stacks, test compatibility carefully",
        ],
        "related": ["docker", "docker-compose", "buildah", "kubectl"],
        "difficulty": "intermediate",
        "extra_flags": {},
    },
    "kubectl": {
        "man_url": "https://kubernetes.io/docs/reference/kubectl/",
        "use_cases": [
            "View running pods in all namespaces with kubectl get pods -A",
            "Debug a failing pod by viewing its logs with kubectl logs pod-name -f --previous",
            "Execute a shell inside a running container with kubectl exec -it pod-name -- /bin/sh",
            "Apply infrastructure changes declaratively with kubectl apply -f deployment.yaml",
        ],
        "gotchas": [
            "Always specify -n namespace or set a default with kubectl config set-context --current --namespace=myns -- forgetting the namespace is a very common source of confusion",
            "kubectl apply tracks changes via annotations -- switching between apply and create/replace can cause conflicts",
            "kubectl delete pod does not prevent recreation -- Deployments automatically recreate deleted pods. Delete the Deployment instead to stop pods permanently",
            "kubectl logs only shows logs from the current container instance -- use --previous to see logs from the crashed previous instance",
        ],
        "related": ["helm", "minikube", "docker", "podman"],
        "difficulty": "intermediate",
        "extra_flags": {
            "--dry-run": "Preview the request without sending it (client or server side)",
            "-w": "Watch for changes to resources in real time",
            "--context": "Specify which kubeconfig context (cluster) to use",
            "--all-namespaces": "List resources across all namespaces (shorthand: -A)",
        },
    },
    "helm": {
        "man_url": "https://helm.sh/docs/helm/",
        "use_cases": [
            "Install a chart from a repository with helm install myrelease bitnami/nginx",
            "Upgrade a release with new values with helm upgrade myrelease ./mychart --values prod-values.yaml",
            "Preview rendered manifests before applying with helm template myrelease ./mychart",
            "Rollback to a previous release version with helm rollback myrelease 2",
        ],
        "gotchas": [
            "helm install and helm upgrade are separate operations -- use helm upgrade --install for idempotent deployments that work regardless of whether the release exists",
            "Helm stores release metadata as Secrets in the namespace -- deleting those secrets breaks Helm's ability to manage the release",
            "Chart values are merged, not replaced -- nested YAML structures may accumulate unexpected values across upgrades",
            "Always use --dry-run and helm diff (plugin) to preview changes before upgrading production releases",
        ],
        "related": ["kubectl", "minikube", "docker"],
        "difficulty": "intermediate",
        "extra_flags": {
            "--atomic": "Roll back automatically if the install/upgrade fails",
            "--debug": "Show verbose debug output and rendered templates",
            "template": "Render chart templates locally without deploying",
            "rollback": "Roll back a release to a previous revision",
        },
    },
    "minikube": {
        "man_url": "https://minikube.sigs.k8s.io/docs/",
        "use_cases": [
            "Start a local Kubernetes cluster for development with minikube start",
            "Access the Kubernetes dashboard with minikube dashboard",
            "Use minikube's Docker daemon to build images directly with eval $(minikube docker-env)",
            "Test with a specific Kubernetes version with minikube start --kubernetes-version=v1.28.0",
        ],
        "gotchas": [
            "minikube runs a single-node cluster -- it does not simulate multi-node scenarios or network policies accurately",
            "minikube tunnel is required for LoadBalancer services to get external IPs -- without it they stay pending",
            "minikube consumes significant memory and CPU -- allocate at least 2 CPUs and 4GB RAM or workloads will be unstable",
        ],
        "related": ["kubectl", "helm", "docker", "kind"],
        "difficulty": "intermediate",
        "extra_flags": {
            "--addons": "Enable specific minikube addons (metrics-server, ingress, etc.)",
            "tunnel": "Create a route to services deployed with type LoadBalancer",
            "service": "Get the URL of a service for browser access",
        },
    },
    "vagrant": {
        "man_url": "https://developer.hashicorp.com/vagrant/docs",
        "use_cases": [
            "Create a reproducible development VM with vagrant init ubuntu/jammy64 && vagrant up",
            "SSH into the development VM with vagrant ssh",
            "Re-run provisioning scripts with vagrant provision after updating your Vagrantfile",
        ],
        "gotchas": [
            "Vagrant requires a hypervisor (VirtualBox, VMware, or libvirt) -- install one before using Vagrant",
            "vagrant destroy permanently deletes the VM and all its data -- use vagrant halt for a temporary stop",
            "Synced folders use VirtualBox shared folders by default which can be slow -- use NFS or rsync for better performance",
        ],
        "related": ["docker", "terraform", "ansible"],
        "difficulty": "intermediate",
        "extra_flags": {},
    },
    "terraform": {
        "man_url": "https://developer.hashicorp.com/terraform/cli",
        "use_cases": [
            "Initialize a project and download providers with terraform init",
            "Preview infrastructure changes before applying with terraform plan -out=tfplan",
            "Apply infrastructure changes with terraform apply tfplan",
            "Tear down all managed infrastructure with terraform destroy (use with extreme caution)",
        ],
        "gotchas": [
            "Terraform state is critical -- losing the state file means Terraform no longer knows about your infrastructure. Use remote backends (S3, GCS) not local state",
            "terraform destroy destroys ALL resources in the state -- there is no undo. Always use -target for selective destruction",
            "State locking prevents concurrent modifications -- if a lock gets stuck, use terraform force-unlock (dangerous)",
            "Terraform plan can show no changes but apply can still fail due to API errors, permissions, or rate limits",
        ],
        "related": ["ansible", "kubectl", "docker"],
        "difficulty": "intermediate",
        "extra_flags": {
            "-compact-warnings": "Show warnings in a compact single-line format",
            "-refresh-only": "Update state to match real infrastructure without changing resources",
            "state": "Advanced state management subcommand (mv, rm, list, show)",
            "import": "Import existing infrastructure into Terraform management",
        },
    },
    "ansible": {
        "man_url": "https://docs.ansible.com/ansible/latest/cli/ansible.html",
        "use_cases": [
            "Run a quick ad-hoc command on all servers with ansible all -m ping -i inventory.yml",
            "Deploy an application with ansible-playbook -i hosts deploy.yml",
            "Test changes without applying with ansible-playbook site.yml --check --diff",
        ],
        "gotchas": [
            "Ansible requires SSH access and Python on managed hosts -- hosts without Python need the raw or script modules",
            "YAML indentation matters -- a misplaced space can cause silent misconfiguration rather than an error",
            "ansible-playbook and ansible are different commands -- use ansible for ad-hoc tasks and ansible-playbook for playbook execution",
            "--check mode does not guarantee idempotency detection -- some modules do not support check mode and will skip",
        ],
        "related": ["terraform", "puppet", "chef", "ssh"],
        "difficulty": "intermediate",
        "extra_flags": {
            "--diff": "Show file change diffs when modifying files on remote hosts",
            "--list-hosts": "List hosts that would be affected without executing",
            "--ask-become-pass": "Prompt for the privilege escalation (sudo) password",
        },
    },
    "puppet": {
        "man_url": "https://www.puppet.com/docs/puppet/latest/man/overview.html",
        "use_cases": [
            "Apply a manifest locally with puppet apply manifest.pp for testing",
            "Run the Puppet agent in test mode with puppet agent --test to see what changes would be made",
            "Dry-run a manifest without making changes with puppet apply --noop site.pp",
        ],
        "gotchas": [
            "Puppet uses a declarative language that is not Ruby despite looking similar -- it has its own syntax rules",
            "Puppet runs are not instant -- the agent checks in periodically (default 30 minutes) and convergence takes multiple runs for complex catalogs",
            "Resource ordering is not guaranteed unless you specify explicit dependencies with require, before, notify, or subscribe",
        ],
        "related": ["ansible", "chef", "terraform"],
        "difficulty": "advanced",
        "extra_flags": {},
    },
    "chef": {
        "man_url": "https://docs.chef.io/workstation/knife/",
        "use_cases": [
            "Apply a recipe locally for testing with chef-client --local-mode -r 'recipe[mycookbook]'",
            "Upload a cookbook to the Chef server with knife cookbook upload mycookbook",
            "List managed nodes with knife node list",
        ],
        "gotchas": [
            "Chef uses Ruby for cookbooks which has a steeper learning curve than Ansible's YAML -- Ruby syntax errors in recipes can be hard to debug",
            "chef-client runs require a Chef Server or chef-zero for local mode -- the architecture is more complex than agentless tools like Ansible",
            "The knife CLI is part of Chef Workstation, not Chef Client -- install Chef Workstation on your development machine",
        ],
        "related": ["ansible", "puppet", "terraform"],
        "difficulty": "advanced",
        "extra_flags": {},
    },

    # =========================================================================
    # DEVELOPMENT - EDITORS
    # =========================================================================
    "code": {
        "man_url": "https://code.visualstudio.com/docs/editor/command-line",
        "use_cases": [
            "Open the current directory in VS Code with code .",
            "Open a file at a specific line with code --goto main.py:42",
            "Compare two files side by side with code --diff old.js new.js",
            "Install an extension from the command line with code --install-extension ms-python.python",
        ],
        "gotchas": [
            "The code command must be installed into PATH on macOS -- open VS Code and run 'Shell Command: Install code command' from the command palette",
            "code --wait is needed for use as a git editor or merge tool -- without it git does not wait for you to close the file",
            "Running code . in WSL opens VS Code with the Remote-WSL extension -- this is by design but can confuse first-time WSL users",
        ],
        "related": ["vim", "nvim", "nano", "emacs"],
        "difficulty": "beginner",
        "extra_flags": {
            "--wait": "Wait for file to be closed before returning (for git editor use)",
            "-r": "Reuse the most recently used window",
            "--locale": "Set the display language (e.g., en, zh-cn)",
        },
    },
    "vim": {
        "man_url": "https://vimhelp.org/",
        "use_cases": [
            "Edit a file starting at a specific line with vim +42 file.txt",
            "Open multiple files in split view with vim -O file1.py file2.py",
            "Compare two files visually with vim -d file1.txt file2.txt (vimdiff)",
            "Search and replace across a file with vim -c '%s/old/new/gc' -c 'wq' file.txt for scripted editing",
        ],
        "gotchas": [
            "Vim starts in normal mode, not insert mode -- press i to start typing. This trips up every new user",
            "Exiting vim: press Escape, then type :wq to save and quit, or :q! to quit without saving -- this is the most searched programming question on the internet",
            "Vim swap files (.swp) are created automatically and can cause issues if vim crashes -- use vim -r file to recover, then delete the .swp file",
            "Avoid using arrow keys in normal mode -- learn hjkl and motions (w, b, e, f, /) for dramatically faster navigation",
        ],
        "related": ["nvim", "vi", "nano", "emacs"],
        "difficulty": "intermediate",
        "extra_flags": {
            "-o": "Open files in horizontal splits",
            "-c": "Execute a vim command after opening the file",
            "-u": "Use a specific vimrc configuration file (use NONE for vanilla vim)",
            "-x": "Open file with encryption (prompted for password)",
        },
    },
    "nvim": {
        "man_url": "https://neovim.io/doc/",
        "use_cases": [
            "Open a file with nvim file.txt and enjoy built-in LSP support for code completion",
            "Run headless for plugin installation with nvim --headless '+Lazy sync' +qa",
            "Start with no configuration to debug plugin issues with nvim --clean file.txt",
            "Use diff mode to compare files with nvim -d file1.txt file2.txt",
        ],
        "gotchas": [
            "Neovim uses ~/.config/nvim/init.lua (or init.vim) not ~/.vimrc -- migrating vim config requires renaming and possibly converting to Lua",
            "Neovim's built-in LSP and Treesitter provide IDE-like features but require plugin setup (mason.nvim, nvim-lspconfig) -- they are not configured out of the box",
            "nvim --headless is useful for CI/CD plugin management but requires proper exit commands (+qa) or it hangs",
        ],
        "related": ["vim", "vi", "code", "emacs"],
        "difficulty": "intermediate",
        "extra_flags": {
            "--startuptime": "Write startup timing to a file for performance profiling",
            "-l": "Execute a Lua script and exit",
        },
    },
    "nano": {
        "man_url": "https://www.nano-editor.org/dist/latest/nano.1.html",
        "use_cases": [
            "Quick-edit a config file on a server with sudo nano /etc/nginx/nginx.conf",
            "Edit with line numbers for reference with nano -l file.py",
            "Create a backup before editing with nano -B important.conf",
        ],
        "gotchas": [
            "Keyboard shortcuts shown at the bottom use ^ for Ctrl and M- for Alt -- ^X means Ctrl+X, M-U means Alt+U",
            "nano wraps long lines by default which can corrupt config files -- use nano -w to disable wrapping for config file editing",
            "nano does not have the modal editing or macro power of vim -- it is excellent for quick edits but limited for large-scale text manipulation",
        ],
        "related": ["vim", "vi", "emacs", "code"],
        "difficulty": "beginner",
        "extra_flags": {
            "-E": "Convert tabs to spaces when typing",
            "-S": "Enable smooth scrolling instead of half-screen jumps",
            "-Y": "Specify syntax highlighting definition to use",
        },
    },
    "emacs": {
        "man_url": "https://www.gnu.org/software/emacs/manual/html_node/emacs/",
        "use_cases": [
            "Edit a file in terminal mode with emacs -nw file.txt",
            "Run Emacs as a daemon for instant startup with emacs --daemon then emacsclient file.txt",
            "Evaluate a Lisp expression for batch processing with emacs --batch --eval '(message \"hello\")'",
        ],
        "gotchas": [
            "Emacs uses Ctrl and Meta (Alt) key combinations extensively -- Ctrl+C Ctrl+F opens a file, Ctrl+X Ctrl+S saves, Ctrl+X Ctrl+C quits",
            "Emacs init files (.emacs or ~/.emacs.d/init.el) can slow startup significantly -- use emacs --daemon + emacsclient for fast subsequent access",
            "The learning curve is steep but different from vim -- Emacs is always in 'insert mode' and uses modifier keys instead of modal switching",
        ],
        "related": ["vim", "nvim", "code", "nano"],
        "difficulty": "advanced",
        "extra_flags": {},
    },
    "ed": {
        "man_url": "https://man7.org/linux/man-pages/man1/ed.1.html",
        "use_cases": [
            "Perform scripted file editing without any terminal UI with echo '1,s/old/new/g\\nw\\nq' | ed -s file.txt",
            "Edit files in environments where no screen-oriented editor is available (recovery mode, minimal containers)",
        ],
        "gotchas": [
            "ed is a line editor with no visual display -- you must use commands like p (print) and n (number) to see file contents",
            "ed silently succeeds on most operations with no feedback -- use -p to set a prompt character so you know ed is waiting for input",
            "ed is the standard POSIX editor -- it works everywhere but is mainly used for scripted edits, not interactive editing",
        ],
        "related": ["ex", "sed", "vim", "vi"],
        "difficulty": "advanced",
        "extra_flags": {},
    },
    "ex": {
        "man_url": "https://man7.org/linux/man-pages/man1/ex.1p.html",
        "use_cases": [
            "Perform batch find-and-replace without opening a visual editor with ex -sc '%s/old/new/g|x' file.txt",
            "Delete all lines matching a pattern with ex -sc 'g/DEBUG/d|x' logfile.txt",
            "Script complex multi-step edits with ex commands piped from a file",
        ],
        "gotchas": [
            "ex is essentially vim's command mode run standalone -- the commands are identical to vim : commands",
            "Use -s for silent batch mode to suppress prompts and messages -- without it ex waits for interactive input",
            "The x command saves and exits (write-quit) -- use q! to discard changes if the script fails midway",
        ],
        "related": ["ed", "vim", "sed"],
        "difficulty": "advanced",
        "extra_flags": {},
    },
    "vi": {
        "man_url": "https://man7.org/linux/man-pages/man1/vi.1p.html",
        "use_cases": [
            "Edit a file on any Unix system where vim may not be installed with vi filename.txt",
            "Use as a fallback editor during system recovery when only base utilities are available",
        ],
        "gotchas": [
            "On most modern systems vi is a symlink to vim or vim in compatible mode -- behavior may differ slightly from POSIX vi",
            "vi has fewer features than vim -- no syntax highlighting, no multiple undo levels, and limited plugin support",
            "vi is always available because POSIX requires it -- it is the editor of last resort for emergency system repairs",
        ],
        "related": ["vim", "nvim", "nano", "ed"],
        "difficulty": "intermediate",
        "extra_flags": {},
    },

    # =========================================================================
    # DEVELOPMENT - DATA PROCESSING
    # =========================================================================
    "jq": {
        "man_url": "https://jqlang.github.io/jq/manual/",
        "use_cases": [
            "Pretty-print JSON from an API with curl -s api.example.com/data | jq '.' for readable output",
            "Extract a specific field with jq '.users[].name' data.json to pull names from an array",
            "Transform JSON structure with jq '{name: .full_name, id: .user_id}' to reshape data for another tool",
            "Filter array elements by condition with jq '[.items[] | select(.price > 100)]' products.json",
            "Merge two JSON files with jq -s '.[0] * .[1]' defaults.json overrides.json",
        ],
        "gotchas": [
            "jq is not installed by default on most systems -- install it with your package manager before relying on it in scripts",
            "String interpolation in jq uses \\() not ${} -- mixing up shell and jq variable syntax is a common source of errors",
            "Use --arg name value to safely pass shell variables into jq expressions -- embedding them with $() risks injection",
            "jq outputs JSON strings with quotes by default -- use -r for raw output when piping to other commands",
        ],
        "related": ["yq", "python", "xmllint", "curl"],
        "difficulty": "intermediate",
        "extra_flags": {
            "-e": "Set exit status based on output (false/null -> exit 1)",
            "--argjson": "Set variable to a JSON value (not string)",
            "--slurpfile": "Read entire file as JSON value into a variable",
            "--rawfile": "Read entire file as a raw string into a variable",
            "-n": "Do not read input, use null as input",
            "--indent": "Set indentation level (default 2)",
        },
    },
    "yq": {
        "man_url": "https://mikefarah.gitbook.io/yq/",
        "use_cases": [
            "Extract a value from a YAML file with yq '.metadata.name' deployment.yaml",
            "Update a value in-place with yq -i '.image.tag = \"v2.0\"' values.yaml",
            "Convert YAML to JSON with yq -o json config.yaml for tools that only accept JSON",
            "Merge multiple YAML files with yq eval-all '. as $item ireduce ({}; . * $item)' a.yaml b.yaml",
        ],
        "gotchas": [
            "There are two different tools called yq -- the Go version (mikefarah/yq) and the Python version (kislyuk/yq) with different syntax. Check which you have with yq --version",
            "yq -i modifies files in-place with no backup -- pipe to a new file or use version control before editing",
            "YAML anchors and aliases may not round-trip perfectly through yq -- test with complex YAML before automating",
            "yq uses jq-like syntax but is not fully jq-compatible -- some jq filters work differently or are unsupported",
        ],
        "related": ["jq", "xmllint", "sed"],
        "difficulty": "intermediate",
        "extra_flags": {
            "-e": "Set exit status based on whether results exist",
            "eval-all": "Evaluate across all YAML documents in the input",
            "--front-matter": "Process YAML front matter in markdown files",
        },
    },
    "xmllint": {
        "man_url": "http://xmlsoft.org/xmllint.html",
        "use_cases": [
            "Validate an XML file against its schema with xmllint --noout --schema schema.xsd file.xml",
            "Pretty-print an XML file with xmllint --format messy.xml > formatted.xml",
            "Extract data with XPath with xmllint --xpath '//item/@name' data.xml",
        ],
        "gotchas": [
            "xmllint requires libxml2 to be installed -- it is usually available as part of the libxml2-utils package",
            "--xpath with namespaces requires explicit namespace declarations which can be very verbose",
            "xmllint --format adds a newline at the end of the file -- this may matter for exact binary comparison of XML files",
        ],
        "related": ["xsltproc", "jq", "yq"],
        "difficulty": "intermediate",
        "extra_flags": {
            "--c14n": "Canonicalize XML output for consistent comparison",
            "--dtdvalid": "Validate against an external DTD file",
            "--recover": "Try to recover from malformed XML",
        },
    },
    "xsltproc": {
        "man_url": "http://xmlsoft.org/xsltproc.html",
        "use_cases": [
            "Transform XML to HTML with xsltproc style.xsl data.xml > output.html",
            "Generate documentation from XML sources with xsltproc -o doc.html docbook.xsl manual.xml",
            "Pass parameters to stylesheets with xsltproc --param version \"'2.0'\" transform.xsl input.xml",
        ],
        "gotchas": [
            "String parameters passed with --param must be wrapped in extra quotes: --param name \"'value'\" (outer quotes for shell, inner for XPath)",
            "xsltproc only supports XSLT 1.0 -- for XSLT 2.0 or 3.0 you need Saxon or another processor",
            "Network access for DTDs and external entities can be slow or fail -- use --nonet to disable",
        ],
        "related": ["xmllint", "jq", "sed"],
        "difficulty": "advanced",
        "extra_flags": {},
    },
    "jsonnet": {
        "man_url": "https://jsonnet.org/ref/language.html",
        "use_cases": [
            "Generate Kubernetes manifests from templates with jsonnet -J lib/ -m output/ k8s.jsonnet",
            "Evaluate a simple expression with jsonnet -e '{ result: 1 + 2 }'",
            "Pass external variables for environment-specific config with jsonnet --ext-str env=prod config.jsonnet",
        ],
        "gotchas": [
            "Jsonnet is purely functional with no side effects -- you cannot read files or make network calls from Jsonnet code",
            "Output is JSON by default -- use -S for string output or -y for YAML (if using the Go implementation)",
            "Jsonnet evaluation is lazy -- errors in unused branches are not reported until those branches are actually referenced",
        ],
        "related": ["jq", "yq", "kubectl", "terraform"],
        "difficulty": "advanced",
        "extra_flags": {},
    },

    # =========================================================================
    # DEVELOPMENT - RUNTIMES & LANGUAGES
    # =========================================================================
    "node": {
        "man_url": "https://nodejs.org/docs/latest/api/cli.html",
        "use_cases": [
            "Run a JavaScript file with node app.js",
            "Start a quick REPL for testing with node (interactive mode)",
            "Evaluate an expression inline with node -e 'console.log(process.version)'",
            "Debug a script with Chrome DevTools with node --inspect-brk app.js then open chrome://inspect",
        ],
        "gotchas": [
            "Node.js uses CommonJS (require) by default -- to use ES modules (import/export) either use .mjs extension or set \"type\": \"module\" in package.json",
            "The --inspect flag opens a debug port (9229) -- never expose this in production as it allows arbitrary code execution",
            "Node.js is single-threaded for JavaScript execution -- CPU-intensive work blocks the event loop and should use worker_threads",
            "Unhandled promise rejections will crash Node.js in newer versions -- always add .catch() or use try/catch with async/await",
        ],
        "related": ["npm", "npx", "deno", "bun"],
        "difficulty": "beginner",
        "extra_flags": {
            "--watch": "Watch for file changes and restart automatically (Node 18+)",
            "--experimental-modules": "Enable ES module support (legacy, now default)",
            "-p": "Evaluate and print an expression (shorthand for -e with console.log)",
            "--max-old-space-size": "Set the V8 heap memory limit in MB (default ~1.5GB)",
            "-r": "Preload a module before executing the script",
            "--env-file": "Load environment variables from a .env file (Node 20+)",
        },
    },
    "python": {
        "man_url": "https://docs.python.org/3/using/cmdline.html",
        "use_cases": [
            "Run a script with python script.py or start an interactive session with just python for quick testing",
            "Spin up a quick local web server with python -m http.server 8000 to serve files from the current directory",
            "Create a virtual environment with python -m venv .venv to isolate project dependencies",
            "Profile a script to find bottlenecks with python -m cProfile -s cumulative script.py",
            "Run a module as a script with python -m json.tool < data.json for pretty-printing JSON",
        ],
        "gotchas": [
            "On many systems, python points to Python 2 while python3 points to Python 3 -- always verify with python --version and use python3 explicitly if needed",
            "Running python without arguments starts the REPL which can be confusing in scripts -- always provide a script path or -c flag in automated contexts",
            "python -m pip install is safer than pip install because it ensures you use the correct Python version's pip",
            "The -u flag (unbuffered output) is important for Docker containers and CI pipelines where stdout buffering hides log output",
        ],
        "related": ["pip", "pip3", "conda", "uv", "ipython"],
        "difficulty": "beginner",
        "extra_flags": {
            "-W": "Warning control (error, ignore, default, all)",
            "-X": "Set implementation-specific options (e.g., -X dev for dev mode with extra checks)",
            "-q": "Quiet mode: suppress copyright and version messages on startup",
            "-O": "Optimize: remove assert statements and __debug__-guarded code",
            "-S": "Do not import the site module on startup (faster but no user site-packages)",
        },
    },
    "deno": {
        "man_url": "https://docs.deno.com/runtime/reference/cli/",
        "use_cases": [
            "Run a TypeScript file directly without compilation with deno run script.ts",
            "Run a web server with explicit permissions with deno run --allow-net --allow-read server.ts",
            "Format and lint code with built-in tools with deno fmt && deno lint",
            "Run tests with deno test for built-in test runner support",
        ],
        "gotchas": [
            "Deno uses explicit permissions by default -- scripts cannot access files, network, or environment without --allow-* flags, which breaks scripts silently if forgotten",
            "Deno uses URL imports not package.json by default -- npm compatibility exists via npm: specifiers but the ecosystem differs from Node.js",
            "Deno does not support __dirname or require() -- use import.meta.url and ES module imports instead",
        ],
        "related": ["node", "bun", "npm", "tsc"],
        "difficulty": "intermediate",
        "extra_flags": {
            "--allow-run": "Allow running subprocesses",
            "--allow-ffi": "Allow loading dynamic libraries",
            "--lock": "Check specified lockfile for integrity",
            "--no-check": "Skip TypeScript type checking for faster startup",
        },
    },
    "bun": {
        "man_url": "https://bun.sh/docs/cli",
        "use_cases": [
            "Install dependencies faster than npm with bun install",
            "Run a TypeScript file directly with bun run script.ts (no tsc needed)",
            "Run tests with the built-in test runner with bun test",
            "Bundle JavaScript for production with bun build ./src/index.ts --outdir ./dist",
        ],
        "gotchas": [
            "Bun aims for Node.js compatibility but not all Node APIs are implemented -- check the compatibility table for edge cases",
            "Bun uses its own lockfile (bun.lockb) which is binary -- it is not compatible with npm's package-lock.json or yarn.lock",
            "Some npm packages with native C++ addons may not work with Bun -- Bun uses JavaScriptCore (not V8) which requires different native bindings",
        ],
        "related": ["node", "deno", "npm", "tsc"],
        "difficulty": "intermediate",
        "extra_flags": {
            "build": "Bundle JavaScript/TypeScript for production",
            "--hot": "Enable hot module reloading during development",
        },
    },
    "ruby": {
        "man_url": "https://ruby-doc.org/3.3/",
        "use_cases": [
            "Run a Ruby script with ruby script.rb",
            "Execute a one-liner with ruby -e 'puts RUBY_VERSION'",
            "Process text line by line with ruby -ne 'puts $_ if /ERROR/' logfile.txt",
            "Check syntax without executing with ruby -c script.rb",
        ],
        "gotchas": [
            "Ruby version management requires rbenv or rvm -- system Ruby is often outdated",
            "Ruby's -i flag for in-place editing requires a backup extension on macOS (ruby -i.bak -pe ...) but not on Linux",
            "Ruby's standard library is being extracted into gems in Ruby 3.x -- some imports that worked before may now require gem install",
        ],
        "related": ["gem", "bundle", "irb", "perl"],
        "difficulty": "intermediate",
        "extra_flags": {},
    },
    "perl": {
        "man_url": "https://perldoc.perl.org/perl",
        "use_cases": [
            "Perform complex find-and-replace across files with perl -pi -e 's/old_api/new_api/g' *.py",
            "Process structured text with field splitting with perl -lane 'print $F[2]' data.tsv",
            "One-liner to sum a column of numbers with perl -lane '$s+=$F[0]; END{print $s}' data.txt",
        ],
        "gotchas": [
            "perl -i edits files in-place and DESTROYS the original -- use -i.bak to create backups",
            "Perl regex is the reference implementation for PCRE -- what works in Perl regex generally works in other PCRE-based tools",
            "The difference between -n (loop without print) and -p (loop with auto-print) is critical for one-liners",
        ],
        "related": ["sed", "awk", "ruby", "grep"],
        "difficulty": "intermediate",
        "extra_flags": {},
    },
    "php": {
        "man_url": "https://www.php.net/manual/en/features.commandline.php",
        "use_cases": [
            "Start a quick development server with php -S localhost:8000",
            "Check file syntax without executing with php -l script.php",
            "Run a quick expression with php -r 'echo phpversion() . \"\\n\";'",
        ],
        "gotchas": [
            "php -S is for development only -- it is single-threaded and not suitable for production traffic",
            "PHP's command-line SAPI uses different php.ini than the web server SAPI -- check with php --ini",
            "PHP's -r flag requires careful shell quoting because PHP uses $ for variables which conflicts with shell variable expansion",
        ],
        "related": ["composer", "node", "python"],
        "difficulty": "intermediate",
        "extra_flags": {},
    },
    "java": {
        "man_url": "https://docs.oracle.com/en/java/javase/21/docs/specs/man/java.html",
        "use_cases": [
            "Run a JAR application with java -jar app.jar",
            "Run a class with specific memory limits with java -Xmx4g -Xms1g -cp classes com.example.Main",
            "Run a single-file source program directly with java Main.java (Java 11+)",
        ],
        "gotchas": [
            "JAVA_HOME must be set correctly -- many tools rely on it and misconfiguration causes confusing errors",
            "-Xmx sets the maximum heap but the JVM uses additional memory for stack, metaspace, and native allocations -- total memory usage is always higher",
            "Classpath separator is : on Unix but ; on Windows -- cross-platform scripts need to handle this",
            "Java 9+ introduced the module system (JPMS) which can cause 'module not found' errors with older code -- use --add-modules or --add-opens for compatibility",
        ],
        "related": ["javac", "mvn", "gradle"],
        "difficulty": "intermediate",
        "extra_flags": {
            "--add-modules": "Add modules to the module graph for compatibility",
            "--add-opens": "Open a module's packages for deep reflection access",
            "-Xss": "Set thread stack size",
        },
    },
    "javac": {
        "man_url": "https://docs.oracle.com/en/java/javase/21/docs/specs/man/javac.html",
        "use_cases": [
            "Compile a Java file with javac Main.java",
            "Compile to a specific output directory with javac -d build/ src/*.java",
            "Compile for a specific Java release with javac --release 17 Main.java",
        ],
        "gotchas": [
            "javac requires all dependent classes on the classpath -- missing dependencies cause compilation errors even if the source is correct",
            "The --release flag is preferred over -source/-target combination because it also checks API availability",
            "javac only compiles .java files explicitly listed -- use build tools (Maven, Gradle) for multi-module projects",
        ],
        "related": ["java", "mvn", "gradle"],
        "difficulty": "intermediate",
        "extra_flags": {},
    },
    "kotlin": {
        "man_url": "https://kotlinlang.org/docs/command-line.html",
        "use_cases": [
            "Compile and bundle a self-contained JAR with kotlinc hello.kt -include-runtime -d hello.jar",
            "Run a Kotlin script with kotlinc -script script.kts",
            "Start the Kotlin REPL for quick prototyping with kotlinc",
        ],
        "gotchas": [
            "kotlinc without -include-runtime creates a JAR that requires the Kotlin runtime on the classpath -- use -include-runtime for standalone JARs",
            "The kotlin command runs JARs while kotlinc compiles -- they are separate tools",
            "Kotlin scripts (.kts) cannot import local .kt files without additional configuration -- use a build tool for multi-file projects",
        ],
        "related": ["java", "javac", "gradle", "scala"],
        "difficulty": "intermediate",
        "extra_flags": {},
    },
    "scala": {
        "man_url": "https://docs.scala-lang.org/scala3/book/tools-scala.html",
        "use_cases": [
            "Compile a Scala file with scalac Hello.scala then run with scala Hello",
            "Start the Scala REPL for interactive exploration with scala",
            "Run a Scala script directly with scala script.sc (Scala 3)",
        ],
        "gotchas": [
            "Scala 2 and Scala 3 have significant syntax differences -- check which version you are using with scala -version",
            "Scala compilation is notoriously slow -- incremental compilation with sbt or Bloop dramatically improves edit-compile-run cycles",
            "The scala command is both a REPL and a script runner -- behavior depends on whether you pass a file argument",
        ],
        "related": ["java", "javac", "kotlin", "sbt"],
        "difficulty": "advanced",
        "extra_flags": {},
    },
    "swift": {
        "man_url": "https://www.swift.org/documentation/",
        "use_cases": [
            "Run a Swift script directly with swift script.swift",
            "Create a new executable package with swift package init --type executable",
            "Build a package in release mode with swift build -c release",
        ],
        "gotchas": [
            "Swift on Linux requires the Swift toolchain to be installed separately -- it is not included in standard Linux distributions",
            "swift build uses Swift Package Manager (SPM) not Xcode build settings -- project structure must follow SPM conventions",
            "Swift REPL is started with just swift (no arguments) -- it can be slow to launch on first use due to compilation",
        ],
        "related": ["swiftc", "xcode", "lldb"],
        "difficulty": "intermediate",
        "extra_flags": {},
    },
    "swiftc": {
        "man_url": "https://www.swift.org/documentation/",
        "use_cases": [
            "Compile a Swift file to an executable with swiftc main.swift -o app",
            "Compile with optimizations for release with swiftc -O main.swift -o release_app",
            "Create a dynamic library with swiftc -emit-library -o libutils.dylib utils.swift",
        ],
        "gotchas": [
            "swiftc compiles individual files -- for multi-file projects with dependencies, use Swift Package Manager (swift build) instead",
            "Swift ABI stability (Swift 5.0+) means the runtime is part of the OS on macOS but must be bundled on Linux",
            "swiftc error messages can be long for generic type errors -- look for 'note:' lines that explain the root cause",
        ],
        "related": ["swift", "clang", "lldb"],
        "difficulty": "intermediate",
        "extra_flags": {},
    },
    "rust": {
        "man_url": "https://doc.rust-lang.org/cargo/",
        "use_cases": [
            "Create a new Rust project with cargo new myproject",
            "Build and run a project with cargo run",
            "Build an optimized release binary with cargo build --release",
            "Run tests with cargo test",
        ],
        "gotchas": [
            "The rust entry in most contexts refers to Cargo, the Rust build tool -- the actual compiler is rustc, but cargo is the standard interface",
            "cargo build --release applies optimizations that make binaries dramatically faster -- always benchmark with --release, not debug builds",
            "First compilation downloads and compiles all dependencies which can take several minutes -- subsequent builds use cached artifacts",
            "Rust's borrow checker produces unique errors that require understanding ownership semantics -- read the error messages carefully as they usually suggest fixes",
        ],
        "related": ["rustc", "rustup", "cargo"],
        "difficulty": "intermediate",
        "extra_flags": {
            "--edition": "Set the Rust edition (2015, 2018, 2021)",
            "clippy": "Run the Rust linter via cargo clippy",
            "fmt": "Format code via cargo fmt",
            "doc": "Generate documentation via cargo doc",
        },
    },
    "rustc": {
        "man_url": "https://doc.rust-lang.org/rustc/",
        "use_cases": [
            "Compile a single Rust file with rustc main.rs",
            "Compile with optimizations with rustc -O main.rs -o app",
            "Cross-compile for a different target with rustc --target aarch64-unknown-linux-gnu main.rs",
        ],
        "gotchas": [
            "rustc is rarely invoked directly -- use cargo which manages dependencies, build configuration, and invokes rustc internally",
            "rustc defaults to the 2015 edition unless --edition is specified -- use --edition 2021 for modern Rust features",
            "Cross-compilation with rustc requires the target to be installed via rustup target add -- the linker for the target must also be available",
        ],
        "related": ["rust", "cargo", "rustup"],
        "difficulty": "intermediate",
        "extra_flags": {},
    },
    "go": {
        "man_url": "https://pkg.go.dev/cmd/go",
        "use_cases": [
            "Build and run a Go program with go run main.go",
            "Build a static binary with go build -o myapp ./cmd/myapp",
            "Run all tests with go test ./...",
            "Clean up module dependencies with go mod tidy",
        ],
        "gotchas": [
            "Go compiles to a single static binary by default -- no runtime dependencies needed on the target system",
            "go get was changed in Go 1.17+ -- it no longer builds/installs, use go install for installing tools",
            "GOPATH is largely irrelevant with Go modules -- ensure go.mod exists in your project root",
            "Unused imports are a compilation error, not a warning -- use goimports or _ prefix for intentionally unused imports",
        ],
        "related": ["gofmt", "golint", "delve"],
        "difficulty": "intermediate",
        "extra_flags": {
            "-ldflags": "Pass flags to the linker (e.g., -s -w to strip debug info for smaller binaries)",
            "-gcflags": "Pass flags to the Go compiler",
            "-trimpath": "Remove file system paths from the compiled binary for reproducibility",
            "vet": "Report likely mistakes in packages (go vet ./...)",
        },
    },

    # =========================================================================
    # DEVELOPMENT - TESTING & LINTING
    # =========================================================================
    "eslint": {
        "man_url": "https://eslint.org/docs/latest/use/command-line-interface",
        "use_cases": [
            "Lint all JavaScript files in a project with eslint .",
            "Auto-fix linting issues with eslint --fix .",
            "Lint specific file types with eslint --ext .ts,.tsx src/",
            "Check specific rules with eslint --rule '{no-console: error}' file.js",
        ],
        "gotchas": [
            "ESLint 9+ uses flat config (eslint.config.js) by default -- the old .eslintrc format is deprecated",
            "--fix only fixes rules marked as fixable -- some issues must be resolved manually",
            "ESLint does not lint TypeScript by default -- you need @typescript-eslint/parser and plugin configured",
        ],
        "related": ["prettier", "tsc", "jest"],
        "difficulty": "beginner",
        "extra_flags": {
            "--cache": "Only check changed files for faster linting on large projects",
            "--max-warnings": "Set max warnings before exit with error (0 for strict)",
            "--no-eslintrc": "Disable use of configuration from .eslintrc files",
            "--format": "Set output format (stylish, json, compact, etc.)",
        },
    },
    "prettier": {
        "man_url": "https://prettier.io/docs/en/cli.html",
        "use_cases": [
            "Format all files in a project with prettier --write .",
            "Check formatting without changing files with prettier --check .",
            "Format a specific file with prettier --write src/index.ts",
        ],
        "gotchas": [
            "prettier --write modifies files in-place with no backup -- commit your changes before running",
            "Prettier is opinionated and has very few configuration options by design -- do not expect to customize every formatting decision",
            "Prettier and ESLint can conflict -- use eslint-config-prettier to disable ESLint rules that conflict with Prettier",
        ],
        "related": ["eslint", "tsc"],
        "difficulty": "beginner",
        "extra_flags": {
            "--single-quote": "Use single quotes instead of double quotes",
            "--trailing-comma": "Print trailing commas (all, es5, none)",
            "--tab-width": "Set the number of spaces per indentation level",
            "--ignore-path": "Specify a file to read ignore patterns from",
            "--cache": "Only format changed files for faster execution",
        },
    },
    "jest": {
        "man_url": "https://jestjs.io/docs/cli",
        "use_cases": [
            "Run all tests with jest",
            "Run tests in watch mode during development with jest --watch",
            "Run tests matching a pattern with jest --testPathPattern='auth'",
            "Generate a coverage report with jest --coverage",
        ],
        "gotchas": [
            "Jest runs tests in parallel by default -- tests that share state (databases, files) may fail intermittently. Use --runInBand for serial execution",
            "Jest uses its own module resolution that does not support ES modules natively -- configure transform with ts-jest or @swc/jest for TypeScript",
            "Jest's --coverage can significantly slow down test runs -- only use it in CI, not during development",
        ],
        "related": ["eslint", "prettier", "node", "tsc"],
        "difficulty": "beginner",
        "extra_flags": {
            "--runInBand": "Run tests serially in the current process instead of parallel workers",
            "--verbose": "Display individual test results in a hierarchy",
            "--bail": "Stop running tests after N failures (default 0 = run all)",
            "--passWithNoTests": "Exit with 0 even if no tests are found",
            "--forceExit": "Force Jest to exit after all tests complete (kills dangling handles)",
        },
    },
    "pytest": {
        "man_url": "https://docs.pytest.org/en/stable/reference/reference.html",
        "use_cases": [
            "Run all tests in a project with pytest",
            "Run a specific test file with pytest tests/test_auth.py",
            "Run tests matching a keyword with pytest -k 'test_login and not slow'",
            "Generate an HTML coverage report with pytest --cov=src --cov-report=html",
        ],
        "gotchas": [
            "pytest discovers tests automatically in files named test_*.py or *_test.py -- naming your test files differently will skip them silently",
            "Fixtures are powerful but can create implicit dependencies that are hard to trace -- use explicit fixture parameters",
            "pytest --cov requires the pytest-cov plugin to be installed -- it is not built into pytest",
            "Tests modify shared state (databases, files) at your peril -- pytest-xdist for parallel execution amplifies any shared-state bugs",
        ],
        "related": ["python", "tox", "coverage"],
        "difficulty": "beginner",
        "extra_flags": {
            "-s": "Do not capture stdout/stderr (show print output during tests)",
            "-m": "Only run tests with specific markers (e.g., -m 'not slow')",
            "--tb": "Traceback style: short, long, line, native, no",
            "--lf": "Re-run only tests that failed last time",
            "--pdb": "Drop into the Python debugger on test failure",
            "-n": "Run tests in parallel with N workers (requires pytest-xdist)",
        },
    },
    "tsc": {
        "man_url": "https://www.typescriptlang.org/docs/handbook/compiler-options.html",
        "use_cases": [
            "Type-check a project without emitting files with tsc --noEmit",
            "Initialize a new TypeScript project with tsc --init",
            "Watch for changes and recompile with tsc -w",
            "Compile a single file with tsc script.ts",
        ],
        "gotchas": [
            "tsc --noEmit is the standard way to use TypeScript for type checking only when a bundler (webpack, esbuild, vite) handles compilation",
            "tsc reads tsconfig.json by default -- command-line flags override tsconfig settings but file lists do not merge intuitively",
            "tsc does not bundle or minify -- it only transpiles TypeScript to JavaScript. Use a bundler for production builds",
            "strict: true in tsconfig.json enables all strict checks -- new projects should always start with this enabled",
        ],
        "related": ["node", "eslint", "prettier", "jest"],
        "difficulty": "intermediate",
        "extra_flags": {
            "--strict": "Enable all strict type-checking options",
            "--outDir": "Redirect output structure to the specified directory",
            "--target": "Set the JavaScript language version for output (es2015, es2020, esnext)",
            "--module": "Set the module system (commonjs, esnext, nodenext)",
            "--declaration": "Generate .d.ts declaration files",
            "--sourceMap": "Generate source map files for debugging",
            "-b": "Build mode for project references",
        },
    },
}
