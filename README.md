# AI Code Assistant Lab: GitHub Copilot and Code Comparison

## Practical 2: AI-assisted code writing and optimization (Java)

This practical compares two Java prime-number checkers. `BasicPrimeChecker`
tests every divisor from 2 to one less than the input. `OptimizedPrimeChecker`
is the AI-assisted candidate: it handles even numbers separately and checks
only odd divisors up to the square root. Both return the same result object,
which also counts divisor checks.

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

For print evidence, capture Copilot Chat showing the optimization prompt and
code, the terminal comparison including the reduction, and the test output.
Use **Win+Shift+S** to save screenshots.

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
