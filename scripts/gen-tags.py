#!/usr/bin/env python3
"""prompts/*.md 의 frontmatter tags를 읽어 TAGS.md를 재생성한다."""
import os
import re
from collections import defaultdict

PROMPTS_DIR = "prompts"
OUTPUT = "TAGS.md"


def parse_frontmatter(content):
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return None, None
    fm = match.group(1)

    title_match = re.search(r"^title:\s*(.+)$", fm, re.MULTILINE)
    tags_match = re.search(r"^tags:\s*\[(.+)\]$", fm, re.MULTILINE)

    title = title_match.group(1).strip() if title_match else None
    tags = [t.strip() for t in tags_match.group(1).split(",")] if tags_match else []
    return title, tags


def main():
    tag_map = defaultdict(list)

    for filename in sorted(os.listdir(PROMPTS_DIR)):
        if not filename.endswith(".md"):
            continue
        filepath = f"{PROMPTS_DIR}/{filename}"
        with open(filepath, encoding="utf-8") as f:
            content = f.read()

        title, tags = parse_frontmatter(content)
        if not title or not tags:
            continue

        for tag in tags:
            tag_map[tag].append((title, filepath))

    lines = [
        "# Tag Index",
        "",
        "태그별 프롬프트 목록. 자동 생성 파일 — 직접 수정하지 마세요.",
        "",
    ]
    for tag in sorted(tag_map.keys()):
        lines.append(f"## {tag}")
        for title, filepath in sorted(tag_map[tag]):
            lines.append(f"- [{title}]({filepath})")
        lines.append("")

    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"TAGS.md generated ({len(tag_map)} tags, {sum(len(v) for v in tag_map.values())} entries)")


if __name__ == "__main__":
    main()
