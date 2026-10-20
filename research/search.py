
import os
from typing import Any

from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()


def search_web(
    query: str,
    max_results: int = 5,
) -> list[dict[str, Any]]:
    """
    Search the web using Tavily and return normalized results.

    Args:
        query: The research question or search query.
        max_results: Maximum number of results to return.

    Returns:
        A list of dictionaries containing title, URL, and content.
    """
    query = query.strip()

    if not query:
        raise ValueError("يجب إدخال سؤال أو عبارة للبحث.")

    if not 1 <= max_results <= 10:
        raise ValueError("يجب أن يكون max_results بين 1 و10.")

    api_key = os.getenv("SEARCH_API_KEY")

    if not api_key:
        raise RuntimeError(
            "مفتاح البحث غير موجود. أضف SEARCH_API_KEY إلى ملف .env."
        )

    client = TavilyClient(api_key=api_key)

    try:
        response = client.search(
            query=query,
            max_results=max_results,
            search_depth="basic",
            include_answer=False,
        )
    except Exception as exc:
        raise RuntimeError(
            f"فشل البحث عبر Tavily: {exc}"
        ) from exc

    results = []

    for item in response.get("results", []):
        url = item.get("url", "").strip()
        title = item.get("title", "").strip()
        content = item.get("content", "").strip()

        if not url:
            continue

        results.append(
            {
                "title": title or "بدون عنوان",
                "url": url,
                "content": content,
                "score": item.get("score"),
            }
        )

    return results


if __name__ == "__main__":
    try:
        query = input("اكتب موضوع البحث: ")
        results = search_web(query)

        if not results:
            print("لم يتم العثور على نتائج.")
        else:
            for index, result in enumerate(results, start=1):
                print(f"\n--- المصدر {index} ---")
                print(f"العنوان: {result['title']}")
                print(f"الرابط: {result['url']}")
                print(f"المقتطف: {result['content'][:500]}")

    except (ValueError, RuntimeError) as exc:
        print(f"\nخطأ: {exc}")
