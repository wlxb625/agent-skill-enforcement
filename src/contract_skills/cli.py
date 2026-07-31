from __future__ import annotations

import argparse
import json
import sys

from .validator import inspect_package, validate_package


def main() -> int:
    parser = argparse.ArgumentParser(prog="contract-skill")
    sub = parser.add_subparsers(dest="command", required=True)

    validate = sub.add_parser("validate", help="Validate a Contract Skill package")
    validate.add_argument("package")
    validate.add_argument("--json", action="store_true", dest="as_json")

    inspect = sub.add_parser("inspect", help="Print a contract summary")
    inspect.add_argument("package")

    args = parser.parse_args()

    if args.command == "validate":
        report = validate_package(args.package)
        if args.as_json:
            print(json.dumps(report.as_dict(), ensure_ascii=False, indent=2))
        else:
            state = "VALID" if report.valid else "INVALID"
            print(f"[{state}] {report.package}")
            for finding in report.findings:
                where = f" ({finding.path})" if finding.path else ""
                print(f"- {finding.level.upper()} {finding.code}{where}: {finding.message}")
            if report.summary:
                print(json.dumps(report.summary, ensure_ascii=False, indent=2))
        return 0 if report.valid else 1

    if args.command == "inspect":
        print(json.dumps(inspect_package(args.package), ensure_ascii=False, indent=2))
        return 0

    return 2


if __name__ == "__main__":
    sys.exit(main())
