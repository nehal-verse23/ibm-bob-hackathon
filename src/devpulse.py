import os
import ast
import subprocess
from datetime import datetime


def find_python_files(project_path):
    python_files = []

    for root, folders, files in os.walk(project_path):
        for file in files:
            if file.endswith(".py"):
                python_files.append(os.path.join(root, file))

    return python_files


def find_dependencies(file_path):
    dependencies = []

    with open(file_path, "r", encoding="utf-8") as file:
        code = file.read()

    tree = ast.parse(code)

    for node in ast.walk(tree):

        if isinstance(node, ast.Import):
            for name in node.names:
                dependencies.append(name.name.split(".")[0])

        elif isinstance(node, ast.ImportFrom):
            if node.module:
                dependencies.append(node.module.split(".")[0])

    return dependencies


def build_dependency_map(files):
    dependency_map = {}

    for file in files:
        filename = os.path.splitext(
            os.path.basename(file)
        )[0]

        dependency_map[filename] = find_dependencies(file)

    return dependency_map


def find_affected_files(dependency_map, changed_file):
    affected_files = []

    for file, dependencies in dependency_map.items():

        if changed_file in dependencies:
            affected_files.append(file)

    return affected_files


def calculate_risk(file):
    if file == "orders":
        return "HIGH"

    return "MEDIUM"


def recommend_tests(changed_file, affected_files):

    tests = []

    if changed_file == "payments":
        tests.append("Successful payment")
        tests.append("Invalid payment amount")
        tests.append("Order payment flow")

    if "orders" in affected_files:
        tests.append("Order placement")

    return tests


def get_changed_files():

    result = subprocess.run(
        ["git", "status", "--short"],
        capture_output=True,
        text=True
    )

    changed_files = []

    for line in result.stdout.splitlines():

        if line.strip():

            file_path = line[3:].strip()

            changed_files.append(file_path)

    return changed_files


def generate_report(
    changed_file,
    affected_files,
    tests
):

    report = []

    report.append("=" * 60)
    report.append("                 DEVPULSE")
    report.append("          CHANGE IMPACT REPORT")
    report.append("=" * 60)

    report.append(
        f"\nGenerated: "
        f"{datetime.now().strftime('%Y-%m-%d %H:%M')}"
    )

    report.append("\nChanged Component:")
    report.append(f"  → {changed_file}.py")

    report.append("\nPotential Impact:")

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
        "\n" + "=" * 60
    )

    return "\n".join(report)


# --------------------------------------------------
# DEVPULSE WORKFLOW
# --------------------------------------------------

project_path = "../sample_project"

files = find_python_files(project_path)

dependency_map = build_dependency_map(files)

changed_files = get_changed_files()

print("\nChanged files detected by Git:")

for file in changed_files:
    print(f"  → {file}")


if not changed_files:

    print(
        "\nNo changed files detected."
    )

    exit()


changed_file_path = changed_files[0]

changed_file = os.path.splitext(
    os.path.basename(changed_file_path)
)[0]


affected_files = find_affected_files(
    dependency_map,
    changed_file
)


tests = recommend_tests(
    changed_file,
    affected_files
)


report = generate_report(
    changed_file,
    affected_files,
    tests
)


print("\n")
print(report)