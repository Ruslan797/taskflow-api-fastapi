import asyncio

from app.ai_agent.agent import generate_response


async def main() -> None:
    print("1. Сейчас отправляем запрос Gemini")

    result = await generate_response(
        "Reply with exactly: TaskFlow AI works"
    )

    print("2. Gemini ответил")
    print(result)


if __name__ == "__main__":
    asyncio.run(main())