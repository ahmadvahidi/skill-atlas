#!/usr/bin/env bash
# Install one skill from upstream ECC (github.com/affaan-m/ECC) into a harness skills directory.
#
#   ./install-skill.sh python-testing                    # -> ~/.claude/skills/python-testing
#   ./install-skill.sh postgres-patterns --dest ~/.codex/skills
#   ./install-skill.sh --list                            # every skill name upstream
#
# Sparse clone: only the requested skill directory is fetched, not the 111 MB tree.
set -euo pipefail

UPSTREAM="https://github.com/affaan-m/ECC.git"
DEST="${HOME}/.claude/skills"
LIST=0
NAME=""

usage() { sed -n '2,9p' "$0" | sed 's/^# \{0,1\}//'; exit 1; }

while [ $# -gt 0 ]; do
  case "$1" in
    --list) LIST=1; shift ;;
    --dest) DEST="${2:-}"; shift 2 ;;
    -h|--help) usage ;;
    -*) echo "unknown option: $1" >&2; usage ;;
    *) NAME="$1"; shift ;;
  esac
done

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

clone_sparse() { # $1 = sparse path
  git clone -q --depth 1 --filter=blob:none --sparse "$UPSTREAM" "$TMP/ecc"
  git -C "$TMP/ecc" sparse-checkout set "$1" >/dev/null 2>&1
}

if [ "$LIST" = "1" ]; then
  clone_sparse skills
  ls "$TMP/ecc/skills"
  exit 0
fi

[ -n "$NAME" ] || usage
echo "› fetching skills/$NAME from upstream"
clone_sparse "skills/$NAME"

if [ ! -d "$TMP/ecc/skills/$NAME" ]; then
  echo "✗ no such skill: $NAME (try --list)" >&2
  exit 1
fi

mkdir -p "$DEST"
if [ -e "$DEST/$NAME" ]; then
  echo "! $DEST/$NAME already exists — not overwriting" >&2
  exit 1
fi

cp -R "$TMP/ecc/skills/$NAME" "$DEST/$NAME"
echo "✓ $DEST/$NAME"
echo "  MIT · upstream: github.com/affaan-m/ECC (keep the attribution)"
