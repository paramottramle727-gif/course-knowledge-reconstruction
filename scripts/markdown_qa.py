#!/usr/bin/env python3
"""Read-only heuristic QA for Markdown course notes.

Checks deterministic or mechanically observable issues only. It never edits files
and does not assess academic correctness.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


@dataclass
class Finding:
    file: str
    line: int
    code: str
    message: str


def escaped(text: str, index: int) -> bool:
    backslashes = 0
    index -= 1
    while index >= 0 and text[index] == "\\":
        backslashes += 1
        index -= 1
    return backslashes % 2 == 1


def count_unescaped(text: str, token: str) -> int:
    count = 0
    start = 0
    while True:
        index = text.find(token, start)
        if index < 0:
            return count
        if not escaped(text, index):
            count += 1
        start = index + len(token)


def table_columns(line: str) -> int:
    stripped = line.strip().strip("|")
    return len(re.split(r"(?<!\\)\|", stripped))


def whole_line_bold(text: str) -> bool:
    """Flag long lines whose words are all bold, not separated phrase anchors.

    Inline code and escaped characters may contain literal emphasis markers.
    This remains a conservative heuristic, not a full Markdown parser.
    """
    if len(text) <= 40:
        return False
    masked = re.sub(r"(`+).*?\1", lambda match: "x" * len(match[0]), text)
    spans = [match for match in re.finditer(r"\*\*(?:\\.|(?!\*\*).)+\*\*", masked)
             if not escaped(masked, match.start())]
    if not spans:
        return False
    outside: list[str] = []
    end = 0
    for match in spans:
        outside.append(masked[end:match.start()])
        end = match.end()
    outside.append(masked[end:])
    return re.fullmatch(r"[\s。！？.!?，、；：,:;]*", "".join(outside)) is not None


class ImageTagParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.images: list[tuple[int, str, bool]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() == "img":
            source = dict(attrs).get("src") or ""
            self.images.append((self.getpos()[0], source, False))


def inspect_image_links(path: Path, text: str, vault_root: Path | None) -> list[Finding]:
    """Check common local image embeds; do not infer visual or semantic quality.

    Supports inline Markdown images, HTML img tags and Obsidian image embeds.
    Remote/data images, inline SVG and renderer-dependent features need visual QA.
    """
    text = re.sub(r"<!--[\s\S]*?-->", lambda match: "\n" * match[0].count("\n"), text)
    parser = ImageTagParser()
    parser.feed(text)
    references = parser.images
    markdown_pattern = r"!\[(?:\\.|[^\]\\])*\]\(\s*(?:<([^>\r\n]*)>|((?:\\.|[^\s()]|\([^()\r\n]*\))*))(?=\s|\))"
    for match in re.finditer(markdown_pattern, text):
        source = match[1] if match[1] is not None else (match[2] or "")
        references.append((text.count("\n", 0, match.start()) + 1, source, False))
    image_extensions = {".svg", ".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp", ".avif", ".tif", ".tiff", ".pdf"}
    for match in re.finditer(r"!\[\[([^\]\r\n]+)\]\]", text):
        source = match[1].split("|", 1)[0]
        if Path(source.split("#", 1)[0]).suffix.lower() in image_extensions:
            references.append((text.count("\n", 0, match.start()) + 1, source, True))

    findings: list[Finding] = []
    for line, raw_source, is_obsidian in references:
        source = unescape(raw_source.strip())
        if not source:
            findings.append(Finding(str(path), line, "image-empty", "图片引用为空，未提供实际图片资源。"))
            continue
        if source.lower().startswith(("http://", "https://", "data:", "//", "#")):
            continue
        if source.lower().startswith("file:"):
            parsed = urlsplit(source)
            source = ("//" + parsed.netloc if parsed.netloc else "") + parsed.path
            if re.match(r"^/[A-Za-z]:/", source):
                source = source[1:]
        elif re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", source) and not re.match(r"^[A-Za-z]:[\\/]", source):
            continue
        source = unquote(source.split("#", 1)[0].split("?", 1)[0])
        source = re.sub(r"\\([\\ ()<>])", r"\1", source)
        candidates = [path.parent / source]
        if is_obsidian and vault_root is not None:
            candidates.append(vault_root / source.lstrip("/"))
        try:
            resolved = next((candidate for candidate in candidates if candidate.is_file()), None)
            if resolved is None:
                code = "image-unresolved" if is_obsidian else "image-missing"
                message = "嵌入图片未在笔记相对路径或指定 Vault 根路径解析；请核对 Obsidian 实际解析。" if is_obsidian else "引用的本地图片文件不存在。"
                findings.append(Finding(str(path), line, code, message))
            elif resolved.stat().st_size == 0:
                findings.append(Finding(str(path), line, "image-empty-file", "引用的本地图片文件为空。"))
        except (OSError, ValueError):
            findings.append(Finding(str(path), line, "image-resource-error", "无法检查本地图片资源，请核对路径与访问状态。"))
    return findings


def inspect_file(path: Path, vault_root: Path | None = None) -> list[Finding]:
    findings: list[Finding] = []
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        findings.append(Finding(str(path), 1, "encoding", "文件不是有效 UTF-8。"))
        return findings

    lines = text.splitlines()
    in_fence = False
    fence_start = 0
    previous_heading = 0
    display_dollar_start = 0
    display_bracket_start = 0
    table_expected: int | None = None
    image_lines: list[str] = []

    for number, raw in enumerate(lines, start=1):
        stripped = raw.strip()

        if re.match(r"^(```|~~~)", stripped):
            image_lines.append("")
            if not in_fence:
                in_fence = True
                fence_start = number
            else:
                in_fence = False
            continue
        if in_fence:
            image_lines.append("")
            continue
        image_lines.append(re.sub(r"(`+).*?\1", "", raw))

        heading = re.match(r"^(#{1,6})\s+\S", raw)
        if heading:
            level = len(heading.group(1))
            if previous_heading and level > previous_heading + 1:
                findings.append(
                    Finding(str(path), number, "heading-jump", f"标题从 H{previous_heading} 跳到 H{level}。")
                )
            previous_heading = level

        if whole_line_bold(stripped):
            findings.append(Finding(str(path), number, "whole-line-bold", "疑似整句或整段加粗。"))

        if count_unescaped(raw, "$$") % 2 == 1:
            if display_dollar_start:
                display_dollar_start = 0
            else:
                display_dollar_start = number

        opens = count_unescaped(raw, r"\[")
        closes = count_unescaped(raw, r"\]")
        if opens != closes:
            if opens > closes and not display_bracket_start:
                display_bracket_start = number
            elif closes > opens and display_bracket_start:
                display_bracket_start = 0

        if count_unescaped(raw, r"\(") != count_unescaped(raw, r"\)"):
            findings.append(Finding(str(path), number, "inline-math", r"本行的 \( 与 \) 数量不匹配。"))

        if stripped.startswith("|") and stripped.endswith("|"):
            columns = table_columns(stripped)
            if table_expected is None:
                table_expected = columns
                if columns > 7:
                    findings.append(Finding(str(path), number, "wide-table", f"表格有 {columns} 列，可能过宽。"))
            elif columns != table_expected:
                findings.append(
                    Finding(str(path), number, "table-columns", f"表格列数为 {columns}，预期 {table_expected}。")
                )
        else:
            table_expected = None

        without_inline_code = re.sub(r"`[^`]*`", "", raw)
        has_math_marker = any(marker in without_inline_code for marker in ("$", r"\(", r"\)", r"\[", r"\]"))
        if not has_math_marker and not display_dollar_start and not display_bracket_start:
            if re.search(r"\\(?:frac|sqrt|sum|prod|int|lim|alpha|beta|gamma|theta|mu|sigma|begin|end)\b", without_inline_code):
                findings.append(Finding(str(path), number, "bare-latex", "疑似在数学定界符外使用 LaTeX 命令。"))

    if in_fence:
        findings.append(Finding(str(path), fence_start, "code-fence", "代码围栏未闭合。"))
    if display_dollar_start:
        findings.append(Finding(str(path), display_dollar_start, "display-math", "$$ 数学块未闭合。"))
    if display_bracket_start:
        findings.append(Finding(str(path), display_bracket_start, "display-math", r"\[ 数学块未闭合。"))

    findings.extend(inspect_image_links(path, "\n".join(image_lines), vault_root))
    return findings


def markdown_files(inputs: list[str]) -> list[Path]:
    files: list[Path] = []
    for item in inputs:
        path = Path(item).expanduser()
        if path.is_file() and path.suffix.lower() in {".md", ".markdown"}:
            files.append(path.resolve())
        elif path.is_dir():
            files.extend(p.resolve() for p in path.rglob("*.md") if p.is_file())
        else:
            print(f"跳过不存在或非 Markdown 的路径：{path}", file=sys.stderr)
    return sorted(set(files), key=lambda p: str(p).lower())


def main() -> int:
    parser = argparse.ArgumentParser(description="只读检查 Markdown 格式与常见本地图片引用；不判断漏画、图文语义或组合图必要性。")
    parser.add_argument("paths", nargs="+", help="Markdown 文件或目录")
    parser.add_argument("--json", action="store_true", help="以 JSON 输出结果")
    parser.add_argument("--vault-root", type=Path, help="可选：仅用于精确解析 Obsidian 嵌入路径，不递归搜索 Vault")
    args = parser.parse_args()

    files = markdown_files(args.paths)
    findings = [finding for path in files for finding in inspect_file(path, args.vault_root)]

    if args.json:
        print(json.dumps({"files_checked": len(files), "findings": [asdict(f) for f in findings]}, ensure_ascii=False, indent=2))
    else:
        print(f"Checked {len(files)} Markdown file(s); found {len(findings)} issue(s).")
        for finding in findings:
            print(f"{finding.file}:{finding.line}: [{finding.code}] {finding.message}")

    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
