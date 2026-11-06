#!/usr/bin/env python3
"""옵시디안 볼트의 표준 틀을 배포용 사본(skills/project-setup/standard/)으로 만든다.

개인 경로·프로젝트 이름·사람 이름·변경 이력을 걷어내고, 남은 것이 있으면 실패한다.
사용: python3 scripts/build_standard.py [원본 폴더]
원본 기본값: $OBSIDIAN_VAULT_PATH/30 Areas/Development Standard
"""

import json
import os
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "skills" / "project-setup" / "standard"
FILES = ["프로젝트 표준 틀.md", "개발 규약.md"]
DIRS = ["개발 규약", "양식"]

# 개인 경로·이름을 바꾸는 규칙은 저장소에 넣지 않는다(.gitignore). 형식:
# {"drop_sections": {"파일명": ["## 제목 접두어"]}, "replace": [["정규식", "값"]], "forbidden": "정규식"}
RULES = Path(__file__).with_name("build_rules.local.json")
GENERIC_FORBIDDEN = r"/Volumes/|/Users/|/home/[a-z]"


def load_rules() -> tuple[dict, list, re.Pattern]:
    rules = json.loads(RULES.read_text(encoding="utf-8")) if RULES.is_file() else {}
    forbidden = "|".join(filter(None, [GENERIC_FORBIDDEN, rules.get("forbidden", "")]))
    return rules.get("drop_sections", {}), rules.get("replace", []), re.compile(forbidden)


DROP_SECTIONS, REPLACE, FORBIDDEN = load_rules()


def drop_sections(text: str, heads: list[str]) -> str:
    out, skip_level = [], 0
    for line in text.split("\n"):
        m = re.match(r"^(#+) ", line)
        if m and skip_level and len(m.group(1)) <= skip_level:
            skip_level = 0
        if any(line.startswith(h) for h in heads):
            skip_level = len(line.split(" ")[0])
            continue
        if not skip_level:
            out.append(line)
    return "\n".join(out).rstrip() + "\n"


def clean(name: str, text: str) -> str:
    text = drop_sections(text, DROP_SECTIONS.get(name, []))
    if "## 변경 이력" in DROP_SECTIONS.get(name, []):
        text += "\n## 변경 이력\n\n배포본은 변경 이력을 싣지 않는다. 버전은 frontmatter `version`과 플러그인 버전을 본다.\n"
    for pattern, repl in REPLACE:
        text = re.sub(pattern, repl, text, flags=re.M)
    return text


def sync_version(src: Path) -> None:
    """틀 frontmatter version(v0.13)을 플러그인 버전(0.13.0)으로 맞춘다."""
    m = re.search(r"^version: v(\d+)\.(\d+)", (src / "프로젝트 표준 틀.md").read_text(encoding="utf-8"), re.M)
    if not m:
        return
    version = f"{m.group(1)}.{m.group(2)}.0"
    for name in ("plugin.json", "marketplace.json"):
        path = ROOT / ".claude-plugin" / name
        text = path.read_text(encoding="utf-8")
        path.write_text(re.sub(r'"version": "[^"]*"', f'"version": "{version}"', text), encoding="utf-8")


def main() -> int:
    vault = os.environ.get("OBSIDIAN_VAULT_PATH", "")
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(vault) / "30 Areas" / "Development Standard"
    if not (src / "프로젝트 표준 틀.md").is_file():
        print(f"원본을 찾을 수 없음: {src}", file=sys.stderr)
        return 1
    if not RULES.is_file() and "Development Standard" in str(src):
        print(f"{RULES.name} 없이 볼트 원본을 빌드하면 개인 정보가 걸러지지 않음", file=sys.stderr)
        return 1
    sources = [src / f for f in FILES] + sorted(p for d in DIRS for p in (src / d).glob("*.md"))
    if OUT.exists():
        shutil.rmtree(OUT)
    leaks = []
    for path in sources:
        rel = path.relative_to(src)
        text = clean(path.name, path.read_text(encoding="utf-8"))
        for no, line in enumerate(text.split("\n"), 1):
            if FORBIDDEN.search(line):
                leaks.append(f"{rel}:{no}: {line[:120]}")
        dest = OUT / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(text, encoding="utf-8")
    if leaks:
        print("개인 정보가 남음 — REPLACE를 고친 뒤 다시 빌드:", *leaks, sep="\n", file=sys.stderr)
        return 1
    sync_version(src)
    print(f"{len(sources)}개 문서 → {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
