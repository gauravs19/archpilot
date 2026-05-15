#!/usr/bin/env python3
import os
import sys
import re
import argparse

def init_project(target_dir):
    """Scaffolds the Archpilot SDD directory structure."""
    specs_dir = os.path.join(target_dir, ".specs")
    if not os.path.exists(specs_dir):
        os.makedirs(specs_dir)
    
    files = {
        "constitution.md": "# Project Constitution\n\n## Tech Stack\n- \n\n## Non-Negotiables\n- \n",
        "requirements.md": "# Requirements\n\n## Functional (EARS)\n- \n\n## RTM (Requirement Traceability Matrix)\n| ID | Requirement | Status | Test ID |\n|---|---|---|---|\n",
        "design.md": "# Solution Design\n\n## Architecture\n\n## Data Models\n\n## Error Handling\n",
        "tasks.md": "# Implementation Tasks\n\n## T-01: [Task Name]\n- **Acceptance Criteria**: \n"
    }

    for filename, content in files.items():
        filepath = os.path.join(specs_dir, filename)
        if not os.path.exists(filepath):
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"✅ Created {filepath}")
        else:
            print(f"⏭️  Skipped {filepath} (Already exists)")
            
    print("\n🚀 Archpilot project initialized! Navigate to .specs/ to begin.")

def lint_specs(target_dir):
    """Lints the markdown files to enforce Enterprise standards."""
    specs_dir = os.path.join(target_dir, ".specs")
    if not os.path.exists(specs_dir):
        print(f"❌ Error: {specs_dir} does not exist. Run 'init' first.")
        sys.exit(1)

    errors = 0
    warnings = 0

    print("🔍 Running Archpilot Linter...")

    # 1. Check for TODOs / TBDs
    for filename in os.listdir(specs_dir):
        if not filename.endswith(".md"):
            continue
        filepath = os.path.join(specs_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                if re.search(r'\b(TODO|TBD|FIXME)\b', line, re.IGNORECASE):
                    print(f"❌ [Error] {filename}:{i+1} Unresolved ambiguity: '{line.strip()}'")
                    errors += 1

    # 2. Enforce Requirements RTM
    req_file = os.path.join(specs_dir, "requirements.md")
    if os.path.exists(req_file):
        with open(req_file, "r", encoding="utf-8") as f:
            content = f.read()
            if "Requirement Traceability Matrix" not in content and "RTM" not in content:
                print(f"❌ [Error] requirements.md is missing the Requirement Traceability Matrix (RTM).")
                errors += 1

    # 3. Enforce Design Error Handling
    des_file = os.path.join(specs_dir, "design.md")
    if os.path.exists(des_file):
        with open(des_file, "r", encoding="utf-8") as f:
            content = f.read()
            if "Error Handling" not in content and "Failure Modes" not in content:
                print(f"⚠️  [Warning] design.md is missing an 'Error Handling' section.")
                warnings += 1

    print("\n" + "=" * 40)
    if errors > 0:
        print(f"💥 LINT FAILED: {errors} Errors, {warnings} Warnings.")
        print("Block PR from merging.")
        sys.exit(1)
    else:
        print(f"✅ LINT PASSED: {errors} Errors, {warnings} Warnings.")
        print("Architecture Specs meet Enterprise Standards.")
        sys.exit(0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Archpilot CLI - Architecture Compliance as Code")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # INIT Command
    init_parser = subparsers.add_parser("init", help="Initialize Archpilot in the current directory")
    init_parser.add_argument("--dir", default=".", help="Target directory")

    # LINT Command
    lint_parser = subparsers.add_parser("lint", help="Lint the .specs/ directory for standard violations")
    lint_parser.add_argument("--dir", default=".", help="Target directory containing .specs/")

    args = parser.parse_args()

    if args.command == "init":
        init_project(args.dir)
    elif args.command == "lint":
        lint_specs(args.dir)
    else:
        parser.print_help()
