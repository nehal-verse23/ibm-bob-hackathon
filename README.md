# DevPulse — AI Change Impact & Regression Risk Agent

DevPulse is an AI-assisted developer workflow that helps identify the impact of a code change before it reaches production.

It combines local change detection, dependency analysis, automated regression testing, and IBM Bob Agent analysis to turn a potentially risky code change into a validated change-impact report.

---

## Problem

When a developer changes one function or component, the impact may extend beyond that file.

Developers often need to manually determine:

- Which files depend on the changed component?
- Which tests are affected?
- Could the change break an existing workflow?
- Are database or notification operations affected?
- Which regression tests should be executed?
- Did the change actually introduce a failure?

This investigation can become time-consuming, especially in larger codebases.

---

## Solution

DevPulse creates a change-impact and regression-validation workflow.

It:

1. Detects modified project files using Git.
2. Analyzes Python dependencies using AST.
3. Identifies potentially affected files.
4. Assigns a risk level to affected components.
5. Recommends relevant regression tests.
6. Automatically executes the pytest suite.
7. Reports actual test failures and passes.
8. Uses IBM Bob Agent for deeper impact analysis and code repair.
9. Validates the repaired code again.

---

## Workflow

```text
Developer changes code
        ↓
Git change detection
        ↓
DevPulse dependency analysis
        ↓
Affected files identified
        ↓
Risk assessment
        ↓
Regression test recommendations
        ↓
Automated pytest validation
        ↓
IBM Bob Agent investigation
        ↓
Root-cause analysis
        ↓
IBM Bob fixes the regression
        ↓
Full test validation
        ↓
Change Impact & Regression Validation Report