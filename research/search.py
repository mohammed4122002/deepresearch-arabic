def search_web(query: str, limit: int = 5) -> list[dict[str, str]]:
    """Return sample web-search results using a provider-neutral interface."""
    if not query.strip() or limit <= 0:
        return []

    return [
        {
            "source_id": "src_1",
            "title": f"نتيجة بحث تجريبية لـ: {query}",
            "url": "https://example.com",
            "snippet": "هذا مقتطف تجريبي لتوضيح كيفية عمل جلب النتائج في النظام.",
        }
    ][:limit]