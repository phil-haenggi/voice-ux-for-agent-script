#!/usr/bin/env python3
"""
lint-patterns.py — validates pattern files in references/patterns/ against the
schema defined in references/patterns/_schema.md.

Run:    python3 scripts/lint-patterns.py
Exit:   0 = all valid, 1 = at least one violation

Checks:
1.  Filename matches "<id>-<name>.md"
2.  Frontmatter parses as YAML and includes required fields
3.  category matches the id prefix (A01 → system-instructions, etc.)
4.  severity is one of high / medium / low
5.  applies_to is a non-empty subset of [migrate, optimize]
6.  detection has at least one entry; every regex compiles
7.  couples_with refers only to existing pattern ids
8.  principle_refs / pattern_refs resolve in voice-ux-principles.md /
    telephony-patterns.md (best-effort string match)
9.  Required body sections present
10. No two pattern files share an id
11. README.md table mentions every pattern file (and every pattern id is in
    README.md's index)

Dependencies: Python 3.7+ stdlib only — no third-party libraries.
"""

from __future__ import annotations

import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

CATEGORY_TO_PREFIX = {
    "system-instructions":      "A",
    "welcome-and-static":       "B",
    "display-formatting":       "C",
    "input-collection":         "D",
    "output-presentation":      "E",
    "crisis-and-safety":        "F",
    "latency-masking":          "G",
    "configuration":            "H",
    "variables":                "I",
}
PREFIX_TO_CATEGORY = {v: k for k, v in CATEGORY_TO_PREFIX.items()}

REQUIRED_FRONTMATTER = ["id", "name", "category", "severity", "applies_to", "detection"]
ALLOWED_SEVERITY = {"high", "medium", "low"}
ALLOWED_MODES = {"migrate", "optimize"}

REQUIRED_SECTIONS = [
    "## Why it matters",
    "## Detection",
    "## Chat example (before)",
    "## Voice example (after) — recommended",
    "## Voice example — alternatives",
    "## Where it lives",
]

FILENAME_RE = re.compile(r"^([A-I]\d{2})-([a-z][a-z0-9-]*)\.md$")


@dataclass
class Violation:
    file: str
    rule: str
    detail: str

    def __str__(self) -> str:
        return f"  [{self.rule}] {self.file}: {self.detail}"


@dataclass
class PatternFile:
    path: Path
    file_id: str | None = None
    file_name: str | None = None
    frontmatter: dict | None = None
    body: str | None = None
    violations: list[Violation] = field(default_factory=list)


def parse_frontmatter(text: str) -> tuple[dict, str] | tuple[None, str]:
    """Tiny hand-rolled YAML-subset parser for our frontmatter shape.

    Supports: scalar strings/numbers/booleans, list of inline strings
    [a, b, c], and list of dicts (one per indented block under a key).
    Sufficient for the schema we use; not a general YAML parser.
    """
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return None, text
    raw = text[4:end]
    body = text[end + 5:]

    data: dict = {}
    lines = raw.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            i += 1
            continue
        if line.startswith(" "):
            # belongs to a previous block; handled by the parent.
            i += 1
            continue
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_]*):\s*(.*)$", line)
        if not m:
            i += 1
            continue
        key, value = m.group(1), m.group(2).strip()
        if value == "":
            # block — collect indented lines
            block: list[str] = []
            i += 1
            while i < len(lines) and (lines[i].startswith(" ") or lines[i].strip() == ""):
                if lines[i].strip():
                    block.append(lines[i])
                i += 1
            data[key] = parse_block(block)
        else:
            data[key] = parse_scalar(value)
            i += 1
    return data, body


def parse_scalar(value: str):
    value = value.strip()
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [parse_scalar(p.strip()) for p in inner.split(",")]
    if value.startswith('"') and value.endswith('"'):
        return value[1:-1]
    if value.startswith("'") and value.endswith("'"):
        return value[1:-1]
    if value.lower() in ("true", "false"):
        return value.lower() == "true"
    try:
        if "." in value:
            return float(value)
        return int(value)
    except ValueError:
        pass
    return value


def parse_block(lines: list[str]) -> list:
    """Parse the indented block under a frontmatter key.

    Two shapes we accept:
      - list of inline dicts:
            - regex: '...'
              in: [a, b]
      - list of scalars (rare):
            - foo
            - bar
    """
    items: list = []
    current: dict | None = None
    for line in lines:
        s = line.strip()
        if s.startswith("- "):
            # new entry
            if current is not None:
                items.append(current)
            rest = s[2:].strip()
            m = re.match(r"^([A-Za-z_][A-Za-z0-9_]*):\s*(.*)$", rest)
            if m:
                current = {m.group(1): parse_scalar(m.group(2))}
            else:
                # scalar list element, not a dict
                if current is not None:
                    items.append(current)
                    current = None
                items.append(parse_scalar(rest))
        elif current is not None:
            m = re.match(r"^\s*([A-Za-z_][A-Za-z0-9_]*):\s*(.*)$", line)
            if m:
                current[m.group(1)] = parse_scalar(m.group(2))
    if current is not None:
        items.append(current)
    return items


def lint_file(path: Path, all_ids: set[str]) -> PatternFile:
    pf = PatternFile(path=path)
    name = path.name

    m = FILENAME_RE.match(name)
    if not m:
        pf.violations.append(Violation(name, "filename",
            f"does not match <ID>-<name>.md (e.g. A01-numbered-list-rule.md)"))
        return pf
    pf.file_id = m.group(1)
    pf.file_name = m.group(2)

    text = path.read_text(encoding="utf-8")
    frontmatter, body = parse_frontmatter(text)
    if frontmatter is None:
        pf.violations.append(Violation(name, "frontmatter",
            "missing or malformed frontmatter (expected '---' fenced YAML at top of file)"))
        return pf
    pf.frontmatter = frontmatter
    pf.body = body

    # Required fields
    for field_name in REQUIRED_FRONTMATTER:
        if field_name not in frontmatter:
            pf.violations.append(Violation(name, "frontmatter",
                f"missing required field '{field_name}'"))

    fm_id = frontmatter.get("id")
    if fm_id and fm_id != pf.file_id:
        pf.violations.append(Violation(name, "id-mismatch",
            f"frontmatter id '{fm_id}' does not match filename id '{pf.file_id}'"))

    fm_name = frontmatter.get("name")
    if fm_name and fm_name != pf.file_name:
        pf.violations.append(Violation(name, "name-mismatch",
            f"frontmatter name '{fm_name}' does not match filename name '{pf.file_name}'"))

    # category vs id prefix
    category = frontmatter.get("category")
    if category and pf.file_id:
        prefix = pf.file_id[0]
        expected_category = PREFIX_TO_CATEGORY.get(prefix)
        if expected_category and category != expected_category:
            pf.violations.append(Violation(name, "category",
                f"id prefix '{prefix}' implies category '{expected_category}', got '{category}'"))

    # severity
    severity = frontmatter.get("severity")
    if severity and severity not in ALLOWED_SEVERITY:
        pf.violations.append(Violation(name, "severity",
            f"'{severity}' not in {sorted(ALLOWED_SEVERITY)}"))

    # applies_to
    applies_to = frontmatter.get("applies_to")
    if applies_to is not None:
        if not isinstance(applies_to, list) or not applies_to:
            pf.violations.append(Violation(name, "applies_to",
                "must be non-empty list, e.g. [migrate, optimize]"))
        else:
            bad = [m for m in applies_to if m not in ALLOWED_MODES]
            if bad:
                pf.violations.append(Violation(name, "applies_to",
                    f"unknown mode(s): {bad}; allowed: {sorted(ALLOWED_MODES)}"))

    # detection
    detection = frontmatter.get("detection")
    if detection is not None:
        if not isinstance(detection, list) or not detection:
            pf.violations.append(Violation(name, "detection",
                "must be non-empty list of entries"))
        else:
            for idx, entry in enumerate(detection):
                if not isinstance(entry, dict):
                    pf.violations.append(Violation(name, "detection",
                        f"entry #{idx + 1} is not a dict"))
                    continue
                if not any(k in entry for k in ("regex", "keyword", "structural")):
                    pf.violations.append(Violation(name, "detection",
                        f"entry #{idx + 1} has no regex/keyword/structural"))
                if "regex" in entry:
                    pat = entry["regex"]
                    try:
                        re.compile(pat)
                    except re.error as e:
                        pf.violations.append(Violation(name, "detection",
                            f"entry #{idx + 1} regex does not compile: {e}"))

    # body sections
    if pf.body:
        missing = [s for s in REQUIRED_SECTIONS if s not in pf.body]
        if missing:
            pf.violations.append(Violation(name, "sections",
                f"missing required section heading(s): {missing}"))

    return pf


def lint_cross_refs(patterns: list[PatternFile]) -> list[Violation]:
    """Run cross-file checks: couples_with resolves, no duplicate ids."""
    violations: list[Violation] = []
    valid_ids: set[str] = set()
    seen_ids: dict[str, list[str]] = defaultdict(list)
    for pf in patterns:
        if pf.file_id:
            valid_ids.add(pf.file_id)
            seen_ids[pf.file_id].append(pf.path.name)

    for pf_id, files in seen_ids.items():
        if len(files) > 1:
            violations.append(Violation(",".join(files), "duplicate-id",
                f"id '{pf_id}' appears in multiple files"))

    for pf in patterns:
        if not pf.frontmatter:
            continue
        couples = pf.frontmatter.get("couples_with") or []
        if isinstance(couples, list):
            for ref in couples:
                if isinstance(ref, str) and ref not in valid_ids:
                    violations.append(Violation(pf.path.name, "couples_with",
                        f"unknown pattern id '{ref}'"))

    return violations


def lint_readme_index(patterns_dir: Path, valid_ids: set[str]) -> list[Violation]:
    """README.md should mention every pattern id, and every id should have a file."""
    violations: list[Violation] = []
    readme = patterns_dir / "README.md"
    if not readme.exists():
        violations.append(Violation("README.md", "readme",
            "references/patterns/README.md is missing"))
        return violations
    text = readme.read_text(encoding="utf-8")
    for pf_id in sorted(valid_ids):
        if pf_id not in text:
            violations.append(Violation("README.md", "readme",
                f"id '{pf_id}' has a file but is not mentioned in README.md index"))
    # The reverse check (ids in README that have no file) is fuzzier — IDs
    # appear in tables and prose. Skip for v1 to avoid false positives.
    return violations


def lint_principle_and_pattern_refs(patterns: list[PatternFile], skill_root: Path) -> list[Violation]:
    """Soft check that every principle_refs / pattern_refs resolves in the
    abstract reference docs. Best-effort — just confirms the citation IDs
    appear somewhere in the relevant reference file.
    """
    violations: list[Violation] = []
    principles_path = skill_root / "references" / "voice-ux-principles.md"
    patterns_doc_path = skill_root / "references" / "telephony-patterns.md"
    principles_text = principles_path.read_text(encoding="utf-8") if principles_path.exists() else ""
    patterns_doc_text = patterns_doc_path.read_text(encoding="utf-8") if patterns_doc_path.exists() else ""

    for pf in patterns:
        if not pf.frontmatter:
            continue
        for ref in (pf.frontmatter.get("principle_refs") or []):
            if isinstance(ref, str) and ref not in principles_text:
                violations.append(Violation(pf.path.name, "principle_refs",
                    f"'{ref}' not found in voice-ux-principles.md"))
        for ref in (pf.frontmatter.get("pattern_refs") or []):
            if isinstance(ref, str) and ref not in patterns_doc_text:
                violations.append(Violation(pf.path.name, "pattern_refs",
                    f"'{ref}' not found in telephony-patterns.md"))
    return violations


def main() -> int:
    here = Path(__file__).resolve()
    skill_root = here.parent.parent
    patterns_dir = skill_root / "references" / "patterns"
    if not patterns_dir.exists():
        print(f"ERROR: patterns directory not found at {patterns_dir}", file=sys.stderr)
        return 1

    files = sorted(p for p in patterns_dir.glob("*.md")
                   if p.name != "README.md" and not p.name.startswith("_"))
    if not files:
        print(f"ERROR: no pattern files in {patterns_dir}", file=sys.stderr)
        return 1

    patterns: list[PatternFile] = []
    all_ids: set[str] = set()
    all_violations: list[Violation] = []

    for path in files:
        pf = lint_file(path, all_ids)
        patterns.append(pf)
        all_violations.extend(pf.violations)
        if pf.file_id:
            all_ids.add(pf.file_id)

    all_violations.extend(lint_cross_refs(patterns))
    all_violations.extend(lint_readme_index(patterns_dir, all_ids))
    all_violations.extend(lint_principle_and_pattern_refs(patterns, skill_root))

    total = len(files)
    if all_violations:
        print(f"FAIL: {len(all_violations)} violation(s) across {total} pattern file(s)\n")
        # Group by file for readability
        by_file: dict[str, list[Violation]] = defaultdict(list)
        for v in all_violations:
            by_file[v.file].append(v)
        for fname in sorted(by_file):
            print(f"{fname}:")
            for v in by_file[fname]:
                print(str(v))
            print()
        return 1
    print(f"OK: {total} pattern file(s) valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
