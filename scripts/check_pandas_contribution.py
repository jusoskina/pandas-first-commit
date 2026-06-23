#!/usr/bin/env python3
"""Lightweight PR readiness checker for pandas contributions."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from enum import Enum
from pathlib import PurePosixPath
from typing import Any

# ---------------------------------------------------------------------------
# Rule definitions — edit these to tune classification and thresholds easily.
# ---------------------------------------------------------------------------

SOURCE_SUFFIXES = (".py", ".pyx", ".pxd", ".pyi")
SOURCE_PREFIX = "pandas/"

TEST_PREFIX = "pandas/tests/"

DOCS_PREFIX = "doc/"
DOCS_SUFFIXES = (".rst", ".md")

CI_CONFIG_PATHS = (
    ".github/",
    "ci/",
    "pyproject.toml",
    "setup.py",
    "setup.cfg",
    "environment.yml",
)

RISKY_INTERNAL_MARKERS = (
    "_libs",
    "core/indexes",
    "core/internals",
    "core/groupby",
)
RISKY_EXTENSIONS = (".pyx", ".pxd")

DEFAULT_BASE = "upstream/main"
DEFAULT_MAX_FILES = 8

# Heuristic patterns suggesting user-facing behavior changes in a diff hunk.
USER_FACING_DIFF_PATTERNS = (
    re.compile(r"^\+.*\bdef [a-zA-Z]"),  # public function/method added/changed
    re.compile(r"^\+.*\braise \w+"),
    re.compile(r"^\+.*\.warn\s*\("),
    re.compile(r"^\+.*warnings\.warn\s*\("),
    re.compile(r"^\+.*__all__"),
)


class Status(str, Enum):
    PASS = "PASS"
    WARN = "WARN"
    FAIL = "FAIL"


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ContributionType(str, Enum):
    DOCS_ONLY = "docs-only"
    TESTS_ONLY = "tests-only"
    CODE_CHANGE = "code change"
    CODE_AND_TESTS = "code + tests"
    CI_CONFIG = "CI/config change"
    MIXED = "mixed/unclear"


@dataclass
class CheckResult:
    name: str
    status: Status
    message: str


@dataclass
class FileCategories:
    source: list[str] = field(default_factory=list)
    test: list[str] = field(default_factory=list)
    docs: list[str] = field(default_factory=list)
    ci_config: list[str] = field(default_factory=list)
    risky: list[str] = field(default_factory=list)
    other: list[str] = field(default_factory=list)

    @property
    def all_files(self) -> list[str]:
        seen: set[str] = set()
        ordered: list[str] = []
        for bucket in (self.source, self.test, self.docs, self.ci_config, self.risky, self.other):
            for path in bucket:
                if path not in seen:
                    seen.add(path)
                    ordered.append(path)
        return ordered


@dataclass
class Report:
    base: str
    changed_files: list[str]
    categories: FileCategories
    contribution_type: ContributionType
    risk_level: RiskLevel
    risk_reasons: list[str]
    checks: list[CheckResult]
    suggested_commands: list[str]

    @property
    def failures(self) -> list[CheckResult]:
        return [c for c in self.checks if c.status == Status.FAIL]

    @property
    def warnings(self) -> list[CheckResult]:
        return [c for c in self.checks if c.status == Status.WARN]


def run_git(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        capture_output=True,
        text=True,
        check=False,
    )


def get_changed_files(base: str) -> tuple[list[str] | None, str | None]:
    """Return changed file paths relative to repo root, or (None, error_message)."""
    result = run_git(["diff", "--name-only", f"{base}...HEAD"])
    if result.returncode != 0:
        stderr = result.stderr.strip() or "unknown git error"
        return None, f"git diff failed for base '{base}': {stderr}"
    files = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    return files, None


def normalize_path(path: str) -> PurePosixPath:
    return PurePosixPath(path.replace("\\", "/"))


def is_source_file(path: str) -> bool:
    p = normalize_path(path)
    return str(p).startswith(SOURCE_PREFIX) and p.suffix in SOURCE_SUFFIXES


def is_test_file(path: str) -> bool:
    return str(normalize_path(path)).startswith(TEST_PREFIX)


def is_docs_file(path: str) -> bool:
    p = normalize_path(path)
    return str(p).startswith(DOCS_PREFIX) or p.suffix in DOCS_SUFFIXES


def is_ci_config_file(path: str) -> bool:
    p = normalize_path(path)
    path_str = str(p)
    if path_str in CI_CONFIG_PATHS:
        return True
    return any(path_str.startswith(prefix) for prefix in CI_CONFIG_PATHS if prefix.endswith("/"))


def is_risky_file(path: str) -> bool:
    p = normalize_path(path)
    path_str = str(p)
    if p.suffix in RISKY_EXTENSIONS:
        return True
    return any(marker in path_str for marker in RISKY_INTERNAL_MARKERS)


def classify_files(files: list[str]) -> FileCategories:
    categories = FileCategories()

    for path in files:
        matched = False
        if is_source_file(path):
            categories.source.append(path)
            matched = True
        if is_test_file(path):
            categories.test.append(path)
            matched = True
        if is_docs_file(path):
            categories.docs.append(path)
            matched = True
        if is_ci_config_file(path):
            categories.ci_config.append(path)
            matched = True
        if is_risky_file(path):
            categories.risky.append(path)
            matched = True
        if not matched:
            categories.other.append(path)

    return categories


def infer_contribution_type(categories: FileCategories) -> ContributionType:
    has_source = bool(categories.source)
    has_test = bool(categories.test)
    has_docs = bool(categories.docs)
    has_ci = bool(categories.ci_config)
    has_other = bool(categories.other)

    if has_source and has_test:
        return ContributionType.CODE_AND_TESTS
    if has_source:
        return ContributionType.CODE_CHANGE
    if has_test and not (has_docs or has_ci or has_other):
        return ContributionType.TESTS_ONLY
    if has_docs and not (has_source or has_test or has_ci or has_other):
        return ContributionType.DOCS_ONLY
    if has_ci and not (has_source or has_test or has_docs):
        return ContributionType.CI_CONFIG
    return ContributionType.MIXED


def infer_risk_level(
    categories: FileCategories,
    contribution_type: ContributionType,
    file_count: int,
    max_files: int,
) -> tuple[RiskLevel, list[str]]:
    reasons: list[str] = []

    if categories.risky:
        reasons.append(
            "Touches risky internals (Cython, _libs, or core indexing/groupby/internals)."
        )

    if file_count > max_files:
        reasons.append(f"Changes {file_count} files (threshold: {max_files}).")

    if contribution_type == ContributionType.CODE_CHANGE:
        reasons.append("Source changed without accompanying test file changes.")

    if categories.ci_config:
        reasons.append("CI or configuration files changed.")

    if contribution_type == ContributionType.DOCS_ONLY:
        return RiskLevel.LOW, reasons or ["Documentation-only change."]

    if contribution_type == ContributionType.TESTS_ONLY and file_count <= max_files:
        if reasons:
            return RiskLevel.MEDIUM, reasons
        return RiskLevel.LOW, ["Test-only change within a narrow scope."]

    if categories.risky or contribution_type == ContributionType.CODE_CHANGE:
        return RiskLevel.HIGH, reasons

    if reasons:
        return RiskLevel.MEDIUM, reasons

    if contribution_type == ContributionType.CODE_AND_TESTS:
        return RiskLevel.LOW, ["Code and tests changed together."]

    return RiskLevel.MEDIUM, reasons or ["Mixed or unclear change scope."]


def get_diff_for_file(base: str, path: str) -> str:
    result = run_git(["diff", f"{base}...HEAD", "--", path])
    if result.returncode != 0:
        return ""
    return result.stdout


def source_diff_suggests_user_facing_change(base: str, source_files: list[str]) -> bool:
    """Heuristic: inspect diffs for signs of user-visible behavior changes."""
    for path in source_files:
        if path.endswith(".pyi"):
            continue
        diff = get_diff_for_file(base, path)
        for line in diff.splitlines():
            for pattern in USER_FACING_DIFF_PATTERNS:
                if pattern.search(line):
                    return True
    return False


def build_checks(
    categories: FileCategories,
    contribution_type: ContributionType,
    file_count: int,
    max_files: int,
    base: str,
    strict: bool,
) -> list[CheckResult]:
    checks: list[CheckResult] = []
    code_without_tests = bool(categories.source) and not categories.test

    if code_without_tests:
        status = Status.FAIL if strict else Status.WARN
        checks.append(
            CheckResult(
                name="tests_for_code_changes",
                status=status,
                message="Code changed but no pandas/tests file changed.",
            )
        )
    elif categories.source and categories.test:
        checks.append(
            CheckResult(
                name="tests_for_code_changes",
                status=Status.PASS,
                message="Source and test files both changed.",
            )
        )

    if contribution_type == ContributionType.DOCS_ONLY:
        checks.append(
            CheckResult(
                name="docs_only_scope",
                status=Status.PASS,
                message="Docs-only change; low risk if scope matches the issue.",
            )
        )

    if contribution_type == ContributionType.TESTS_ONLY:
        scope_status = Status.WARN if file_count > max_files else Status.PASS
        checks.append(
            CheckResult(
                name="tests_only_scope",
                status=scope_status,
                message=(
                    "Tests-only change covers many files; confirm scope is still narrow."
                    if file_count > max_files
                    else "Tests-only change; verify assertions match intended behavior."
                ),
            )
        )

    if categories.risky:
        checks.append(
            CheckResult(
                name="risky_internals",
                status=Status.WARN,
                message=(
                    "Risky internals touched "
                    f"({len(categories.risky)} file(s)): "
                    + ", ".join(categories.risky[:5])
                    + (" ..." if len(categories.risky) > 5 else "")
                    + ". First contributions should avoid these areas unless explicitly scoped."
                ),
            )
        )

    if categories.ci_config:
        checks.append(
            CheckResult(
                name="ci_config_changes",
                status=Status.WARN,
                message="CI/config files changed; DevOps/CI review may be needed.",
            )
        )

    if file_count > max_files:
        checks.append(
            CheckResult(
                name="contribution_scope",
                status=Status.WARN,
                message=(
                    f"Contribution touches {file_count} files (threshold: {max_files}). "
                    "Consider narrowing scope for a first PR."
                ),
            )
        )
    else:
        checks.append(
            CheckResult(
                name="contribution_scope",
                status=Status.PASS,
                message=f"File count ({file_count}) is within the threshold ({max_files}).",
            )
        )

    user_facing = (
        bool(categories.source)
        and not categories.docs
        and source_diff_suggests_user_facing_change(base, categories.source)
    )
    if user_facing:
        checks.append(
            CheckResult(
                name="docs_for_user_facing_changes",
                status=Status.WARN,
                message="Consider whether docs, docstrings, or release notes are needed.",
            )
        )
    elif categories.source and categories.docs:
        checks.append(
            CheckResult(
                name="docs_for_user_facing_changes",
                status=Status.PASS,
                message="Docs changed alongside source files.",
            )
        )

    return checks


def suggest_commands(categories: FileCategories, changed_files: list[str]) -> list[str]:
    commands: list[str] = []

    if categories.test:
        for test_file in categories.test:
            commands.append(f"pytest {test_file}")
    elif categories.source:
        module_hint = categories.source[0]
        commands.append(
            "# No test files changed yet — locate the nearest existing test file, e.g.:"
        )
        commands.append(f"git grep -l \"{PurePosixPath(module_hint).stem}\" pandas/tests/")
        commands.append("# Then add a failing regression test before implementing the fix.")

    if categories.docs or categories.source:
        commands.append("./ci/code_checks.sh docstrings")
        commands.append("./ci/code_checks.sh doctests")
        commands.append("./ci/code_checks.sh code")

    if changed_files:
        file_args = " ".join(changed_files)
        commands.append(f"pre-commit run --files {file_args}")

    return commands


def build_report(base: str, max_files: int, strict: bool) -> tuple[Report | None, str | None]:
    changed_files, error = get_changed_files(base)
    if error:
        return None, error
    if changed_files is None:
        return None, "Unable to read changed files from git."

    if not changed_files:
        return None, None  # signal: no changes

    categories = classify_files(changed_files)
    contribution_type = infer_contribution_type(categories)
    file_count = len(changed_files)
    risk_level, risk_reasons = infer_risk_level(
        categories, contribution_type, file_count, max_files
    )
    checks = build_checks(
        categories, contribution_type, file_count, max_files, base, strict
    )
    commands = suggest_commands(categories, changed_files)

    return Report(
        base=base,
        changed_files=changed_files,
        categories=categories,
        contribution_type=contribution_type,
        risk_level=risk_level,
        risk_reasons=risk_reasons,
        checks=checks,
        suggested_commands=commands,
    ), None


def format_text_report(report: Report) -> str:
    lines: list[str] = []
    lines.append("=" * 60)
    lines.append("PANDAS PR READINESS CHECK")
    lines.append("=" * 60)
    lines.append(f"Base branch: {report.base}")
    lines.append(f"Changed files: {len(report.changed_files)}")
    lines.append("")

    lines.append("Changed files by category")
    lines.append("-" * 40)
    for label, bucket in (
        ("Source", report.categories.source),
        ("Tests", report.categories.test),
        ("Docs", report.categories.docs),
        ("CI/Config", report.categories.ci_config),
        ("Risky internals", report.categories.risky),
        ("Other", report.categories.other),
    ):
        lines.append(f"  {label} ({len(bucket)}):")
        if bucket:
            for path in bucket:
                lines.append(f"    - {path}")
        else:
            lines.append("    (none)")
    lines.append("")

    lines.append(f"Inferred contribution type: {report.contribution_type.value}")
    lines.append(f"Risk level: {report.risk_level.value}")
    if report.risk_reasons:
        lines.append("Risk reasons:")
        for reason in report.risk_reasons:
            lines.append(f"  - {reason}")
    lines.append("")

    lines.append("Checklist")
    lines.append("-" * 40)
    for check in report.checks:
        lines.append(f"  [{check.status.value}] {check.message}")
    lines.append("")

    lines.append("Suggested commands (not run by this checker)")
    lines.append("-" * 40)
    for cmd in report.suggested_commands:
        lines.append(f"  {cmd}")
    lines.append("")
    lines.append(
        "Note: This checker does not prove correctness or CI success. "
        "Run the suggested commands locally before opening a PR."
    )

    return "\n".join(lines)


def report_to_dict(report: Report) -> dict[str, Any]:
    return {
        "base": report.base,
        "changed_files": report.changed_files,
        "categories": {
            "source": report.categories.source,
            "test": report.categories.test,
            "docs": report.categories.docs,
            "ci_config": report.categories.ci_config,
            "risky": report.categories.risky,
            "other": report.categories.other,
        },
        "contribution_type": report.contribution_type.value,
        "risk_level": report.risk_level.value,
        "risk_reasons": report.risk_reasons,
        "checks": [
            {"name": c.name, "status": c.status.value, "message": c.message}
            for c in report.checks
        ],
        "suggested_commands": report.suggested_commands,
        "summary": {
            "failures": len(report.failures),
            "warnings": len(report.warnings),
        },
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check pandas contribution PR readiness against a git base branch.",
    )
    parser.add_argument(
        "--base",
        default=DEFAULT_BASE,
        help=f"Git base ref for diff (default: {DEFAULT_BASE})",
    )
    parser.add_argument(
        "--max-files",
        type=int,
        default=DEFAULT_MAX_FILES,
        help=f"Warn when more than this many files change (default: {DEFAULT_MAX_FILES})",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Also print a machine-readable JSON report after the text output",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat code-without-tests warnings as failures",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    # Verify git is available.
    git_version = run_git(["--version"])
    if git_version.returncode != 0:
        print("Error: git is unavailable or failed to run.", file=sys.stderr)
        return 1

    report, error = build_report(args.base, args.max_files, args.strict)

    if error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    if report is None:
        print("No changed files detected compared to base branch.")
        print(f"  Base: {args.base}")
        print("  Tip: commit your work on the current branch, then re-run this checker.")
        return 0

    text = format_text_report(report)
    print(text)

    if args.json:
        print("\n--- JSON ---")
        print(json.dumps(report_to_dict(report), indent=2))

    has_failures = bool(report.failures)
    return 1 if has_failures else 0


if __name__ == "__main__":
    sys.exit(main())
