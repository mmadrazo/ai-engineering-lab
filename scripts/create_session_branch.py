#!/usr/bin/env python3
"""Create Git branches for session milestones."""

from __future__ import annotations

import argparse
import subprocess
import sys

VALID_PHASES = ("pre", "session", "post")


def run_git_command(args: list[str]) -> None:
    completed = subprocess.run(
        ["git", *args],
        check=False,
        text=True,
        capture_output=True,
    )
    if completed.returncode != 0:
        stderr = completed.stderr.strip() or "Unknown git error."
        raise SystemExit(stderr)


def branch_name(phase: str, number: int) -> str:
    return f"{phase}-session-{number}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a session branch like pre-session-1 or session-2."
    )
    parser.add_argument(
        "--phase",
        choices=VALID_PHASES,
        required=True,
        help="Branch phase: pre, session or post.",
    )
    parser.add_argument(
        "--number",
        type=int,
        required=True,
        help="Session number, for example 1 or 2.",
    )
    parser.add_argument(
        "--base",
        default="main",
        help="Base ref used to create the branch. Defaults to main.",
    )
    parser.add_argument(
        "--checkout",
        action="store_true",
        help="Checkout the branch after creating it.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.number < 1:
        raise SystemExit("--number must be greater than 0.")

    target_branch = branch_name(args.phase, args.number)
    run_git_command(["rev-parse", "--verify", args.base])
    run_git_command(["branch", target_branch, args.base])

    if args.checkout:
        run_git_command(["checkout", target_branch])

    action = "created and checked out" if args.checkout else "created"
    print(f"Branch {target_branch} {action} from {args.base}.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(130)
