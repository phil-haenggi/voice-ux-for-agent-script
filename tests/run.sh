#!/usr/bin/env bash
# tests/run.sh — surface every fixture as an input/expected/notes triple for human review.
#
# Why this isn't an automated diff:
#   The skill's rewrite step is LLM-driven, not deterministic. Two runs against
#   the same input produce semantically equivalent but lexically different output
#   ("Tuesday the fifth at five-thirty" vs "Tuesday at five-thirty in the
#   afternoon"). A literal diff would fail constantly and prove nothing.
#
# What this script does instead:
#   - Lists every fixture
#   - For each, prints the input, the expected output, and the notes
#   - Surfaces them so a reviewer can run the skill manually against the input
#     and compare the result against expected by eye (or against a saved
#     "produced" output from a prior run).
#
# Usage:
#   bash tests/run.sh                  # list all fixtures
#   bash tests/run.sh 01-numbered-list # show one fixture
#   bash tests/run.sh --check          # placeholder for future automated check
#
# When the skill grows a deterministic codegen step (vs. LLM rewrite), this
# script becomes a real test runner. Today it's the scaffolding.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FIXTURES_DIR="$SCRIPT_DIR/fixtures"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

if [[ ! -d "$FIXTURES_DIR" ]]; then
    echo "ERROR: fixtures directory not found at $FIXTURES_DIR" >&2
    exit 1
fi

show_fixture() {
    local fixture_dir="$1"
    local name
    name="$(basename "$fixture_dir")"

    echo
    echo "=========================================================================="
    echo "Fixture: $name"
    echo "=========================================================================="
    echo

    if [[ ! -f "$fixture_dir/input.agent" ]]; then
        echo "  WARN: input.agent missing"
    else
        echo "----- input.agent -----"
        cat "$fixture_dir/input.agent"
        echo
    fi

    if [[ ! -f "$fixture_dir/expected-output.agent" ]]; then
        echo "  WARN: expected-output.agent missing"
    else
        echo "----- expected-output.agent -----"
        cat "$fixture_dir/expected-output.agent"
        echo
    fi

    if [[ ! -f "$fixture_dir/notes.md" ]]; then
        echo "  WARN: notes.md missing"
    else
        echo "----- notes.md -----"
        cat "$fixture_dir/notes.md"
        echo
    fi
}

run_check_mode() {
    # Placeholder for a future automated check. Right now we only verify each
    # fixture has the three required files; behavioral checks are manual.
    local missing=0
    local total=0
    for fixture_dir in "$FIXTURES_DIR"/*/; do
        total=$((total + 1))
        local name
        name="$(basename "$fixture_dir")"
        for required in input.agent expected-output.agent notes.md; do
            if [[ ! -f "$fixture_dir/$required" ]]; then
                echo "MISSING: $name/$required"
                missing=$((missing + 1))
            fi
        done
    done
    if [[ "$missing" -gt 0 ]]; then
        echo
        echo "FAIL: $missing missing files across $total fixtures"
        exit 1
    fi
    echo "OK: $total fixtures structurally valid (input.agent + expected-output.agent + notes.md present)"
}

case "${1:-}" in
    --check|-c)
        run_check_mode
        ;;
    "")
        echo "Fixtures in $FIXTURES_DIR:"
        for fixture_dir in "$FIXTURES_DIR"/*/; do
            echo "  $(basename "$fixture_dir")"
        done
        echo
        echo "Usage: bash tests/run.sh <fixture-name>   # show one"
        echo "       bash tests/run.sh --check          # structural check"
        ;;
    *)
        target_dir="$FIXTURES_DIR/$1"
        if [[ ! -d "$target_dir" ]]; then
            echo "ERROR: fixture '$1' not found at $target_dir" >&2
            echo "Available:"
            for fixture_dir in "$FIXTURES_DIR"/*/; do
                echo "  $(basename "$fixture_dir")"
            done
            exit 1
        fi
        show_fixture "$target_dir"
        ;;
esac
