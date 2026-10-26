import asyncio

from google.genai import types
from sqlalchemy.orm import Session

from app.ai_agent.client import gemini_client
from app.ai_agent.tools import get_tasks_tool

get_tasks_declaration = types.FunctionDeclaration(
    name="get_tasks",
    description="Get all tasks belonging to the current authenticated user.",
    parameters={
        "type": "object",
        "properties": {},
    },
)

task_tools = types.Tool(
    function_declarations=[get_tasks_declaration]
)


async def generate_response(message: str, db: Session, user_id: int,) -> str:
    response = await asyncio.wait_for(
        gemini_client.aio.models.generate_content(
            model="gemini-3.6-flash",
            contents=message,
            config=types.GenerateContentConfig(
                tools=[task_tools],
            ),
        ),
        timeout=30,
    )

    candidate = response.candidates[0]
    part = candidate.content.parts[0]

    if part.function_call:
        function_call = part.function_call

        if function_call.name == "get_tasks":
            tasks = get_tasks_tool(
                db=db,
                user_id=user_id,
            )

            return str(tasks)

        return f"Unknown tool: {function_call.name}"

    return response.text


