#!/usr/bin/env python3
import argparse
import sys
import re
import os
from datetime import datetime

LEVELS = {"debug": 0, "info": 1, "warn": 2, "warning": 2, "error": 3, "fatal": 4, "critical": 4}

def parse_level(line):
    for lvl in ["DEBUG", "INFO", "WARN", "WARNING", "ERROR", "FATAL", "CRITICAL"]:
        if lvl in line.upper():
            return lvl.lower().replace("warning", "warn")
    return None

def cmd_tail(args):
    path = args.file
    n = args.lines
    with open(path) as f:
        lines = f.readlines()
    for line in lines[-n:]:
        print(line, end="")

def cmd_filter(args):
    path = args.file
    min_level = LEVELS.get(args.level.lower(), 0)
    with open(path) as f:
        for line in f:
            lvl = parse_level(line)
            if lvl and LEVELS.get(lvl, 0) >= min_level:
                print(line, end="")

def cmd_search(args):
    path = args.file
    pattern = re.compile(args.pattern, re.IGNORECASE)
    with open(path) as f:
        for i, line in enumerate(f, 1):
            if pattern.search(line):
                print(f"{i}: {line}", end="")

def cmd_count(args):
    path = args.file
    counts = {}
    with open(path) as f:
        for line in f:
            lvl = parse_level(line)
            if lvl:
                counts[lvl] = counts.get(lvl, 0) + 1
    for lvl in ["debug", "info", "warn", "error", "fatal"]:
        if lvl in counts:
            print(f"{lvl}: {counts[lvl]}")

def cmd_stats(args):
    path = args.file
    total = 0
    levels = {}
    with open(path) as f:
        for line in f:
            total += 1
            lvl = parse_level(line)
            if lvl:
                levels[lvl] = levels.get(lvl, 0) + 1
    print(f"total lines: {total}")
    for lvl, count in sorted(levels.items()):
        pct = (count / total * 100) if total else 0
        print(f"  {lvl}: {count} ({pct:.1f}%)")

def main():
    parser = argparse.ArgumentParser(prog="logx", description="Analyze logs from your terminal. Zero dependencies.")
    sub = parser.add_subparsers(dest="command")

    p_tail = sub.add_parser("tail", help="show last N lines")
    p_tail.add_argument("file", help="log file")
    p_tail.add_argument("-n", "--lines", type=int, default=10, help="number of lines")
    p_tail.set_defaults(func=cmd_tail)

    p_filter = sub.add_parser("filter", help="filter by log level")
    p_filter.add_argument("file", help="log file")
    p_filter.add_argument("--level", default="info", help="minimum level (debug/info/warn/error/fatal)")
    p_filter.set_defaults(func=cmd_filter)

    p_search = sub.add_parser("search", help="search for pattern")
    p_search.add_argument("file", help="log file")
    p_search.add_argument("pattern", help="regex pattern")
    p_search.set_defaults(func=cmd_search)

    p_count = sub.add_parser("count", help="count by level")
    p_count.add_argument("file", help="log file")
    p_count.set_defaults(func=cmd_count)

    p_stats = sub.add_parser("stats", help="show statistics")
    p_stats.add_argument("file", help="log file")
    p_stats.set_defaults(func=cmd_stats)

    args = parser.parse_args()
    if not args.command:
        if len(sys.argv) > 1 and not sys.argv[1].startswith("-"):
            args.command = "tail"
            args.file = sys.argv[1]
            args.lines = 10
            cmd_tail(args)
            return
        parser.print_help()
        sys.exit(1)
    args.func(args)

if __name__ == "__main__":
    main()
