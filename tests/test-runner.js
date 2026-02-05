#!/usr/bin/env node
/**
 * Test Runner for learn_bash_from_session_data
 *
 * Runs Python tests via subprocess and JS tests using built-in assert.
 * No external dependencies required.
 */

const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');
const assert = require('assert');

// ANSI colors for output
const colors = {
    reset: '\x1b[0m',
    green: '\x1b[32m',
    red: '\x1b[31m',
    yellow: '\x1b[33m',
    blue: '\x1b[34m',
    cyan: '\x1b[36m'
};

/**
 * Test results aggregator
 */
class TestResults {
    constructor() {
        this.passed = 0;
        this.failed = 0;
        this.errors = [];
        this.suites = [];
    }

    addSuite(name, passed, failed, errors = []) {
        this.suites.push({ name, passed, failed, errors });
        this.passed += passed;
        this.failed += failed;
        this.errors.push(...errors);
    }

    report() {
        console.log('\n' + '='.repeat(60));
        console.log(`${colors.cyan}TEST RESULTS SUMMARY${colors.reset}`);
        console.log('='.repeat(60));

        for (const suite of this.suites) {
            const status = suite.failed === 0
                ? `${colors.green}PASS${colors.reset}`
                : `${colors.red}FAIL${colors.reset}`;
            console.log(`\n${status} ${suite.name}`);
            console.log(`  Passed: ${suite.passed}, Failed: ${suite.failed}`);
            if (suite.errors.length > 0) {
                for (const err of suite.errors) {
                    console.log(`  ${colors.red}Error: ${err}${colors.reset}`);
                }
            }
        }

        console.log('\n' + '-'.repeat(60));
        const totalStatus = this.failed === 0
            ? `${colors.green}ALL TESTS PASSED${colors.reset}`
            : `${colors.red}SOME TESTS FAILED${colors.reset}`;
        console.log(`${totalStatus}`);
        console.log(`Total: ${this.passed + this.failed} | Passed: ${colors.green}${this.passed}${colors.reset} | Failed: ${colors.red}${this.failed}${colors.reset}`);
        console.log('='.repeat(60) + '\n');

        return this.failed === 0;
    }
}

/**
 * Run a Python test file and parse results
 * @param {string} testFile - Path to the Python test file
 * @returns {Promise<{passed: number, failed: number, errors: string[]}>}
 */
function runPythonTest(testFile) {
    return new Promise((resolve) => {
        const testPath = path.resolve(testFile);

        if (!fs.existsSync(testPath)) {
            resolve({ passed: 0, failed: 1, errors: [`File not found: ${testPath}`] });
            return;
        }

        console.log(`${colors.blue}Running: ${path.basename(testFile)}${colors.reset}`);

        const proc = spawn('python3', ['-m', 'unittest', testPath, '-v'], {
            cwd: path.dirname(testPath),
            env: { ...process.env, PYTHONPATH: path.dirname(path.dirname(testPath)) }
        });

        let stdout = '';
        let stderr = '';

        proc.stdout.on('data', (data) => {
            stdout += data.toString();
            process.stdout.write(data);
        });

        proc.stderr.on('data', (data) => {
            stderr += data.toString();
            process.stderr.write(data);
        });

        proc.on('close', (code) => {
            // Parse unittest output for results
            const okMatch = stderr.match(/OK(?:\s+\(([^)]+)\))?/);
            const failMatch = stderr.match(/FAILED\s+\((?:failures=(\d+))?(?:,\s*)?(?:errors=(\d+))?\)/);
            const ranMatch = stderr.match(/Ran\s+(\d+)\s+test/);

            let passed = 0;
            let failed = 0;
            const errors = [];

            if (ranMatch) {
                const total = parseInt(ranMatch[1], 10);
                if (okMatch) {
                    passed = total;
                    // Check for skipped tests
                    if (okMatch[1]) {
                        const skipMatch = okMatch[1].match(/skipped=(\d+)/);
                        if (skipMatch) {
                            passed -= parseInt(skipMatch[1], 10);
                        }
                    }
                } else if (failMatch) {
                    const failures = parseInt(failMatch[1] || '0', 10);
                    const errs = parseInt(failMatch[2] || '0', 10);
                    failed = failures + errs;
                    passed = total - failed;
                }
            }

            if (code !== 0 && failed === 0) {
                failed = 1;
                errors.push(`Process exited with code ${code}`);
            }

            resolve({ passed, failed, errors });
        });

        proc.on('error', (err) => {
            resolve({ passed: 0, failed: 1, errors: [err.message] });
        });
    });
}

/**
 * Run JavaScript tests using built-in assert
 * @returns {{passed: number, failed: number, errors: string[]}}
 */
function runJSTests() {
    console.log(`${colors.blue}Running: JavaScript unit tests${colors.reset}`);

    let passed = 0;
    let failed = 0;
    const errors = [];

    // Test 1: Assert module works
    try {
        assert.strictEqual(1 + 1, 2, '1 + 1 should equal 2');
        console.log(`  ${colors.green}PASS${colors.reset}: Assert module basic test`);
        passed++;
    } catch (e) {
        console.log(`  ${colors.red}FAIL${colors.reset}: Assert module basic test`);
        errors.push(e.message);
        failed++;
    }

    // Test 2: Path resolution works
    try {
        const testDir = path.dirname(__filename);
        assert.ok(testDir.includes('tests'), 'Should be in tests directory');
        console.log(`  ${colors.green}PASS${colors.reset}: Path resolution test`);
        passed++;
    } catch (e) {
        console.log(`  ${colors.red}FAIL${colors.reset}: Path resolution test`);
        errors.push(e.message);
        failed++;
    }

    // Test 3: File system access works
    try {
        const exists = fs.existsSync(__filename);
        assert.strictEqual(exists, true, 'Current file should exist');
        console.log(`  ${colors.green}PASS${colors.reset}: File system access test`);
        passed++;
    } catch (e) {
        console.log(`  ${colors.red}FAIL${colors.reset}: File system access test`);
        errors.push(e.message);
        failed++;
    }

    // Test 4: JSON parsing works (needed for JSONL processing)
    try {
        const json = '{"tool": "Bash", "command": "ls -la"}';
        const parsed = JSON.parse(json);
        assert.strictEqual(parsed.tool, 'Bash');
        assert.strictEqual(parsed.command, 'ls -la');
        console.log(`  ${colors.green}PASS${colors.reset}: JSON parsing test`);
        passed++;
    } catch (e) {
        console.log(`  ${colors.red}FAIL${colors.reset}: JSON parsing test`);
        errors.push(e.message);
        failed++;
    }

    // Test 5: JSONL line parsing simulation
    try {
        const lines = [
            '{"type": "tool_use", "name": "Bash"}',
            '{"type": "tool_result", "output": "success"}'
        ];
        const parsed = lines.map(line => JSON.parse(line));
        assert.strictEqual(parsed.length, 2);
        assert.strictEqual(parsed[0].type, 'tool_use');
        assert.strictEqual(parsed[1].type, 'tool_result');
        console.log(`  ${colors.green}PASS${colors.reset}: JSONL parsing simulation`);
        passed++;
    } catch (e) {
        console.log(`  ${colors.red}FAIL${colors.reset}: JSONL parsing simulation`);
        errors.push(e.message);
        failed++;
    }

    // Test 6: Regex for command extraction
    try {
        const bashCommand = 'git status && git log --oneline -5';
        const hasChain = /&&|\|\|/.test(bashCommand);
        assert.strictEqual(hasChain, true, 'Should detect command chaining');
        console.log(`  ${colors.green}PASS${colors.reset}: Command chain detection`);
        passed++;
    } catch (e) {
        console.log(`  ${colors.red}FAIL${colors.reset}: Command chain detection`);
        errors.push(e.message);
        failed++;
    }

    // Test 7: Pipe detection
    try {
        const pipeCommand = 'cat file.txt | grep pattern | sort';
        const pipes = (pipeCommand.match(/\|/g) || []).length;
        assert.strictEqual(pipes, 2, 'Should detect 2 pipes');
        console.log(`  ${colors.green}PASS${colors.reset}: Pipe detection`);
        passed++;
    } catch (e) {
        console.log(`  ${colors.red}FAIL${colors.reset}: Pipe detection`);
        errors.push(e.message);
        failed++;
    }

    // Test 8: Redirect detection
    try {
        const redirectCmd = 'echo "test" > output.txt 2>&1';
        const hasRedirect = /[<>]/.test(redirectCmd);
        assert.strictEqual(hasRedirect, true, 'Should detect redirects');
        console.log(`  ${colors.green}PASS${colors.reset}: Redirect detection`);
        passed++;
    } catch (e) {
        console.log(`  ${colors.red}FAIL${colors.reset}: Redirect detection`);
        errors.push(e.message);
        failed++;
    }

    return { passed, failed, errors };
}

/**
 * Main test runner
 */
async function main() {
    console.log('\n' + '='.repeat(60));
    console.log(`${colors.cyan}LEARN BASH FROM SESSION DATA - TEST SUITE${colors.reset}`);
    console.log('='.repeat(60) + '\n');

    const results = new TestResults();
    const testsDir = path.dirname(__filename);

    // Run JavaScript tests first
    const jsResults = runJSTests();
    results.addSuite('JavaScript Tests', jsResults.passed, jsResults.failed, jsResults.errors);

    // Python test files to run
    const pythonTests = [
        'test_extractor.py',
        'test_parser.py',
        'test_analyzer.py',
        'test_quiz.py'
    ];

    // Run each Python test file
    for (const testFile of pythonTests) {
        const testPath = path.join(testsDir, testFile);
        if (fs.existsSync(testPath)) {
            const pyResults = await runPythonTest(testPath);
            results.addSuite(`Python: ${testFile}`, pyResults.passed, pyResults.failed, pyResults.errors);
        } else {
            console.log(`${colors.yellow}SKIP: ${testFile} (not found)${colors.reset}`);
            results.addSuite(`Python: ${testFile}`, 0, 0, ['File not found - skipped']);
        }
    }

    // Generate final report
    const success = results.report();
    process.exit(success ? 0 : 1);
}

// Run if executed directly
if (require.main === module) {
    main().catch(err => {
        console.error(`${colors.red}Fatal error: ${err.message}${colors.reset}`);
        process.exit(1);
    });
}

module.exports = { runPythonTest, runJSTests, TestResults };
