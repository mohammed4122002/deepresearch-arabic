from types import SimpleNamespace
import unittest
from unittest.mock import patch

from research.report import generate_report


def _response(content: str) -> SimpleNamespace:
    return SimpleNamespace(
        message=SimpleNamespace(content=content),
    )


class GenerateReportCitationTests(unittest.TestCase):
    @patch("research.report.chat")
    def test_retries_report_without_citations_and_returns_valid_references(
        self,
        mock_chat,
    ):
        mock_chat.side_effect = [
            _response("تقرير بلا إحالات."),
            _response("توضح المصادر أهمية الموضوع [1]."),
        ]
        sources = [
            {
                "title": "مصدر موثوق",
                "url": "https://example.com/source",
                "content": "مقتطف المصدر",
            }
        ]

        result = generate_report("سؤال البحث", sources)

        self.assertEqual(mock_chat.call_count, 2)
        self.assertIn(
            "أعد كتابة التقرير",
            mock_chat.call_args_list[1].kwargs["messages"][-1]["content"],
        )
        self.assertIn(
            "[1] مصدر موثوق\nhttps://example.com/source",
            result["report"],
        )
        self.assertEqual(
            result["cited_sources"],
            [
                {
                    "id": 1,
                    "title": "مصدر موثوق",
                    "url": "https://example.com/source",
                    "content": "مقتطف المصدر",
                }
            ],
        )
        self.assertEqual(result["warnings"], [])


    @patch("research.report.chat")
    def test_falls_back_to_cited_source_excerpts_after_invalid_citations(
        self,
        mock_chat,
    ):
        mock_chat.side_effect = [
            _response("إجابة بلا إحالة."),
            _response("إجابة بإحالة غير موجودة [9]."),
        ]
        sources = [
            {
                "title": "مصدر",
                "url": "https://example.com/source",
                "content": "مقتطف",
            }
        ]

        result = generate_report("سؤال البحث", sources)

        self.assertEqual(mock_chat.call_count, 2)
        self.assertIn("مقتطفات البحث كما وردت", result["report"])
        self.assertIn("> مقتطف", result["report"])
        self.assertIn("[1] مصدر\nhttps://example.com/source", result["report"])
        self.assertNotIn("[9]", result["report"])
        self.assertEqual(
            result["warnings"],
            ["تعذر توليد تقرير بإحالات صالحة؛ عُرضت مقتطفات المصادر بدلًا منه."],
        )
