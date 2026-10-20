
from research.search import search_web
from research.report import generate_report


def main():
    question = "ما هو الذكاء الاصطناعي، وما أبرز استخداماته وتحدياته؟"

    print("1. البحث عن المصادر...")
    sources = search_web(question, max_results=3)

    print(f"تم العثور على {len(sources)} مصادر.")

    print("\n2. إنشاء التقرير باستخدام Ollama...")
    result = generate_report(question, sources)

    print("\n" + "=" * 60)
    print(result["report"])
    print("=" * 60)

    if result["warnings"]:
        print("\nتحذيرات التحقق:")
        for warning in result["warnings"]:
            print(f"- {warning}")
    else:
        print("\nاكتمل فحص أرقام الإحالات دون تحذيرات.")


if __name__ == "__main__":
    main()
