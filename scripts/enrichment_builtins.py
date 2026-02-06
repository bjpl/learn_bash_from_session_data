"""
Enrichment data for Shell Builtins and File System commands.

This module provides additional educational metadata (use_cases, gotchas,
related commands, difficulty, and supplementary flags) for commands that
exist in COMMAND_DB but are missing these fields.

Sources:
  - GNU Bash Reference Manual (v5.3, 2025): https://www.gnu.org/software/bash/manual/bash.html
  - man7.org Linux man-pages: https://man7.org/linux/man-pages/dir_section_1.html
  - Greg's Wiki / BashPitfalls: https://mywiki.wooledge.org/BashPitfalls
  - Bash Hackers Wiki: https://bash-hackers.gabe565.com/
"""

ENRICHMENT_DATA = {
    # =========================================================================
    # SHELL BUILTINS
    # =========================================================================

    "echo": {
        "man_url": "https://man7.org/linux/man-pages/man1/echo.1.html",
        "use_cases": [
            "Print variable values for debugging: echo \"Value is: $MY_VAR\"",
            "Write content to files: echo 'config_line' >> config.txt",
            "Print colored output in terminals: echo -e '\\033[31mError\\033[0m'",
            "Generate simple text output in scripts for user feedback",
        ],
        "gotchas": [
            "echo -e interpretation varies between shells and systems -- use printf for portable escape handling",
            "echo without quotes on a variable with spaces causes word splitting: echo $var vs echo \"$var\"",
            "echo -n may print literal '-n' in some shells (dash, POSIX sh) instead of suppressing the newline",
            "If the string starts with a dash, echo may interpret it as an option -- use printf '%s\\n' instead",
        ],
        "related": ["printf", "cat", "tee"],
        "difficulty": "beginner",
        "extra_flags": {
            "-E": "Disable interpretation of backslash escapes (default in bash)",
        },
    },

    "printf": {
        "man_url": "https://man7.org/linux/man-pages/man1/printf.1.html",
        "use_cases": [
            "Portable formatted output in scripts: printf '%s\\n' \"$message\"",
            "Print padded or aligned columns: printf '%-20s %5d\\n' \"$name\" \"$count\"",
            "Generate NUL-delimited output for xargs -0: printf '%s\\0' \"${files[@]}\"",
            "Create formatted log entries with timestamps: printf '[%s] %s\\n' \"$(date)\" \"$msg\"",
            "Safely print strings that may start with dashes (unlike echo)",
        ],
        "gotchas": [
            "printf does NOT add a trailing newline by default -- you must include \\n explicitly",
            "The format string is reused if there are more arguments than format specifiers: printf '%s\\n' a b c prints three lines",
            "Octal escape \\0NNN in printf format differs from echo -e which uses \\NNN",
            "%q format is bash-specific and not POSIX portable",
        ],
        "related": ["echo", "cat", "tee", "seq"],
        "difficulty": "beginner",
        "extra_flags": {
            "-v": "Assign the output to a variable instead of printing to stdout (bash extension)",
        },
    },

    "read": {
        "man_url": "https://www.gnu.org/software/bash/manual/html_node/Bash-Builtins.html",
        "use_cases": [
            "Prompt for user input: read -p 'Enter your name: ' name",
            "Read a password without echoing: read -s -p 'Password: ' pass",
            "Parse delimited data: IFS=: read -r user _ uid gid _ home shell < /etc/passwd",
            "Read a file line by line: while IFS= read -r line; do echo \"$line\"; done < file.txt",
            "Read with a timeout for non-blocking input: read -t 5 -p 'Quick! ' answer",
        ],
        "gotchas": [
            "Without -r, backslashes are treated as escape characters and consumed -- always use read -r for raw input",
            "Without setting IFS='', leading and trailing whitespace is trimmed from the input",
            "Piping into read runs it in a subshell, so variables set inside are lost: echo x | read var (var is empty after)",
            "The correct pattern for file reading is: while IFS= read -r line; do ...; done < file (not cat file | while read)",
            "read returns non-zero at EOF even if it read partial data -- check the variable, not just the exit status",
        ],
        "related": ["echo", "printf", "cat", "select"],
        "difficulty": "beginner",
        "extra_flags": {
            "-a": "Read words into an indexed array variable",
            "-d": "Use specified delimiter instead of newline to terminate input",
            "-n": "Read exactly N characters (does not wait for newline)",
            "-N": "Read exactly N characters, ignoring delimiters",
            "-i": "Use specified text as initial input for readline editing (with -e)",
            "-e": "Use readline for input (allows arrow keys, history in interactive use)",
            "-u": "Read from file descriptor N instead of stdin",
        },
    },

    "source": {
        "man_url": "https://www.gnu.org/software/bash/manual/html_node/Bourne-Shell-Builtins.html",
        "use_cases": [
            "Reload shell configuration after editing: source ~/.bashrc",
            "Activate a Python virtual environment: source venv/bin/activate",
            "Load environment variables from a .env file: source .env",
            "Include shared function libraries in scripts: source lib/utils.sh",
        ],
        "gotchas": [
            "source executes in the current shell, so any exit call in the sourced file will terminate YOUR shell session",
            "Variables and functions from the sourced file persist in the current shell -- there is no isolation",
            "If the sourced file has a syntax error, it can leave your shell in a broken state",
            "source searches PATH if the filename has no slashes -- use ./file to be explicit about the current directory",
            "The . (dot) command is the POSIX equivalent; source is a bash extension not available in dash or strict POSIX sh",
        ],
        "related": [".", "exec", "eval", "bash"],
        "difficulty": "beginner",
    },

    ".": {
        "man_url": "https://www.gnu.org/software/bash/manual/html_node/Bourne-Shell-Builtins.html",
        "use_cases": [
            "Load environment variables: . /etc/profile",
            "Include function definitions: . ./lib/helpers.sh",
            "POSIX-compatible alternative to source: . ~/.bashrc",
        ],
        "gotchas": [
            "Identical to source in bash, but . is the POSIX-standard form and works in all POSIX shells",
            "If given a filename without a path component, searches PATH -- use ./ prefix for current directory files",
            "An exit in the sourced file terminates the calling shell",
        ],
        "related": ["source", "exec", "eval"],
        "difficulty": "beginner",
    },

    "exec": {
        "man_url": "https://www.gnu.org/software/bash/manual/html_node/Bourne-Shell-Builtins.html",
        "use_cases": [
            "Replace shell with another process in Docker entrypoints: exec python app.py",
            "Redirect all subsequent script output to a log file: exec > /var/log/script.log 2>&1",
            "Open a file descriptor for reading: exec 3< input.txt",
            "Replace the current shell with a login shell: exec -l bash",
            "Ensure a wrapper script does not remain as a parent process: exec \"$@\" in entrypoint.sh",
        ],
        "gotchas": [
            "exec replaces the current process -- any code after exec never runs (unless exec fails)",
            "When used for redirection (exec > file), it affects ALL subsequent commands in the shell, not just one",
            "exec without a command but with redirections only changes file descriptors for the current shell",
            "In Docker, failing to use exec means signals (SIGTERM) go to the shell, not your application",
        ],
        "related": ["source", "eval", "bash", "nohup"],
        "difficulty": "intermediate",
    },

    "eval": {
        "man_url": "https://www.gnu.org/software/bash/manual/html_node/Bourne-Shell-Builtins.html",
        "use_cases": [
            "Initialize ssh-agent in a shell session: eval \"$(ssh-agent -s)\"",
            "Execute dynamically constructed commands from trusted sources",
            "Perform indirect variable expansion in older bash: eval echo \\$$varname",
            "Process output of commands that print shell variable assignments",
        ],
        "gotchas": [
            "eval performs an EXTRA round of expansion before execution -- this is a major injection risk with untrusted input",
            "Never pass user-supplied or external data to eval without rigorous sanitization; attackers can inject arbitrary commands",
            "Prefer bash-native alternatives: ${!varname} for indirect expansion, arrays for dynamic arguments, declare -n for namerefs",
            "Debugging eval is difficult because errors refer to the evaluated string, not your source code line",
            "CVE-2019-9891 was issued for an insecure eval in a widely-used bash scripting guide -- the risk is real",
        ],
        "related": ["exec", "source", "bash"],
        "difficulty": "advanced",
    },

    "set": {
        "man_url": "https://www.gnu.org/software/bash/manual/html_node/The-Set-Builtin.html",
        "use_cases": [
            "Make scripts fail-safe: set -euo pipefail at the top of every script",
            "Enable debug tracing: set -x to see each command before it runs, set +x to stop",
            "Reset positional parameters: set -- \"$file1\" \"$file2\" to reassign $1, $2",
            "Disable globbing temporarily: set -f before processing patterns literally",
        ],
        "gotchas": [
            "set -e does NOT cause exit inside if conditions, while/until loops, or commands followed by && or ||",
            "set -e with arithmetic: ((count++)) returns 1 when count is 0, causing unexpected script exit",
            "set -o pipefail makes grep returning no matches (exit 1) fail the entire pipeline",
            "set -u treats ${array[@]} as an unbound variable error on empty arrays in bash < 4.4",
            "set with no arguments prints ALL shell variables and functions -- use set -o to see just options",
            "Use set +o to reset options: save state with oldopts=$(set +o), restore with eval \"$oldopts\"",
        ],
        "related": ["shopt", "trap", "bash"],
        "difficulty": "intermediate",
        "extra_flags": {
            "-a": "Automatically export all subsequently defined or modified variables",
            "-b": "Report terminated background jobs immediately",
            "-n": "Read commands but do not execute them (syntax checking mode)",
            "-v": "Print shell input lines as they are read",
            "-h": "Hash commands as they are looked up for execution",
            "-C": "Prevent output redirection from overwriting existing files (noclobber)",
            "-T": "Inherit DEBUG and RETURN traps in shell functions",
        },
    },

    "unset": {
        "man_url": "https://www.gnu.org/software/bash/manual/html_node/Bourne-Shell-Builtins.html",
        "use_cases": [
            "Remove a temporary variable after use: unset temp_file",
            "Clear an environment variable to prevent child processes from inheriting it: unset DATABASE_URL",
            "Remove a function definition: unset -f my_helper",
            "Clean up associative array entries: unset 'mymap[key]'",
        ],
        "gotchas": [
            "unset cannot remove readonly variables -- you get an error and the variable persists for the shell's lifetime",
            "unset on a nameref (-n) variable unsets the reference, not the target -- use unset -n to remove the nameref itself",
            "Without -v or -f, unset tries the name as a variable first, then as a function -- be explicit with the flag",
            "Unsetting positional parameters ($1, $2) is not possible with unset -- use shift instead",
        ],
        "related": ["set", "export", "declare", "readonly"],
        "difficulty": "beginner",
    },

    "export": {
        "man_url": "https://www.gnu.org/software/bash/manual/html_node/Bourne-Shell-Builtins.html",
        "use_cases": [
            "Set PATH for child processes: export PATH=\"$PATH:/usr/local/go/bin\"",
            "Configure application behavior: export NODE_ENV=production",
            "Pass credentials to subcommands: export AWS_PROFILE=staging",
            "List all exported variables: export -p",
        ],
        "gotchas": [
            "export only affects child processes -- it does NOT send variables back to the parent shell",
            "export -n removes the export attribute but keeps the variable defined locally",
            "Variables set without export are shell-local and invisible to commands you run",
            "Exporting in a subshell (pipe, $(...)) does not affect the parent -- the subshell's environment is discarded",
        ],
        "related": ["declare", "set", "unset", "env"],
        "difficulty": "beginner",
    },

    "declare": {
        "man_url": "https://www.gnu.org/software/bash/manual/html_node/Bash-Builtins.html",
        "use_cases": [
            "Create an associative array (dictionary): declare -A config; config[host]='localhost'",
            "Enforce integer-only variables: declare -i count=0; count+=5 gives 5, not '05'",
            "Make a variable readonly: declare -r VERSION='1.0.0'",
            "Force lowercase: declare -l name; name='ALICE' stores 'alice'",
            "List all functions and their definitions: declare -f",
            "Inspect a variable's type: declare -p myvar",
        ],
        "gotchas": [
            "Inside functions, declare creates LOCAL variables by default -- use declare -g to create globals",
            "declare -A requires bash 4.0+ -- not available on macOS default bash (3.2) without upgrading",
            "declare -i makes ALL assignments arithmetic: declare -i x; x=hello sets x to 0 (no error)",
            "declare -n (nameref) requires bash 4.3+ and can cause confusing circular reference errors",
        ],
        "related": ["local", "typeset", "readonly", "export"],
        "difficulty": "intermediate",
        "extra_flags": {
            "-l": "Convert value to lowercase on assignment",
            "-u": "Convert value to uppercase on assignment",
            "-n": "Make the variable a nameref (alias for another variable name)",
            "-g": "Create global variable even when used inside a function",
            "-f": "Restrict action to function names and definitions",
            "-F": "Display only function names (not definitions) when listing",
            "-t": "Give the variable the trace attribute (for debugging with DEBUG trap)",
        },
    },

    "local": {
        "man_url": "https://www.gnu.org/software/bash/manual/html_node/Bash-Builtins.html",
        "use_cases": [
            "Prevent variable leaking in functions: local temp_file=$(mktemp)",
            "Create a local copy of IFS: local IFS=,",
            "Local integer variable: local -i count=0",
            "Local array: local -a items=()",
        ],
        "gotchas": [
            "local can only be used inside a function -- calling it at the top level is an error",
            "local var=$(command) masks the exit status of command -- $? always reflects local's success",
            "In bash, local uses dynamic scoping, not lexical -- called functions can see the caller's locals",
            "local -r creates a readonly local that cannot be unset even within the function",
        ],
        "related": ["declare", "typeset", "readonly"],
        "difficulty": "intermediate",
    },

    "readonly": {
        "man_url": "https://www.gnu.org/software/bash/manual/html_node/Bourne-Shell-Builtins.html",
        "use_cases": [
            "Define constants: readonly DB_HOST='localhost'",
            "Protect critical variables from accidental modification: readonly PATH",
            "Make a function immutable: readonly -f critical_function",
            "List all readonly variables: readonly -p",
        ],
        "gotchas": [
            "Readonly variables CANNOT be unset -- they persist for the entire shell session",
            "A readonly variable in a parent shell is NOT inherited as readonly by child processes",
            "If you source a file that sets readonly variables, you cannot change them afterward in that session",
            "readonly -a applies to indexed arrays; readonly -A applies to associative arrays",
        ],
        "related": ["declare", "local", "export", "unset"],
        "difficulty": "intermediate",
    },

    "typeset": {
        "man_url": "https://www.gnu.org/software/bash/manual/html_node/Bash-Builtins.html",
        "use_cases": [
            "Ksh-compatible integer variable: typeset -i counter=0",
            "Cross-shell scripting where ksh compatibility is needed",
            "Uppercase variable: typeset -u STATUS; STATUS='ok' stores 'OK'",
        ],
        "gotchas": [
            "typeset is considered deprecated in bash since version 4.0 -- use declare instead",
            "typeset exists in bash primarily for ksh compatibility -- new scripts should avoid it",
            "Functionally identical to declare in bash, but declare is the documented and preferred form",
        ],
        "related": ["declare", "local", "readonly"],
        "difficulty": "intermediate",
    },

    "alias": {
        "man_url": "https://www.gnu.org/software/bash/manual/html_node/Bash-Builtins.html",
        "use_cases": [
            "Shorten frequent commands: alias gs='git status'",
            "Add safety nets: alias rm='rm -i'",
            "List all defined aliases: alias",
            "Create multi-command shortcuts: alias update='sudo apt update && sudo apt upgrade'",
        ],
        "gotchas": [
            "Aliases are NOT expanded in non-interactive shells (scripts) by default -- use shopt -s expand_aliases to enable",
            "Aliases do not accept arguments -- use a function if you need parameters",
            "Aliases are expanded at definition time, not execution time -- redefining a referenced command after the alias has no effect",
            "Alias expansion happens before other expansions, which can cause surprising interactions",
        ],
        "related": ["unalias", "function", "command", "builtin"],
        "difficulty": "beginner",
    },

    "unalias": {
        "man_url": "https://www.gnu.org/software/bash/manual/html_node/Bash-Builtins.html",
        "use_cases": [
            "Remove a specific alias: unalias ll",
            "Clear all aliases in the current session: unalias -a",
            "Undo a safety alias to run the real command: unalias rm",
        ],
        "gotchas": [
            "unalias only affects the current shell session -- aliases in .bashrc will return on next login",
            "unalias on a non-existent alias produces an error unless you redirect stderr",
            "To temporarily bypass an alias without removing it, prefix with backslash: \\rm file",
        ],
        "related": ["alias", "command", "builtin"],
        "difficulty": "beginner",
    },

    "builtin": {
        "man_url": "https://www.gnu.org/software/bash/manual/html_node/Bash-Builtins.html",
        "use_cases": [
            "Call the real cd from inside a cd wrapper function: builtin cd \"$dir\"",
            "Force use of bash's echo instead of /bin/echo: builtin echo 'text'",
            "Avoid infinite recursion when overriding a builtin with a function of the same name",
        ],
        "gotchas": [
            "If the specified name is not a shell builtin, builtin returns a non-zero exit status",
            "builtin bypasses functions and aliases but NOT shell keywords (like if, for, while)",
            "Only works for actual builtins -- for external commands, use command instead",
        ],
        "related": ["command", "enable", "type", "alias"],
        "difficulty": "intermediate",
    },

    "command": {
        "man_url": "https://www.gnu.org/software/bash/manual/html_node/Bash-Builtins.html",
        "use_cases": [
            "Check if a command exists: command -v git >/dev/null 2>&1 && echo 'git found'",
            "Bypass a function or alias: command ls (runs /bin/ls, not an alias)",
            "POSIX-portable alternative to which: command -v python3",
            "Inside a function overriding an external command, call the real one: command grep pattern file",
        ],
        "gotchas": [
            "command -v is preferred over which because which is not POSIX and behaves differently across systems",
            "command bypasses functions and aliases but still runs builtins -- use the external path directly to avoid builtins",
            "command -v returns the path for external commands, 'builtin' for builtins, and 'alias ...' for aliases",
            "command -p uses a default system PATH, which may differ from your custom PATH",
        ],
        "related": ["builtin", "type", "which", "enable"],
        "difficulty": "intermediate",
    },

    "enable": {
        "man_url": "https://www.gnu.org/software/bash/manual/html_node/Bash-Builtins.html",
        "use_cases": [
            "Disable a builtin to use an external version: enable -n echo (then /bin/echo is used)",
            "List all builtins with their enabled/disabled status: enable -a",
            "Load a dynamically loadable builtin: enable -f /path/to/lib builtin_name",
            "Re-enable a previously disabled builtin: enable echo",
        ],
        "gotchas": [
            "Disabling a builtin is per-shell-session only -- it resets on new shell launch",
            "enable -f for loadable builtins requires that bash was compiled with loadable builtin support",
            "Disabling critical builtins (cd, exit) can make the shell session hard to use",
        ],
        "related": ["builtin", "command", "type"],
        "difficulty": "advanced",
    },

    "hash": {
        "man_url": "https://www.gnu.org/software/bash/manual/html_node/Bourne-Shell-Builtins.html",
        "use_cases": [
            "Clear the command path cache after installing new software: hash -r",
            "See which commands have been cached and their hit counts: hash",
            "Force bash to use a specific path for a command: hash -p /usr/local/bin/python python",
            "Remove a single stale entry: hash -d old_command",
        ],
        "gotchas": [
            "If you install a new version of a command in a different PATH location, bash may still use the old cached path until you run hash -r",
            "hash -r clears the entire table -- there is no way to selectively refresh entries",
            "The hash table is per-shell-session and not shared between terminal windows",
            "In scripts with set -e, hash -d on a command not in the table causes the script to exit",
        ],
        "related": ["command", "type", "which", "enable"],
        "difficulty": "intermediate",
    },

    "pushd": {
        "man_url": "https://www.gnu.org/software/bash/manual/html_node/Directory-Stack-Builtins.html",
        "use_cases": [
            "Save current directory and jump to another: pushd /tmp",
            "Navigate between project directories: pushd ~/project-a, then pushd ~/project-b",
            "Rotate the directory stack: pushd +2 brings the third entry to the top",
            "Build scripts that work in multiple directories and return cleanly",
        ],
        "gotchas": [
            "pushd prints the entire directory stack after each call, which can be noisy -- redirect to /dev/null if unwanted",
            "pushd with no arguments swaps the top two directories on the stack (like cd -)",
            "The directory stack is per-shell and not shared across terminal sessions",
            "Numeric arguments (+N, -N) count from the top or bottom of the stack, not from 0",
        ],
        "related": ["popd", "dirs", "cd"],
        "difficulty": "intermediate",
    },

    "popd": {
        "man_url": "https://www.gnu.org/software/bash/manual/html_node/Directory-Stack-Builtins.html",
        "use_cases": [
            "Return to the previous directory after pushd: popd",
            "Remove a specific entry from the directory stack: popd +2",
            "Use in scripts paired with pushd for reliable directory restoration",
        ],
        "gotchas": [
            "popd on an empty stack (only the current directory) produces an error",
            "popd changes the working directory -- use popd -n to remove from the stack without changing dirs",
            "The stack index changes after each pop, so removing multiple entries requires care with indices",
        ],
        "related": ["pushd", "dirs", "cd"],
        "difficulty": "intermediate",
    },

    "dirs": {
        "man_url": "https://www.gnu.org/software/bash/manual/html_node/Directory-Stack-Builtins.html",
        "use_cases": [
            "View the current directory stack: dirs -v (shows numbered list)",
            "Clear the directory stack: dirs -c",
            "Show full paths instead of tilde abbreviation: dirs -l",
        ],
        "gotchas": [
            "dirs always includes the current working directory as the first entry, even if pushd was never used",
            "dirs -v numbers entries from 0, which matches the +N argument for pushd and popd",
            "The output of dirs without flags is space-separated on one line, which is hard to parse for paths with spaces",
        ],
        "related": ["pushd", "popd", "cd", "pwd"],
        "difficulty": "intermediate",
    },

    "shopt": {
        "man_url": "https://www.gnu.org/software/bash/manual/html_node/The-Shopt-Builtin.html",
        "use_cases": [
            "Enable recursive globbing: shopt -s globstar (then **/*.py matches all Python files)",
            "Case-insensitive globbing: shopt -s nocaseglob",
            "Append to history instead of overwriting: shopt -s histappend",
            "Allow cd to correct minor typos: shopt -s cdspell",
            "Include dotfiles in glob expansion: shopt -s dotglob",
            "Check option status quietly: shopt -q globstar && echo 'on'",
        ],
        "gotchas": [
            "shopt options are different from set options -- shopt -s vs set -o control different settings",
            "globstar (**) in bash < 4.0 is not available; bash on macOS defaults to 3.2",
            "shopt -s failglob causes an error when a glob matches nothing, instead of returning the pattern literally",
            "Some shopt settings affect interactive shells only (like cdspell) and are irrelevant in scripts",
        ],
        "related": ["set", "bash"],
        "difficulty": "intermediate",
    },

    "bind": {
        "man_url": "https://www.gnu.org/software/bash/manual/html_node/Bash-Builtins.html",
        "use_cases": [
            "Enable vi editing mode: bind -m vi",
            "Bind up-arrow to history search: bind '\"\\e[A\": history-search-backward'",
            "List all current key bindings: bind -p",
            "List all available readline functions: bind -l",
            "Load bindings from an inputrc file: bind -f ~/.inputrc",
        ],
        "gotchas": [
            "bind changes only affect the current shell session unless saved in ~/.inputrc",
            "Key binding syntax uses readline notation, which differs from terminal escape codes",
            "bind -x bindings run as shell commands, which can slow down interactive response if complex",
            "Binding conflicts with terminal emulator shortcuts may cause bindings to not work as expected",
        ],
        "related": ["set", "shopt", "history"],
        "difficulty": "advanced",
    },

    "history": {
        "man_url": "https://www.gnu.org/software/bash/manual/html_node/Bash-History-Builtins.html",
        "use_cases": [
            "Search previous commands: history | grep ssh",
            "Re-execute command number 42: !42",
            "Delete a sensitive entry: history -d 150",
            "Write current history to file immediately: history -w",
            "Read history from file (sync across terminals): history -r",
            "Clear all history for the session: history -c",
        ],
        "gotchas": [
            "history -c clears the in-memory history but not the file -- use history -c && history -w to clear both",
            "Passwords or secrets typed on the command line are saved in ~/.bash_history -- delete sensitive entries with history -d",
            "By default, history is written when the shell exits -- concurrent terminals can overwrite each other's history",
            "Use HISTCONTROL=ignorespace to prevent commands starting with a space from being saved",
            "HISTSIZE controls in-memory entries; HISTFILESIZE controls on-disk entries -- set both",
        ],
        "related": ["fc", "bind", "shopt"],
        "difficulty": "beginner",
        "extra_flags": {
            "-a": "Append the current session's new history lines to the history file",
            "-n": "Read history lines not already read from the history file into the current list",
            "-w": "Write current history list to the history file (overwrite)",
            "-r": "Read the history file and append its contents to the current history list",
            "-p": "Perform history expansion on the arguments and display the result without storing",
            "-s": "Append the arguments to the history list as a single entry (without executing)",
        },
    },

    "fc": {
        "man_url": "https://www.gnu.org/software/bash/manual/html_node/Bash-History-Builtins.html",
        "use_cases": [
            "Edit and re-run the last command in your editor: fc",
            "List the last 10 commands: fc -l -10",
            "Re-execute a command by number without editing: fc -s 42",
            "Quick substitution and re-run: fc -s old=new (replaces 'old' with 'new' in the last command)",
            "Use a specific editor: fc -e vim",
        ],
        "gotchas": [
            "fc with no arguments opens the LAST command in an editor -- saving and quitting immediately re-runs it",
            "The editor used depends on FCEDIT, then EDITOR, then defaults to vi -- make sure you know which one",
            "fc -s with no pattern re-runs the last command, which can be dangerous if the last command was destructive",
            "fc -l without -n includes line numbers, which may confuse copy-paste workflows",
        ],
        "related": ["history", "bind"],
        "difficulty": "intermediate",
    },

    "true": {
        "man_url": "https://man7.org/linux/man-pages/man1/true.1.html",
        "use_cases": [
            "Create an infinite loop: while true; do process_queue; sleep 1; done",
            "Provide a guaranteed-success command in a pipeline or conditional",
            "Default success action: command || true (suppress failure exit code)",
            "Placeholder for an unfinished function body",
        ],
        "gotchas": [
            "true is both a shell builtin and an external command (/bin/true) -- the builtin is faster",
            "In some contexts, : (colon) is preferred over true as the no-op command because it is always a builtin",
            "true ignores all arguments silently -- true --help still returns 0 (the builtin version)",
        ],
        "related": ["false", ":", "test"],
        "difficulty": "beginner",
    },

    "false": {
        "man_url": "https://man7.org/linux/man-pages/man1/false.1.html",
        "use_cases": [
            "Test error handling: false || echo 'caught failure'",
            "Force a script to exit under set -e: false",
            "Disable a feature flag: ENABLED=false; if $ENABLED; then ... (note: this runs the false command)",
        ],
        "gotchas": [
            "false always returns exit code 1, not an arbitrary non-zero value",
            "Using $ENABLED where ENABLED=false runs the false command -- this works but is unconventional; prefer [[ $ENABLED == true ]]",
            "false is both a builtin and an external binary; the builtin is used by default",
        ],
        "related": ["true", ":", "exit", "return"],
        "difficulty": "beginner",
    },

    "test": {
        "man_url": "https://man7.org/linux/man-pages/man1/test.1.html",
        "use_cases": [
            "Check if a file exists: test -f config.yaml && source config.yaml",
            "Compare integers: test $count -gt 0",
            "Check if a variable is set: test -n \"$VAR\"",
            "Check if a string is empty: test -z \"$input\"",
        ],
        "gotchas": [
            "Unquoted variables in test cause errors with spaces or empty values: test -f $file fails if file is empty or has spaces",
            "test uses single = for string comparison (not ==, though bash's test also accepts ==)",
            "Numeric comparisons use -eq, -lt, -gt -- not < or > (which are redirections inside [ ])",
            "test and [ are identical -- [ is not special syntax, it is a command that requires a closing ]",
        ],
        "related": ["[", "[[", "if"],
        "difficulty": "beginner",
        "extra_flags": {
            "-s": "True if file exists and has size greater than zero",
            "-L": "True if file is a symbolic link",
            "-p": "True if file is a named pipe (FIFO)",
            "-S": "True if file is a socket",
            "-O": "True if file is owned by the effective user ID",
            "-G": "True if file is owned by the effective group ID",
            "-nt": "True if file1 is newer than file2 (modification date)",
            "-ot": "True if file1 is older than file2",
            "-ef": "True if file1 and file2 refer to the same inode (hard links)",
        },
    },

    "[": {
        "man_url": "https://man7.org/linux/man-pages/man1/test.1.html",
        "use_cases": [
            "Conditional file check in if block: if [ -f /etc/hosts ]; then echo 'exists'; fi",
            "String comparison: [ \"$answer\" = 'yes' ]",
            "Numeric comparison: [ $x -le 100 ]",
            "Combine conditions: [ -d dir ] && [ -w dir ]",
        ],
        "gotchas": [
            "[ is a command, not syntax -- there MUST be spaces around [ and ] or you get parse errors",
            "Always quote variables inside [ ]: [ -f $file ] breaks if file is empty or has spaces",
            "Do not use && or || inside [ ] -- use -a and -o, or use separate [ ] tests joined by shell && / ||",
            "< and > inside [ ] are redirection operators, not comparison -- use -lt and -gt for numbers, or use [[ ]] for string comparison",
            "The closing ] is actually an argument to [ -- forgetting it gives 'missing ]' errors",
        ],
        "related": ["test", "[[", "if"],
        "difficulty": "beginner",
    },

    "[[": {
        "man_url": "https://www.gnu.org/software/bash/manual/html_node/Conditional-Constructs.html",
        "use_cases": [
            "Pattern matching: [[ $filename == *.tar.gz ]]",
            "Regex matching: [[ $email =~ ^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$ ]]",
            "Safe unquoted variable comparison: [[ -z $var ]] (no word splitting inside [[)",
            "Combine conditions naturally: [[ -f file && -r file ]]",
        ],
        "gotchas": [
            "[[ is bash-specific -- it will not work in POSIX sh, dash, or other minimal shells",
            "== inside [[ does PATTERN matching (glob), not exact string comparison -- quote the right side for literal match: [[ $x == \"$y\" ]]",
            "Regex with =~ does not quote the pattern: [[ $s =~ ^[0-9]+$ ]] works, but [[ $s =~ '^[0-9]+$' ]] matches literally",
            "The regex dialect for =~ is ERE (Extended Regular Expressions) from the system's C library, which varies by OS",
            "[[ does not support -a and -o -- use && and || between conditions instead",
        ],
        "related": ["[", "test", "if", "case"],
        "difficulty": "intermediate",
    },

    "exit": {
        "man_url": "https://www.gnu.org/software/bash/manual/html_node/Bourne-Shell-Builtins.html",
        "use_cases": [
            "End a script with success: exit 0",
            "Signal an error condition: exit 1",
            "Use in error handlers: || { echo 'Failed'; exit 1; }",
            "Exit with the status of the last command: exit $?",
        ],
        "gotchas": [
            "exit in a sourced script terminates the CALLING shell, not just the script -- use return instead in sourced files",
            "Exit codes above 125 have special meanings: 126 = command not executable, 127 = command not found, 128+N = killed by signal N",
            "exit triggers the EXIT trap -- do not call exit inside an EXIT trap handler or you risk infinite recursion",
            "In a subshell (parentheses or pipe), exit only exits the subshell, not the parent script",
        ],
        "related": ["return", "trap", "break"],
        "difficulty": "beginner",
    },

    "return": {
        "man_url": "https://www.gnu.org/software/bash/manual/html_node/Bourne-Shell-Builtins.html",
        "use_cases": [
            "Return success from a function: return 0",
            "Return error from a function: return 1",
            "Early exit from a sourced script without killing the caller: return",
            "Propagate a command's exit status: command; return $?",
        ],
        "gotchas": [
            "return can only be used inside a function or a sourced script -- anywhere else gives an error",
            "return with no argument returns the exit status of the last command executed",
            "return does NOT print output -- it only sets the exit code; use echo before return to pass data",
            "In a sourced file, return exits the sourcing back to the caller -- it does not exit the shell like exit would",
        ],
        "related": ["exit", "break", "continue"],
        "difficulty": "beginner",
    },

    "break": {
        "man_url": "https://www.gnu.org/software/bash/manual/html_node/Bourne-Shell-Builtins.html",
        "use_cases": [
            "Exit a loop when a condition is met: [[ $found == true ]] && break",
            "Break out of nested loops: break 2 exits both inner and outer loop",
            "Stop processing after finding a match in a for loop",
        ],
        "gotchas": [
            "break N exits N levels of nested loops -- break 2 exits two loops, not one",
            "break outside a loop causes an error in strict shells and a warning in bash",
            "break in a case statement inside a loop exits the loop, not the case (case uses ;; to end each pattern)",
        ],
        "related": ["continue", "return", "exit"],
        "difficulty": "beginner",
    },

    "continue": {
        "man_url": "https://www.gnu.org/software/bash/manual/html_node/Bourne-Shell-Builtins.html",
        "use_cases": [
            "Skip an iteration: [[ $file == *.tmp ]] && continue",
            "Skip to the next iteration of an outer loop: continue 2",
            "Filter out unwanted items in a processing loop",
        ],
        "gotchas": [
            "continue N resumes the Nth enclosing loop, not the current one -- continue 2 affects the outer loop",
            "continue outside a loop causes an error in strict shells and a warning in bash",
            "continue does not skip the rest of a pipeline stage -- it skips the rest of the loop body",
        ],
        "related": ["break", "return", "for", "while"],
        "difficulty": "beginner",
    },

    "shift": {
        "man_url": "https://www.gnu.org/software/bash/manual/html_node/Bourne-Shell-Builtins.html",
        "use_cases": [
            "Process command-line arguments one at a time: while [[ $# -gt 0 ]]; do arg=$1; shift; done",
            "Skip processed options: shift 2 to discard both the flag and its value",
            "Implement custom argument parsing in shell scripts",
        ],
        "gotchas": [
            "shift when there are no positional parameters ($# is 0) returns an error and does nothing",
            "shift N where N is greater than $# also returns an error in bash",
            "$0 (the script name) is never shifted -- shift only affects $1, $2, etc.",
            "Shifted parameters are gone permanently -- save them to variables first if you need them later",
        ],
        "related": ["getopts", "set"],
        "difficulty": "beginner",
    },

    "getopts": {
        "man_url": "https://www.gnu.org/software/bash/manual/html_node/Bourne-Shell-Builtins.html",
        "use_cases": [
            "Parse script options: while getopts 'vf:o:h' opt; do case $opt in v) verbose=1;; f) file=$OPTARG;; h) usage;; esac; done",
            "Handle options with required arguments: getopts 'f:' (colon means -f requires an argument)",
            "Skip processed options to access remaining arguments: shift $((OPTIND - 1))",
        ],
        "gotchas": [
            "getopts only supports single-character options -- it cannot parse --long-options (use getopt or manual parsing for those)",
            "A colon after a letter means it requires an argument: 'f:' means -f VALUE -- missing the colon makes it a flag",
            "OPTIND must be reset to 1 if you want to parse a different set of arguments or call getopts again",
            "A leading colon in the optstring (':vf:') enables silent error mode, putting the bad option in OPTARG instead of printing an error",
            "getopts stops at the first non-option argument -- options after positional args are not parsed",
        ],
        "related": ["shift", "case", "set"],
        "difficulty": "intermediate",
    },

    "trap": {
        "man_url": "https://www.gnu.org/software/bash/manual/html_node/Bourne-Shell-Builtins.html",
        "use_cases": [
            "Clean up temporary files on exit: trap 'rm -f $tmpfile' EXIT",
            "Handle Ctrl-C gracefully: trap 'echo Interrupted; cleanup; exit 130' INT",
            "Log script completion: trap 'echo \"Script finished at $(date)\"' EXIT",
            "Debug function entry/exit: trap 'echo \"Entering: $FUNCNAME\"' DEBUG",
            "Reset a trap: trap - INT (restores default signal handling for SIGINT)",
        ],
        "gotchas": [
            "trap on EXIT fires on ANY exit (success, failure, signals) -- but NOT on SIGKILL (kill -9), which cannot be caught",
            "Inside a trap handler, calling exit re-triggers the EXIT trap -- avoid recursive exit calls in EXIT handlers",
            "ERR traps are NOT inherited by functions by default -- use set -E (errtrace) to propagate them",
            "Trap handlers execute in the context of the current shell -- be careful with variable scope",
            "Setting a trap replaces any previous trap for that signal -- you cannot stack multiple handlers",
            "Use signal names (INT, TERM, EXIT) not numbers for portability -- signal numbers vary across operating systems",
        ],
        "related": ["kill", "exit", "set"],
        "difficulty": "intermediate",
    },

    "ulimit": {
        "man_url": "https://www.gnu.org/software/bash/manual/html_node/Bash-Builtins.html",
        "use_cases": [
            "Show all current resource limits: ulimit -a",
            "Increase open file limit for a database server: ulimit -n 65536",
            "Set maximum process stack size: ulimit -s unlimited",
            "Check the maximum number of user processes: ulimit -u",
            "Set core dump file size to unlimited for debugging: ulimit -c unlimited",
        ],
        "gotchas": [
            "A regular user can only LOWER hard limits -- once lowered, only root can raise them back",
            "Soft limits can be raised up to the hard limit value; hard limits can only be lowered (unless root)",
            "ulimit affects the current shell and its children -- it does not persist across sessions unless set in .bashrc or /etc/security/limits.conf",
            "ulimit -n changes are per-process -- each new shell gets its own copy of the limit",
            "The 'unlimited' keyword means no limit, but the kernel may still enforce system-wide maximums",
        ],
        "related": ["sysctl"],
        "difficulty": "intermediate",
        "extra_flags": {
            "-c": "Maximum size of core files created (blocks)",
            "-d": "Maximum size of a process's data segment (kbytes)",
            "-f": "Maximum size of files written by the shell and children (blocks)",
            "-l": "Maximum size that may be locked into memory (kbytes)",
            "-m": "Maximum resident set size (kbytes, not effective on many systems)",
            "-t": "Maximum amount of CPU time (seconds)",
            "-p": "Pipe buffer size (512-byte blocks)",
        },
    },

    "times": {
        "man_url": "https://www.gnu.org/software/bash/manual/html_node/Bourne-Shell-Builtins.html",
        "use_cases": [
            "Measure total CPU time used by a shell session: times",
            "Check how much user vs system time scripts consumed",
            "Quick profiling to see if your session is CPU-intensive",
        ],
        "gotchas": [
            "times shows cumulative time for the shell AND all child processes, not individual command times -- use time for that",
            "Output has two lines: first line is the shell itself, second line is all child processes",
            "times takes no arguments -- it always reports on the current shell",
            "The values are only meaningful for long-running sessions; short sessions show 0m0.000s",
        ],
        "related": ["time", "ps"],
        "difficulty": "intermediate",
    },

    "let": {
        "man_url": "https://www.gnu.org/software/bash/manual/html_node/Bash-Builtins.html",
        "use_cases": [
            "Increment a counter: let count++",
            "Perform arithmetic assignment: let 'result = a + b'",
            "Multiple operations: let 'x = 5' 'y = x * 2'",
            "Evaluate a condition arithmetically: let 'x > 0' (returns 0 if true)",
        ],
        "gotchas": [
            "let with an expression that evaluates to 0 returns exit code 1 (failure) -- let 'x = 0' returns 1, which triggers set -e",
            "let only handles integer arithmetic -- no floating point support",
            "Quoting is important: let x = 5 fails (spaces make them separate arguments); use let 'x = 5' or let x=5",
            "Prefer (( )) arithmetic syntax in modern bash: (( count++ )) is clearer than let 'count++'",
        ],
        "related": ["expr", "bc"],
        "difficulty": "intermediate",
    },

    ":": {
        "man_url": "https://www.gnu.org/software/bash/manual/html_node/Bourne-Shell-Builtins.html",
        "use_cases": [
            "Infinite loop: while :; do check_status; sleep 5; done",
            "Set default variable values: : ${TIMEOUT:=30} (sets TIMEOUT to 30 if unset)",
            "No-op placeholder in an if branch: if condition; then :; else handle_else; fi",
            "Comment-like usage in legacy scripts (though # is preferred for comments)",
        ],
        "gotchas": [
            ": is a POSIX special builtin -- errors from : can cause a non-interactive shell to exit in strict POSIX mode",
            "Arguments to : ARE expanded (variable expansion, globbing, etc.) even though the result is discarded",
            ": ${VAR:=default} is an idiom for defaults, but : ${VAR:=command $(that runs)} will execute the command substitution",
            "The colon command is faster than true because it is always a builtin with zero overhead",
        ],
        "related": ["true", "false", "test"],
        "difficulty": "intermediate",
    },

    "compgen": {
        "man_url": "https://www.gnu.org/software/bash/manual/html_node/Programmable-Completion-Builtins.html",
        "use_cases": [
            "List all available commands: compgen -c",
            "List all shell aliases: compgen -A alias",
            "List shell variables matching a prefix: compgen -v PATH",
            "Generate completions from a word list: compgen -W 'start stop restart status' -- 'st'",
            "List all builtin commands: compgen -b",
        ],
        "gotchas": [
            "compgen outputs one match per line -- pipe to sort or grep for filtering",
            "The -- before the prefix word is required to separate compgen options from the word being completed",
            "compgen -c lists ALL commands (builtins, aliases, functions, external) -- use -b, -A function, etc. for specific types",
            "compgen is primarily designed for use inside completion functions, but is useful interactively for discovery",
        ],
        "related": ["complete", "compopt", "type"],
        "difficulty": "advanced",
    },

    "complete": {
        "man_url": "https://www.gnu.org/software/bash/manual/html_node/Programmable-Completion-Builtins.html",
        "use_cases": [
            "Register a completion function: complete -F _my_git_complete git",
            "Simple word-list completion: complete -W 'start stop restart' myservice",
            "File completion for a command: complete -f myeditor",
            "Directory-only completion: complete -d mycd",
            "View existing completions: complete -p",
            "Remove a completion: complete -r mycommand",
        ],
        "gotchas": [
            "complete definitions are session-only -- persist them in ~/.bash_completion or /etc/bash_completion.d/",
            "The completion function receives COMP_WORDS, COMP_CWORD, and must populate COMPREPLY array",
            "complete -o filenames tells bash to treat results as filenames (adds trailing slashes to directories)",
            "Overwriting an existing completion replaces it entirely -- there is no way to extend one",
        ],
        "related": ["compgen", "compopt", "bind"],
        "difficulty": "advanced",
    },

    "compopt": {
        "man_url": "https://www.gnu.org/software/bash/manual/html_node/Programmable-Completion-Builtins.html",
        "use_cases": [
            "Enable filename handling mid-completion: compopt -o filenames",
            "Disable space after completion: compopt -o nospace",
            "Switch completion behavior based on context inside a completion function",
        ],
        "gotchas": [
            "compopt can only be called from within a completion function -- it has no effect elsewhere",
            "compopt modifies options for the current completion attempt, not the complete specification permanently",
            "Available options: filenames, nospace, default, dirnames, plusdirs -- not all combinations are useful",
        ],
        "related": ["complete", "compgen"],
        "difficulty": "advanced",
    },

    # =========================================================================
    # FILE SYSTEM COMMANDS
    # =========================================================================

    "ln": {
        "man_url": "https://man7.org/linux/man-pages/man1/ln.1.html",
        "use_cases": [
            "Create a symlink to a config file: ln -s /etc/nginx/sites-available/mysite /etc/nginx/sites-enabled/",
            "Create a version-independent symlink: ln -s python3.11 /usr/local/bin/python3",
            "Replace an existing symlink atomically: ln -sf /new/target linkname",
            "Create a relative symlink: ln -sr ../shared/lib.sh lib.sh",
        ],
        "gotchas": [
            "Hard links cannot cross filesystem boundaries -- use symbolic links (-s) for cross-device linking",
            "Hard links cannot point to directories (to prevent filesystem loops) -- only symlinks can",
            "Symlinks can become dangling (broken) if the target is moved or deleted -- the link still exists but points nowhere",
            "Without -s, ln creates hard links, which share the same inode -- deleting the original does not break the link",
            "ln TARGET LINK_NAME order is the opposite of cp -- the target comes FIRST, the link name comes SECOND",
        ],
        "related": ["readlink", "realpath", "cp", "stat"],
        "difficulty": "intermediate",
        "extra_flags": {
            "-n": "Treat LINK_NAME as a normal file if it is a symlink to a directory (important for overwriting symlinks to dirs)",
            "-t": "Specify the target directory (useful with xargs)",
            "-b": "Make a backup of each existing destination file",
        },
    },

    "touch": {
        # touch already has use_cases, gotchas, related, difficulty -- only add extra_flags if missing
        "extra_flags": {
            "-t": "Use specified timestamp [[CC]YY]MMDDhhmm[.ss] instead of current time",
            "-r": "Use the timestamps of a reference file instead of current time",
        },
    },

    "file": {
        "man_url": "https://man7.org/linux/man-pages/man1/file.1.html",
        "use_cases": [
            "Identify file type before processing: file downloaded_file",
            "Check MIME type for HTTP Content-Type: file -i document.pdf",
            "Verify a binary's architecture: file /usr/bin/ls",
            "Batch-check all files in a directory: file *",
            "Determine encoding of a text file: file -i textfile.txt",
        ],
        "gotchas": [
            "file examines content, not the extension -- renaming a PNG to .txt does not fool it",
            "file may not correctly identify files with unusual or corrupted headers",
            "-i on macOS gives different output format than on Linux (macOS uses --mime instead)",
            "The magic database (/usr/share/misc/magic) can be customized but rarely needs to be",
        ],
        "related": ["stat", "ls", "hexdump"],
        "difficulty": "beginner",
        "extra_flags": {
            "-L": "Follow symbolic links",
            "-z": "Try to look inside compressed files",
            "-k": "Keep going after the first match (show all matching types)",
            "--mime-type": "Print only the MIME type without encoding",
            "--mime-encoding": "Print only the MIME encoding",
        },
    },

    "stat": {
        "man_url": "https://man7.org/linux/man-pages/man1/stat.1.html",
        "use_cases": [
            "View complete file metadata: stat file.txt",
            "Get numeric permissions: stat -c '%a' file.txt",
            "Get file size in bytes: stat -c '%s' file.txt",
            "Check inode number: stat -c '%i' file.txt",
            "Get human-readable modification time: stat -c '%y' file.txt",
        ],
        "gotchas": [
            "stat -c (format) is GNU/Linux syntax; macOS uses stat -f with different format specifiers",
            "stat follows symlinks by default -- use -L to see the link itself (inverted logic from ls)",
            "The output format tokens (like %a, %s, %y) are completely different between Linux and macOS",
            "stat may show different block sizes depending on the filesystem (512-byte vs 4096-byte blocks)",
        ],
        "related": ["ls", "file", "touch", "chmod"],
        "difficulty": "intermediate",
        "extra_flags": {
            "-L": "Follow symlinks (show target file info)",
            "-f": "Display filesystem status instead of file status",
            "-t": "Print information in terse (machine-parseable) form",
        },
    },

    "basename": {
        "man_url": "https://man7.org/linux/man-pages/man1/basename.1.html",
        "use_cases": [
            "Extract filename from a full path: basename /home/user/documents/report.pdf",
            "Strip a known extension: basename report.pdf .pdf gives 'report'",
            "Get script name inside a script: script_name=$(basename \"$0\")",
            "Process multiple files with -a: basename -a /path/to/file1 /path/to/file2",
        ],
        "gotchas": [
            "basename is purely string manipulation -- it does not check if the file exists",
            "For extension stripping, the suffix must match exactly: basename file.tar.gz .gz gives 'file.tar', not 'file'",
            "In bash, parameter expansion can replace basename: ${path##*/} is faster than $(basename \"$path\")",
            "basename with a trailing slash on a directory path still returns the directory name",
        ],
        "related": ["dirname", "realpath", "readlink"],
        "difficulty": "beginner",
        "extra_flags": {
            "-a": "Support multiple arguments (print basename of each)",
            "-z": "End each output line with NUL instead of newline (for use with xargs -0)",
        },
    },

    "dirname": {
        "man_url": "https://man7.org/linux/man-pages/man1/dirname.1.html",
        "use_cases": [
            "Get the parent directory of a file: dirname /home/user/file.txt gives /home/user",
            "Navigate relative to the script's location: cd \"$(dirname \"$0\")\"",
            "Construct sibling paths: config=$(dirname \"$0\")/config.ini",
        ],
        "gotchas": [
            "dirname is purely string manipulation -- it does not check if the directory exists or resolve symlinks",
            "dirname of a bare filename (no slashes) returns '.' (the current directory)",
            "In bash, parameter expansion can replace dirname: ${path%/*} is faster than $(dirname \"$path\")",
            "dirname on a path ending with / may return the same path or the parent depending on trailing slash handling",
        ],
        "related": ["basename", "realpath", "readlink", "pwd"],
        "difficulty": "beginner",
        "extra_flags": {
            "-z": "End each output line with NUL instead of newline",
        },
    },

    "realpath": {
        "man_url": "https://man7.org/linux/man-pages/man1/realpath.1.html",
        "use_cases": [
            "Get the absolute path of a file: realpath ../relative/file.txt",
            "Resolve all symlinks: realpath /usr/bin/python",
            "Normalize a messy path: realpath /home/user/../user/./docs",
            "Check if symlinks resolve without existing: realpath -m /potentially/missing/path",
        ],
        "gotchas": [
            "realpath may not be available on older systems or macOS without coreutils -- use readlink -f as an alternative",
            "realpath -e fails if any path component does not exist; realpath without -e resolves what it can",
            "realpath is not a POSIX standard utility, so it may be missing on minimal systems",
            "On macOS, install coreutils via Homebrew to get GNU realpath (grealpath)",
        ],
        "related": ["readlink", "dirname", "basename", "pwd"],
        "difficulty": "beginner",
        "extra_flags": {
            "--relative-to": "Print the path relative to a specified directory",
            "--relative-base": "Print relative paths if both are descendants of the given base, otherwise absolute",
            "-q": "Quiet mode -- suppress most error messages",
        },
    },

    "readlink": {
        "man_url": "https://man7.org/linux/man-pages/man1/readlink.1.html",
        "use_cases": [
            "Find what a symlink points to: readlink /usr/bin/python3",
            "Resolve the full canonical path: readlink -f /usr/local/bin/node",
            "Get the real path of the current script: readlink -f \"$0\"",
            "Debug broken symlinks by seeing the stored target",
        ],
        "gotchas": [
            "readlink without -f only shows the direct target of a symlink -- it does not resolve chains of symlinks",
            "readlink -f is equivalent to realpath on most systems, but realpath is more portable in GNU/Linux",
            "readlink on a non-symlink file prints nothing and returns 1 (without -f, -e, or -m flags)",
            "readlink -f on macOS requires GNU coreutils (greadlink) -- the BSD readlink does not support -f",
        ],
        "related": ["realpath", "ln", "stat", "file"],
        "difficulty": "intermediate",
    },

    "rmdir": {
        "man_url": "https://man7.org/linux/man-pages/man1/rmdir.1.html",
        "use_cases": [
            "Safely remove an empty directory: rmdir temp/",
            "Remove a chain of empty parent directories: rmdir -p a/b/c removes c, then b, then a (if all empty)",
            "Clean up after a build: rmdir -v build/ obj/ (verbose output shows what was removed)",
            "Use in scripts as a safe alternative to rm -r when you only want to remove empty dirs",
        ],
        "gotchas": [
            "rmdir REFUSES to delete a directory that contains any files (including hidden files) -- this is a safety feature",
            "rmdir -p stops at the first non-empty parent; it does not error unless all directories fail",
            "rmdir does not have a -f (force) option -- if it cannot remove the dir, it always reports an error",
            "Hidden files (dotfiles) count as contents -- rmdir fails even if the directory appears empty in ls (without -a)",
        ],
        "related": ["rm", "mkdir", "find"],
        "difficulty": "beginner",
    },

    "locate": {
        "man_url": "https://man7.org/linux/man-pages/man1/locate.1.html",
        "use_cases": [
            "Find files instantly by name: locate nginx.conf",
            "Case-insensitive search: locate -i readme",
            "Count matching files: locate -c '*.log'",
            "Limit output: locate -n 5 pattern",
        ],
        "gotchas": [
            "locate uses a database (updated by updatedb) that may be hours or days old -- recently created files may not appear",
            "Run sudo updatedb to refresh the database before searching if you need current results",
            "locate returns files that have been DELETED since the last updatedb run -- they no longer exist on disk",
            "The database typically excludes certain directories (like /tmp, /proc) and network mounts",
            "On many modern systems, mlocate or plocate has replaced locate with incremental updates",
        ],
        "related": ["find", "updatedb", "which", "whereis"],
        "difficulty": "beginner",
    },

    "which": {
        "man_url": "https://linux.die.net/man/1/which",
        "use_cases": [
            "Find where a command lives: which python3",
            "Check if a command is installed: which docker || echo 'docker not found'",
            "Find all versions in PATH: which -a python",
            "Verify which version runs by default: which node",
        ],
        "gotchas": [
            "which only searches PATH for external executables -- it does not find shell builtins, functions, or aliases",
            "Prefer 'command -v' or 'type' in scripts -- which is not POSIX standard and behavior varies across systems",
            "On some systems, which is a shell script that parses alias output, which can give unexpected results",
            "which may show different results than what actually runs if there are aliases or functions shadowing the command",
        ],
        "related": ["whereis", "type", "command", "hash"],
        "difficulty": "beginner",
    },

    "whereis": {
        "man_url": "https://man7.org/linux/man-pages/man1/whereis.1.html",
        "use_cases": [
            "Find binary, source, and man page locations: whereis gcc",
            "Find only the binary: whereis -b python",
            "Find only man pages: whereis -m bash",
            "Discover installed documentation: whereis -m ls",
        ],
        "gotchas": [
            "whereis searches hardcoded system directories, not your PATH -- it may miss binaries in non-standard locations",
            "whereis may return multiple results if the same name exists in different standard locations",
            "Unlike which, whereis does not tell you which binary would actually run -- it just lists known locations",
            "whereis is not available on all systems (it comes from util-linux on Linux)",
        ],
        "related": ["which", "type", "command", "locate", "man"],
        "difficulty": "beginner",
    },

    "type": {
        "man_url": "https://www.gnu.org/software/bash/manual/html_node/Bash-Builtins.html",
        "use_cases": [
            "Determine how a command name is resolved: type ls (shows alias, builtin, or path)",
            "Get just the type classification: type -t cd gives 'builtin'",
            "Show all interpretations: type -a echo shows both the builtin and /usr/bin/echo",
            "Check if something is a function: type -t my_func gives 'function'",
        ],
        "gotchas": [
            "type is a bash builtin that shows how BASH would resolve a name -- including aliases, functions, builtins, and PATH lookup",
            "type -t returns one of: alias, keyword, function, builtin, file -- useful for conditional logic in scripts",
            "Unlike which, type knows about shell internals (builtins, aliases, functions) and is always correct for the current shell",
            "type -a can show that a name resolves multiple ways -- e.g., echo is both a builtin and an external binary",
        ],
        "related": ["which", "command", "whereis", "hash"],
        "difficulty": "beginner",
    },

    "less": {
        "man_url": "https://man7.org/linux/man-pages/man1/less.1.html",
        "use_cases": [
            "View a large file with scrolling: less /var/log/syslog",
            "Search within a file: press / then type a pattern",
            "View command output: ps aux | less",
            "Follow a growing file (like tail -f): less +F logfile.log",
            "View multiple files: less file1.txt file2.txt (use :n and :p to navigate)",
        ],
        "gotchas": [
            "less loads files lazily and does not read the entire file into memory -- ideal for huge files",
            "Press q to quit, not Ctrl-C (Ctrl-C interrupts a search or input, it does not exit)",
            "Use -R to properly display colored output from commands like git diff or grep --color",
            "less interprets some escape codes by default; use -r (raw) for full binary passthrough, or -R for ANSI only",
            "Setting LESSOPEN/LESSCLOSE can make less interpret compressed files, PDFs, etc.",
        ],
        "related": ["more", "cat", "head", "tail"],
        "difficulty": "beginner",
        "extra_flags": {
            "-F": "Quit immediately if the entire file fits on one screen",
            "-X": "Don't clear the screen on exit (leave content visible)",
            "-i": "Case-insensitive search (unless pattern has uppercase)",
            "-g": "Highlight only the current search match (not all matches)",
            "+G": "Start at the end of the file",
        },
    },

    "more": {
        "man_url": "https://man7.org/linux/man-pages/man1/more.1.html",
        "use_cases": [
            "View a file one screen at a time: more file.txt",
            "Pipe long output for pagination: dmesg | more",
            "Start at a specific line: more +100 file.txt",
        ],
        "gotchas": [
            "more only scrolls forward, not backward -- use less if you need to scroll up",
            "more exits automatically when you reach the end of the file",
            "On most modern Linux systems, more is actually a simplified version of less",
            "more does not support searching as well as less does",
        ],
        "related": ["less", "cat", "head", "tail"],
        "difficulty": "beginner",
        "extra_flags": {
            "-d": "Display help message at the bottom instead of ringing bell on illegal key",
            "-s": "Squeeze multiple blank lines into one",
            "+/pattern": "Start displaying at the first line matching the pattern",
        },
    },

    "clear": {
        "man_url": "https://man7.org/linux/man-pages/man1/clear.1.html",
        "use_cases": [
            "Clear the terminal screen: clear",
            "Clear screen in a script for clean output presentation",
            "Clear screen and scrollback buffer: clear -x (if supported)",
        ],
        "gotchas": [
            "clear sends terminal escape codes -- it does not actually delete anything from the scrollback on all terminals",
            "Ctrl-L in bash also clears the screen but preserves the current command line (different from running clear)",
            "In scripts, printf '\\033[2J\\033[H' is a more portable way to clear the screen",
            "Some terminal emulators support clear -x to also clear the scrollback buffer",
        ],
        "related": ["reset", "tput"],
        "difficulty": "beginner",
        "extra_flags": {
            "-T": "Specify the terminal type to use instead of the TERM environment variable",
            "-V": "Print version information",
        },
    },

    "man": {
        "man_url": "https://man7.org/linux/man-pages/man1/man.1.html",
        "use_cases": [
            "Read the manual for a command: man ls",
            "Search for a keyword across all man pages: man -k compression",
            "View a specific section: man 3 printf (C library function, not shell command)",
            "View the man page for man itself: man man",
            "Display a one-line description: man -f ls (equivalent to whatis)",
        ],
        "gotchas": [
            "Man page sections matter: man printf shows the shell command; man 3 printf shows the C function",
            "man -k requires the mandb database to be built -- run sudo mandb if -k returns nothing",
            "Man pages are displayed using a pager (usually less) -- all less keybindings work inside man",
            "Some builtins (like cd, source) do not have their own man page -- use man bash and search within it",
            "MANPATH controls where man looks; if it is incorrectly set, man may not find pages",
        ],
        "related": ["info", "help", "apropos", "whatis"],
        "difficulty": "beginner",
        "extra_flags": {
            "-a": "Display all matching man pages in sequence, not just the first",
            "-w": "Print the location of the man page file instead of displaying it",
            "-K": "Search for a string in all man pages (slow full-text search)",
        },
    },
}
