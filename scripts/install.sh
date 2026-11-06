#!/usr/bin/env bash
# project-setup 스킬(표준 틀 사본 포함)을 설치한다. 플러그인 없이 쓰는 경우용.
# 사용: scripts/install.sh [--codex] [--vault] [--force]
#   기본       ~/.claude/skills/project-setup 에 복사
#   --codex    ${AGENT_SKILLS_HOME:-~/.agents/skills}/project-setup 에도 복사
#   --vault    $OBSIDIAN_VAULT_PATH/30 Areas/Development Standard/ 에 표준 틀 복사(있는 파일은 덮어쓰지 않음)
#   --force    이미 설치된 스킬 폴더를 바꿈
set -euo pipefail
here="$(cd "$(dirname "$0")/.." && pwd)"
src="$here/skills/project-setup"
dests=("$HOME/.claude/skills") vault=0 force=0
for arg in "$@"; do
  case "$arg" in
    --codex) dests+=("${AGENT_SKILLS_HOME:-$HOME/.agents/skills}") ;;
    --vault) vault=1 ;;
    --force) force=1 ;;
    *) echo "모르는 옵션: $arg" >&2; exit 2 ;;
  esac
done
for d in "${dests[@]}"; do
  target="$d/project-setup"
  if [ -e "$target" ] && [ "$force" -ne 1 ]; then
    echo "이미 있음: $target (바꾸려면 --force)" >&2; exit 1
  fi
  mkdir -p "$d"; rm -rf "$target"; cp -R "$src" "$target"
  echo "설치: $target"
done
if [ "$vault" -eq 1 ]; then
  : "${OBSIDIAN_VAULT_PATH:?--vault 에는 OBSIDIAN_VAULT_PATH 가 필요}"
  vt="$OBSIDIAN_VAULT_PATH/30 Areas/Development Standard"
  mkdir -p "$vt"
  # 볼트에서 고친 틀을 지키려고 있는 파일은 건너뛴다
  (cd "$src/standard" && find . -type f -name '*.md' | while read -r f; do
    if [ -e "$vt/$f" ]; then echo "건너뜀(있음): $f"; else mkdir -p "$vt/$(dirname "$f")"; cp "$f" "$vt/$f"; fi
  done)
  echo "표준 틀: $vt"
fi
