"""Compile and run the Java Practical 2 execution-time comparison."""

from pathlib import Path
import shutil
import subprocess
import tempfile


PRACTICAL_DIR = Path(__file__).resolve().parent
JAVA_SOURCES = (
    "CheckResult.java",
    "BasicPrimeChecker.java",
    "OptimizedPrimeChecker.java",
    "Practical2Timing.java",
)


def main() -> None:
    javac = shutil.which("javac")
    java = shutil.which("java")
    if javac is None or java is None:
        raise SystemExit("Java JDK not found. Install a JDK and make sure java and javac are on PATH.")

    with tempfile.TemporaryDirectory(prefix="practical2-timing-") as output_dir:
        classes_dir = Path(output_dir)
        sources = [str(PRACTICAL_DIR / source) for source in JAVA_SOURCES]
        print("Compiling Practical 2 Java timing benchmark...")
        subprocess.run([javac, "-d", str(classes_dir), *sources], check=True)
        print()
        subprocess.run([java, "-cp", str(classes_dir), "Practical2Timing"], check=True)


if __name__ == "__main__":
    main()
