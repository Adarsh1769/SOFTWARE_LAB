# AI Code Assistant Lab: GitHub Copilot and Code Comparison

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
