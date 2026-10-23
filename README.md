# AI Code Assistant Lab: GitHub Copilot and Code Comparison

## Practical 8: AI-based conversion of requirements into user stories

This practical converts an SRS excerpt into user stories and acceptance
criteria, evaluates a first draft with a small Python completeness checker,
then re-checks a revised draft. The checker uses only Python's standard
library. Its checks are structural and traceability checks, not a substitute
for reviewing whether acceptance criteria accurately satisfy the SRS.

### Step 1 - Input: `srs_excerpt.txt`

Read `practical-8-python/srs_excerpt.txt`. It defines four account-access
requirements: account creation, email verification, sign-in and lockout, and
password reset.

### Step 2 - Draft 1 of the user stories

Open `practical-8-python/draft1_stories.md` for the sample AI-generated first
draft. To generate your own draft, give the SRS excerpt to GitHub Copilot,
Windsurf, or Ollama with this prompt:

> Convert this SRS excerpt into one user story for each requirement. Use the
> format “As a [role], I want [goal], so that [benefit].” Add acceptance
> criteria as Given/When/Then bullet points. Preserve every stated rule,
> limit, expiry, and failure case. Label each story with its SRS requirement
> ID, and do not invent behavior.

Review the AI output and save it as a Markdown file in
`practical-8-python/` before evaluating it.

### Step 3 - Completeness checker: `check_stories.py`

The checker reads requirement IDs from the SRS and checks each story for
traceability, the role/goal/benefit format, and explicit `Given:`, `When:`,
and `Then:` labels in every acceptance-criteria bullet. It reports each check
and returns a nonzero exit code for an incomplete draft. It checks structure
and presence, so reviewers must also compare the actual criteria with the
requirement details.

### Step 4 - Evaluate Draft 1

From the lab root, run:

```powershell
py -3 practical-8-python\check_stories.py practical-8-python\draft1_stories.md
```

The example draft is expected to be **INCOMPLETE**: it omits the benefit from
one story, omits a `Then` criterion from another, and does not cover REQ-04.
The checker exits with status 1 for this result; that is expected.

### Step 5 - Revised user stories

Open `practical-8-python/revised_stories.md` to see the revised example. It
covers all four requirement IDs, uses the complete user-story format, and
includes Given/When/Then criteria. Review that the criteria preserve details
such as the 12-character password minimum, 24-hour verification link expiry,
five-attempt/15-minute lockout, and single-use 30-minute reset link.

For your own revision, ask the AI tool to address the failed checks and
preserve each SRS constraint. Review its changes rather than accepting them
without checking.

### Step 6 - Re-check the revised stories

Run the checker against the revised example:

```powershell
py -3 practical-8-python\check_stories.py practical-8-python\revised_stories.md
```

Expected result: **20/20 checks passed** and `Result: COMPLETE`. Run the
checker unit tests as an additional verification:

```powershell
py -3 -m unittest discover -s practical-8-python -p test_check_stories.py -v
```

Both tests should pass, confirming that the incomplete draft is flagged and
the revised stories pass the structural completeness checks.

## Practical 7: AI-generated API documentation (Python)

This practical uses a small WSGI backend and a local Ollama model to generate
API documentation, then validates the documented behavior with five tests.
The example needs only Python's standard library for the API and tests.

### Step 1 - Backend code: `app.py`

Open `practical-7-python/app.py`. It implements `GET /api/products` with an
optional `category` query parameter and `POST /api/products` with JSON input.
It returns **404** for unknown routes, **201** for a valid product request, and
**422** for invalid JSON or product fields. The example does not persist
created products.

### Step 2 - Documentation generator: `generate_docs.py`

The generator reads `app.py` and sends it to a local Ollama model. Install
[Ollama](https://ollama.com/) and download the default model once:

```powershell
ollama pull llama3.2
```

Alternatively, set `OLLAMA_MODEL` to a model already available locally. To
generate docs with GitHub Copilot or Windsurf instead, use this prompt with
`app.py` and save the reviewed result as `practical-7-python/API.md`:

> Generate concise Markdown API documentation from app.py only. Document every
> route, HTTP method, optional query parameter, JSON request and response,
> status code, validation rule, and persistence behavior. Do not invent
> behavior. Include examples for the 404, 201, and 422 responses.

### Step 3 - Generate the documentation

In a VS Code terminal at the lab root, start Ollama if it is not already
running, then run:

```powershell
py -3 practical-7-python/generate_docs.py
```

The generated result is written to `practical-7-python/API.md`. Review the
model output against the backend before treating it as authoritative.

### Step 4 - Generated documentation: `API.md`

Open `practical-7-python/API.md`. It documents the collection endpoint,
category filtering, product creation, validation responses, and non-persistent
sample behavior.

### Step 5 - Validation tests: `test_docs.py`

The five tests exercise the API through its WSGI interface and check the
documented collection response, query parameter, **201 Created**, **422
Unprocessable Entity**, and **404 Not Found** behavior.

### Step 6 - Validation run

Run the checks from the lab root:

```powershell
py -3 -m unittest discover -s practical-7-python -p test_docs.py -v
```

Expected result:

```text
Ran 5 tests
OK
```

All five checks pass. The documented 404, category query parameter, 201, and
422 responses behave as written. Capture the generated `API.md` and passing
test output with **Win+Shift+S** for the lab record.

## Practical 6: AI-based static code analysis and vulnerability scanning (Python)

This isolated sample uses Bandit to scan a deliberately unsafe calculator,
then scans a corrected version and runs tests. The unsafe file is for static
analysis only: never pass untrusted input to `app.py`.

### Step 3 - `app.py` (before)

Open `practical-6-python/app.py`. The `calculate` function calls Python's
`eval` on its expression. This sample uses a harmless constant when run, but
the function itself must not be used with user-controlled text.

From the lab root, run the before-scan:

```powershell
py -3 -m pip install bandit
Set-Location practical-6-python
py -3 -m bandit -f txt app.py
```

### Step 4 - Vulnerability report (before)

Bandit 1.9.4 reports one issue:

```text
Issue: [B307:blacklist] Use of possibly insecure function
Severity: Medium   Confidence: High
Location: app.py:6:11
Total issues: Medium 1, High 0, Low 0
```

Bandit's scan exits with status 1 when it finds this issue; that is an expected
scanner result, not a failure to run the tool.

### Step 5 - AI explanation

Ask Copilot Chat:

> Explain Bandit's B307 finding for the eval call in app.py. Describe why
> evaluating a string as Python code is unsafe when the string can be
> user-controlled. Suggest a fix for a calculator that accepts only numeric
> literals and the operators +, -, *, and /; preserve normal arithmetic and
> reject all other syntax. Do not suppress the Bandit warning.

`eval` parses and executes general Python expressions, not just arithmetic.
If an expression comes from an untrusted source, it can perform actions beyond
calculation. Bandit flags the dangerous function call but does not prove that
the current constant sample input is attacker-controlled.

### Step 6 - AI-suggested fix (after)

Review `practical-6-python/fixed_app.py`. It parses input as an AST and
evaluates only numeric literals and explicitly allowlisted arithmetic
operators. It limits expression length, syntax-tree size, and result magnitude.
Unsupported syntax such as names, function calls, and exponentiation is rejected.
No `eval` call or warning suppression is used.

### Step 7 - Re-scan report (after)

From the `practical-6-python` directory, run:

```powershell
py -3 -m bandit -f txt fixed_app.py
```

Verified Bandit 1.9.4 result:

```text
Test results:
    No issues identified.
Total issues: Medium 0, High 0, Low 0
```

Verify the fix with the tests:

```powershell
py -3 -m unittest discover -s . -p test_fixed_app.py -v
```

The test report should show `Ran 6 tests` and `OK`. The tests check supported
arithmetic and rejection of unsupported expressions, including a code-shaped
string (which is parsed but never executed). For the lab record, capture the
before-scan finding, Copilot's explanation, the fixed implementation, the
clean re-scan, and test results with **Win+Shift+S**.

## Practical 5: AI-generated unit test cases (Python)

This practical adds three basic validation functions and tests them with
Python's built-in `unittest` framework. The test module separates suggested
AI-generated examples from additional manually selected boundary cases.

### Step 3 - `validators.py`

Open `practical-5-python/validators.py`. It provides:

- `is_valid_username`: accepts 3-20 ASCII letters, digits, or underscores.
- `is_valid_age`: accepts integer ages from 0 through 120; booleans are not
  treated as ages.
- `is_valid_email`: checks a basic email format. It does not verify that a
  mailbox exists or implement every email standard.

### Step 4/5 - AI-generated tests plus manual tests

Open `practical-5-python/test_validators.py`. The
`AIGeneratedValidatorTests` class contains representative cases suggested by
an AI assistant. `ManualValidatorTests` adds boundary, malformed-input, and
type-checking cases.

To demonstrate AI test generation, ask Copilot Chat:

> Generate Python unittest test cases for validators.py. Cover valid and
> invalid usernames, ages, and basic email addresses; include length/range
> boundaries, malformed values, and wrong input types. Do not modify the
> validator implementation. Keep the test module discoverable by unittest.

Review the suggestions and compare them to the cases already in
`test_validators.py`. The committed file includes runnable example tests so
the practical can be executed even before using Copilot.

### Step 6/9 - Test execution report

From the lab root, run:

```powershell
py -3 -m unittest discover -s practical-5-python -p test_validators.py -v
```

Expected report:

```text
Ran 10 tests
OK
```

The tests cover valid and invalid values for all three validators, username
length boundaries, inclusive age boundaries, malformed email strings, and
wrong types. On this workspace, all 10 tests passed. Capture the
`test_validators.py` cases and the terminal test report using **Win+Shift+S**
for the lab record.

## Practical 4: AI-assisted code refactoring and auto-documentation (Python)

This practical preserves a small legacy order-summary program and refactors it
into documented, readable Python while keeping its existing output behavior.

### Step 1/2 - `messy.py` (original)

Open `practical-4-python/messy.py`. It summarizes order rows, but uses
single-letter variable names, nested conditions, and no function documentation.
It ignores rows with fewer than three fields, non-positive quantities, or
negative prices. A 10% discount applies when a line total is strictly greater
than 100.

Run the original from the lab root:

```powershell
py -3 practical-4-python/messy.py
```

Expected output:

```text
{'total': 185.0, 'units': 3, 'average': 61.67}
```

### Step 3-5 - AI-refactored `clean.py`

Open `practical-4-python/clean.py` in VS Code and use Copilot Chat with this
prompt:

> Refactor messy.py into clean.py. Preserve its behavior exactly, including
> ignored malformed rows, quantity/price rules, the strict greater-than-100
> discount threshold, rounding, result dictionary keys, and empty-input
> behavior. Improve naming and structure, add type hints and useful
> docstrings/comments, and do not add third-party dependencies.

The included `clean.py` is a runnable refactored example. It names the pricing
rules, extracts line-total calculation into a helper, adds a documented public
function, and keeps the legacy rules. The `compare_refactor.py` program checks
both versions on identical input:

```powershell
py -3 practical-4-python/clean.py
py -3 practical-4-python/compare_refactor.py
```

Expected comparison output:

```text
Original:   {'total': 185.0, 'units': 3, 'average': 61.67}
Refactored: {'total': 185.0, 'units': 3, 'average': 61.67}
Behavior preserved: True
```

Run the verification tests:

```powershell
py -3 -m unittest discover -s practical-4-python -p test_clean.py -v
```

The test command should report `Ran 3 tests` and `OK`. For the lab record,
capture the original code, Copilot Chat prompt/refactoring explanation,
documented `clean.py`, comparison output, and passing tests with **Win+Shift+S**.

## Practical 3: AI-assisted debugging (Java)

The original practical asks for `.py` files, but this repository's practicals
are being completed in Java. The equivalent Java source files below preserve
the same debugging steps and outputs.

### Bug 1 - `Buggy.java` (Step 1)

Open `practical-3-java/Buggy.java`. It tries to sum `{1, 2, 3, 4, 5}`, but
the loop condition is `index <= values.length`.

### Step 2/3 - Run and traceback

From the lab root in the VS Code PowerShell terminal:

```powershell
Set-Location practical-3-java
javac Buggy.java Fixed.java Buggy2.java Fixed2.java Practical3Test.java
java Buggy
```

The program prints an `ArrayIndexOutOfBoundsException` stack trace. Java's
exact line number can vary, but the exception points to the array access in
`Buggy.sum`.

### AI explanation of the root cause

Ask Copilot Chat:

> Explain why Buggy.java throws ArrayIndexOutOfBoundsException. Trace the
> loop values for an array of length 5, identify the first invalid index, and
> propose the smallest correct change. Do not change the intended sum behavior.

The array has valid indexes 0 through 4. With `index <= values.length`, the
loop also runs at index 5, so `values[5]` throws. Use `index < values.length`
so the final valid index is 4.

### Step 6/7 - `Fixed.java` and output

Run:

```powershell
java Fixed
```

Expected output:

```text
Sum: 15
```

### Bug 2 - wrong operator (Steps 8 and 9): `Buggy2.java`

`Buggy2.java` evaluates a score of 75 using `score <= PASS_MARK`. That
comparison is reversed: a score greater than or equal to 40 should pass.
Run the buggy example:

```powershell
java Buggy2
```

Expected buggy output:

```text
Score: 75
Expected result: PASS
Actual result: FAIL
```

Ask Copilot Chat:

> Debug Buggy2.java. For a passing mark of 40, determine why score 75 is
> classified as FAIL. Identify the incorrect comparison operator, suggest
> the smallest fix, and keep the pass mark inclusive.

### `Fixed2.java` and output

The corrected comparison is `score >= PASS_MARK`. Run:

```powershell
java Fixed2
```

Expected output:

```text
Score: 75
Expected result: PASS
Actual result: PASS
```

### Verify both fixes

Run the dependency-free checks:

```powershell
java Practical3Test
```

Expected output:

```text
Passed 7 debugging checks.
```

The checks confirm the first bug throws as expected, the array fix returns 15,
the wrong operator reproduces the incorrect classification, and the corrected
operator handles below, at, and above the pass mark.

For print evidence, capture `Buggy.java`, its terminal stack trace, Copilot's
root-cause explanation, `Fixed.java` with its output, `Buggy2.java`'s wrong
result, and `Fixed2.java` plus the passing verification output. Use
**Win+Shift+S** for screenshots. Commit and push the practical with the other
lab files in the `SOFTWARE_LAB` repository.

## Practical 2: AI-assisted code writing and optimization (Java)

This practical compares two Java prime-number checkers. `BasicPrimeChecker`
tests every divisor from 2 to one less than the input. `OptimizedPrimeChecker`
is the AI-assisted candidate: it handles even numbers separately and checks
only odd divisors up to the square root. Both return the same result object,
which also counts divisor checks.

### AI explanation of complexity

Ask Copilot Chat to explain the algorithms in the practical using this prompt:

> Explain the time and extra-space complexity of BasicPrimeChecker and
> OptimizedPrimeChecker in this project. Give best- and worst-case behavior,
> explain why trial division only needs to reach the square root, and relate
> the explanation to divisor counts without claiming benchmark timings prove
> Big-O complexity.

For an input `n`, the basic checker can test every integer from 2 through
`n - 1`. A prime has no early divisor to stop the loop, so its worst-case time
is **O(n)**; it uses **O(1)** extra space.

The optimized checker handles 2 and even values separately, then tests odd
divisors only while `divisor <= n / divisor`. If `n` is composite, at least
one factor must be at most its square root; otherwise both factors would be
greater than the square root and their product would exceed `n`. Thus it needs
at most about `sqrt(n) / 2` odd-divisor checks: **O(sqrt(n))** worst-case time
and **O(1)** extra space. Division in the loop condition avoids the
overflow-prone multiplication in `divisor * divisor <= n`. Composite values
with small factors can return earlier. The prime-number practical's deterministic
divisor counts show the algorithmic improvement independently of machine speed.

The optimized candidate in the repository is a working example. To perform
the AI-assisted part with GitHub Copilot, open
`practical-2-java/OptimizedPrimeChecker.java` in VS Code and ask Copilot Chat:

> Optimize this Java prime-number checker for fewer divisor checks. Keep the
> public class name OptimizedPrimeChecker and the static method signature
> `CheckResult check(int number)`. Return false for numbers below 2, handle 2
> and even numbers efficiently, and only test odd divisors up to the square
> root without overflow-prone multiplication. Count each divisibility check
> in the returned CheckResult. Keep it correct for all int values.

Review Copilot's suggestion, apply it to the file, then run the same commands
below. Record whether it remains correct and how the divisor-check counts
compare. This provides a repeatable efficiency measure; elapsed time is not
used because it varies with the machine and system load.

Open the VS Code terminal in the lab folder and run:

```powershell
Set-Location practical-2-java
javac CheckResult.java BasicPrimeChecker.java OptimizedPrimeChecker.java Practical2Main.java Practical2Test.java
java Practical2Main
java Practical2Test
```

The comparison should show `Results match: YES`, fewer total divisor checks
for the optimized checker, and a percentage reduction. With the included test
cases, the checks should report `Passed 5032 Java checks.` No third-party
dependencies are required.

### Execution-time comparison

To time the Java implementations, run the Python launcher from the lab folder:

```powershell
py -3 practical-2-java/compare_timing.py
```

The script compiles the Java benchmark into a temporary folder and executes
it; it does not time Python versions of the algorithms. The Java benchmark
warms up both implementations, alternates measurement order, takes the median
of seven batches (five calls per batch), and reports milliseconds per call
and measured speedup. Compilation is excluded. Timings vary with the CPU,
JVM, and system load, so use the divisor-check results as the stable measure
and treat elapsed time as a practical observation, not a complexity proof.

For print evidence, capture Copilot Chat showing the optimization prompt and
code, the terminal comparison including the reduction, the Java timing
comparison, and the test output. Use **Win+Shift+S** to save screenshots.

## Java version

This lab also includes a Java version in `java-lab/`. It compares an
AI-generated grade classifier with a manually written implementation, using
the same scores and validation rules. The AI candidate separates validation
into a helper; the manual candidate keeps the implementation compact.

To perform the Java experiment with GitHub Copilot, open `java-lab/AiCandidate.java`
in VS Code, open Copilot Chat, and submit this prompt. Review the generated
code, apply it to the file, and run the comparison and checks again:

> Write a Java class named AiCandidate with a public static getGrade(double
> score) method. Accept finite scores from 0 through 100; return A for 90+,
> B for 80-89, C for 70-79, D for 60-69, and F below 60. Throw
> IllegalArgumentException for non-finite or out-of-range values. Use clear
> type-safe Java and include a short class comment.

From the lab folder, compile and run the comparison and dependency-free checks:

```powershell
Set-Location java-lab
javac AiCandidate.java ManualCandidate.java Main.java GradeClassifierTest.java
java Main
java GradeClassifierTest
```

The comparison should report `Matching outputs: 5/5`; the check program should
report `Passed 18 Java checks.` No Java testing framework or third-party
dependencies are needed. Java 8 or newer is required.

Expected comparison output:

```text
AI Code Assistant Lab: Java Grade Classifier Comparison
--------------------------------------------------------------
Score     AI candidate      Manual      Result
--------------------------------------------------------------
95        A                 A           PASS
82        B                 B           PASS
74        C                 C           PASS
63        D                 D           PASS
40        F                 F           PASS
--------------------------------------------------------------
Matching outputs: 5/5
Both implementations use the same input-validation rules.
```

For screenshots, capture the Copilot prompt and generated Java code, the
terminal showing `Matching outputs: 5/5`, and the terminal showing
`Passed 18 Java checks.` Use **Win+Shift+S** to take screenshots.

## Python version

## Aim

Set up GitHub Copilot in Visual Studio Code, use an AI assistant to produce a
small code implementation, and compare its output with a manually written
implementation.

## Experiment

Both implementations solve the same task: convert a score from 0 to 100 into a
letter grade. The AI candidate uses a separate validation helper and explanatory
docstrings. The manual candidate keeps the same validation and grading behavior
in one compact function. The comparison program checks both against identical
scores; the tests also exercise grade boundaries and invalid inputs.

The checked-in Python AI candidate is a runnable example generated for this lab. To
make the experiment specific to the GitHub Copilot extension you install, use
the prompt below in Copilot Chat and replace the contents of
`ai_candidate.py` with its result. Keep the function name `get_grade` and run
the comparison and tests again.

> Write a Python function named get_grade(score) that accepts an integer or
> float from 0 to 100 and returns A for 90+, B for 80-89, C for 70-79, D for
> 60-69, and F below 60. Reject booleans and non-numbers with TypeError, and
> out-of-range scores with ValueError. Add type hints and a short docstring.

## Configure GitHub Copilot in VS Code

1. Open Visual Studio Code and open this lab folder.
2. Open **Extensions** (`Ctrl+Shift+X`), search for **GitHub Copilot**, and
   install the official GitHub Copilot extension. Install **GitHub Copilot
   Chat** too if VS Code lists it separately.
3. Sign in when prompted and authorize the GitHub account that has Copilot
   access. Confirm Copilot Chat is available in the Activity Bar.
4. Open `ai_candidate.py`, open Copilot Chat, and submit the experiment prompt
   above. Review the result, apply it to the file, and save.
5. Run the comparison and tests below. If Copilot's code differs, record what
   changed and whether the same tests still pass.

## Run the experiment on Windows

Open the VS Code terminal (**Terminal > New Terminal**) in this folder. Check
that Python is available:

```powershell
py -3 --version
```

Run the side-by-side comparison:

```powershell
py -3 main.py
```

Run the automated checks:

```powershell
py -3 -m unittest discover -s tests -v
```

No third-party Python packages are required.

## Expected comparison output

```text
AI Code Assistant Lab: Grade Classifier Comparison
----------------------------------------------------------
Score     AI candidate      Manual      Result
----------------------------------------------------------
95        A                 A           PASS
82        B                 B           PASS
74        C                 C           PASS
63        D                 D           PASS
40        F                 F           PASS
----------------------------------------------------------
Matching outputs: 5/5
Both implementations use the same input-validation rules.
```

The test command should finish with `Ran 2 tests` and `OK`.

## Observation and conclusion

Record the Copilot-generated version's structure, readability, and validation
choices, then compare them with `manual_candidate.py`. Both should produce the
same grades and reject the tested invalid inputs. The AI candidate is more
explicit and documented; the manual candidate is shorter. The comparison is
about these two examples, not a claim that one coding approach is always better.

## Screenshots for the lab record

Capture these in VS Code with **Win+Shift+S** (Snipping Tool), then save the
images in your lab record or report:

1. The GitHub Copilot extension installed in the VS Code Extensions view.
2. Copilot Chat showing your prompt and its generated `get_grade` code.
3. The terminal after `py -3 main.py`, including `Matching outputs: 5/5`.
4. The terminal after the test command, showing `Ran 2 tests` and `OK`.

For a single print-friendly result, maximize VS Code, enlarge the terminal
font if needed, run `py -3 main.py` and the test command, and capture the
terminal output. Keep a separate screenshot of Copilot Chat as evidence of the
AI-assistant setup and generation.
