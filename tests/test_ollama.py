
from ollama import chat

from config import LLM_MODEL


def test_ollama_connection():
    response = chat(
        model=LLM_MODEL,
        messages=[
            {
                "role": "user",
                "content": "أجب بالعربية: ما الهدف من مشروع DeepResearch Arabic؟",
            }
        ],
    )

    answer = response.message.content

    assert answer and answer.strip(), "النموذج أعاد إجابة فارغة"
    print("\nإجابة النموذج:\n", answer)


if __name__ == "__main__":
    test_ollama_connection()
