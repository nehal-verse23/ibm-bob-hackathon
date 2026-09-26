import os
import ast
import subprocess
from datetime import datetime


# --------------------------------------------------
# PATH CONFIGURATION
# --------------------------------------------------

SRC_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SRC_DIR)

SAMPLE_PROJECT = os.path.join(
    PROJECT_ROOT,
    "sample_project"
)

TESTS_DIR = os.path.join(
    PROJECT_ROOT,
    "tests"
)


# --------------------------------------------------
# FIND PYTHON FILES
# --------------------------------------------------

def find_python_files(project_path):

    python_files = []

    for root, folders, files in os.walk(project_path):

        for file in files:

            if file.endswith(".py"):

                python_files.append(
                    os.path.join(root, file)
                )

    return python_files


# --------------------------------------------------
# FIND DEPENDENCIES
# --------------------------------------------------

def find_dependencies(file_path):

    dependencies = []

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        code = file.read()

    tree = ast.parse(code)

    for node in ast.walk(tree):

        if isinstance(node, ast.Import):

            for name in node.names:

                dependencies.append(
                    name.name.split(".")[-1]
                )

        elif isinstance(node, ast.ImportFrom):

            if node.module:

                dependencies.append(
                    node.module.split(".")[-1]
                )

    return dependencies


# --------------------------------------------------
# BUILD DEPENDENCY MAP
# --------------------------------------------------

def build_dependency_map(files):

    dependency_map = {}

    for file in files:

        filename = os.path.splitext(
            os.path.basename(file)
        )[0]

        dependency_map[filename] = (
            find_dependencies(file)
        )

    return dependency_map


# --------------------------------------------------
# FIND AFFECTED FILES
# --------------------------------------------------

def find_affected_files(
    dependency_map,
    changed_file
):

    affected_files = []

    for file, dependencies in dependency_map.items():

        if file == changed_file:
            continue

        if changed_file in dependencies:

            affected_files.append(file)

    return affected_files


# --------------------------------------------------
# CALCULATE RISK
# --------------------------------------------------

def calculate_risk(file):

    if file in ["orders", "database"]:
        return "HIGH"

    if file in ["notifications", "tests"]:
        return "MEDIUM"

    return "LOW"


# --------------------------------------------------
# RECOMMEND TESTS
# --------------------------------------------------

def recommend_tests(
    changed_file,
    affected_files
):

    tests = []

    if changed_file == "payments":

        tests.append(
            "Successful payment"
        )

        tests.append(
            "Invalid payment amount"
        )

        tests.append(
            "Negative payment amount"
        )

        tests.append(
            "Payment database interaction"
        )

    if "orders" in affected_files:

        tests.append(
            "Order placement"
        )

        tests.append(
            "Order failure on invalid payment"
        )

        tests.append(
            "Payment notification on successful order"
        )

        tests.append(
            "No notification on failed order"
        )

    return tests


# --------------------------------------------------
# GET CHANGED FILES
# --------------------------------------------------

def get_changed_files():

    result = subprocess.run(
        [
            "git",
            "status",
            "--short"
        ],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True
    )

    changed_files = []

    for line in result.stdout.splitlines():

        if not line.strip():
            continue

        file_path = line[3:].strip()

        # Ignore DevPulse itself
        if file_path == "src/devpulse.py":
            continue

        # Only analyze sample project files
        if file_path.startswith(
            "sample_project/"
        ):

            if file_path.endswith(".py"):

                changed_files.append(
                    file_path
                )

    return changed_files


# --------------------------------------------------
# RUN REGRESSION TESTS
# --------------------------------------------------

def run_tests():

    print(
        "\nRunning regression tests...\n"
    )

    result = subprocess.run(
        [
            "python",
            "-m",
            "pytest",
            "tests",
            "-v"
        ],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True
    )

    return (
        result.returncode,
        result.stdout,
        result.stderr
    )


# --------------------------------------------------
# GENERATE REPORT
# --------------------------------------------------

def generate_report(
    changed_file,
    affected_files,
    tests,
    test_status,
    test_output
):

    report = []

    report.append("=" * 65)

    report.append(
        "                    DEVPULSE"
    )

    report.append(
        "             CHANGE IMPACT REPORT"
    )

    report.append("=" * 65)

    report.append(
        f"\nGenerated: "
        f"{datetime.now().strftime('%Y-%m-%d %H:%M')}"
    )

    report.append(
        "\nChanged Component:"
    )

    report.append(
        f"  → {changed_file}.py"
    )

    report.append(
        "\nPotential Impact:"
    )

    if affected_files:

        for file in affected_files:

            risk = calculate_risk(file)

            report.append(
                f"  [{risk}] {file}.py"
            )

    else:

        report.append(
            "  No affected files detected."
        )

    report.append(
        "\nRecommended Regression Tests:"
    )

    if tests:

        for test in tests:

            report.append(
                f"  ✓ {test}"
            )

    else:

        report.append(
            "  No specific tests recommended."
        )

    report.append(
        "\nValidation Result:"
    )

    if test_status == 0:

        report.append(
            "  ✓ ALL REGRESSION TESTS PASSED"
        )

    else:

        report.append(
            "  ✗ REGRESSION TESTS FAILED"
        )

    report.append(
        "\nTest Execution Output:"
    )

    report.append(
        "-" * 65
    )

    report.append(
        test_output
    )

    report.append(
        "-" * 65
    )

    report.append(
        "\nRecommendation:"
    )

    if test_status == 0:

        report.append(
            "  Change passed automated "
            "regression validation."
        )

    else:

        report.append(
            "  Investigate failing regression "
            "tests before release."
        )

    report.append(
        "\n" + "=" * 65
    )

    return "\n".join(report)


# --------------------------------------------------
# DEVPULSE WORKFLOW
# --------------------------------------------------

files = find_python_files(
    SAMPLE_PROJECT
)

dependency_map = build_dependency_map(
    files
)

changed_files = get_changed_files()

print(
    "\nChanged files detected by Git:"
)

for file in changed_files:

    print(
        f"  → {file}"
    )


if not changed_files:

    print(
        "\nNo changed sample project files detected."
    )

    exit()


changed_file_path = changed_files[0]

changed_file = os.path.splitext(
    os.path.basename(
        changed_file_path
    )
)[0]


affected_files = find_affected_files(
    dependency_map,
    changed_file
)


tests = recommend_tests(
    changed_file,
    affected_files
)


test_status, test_output, test_error = (
    run_tests()
)


report = generate_report(
    changed_file,
    affected_files,
    tests,
    test_status,
    test_output
)


print("\n")

print(report)