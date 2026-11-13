"""Regression checks for observable Markdown and local image failures."""

from pathlib import Path
import sys
import tempfile
import unittest

sys.dont_write_bytecode = True
from markdown_qa import inspect_file


class ImageReferenceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.workspace = tempfile.TemporaryDirectory()
        self.addCleanup(self.workspace.cleanup)
        self.root = Path(self.workspace.name)
        self.note = self.root / "note.md"
        for name in ("图.svg", "space name.svg", "curve(test).svg"):
            (self.root / name).write_text('<svg xmlns="http://www.w3.org/2000/svg"/>', encoding="utf-8")

    def codes(self, text: str, vault_root: Path | None = None) -> list[str]:
        self.note.write_text(text, encoding="utf-8")
        return [finding.code for finding in inspect_file(self.note, vault_root)]

    def test_markdown_destinations_and_titles(self) -> None:
        self.assertEqual(self.codes('![图](图.svg)\n![图](<space name.svg> "标题")\n![图](curve(test).svg)'), [])

    def test_missing_file_has_source_line(self) -> None:
        self.note.write_text("解释\n\n![图](missing.svg)\n", encoding="utf-8")
        findings = inspect_file(self.note)
        self.assertEqual([(finding.code, finding.line) for finding in findings], [("image-missing", 3)])

    def test_empty_reference_and_empty_file(self) -> None:
        (self.root / "empty.svg").touch()
        self.assertEqual(self.codes("![图]()\n![图](empty.svg)"), ["image-empty", "image-empty-file"])

    def test_html_image_and_empty_source(self) -> None:
        self.assertEqual(self.codes('<img src="space name.svg">'), [])
        self.assertEqual(self.codes('<img src="missing.svg"/>\n<img alt="图">'), ["image-missing", "image-empty"])

    def test_obsidian_root_and_alias(self) -> None:
        self.note = self.root / "notes" / "note.md"
        self.note.parent.mkdir()
        self.assertEqual(self.codes("![[图.svg#section|400]]", self.root), [])
        self.assertEqual(self.codes("![[missing.svg]]", self.root), ["image-unresolved"])
        self.assertEqual(self.codes("![[other-note]]"), [])

    def test_remote_embedded_and_inline_svg_not_claimed_checked(self) -> None:
        self.assertEqual(self.codes('![图](https://example.test/image.svg)\n<img src="data:image/svg+xml,svg">\n<svg></svg>'), [])

    def test_urlencoded_and_file_uri(self) -> None:
        self.assertEqual(self.codes(f'![图](space%20name.svg)\n<img src="{(self.root / "图.svg").as_uri()}">'), [])

    def test_invalid_path_reports_failure_without_crashing(self) -> None:
        self.assertTrue(self.codes("![图](bad%00name.svg)"))

    def test_examples_in_code_and_comments_are_not_resources(self) -> None:
        self.assertEqual(self.codes('```markdown\n![示例](missing.svg)\n```\n`![示例](missing.svg)`\n<!-- ![示例](missing.svg) -->'), [])

    def test_existing_math_checks_still_work(self) -> None:
        self.assertIn("display-math", self.codes("$$\nx = 1\n"))


class BoldSpanTests(unittest.TestCase):
    def setUp(self) -> None:
        self.workspace = tempfile.TemporaryDirectory()
        self.addCleanup(self.workspace.cleanup)
        self.note = Path(self.workspace.name) / "note.md"

    def bold_findings(self, text: str) -> list[tuple[str, int]]:
        self.note.write_text(text, encoding="utf-8")
        return [(finding.code, finding.line) for finding in inspect_file(self.note)
                if finding.code == "whole-line-bold"]

    def test_separate_anchors_do_not_cover_plain_explanation(self) -> None:
        text = "**短锚点**" + "这里是没有加粗的正常解释文字。" * 5 + "**另一锚点**"
        self.assertEqual(self.bold_findings(text), [])

    def test_long_strong_span_then_plain_text_is_not_whole_line(self) -> None:
        text = "**" + "这一部分虽然很长但只是行内的一段重点。" * 3 + "**普通解释**结束锚点**"
        self.assertEqual(self.bold_findings(text), [])

    def test_actual_whole_line_bold_keeps_source_line(self) -> None:
        text = "说明\n\n**" + "这一整段文字都被放进了同一个粗体区间。" * 4 + "**"
        self.assertEqual(self.bold_findings(text), [("whole-line-bold", 3)])

    def test_whole_line_bold_allows_trailing_sentence_punctuation(self) -> None:
        for punctuation in "。！？.!?":
            with self.subTest(punctuation=punctuation):
                text = "**" + "这一整段文字都被放进了同一个粗体区间。" * 4 + "**" + punctuation
                self.assertEqual(self.bold_findings(text), [("whole-line-bold", 1)])

    def test_normal_short_anchor_is_not_flagged(self) -> None:
        self.assertEqual(self.bold_findings("**关键条件**"), [])

    def test_adjacent_strong_spans_still_cover_whole_line(self) -> None:
        first = "**" + "第一段全部加粗的内容。" * 3 + "**"
        second = "**" + "第二段也没有正常正文。" * 3 + "**"
        for separator in (" ", "，", "。 "):
            with self.subTest(separator=separator):
                self.assertEqual(self.bold_findings(first + separator + second),
                                 [("whole-line-bold", 1)])

    def test_plain_prefix_suffix_or_inline_code_breaks_whole_line(self) -> None:
        bold = "**" + "只应提醒真正覆盖全行的粗体。" * 4 + "**"
        for text in ("正常引入" + bold, bold + "正常解释", bold + " `plain` " + bold):
            with self.subTest(text=text):
                self.assertEqual(self.bold_findings(text), [])

    def test_literal_markers_inside_bold_do_not_hide_whole_line(self) -> None:
        for literal in (r"\*\*", "`**`", "``a ** b``"):
            with self.subTest(literal=literal):
                text = "**" + "整行加粗仍须识别。" * 4 + literal + "保留原有检查。" * 3 + "**"
                self.assertEqual(self.bold_findings(text), [("whole-line-bold", 1)])

    def test_code_examples_and_escaped_outer_markers_are_not_bold(self) -> None:
        inner = "**" + "这只是代码或转义后的普通标记。" * 4 + "**"
        self.assertEqual(self.bold_findings("```markdown\n" + inner + "\n```"), [])
        self.assertEqual(self.bold_findings("`" + inner + "`"), [])
        self.assertEqual(self.bold_findings(r"\*\*" + "这不是粗体。" * 10 + r"\*\*"), [])


if __name__ == "__main__":
    unittest.main()
