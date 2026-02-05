#!/usr/bin/env node

/**
 * learn-bash CLI
 * Learn bash from your Claude Code sessions - extracts commands and generates interactive HTML lessons
 *
 * Usage:
 *   learn-bash [options]
 *   learn-bash --list                    List available Claude Code projects
 *   learn-bash --sessions 5              Process last 5 sessions from current project
 *   learn-bash --file path/to/session    Process a specific session file
 *   learn-bash --project "project-name"  Process sessions from a specific project
 *   learn-bash --output ./my-lesson.html Specify output file location
 *   learn-bash --no-open                 Don't auto-open the generated HTML
 */

const fs = require('fs');
const path = require('path');
const { spawn, execSync } = require('child_process');
const os = require('os');

// ANSI color codes for terminal output
const colors = {
  reset: '\x1b[0m',
  bright: '\x1b[1m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  cyan: '\x1b[36m'
};

/**
 * Parse command line arguments (minimist-style, no dependencies)
 */
function parseArgs(args) {
  const result = {
    _: [],
    sessions: null,
    file: null,
    output: null,
    list: false,
    'no-open': false,
    project: null,
    help: false
  };

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    const nextArg = args[i + 1];

    if (arg === '--help' || arg === '-h') {
      result.help = true;
    } else if (arg === '--list' || arg === '-l') {
      result.list = true;
    } else if (arg === '--no-open') {
      result['no-open'] = true;
    } else if (arg === '--sessions' || arg === '-n') {
      result.sessions = parseInt(nextArg, 10);
      i++;
    } else if (arg === '--file' || arg === '-f') {
      result.file = nextArg;
      i++;
    } else if (arg === '--output' || arg === '-o') {
      result.output = nextArg;
      i++;
    } else if (arg === '--project' || arg === '-p') {
      result.project = nextArg;
      i++;
    } else if (!arg.startsWith('-')) {
      result._.push(arg);
    }
  }

  return result;
}

/**
 * Print usage information
 */
function printHelp() {
  console.log(`
${colors.bright}${colors.cyan}learn-bash${colors.reset} - Learn bash from your Claude Code sessions

${colors.bright}USAGE:${colors.reset}
  learn-bash [options]

${colors.bright}OPTIONS:${colors.reset}
  -n, --sessions <count>   Number of recent sessions to process (default: all)
  -f, --file <path>        Process a specific session file
  -o, --output <path>      Output HTML file path (default: ./bash-lesson.html)
  -p, --project <name>     Process sessions from a specific project
  -l, --list               List available Claude Code projects
      --no-open            Don't auto-open the generated HTML in browser
  -h, --help               Show this help message

${colors.bright}EXAMPLES:${colors.reset}
  ${colors.green}learn-bash${colors.reset}                           Process all sessions from current project
  ${colors.green}learn-bash -n 5${colors.reset}                      Process last 5 sessions
  ${colors.green}learn-bash --list${colors.reset}                    List available projects
  ${colors.green}learn-bash -p "my-project"${colors.reset}           Process sessions from specific project
  ${colors.green}learn-bash -f ~/.claude/sessions/abc.json${colors.reset}
  ${colors.green}learn-bash -o ./lesson.html --no-open${colors.reset}

${colors.bright}SESSION LOCATION:${colors.reset}
  Claude Code sessions are stored at: ${colors.yellow}~/.claude/projects/${colors.reset}
`);
}

/**
 * Check if running in WSL
 */
function isWSL() {
  try {
    const version = fs.readFileSync('/proc/version', 'utf8').toLowerCase();
    return version.includes('microsoft') || version.includes('wsl');
  } catch (e) {
    return false;
  }
}

/**
 * Get the Claude projects directory path
 * Handles WSL by checking both Linux and Windows paths
 */
function getClaudeProjectsDir() {
  const homeDir = os.homedir();
  const linuxPath = path.join(homeDir, '.claude', 'projects');

  // Check if running in WSL
  if (isWSL()) {
    // Try Windows user directories
    const windowsUsers = '/mnt/c/Users';
    if (fs.existsSync(windowsUsers)) {
      // Try current username first
      const username = process.env.USER || '';
      const windowsPath = path.join(windowsUsers, username, '.claude', 'projects');
      if (fs.existsSync(windowsPath)) {
        return windowsPath;
      }

      // Try to find any user with .claude folder
      try {
        const users = fs.readdirSync(windowsUsers, { withFileTypes: true });
        for (const user of users) {
          if (user.isDirectory() && !user.name.startsWith('Public') && !user.name.startsWith('Default')) {
            const potentialPath = path.join(windowsUsers, user.name, '.claude', 'projects');
            if (fs.existsSync(potentialPath)) {
              return potentialPath;
            }
          }
        }
      } catch (e) {
        // Ignore errors reading Windows users
      }
    }
  }

  return linuxPath;
}

/**
 * List available Claude Code projects
 */
function listProjects() {
  const projectsDir = getClaudeProjectsDir();

  if (!fs.existsSync(projectsDir)) {
    console.log(`${colors.yellow}No Claude Code projects directory found at:${colors.reset}`);
    console.log(`  ${projectsDir}`);
    console.log(`\n${colors.cyan}Make sure you have used Claude Code at least once.${colors.reset}`);
    return [];
  }

  const entries = fs.readdirSync(projectsDir, { withFileTypes: true });
  const projects = entries
    .filter(entry => entry.isDirectory())
    .map(entry => {
      const projectPath = path.join(projectsDir, entry.name);
      const sessionsPath = path.join(projectPath, 'sessions');
      let sessionCount = 0;

      // Check for sessions in sessions/ subdirectory (new structure)
      if (fs.existsSync(sessionsPath)) {
        const sessions = fs.readdirSync(sessionsPath)
          .filter(f => f.endsWith('.json') || f.endsWith('.jsonl'));
        sessionCount += sessions.length;
      }

      // Also check for .jsonl files directly in project directory (old structure)
      const directJsonl = fs.readdirSync(projectPath)
        .filter(f => f.endsWith('.jsonl') && !f.startsWith('.'));
      sessionCount += directJsonl.length;

      return {
        name: entry.name,
        path: projectPath,
        sessionCount
      };
    })
    .filter(p => p.sessionCount > 0);

  if (projects.length === 0) {
    console.log(`${colors.yellow}No projects with sessions found.${colors.reset}`);
    return [];
  }

  console.log(`\n${colors.bright}${colors.cyan}Available Claude Code Projects:${colors.reset}\n`);
  projects.forEach((project, index) => {
    console.log(`  ${colors.green}${index + 1}.${colors.reset} ${project.name}`);
    console.log(`     ${colors.yellow}Sessions:${colors.reset} ${project.sessionCount}`);
    console.log(`     ${colors.yellow}Path:${colors.reset} ${project.path}\n`);
  });

  return projects;
}

/**
 * Check if Python 3 is available
 */
function checkPython() {
  const pythonCommands = ['python3', 'python'];

  for (const cmd of pythonCommands) {
    try {
      const version = execSync(`${cmd} --version 2>&1`, { encoding: 'utf8' });
      if (version.includes('Python 3')) {
        return cmd;
      }
    } catch (e) {
      // Command not found, try next
    }
  }

  return null;
}

/**
 * Open a file in the default browser
 */
function openInBrowser(filePath) {
  const platform = os.platform();
  let cmd;
  let args;

  switch (platform) {
    case 'darwin':
      cmd = 'open';
      args = [filePath];
      break;
    case 'win32':
      cmd = 'cmd';
      args = ['/c', 'start', '', filePath];
      break;
    default:
      // Linux and others
      cmd = 'xdg-open';
      args = [filePath];
  }

  try {
    spawn(cmd, args, { detached: true, stdio: 'ignore' }).unref();
    return true;
  } catch (e) {
    return false;
  }
}

/**
 * Find the Python main.py script
 */
function findPythonScript() {
  // Check relative to this script's location
  const scriptDir = path.dirname(__filename);
  const possiblePaths = [
    path.join(scriptDir, '..', 'scripts', 'main.py'),
    path.join(scriptDir, 'scripts', 'main.py'),
    path.join(process.cwd(), 'scripts', 'main.py')
  ];

  for (const p of possiblePaths) {
    if (fs.existsSync(p)) {
      return path.resolve(p);
    }
  }

  return null;
}

/**
 * Main entry point
 */
function main() {
  const args = parseArgs(process.argv.slice(2));

  // Show help
  if (args.help) {
    printHelp();
    process.exit(0);
  }

  // List projects
  if (args.list) {
    listProjects();
    process.exit(0);
  }

  // Check Python availability
  const pythonCmd = checkPython();
  if (!pythonCmd) {
    console.error(`${colors.red}${colors.bright}Error:${colors.reset} Python 3 is required but not found.`);
    console.error(`Please install Python 3 from: ${colors.cyan}https://www.python.org/downloads/${colors.reset}`);
    process.exit(1);
  }

  // Find the Python script
  const pythonScript = findPythonScript();
  if (!pythonScript) {
    console.error(`${colors.red}${colors.bright}Error:${colors.reset} Could not find scripts/main.py`);
    console.error(`Make sure you're running from the package directory or it's properly installed.`);
    process.exit(1);
  }

  // Build Python script arguments
  const pythonArgs = [pythonScript];

  if (args.sessions) {
    pythonArgs.push('--sessions', args.sessions.toString());
  }

  if (args.file) {
    pythonArgs.push('--file', args.file);
  }

  if (args.output) {
    pythonArgs.push('--output', args.output);
  }

  if (args.project) {
    pythonArgs.push('--project', args.project);
  }

  // Default output path if not specified
  const outputPath = args.output || path.join(process.cwd(), 'bash-lesson.html');

  console.log(`\n${colors.bright}${colors.cyan}learn-bash${colors.reset} - Extracting bash commands from Claude Code sessions...\n`);

  // Spawn Python process
  const pythonProcess = spawn(pythonCmd, pythonArgs, {
    stdio: 'inherit',
    cwd: process.cwd()
  });

  pythonProcess.on('close', (code) => {
    if (code === 0) {
      console.log(`\n${colors.green}${colors.bright}Success!${colors.reset} Generated: ${colors.cyan}${outputPath}${colors.reset}`);

      // Open in browser unless --no-open specified
      if (!args['no-open'] && fs.existsSync(outputPath)) {
        console.log(`${colors.yellow}Opening in browser...${colors.reset}`);
        if (!openInBrowser(outputPath)) {
          console.log(`${colors.yellow}Could not auto-open. Please open manually:${colors.reset} ${outputPath}`);
        }
      }
    } else {
      console.error(`\n${colors.red}${colors.bright}Error:${colors.reset} Python script exited with code ${code}`);
      process.exit(code);
    }
  });

  pythonProcess.on('error', (err) => {
    console.error(`${colors.red}${colors.bright}Error:${colors.reset} Failed to start Python process:`, err.message);
    process.exit(1);
  });
}

// Run main
main();
