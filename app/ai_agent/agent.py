import asyncio

from google.genai import types
from sqlalchemy.orm import Session

from app.ai_agent.client import gemini_client
from app.ai_agent.tools import (
    get_tasks_tool,
    create_task_tool,
    update_task_tool,
    delete_task_tool,
)


get_tasks_declaration = types.FunctionDeclaration(
    name="get_tasks",
    description="Get all tasks belonging to the current authenticated user.",
    parameters={
        "type": "object",
        "properties": {},
    },
)


create_task_declaration = types.FunctionDeclaration(
    name="create_task",
    description="Create a new task for the current authenticated user.",
    parameters={
        "type": "object",
        "properties": {
            "title": {
                "type": "string",
                "description": "Title of the task.",
            },
            "description": {
                "type": "string",
                "description": "Optional description of the task.",
            },
        },
        "required": ["title"],
    },
)


update_task_declaration = types.FunctionDeclaration(
    name="update_task",
    description=(
        "Update an existing task belonging to the current authenticated user. "
        "Only provide fields that should be changed."
    ),
    parameters={
        "type": "object",
        "properties": {
            "task_id": {
                "type": "integer",
                "description": "ID of the task to update.",
            },
            "title": {
                "type": "string",
                "description": "New title of the task.",
            },
            "description": {
                "type": "string",
                "description": "New description of the task.",
            },
        },
        "required": ["task_id"],
    },
)


delete_task_declaration = types.FunctionDeclaration(
    name="delete_task",
    description="Delete a task belonging to the current authenticated user.",
    parameters={
        "type": "object",
        "properties": {
            "task_id": {
                "type": "integer",
                "description": "ID of the task to delete.",
            },
        },
        "required": ["task_id"],
    },
)


task_tools = types.Tool(
    function_declarations=[
        get_tasks_declaration,
        create_task_declaration,
        update_task_declaration,
        delete_task_declaration,
    ]
)


async def generate_response(
    message: str,
    db: Session,
    user_id: int,
) -> str:
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
            tool_result = get_tasks_tool(
                db=db,
                user_id=user_id,
            )

        elif function_call.name == "create_task":
            args = function_call.args

            tool_result = create_task_tool(
                db=db,
                user_id=user_id,
                title=args["title"],
                description=args.get("description"),
            )

        elif function_call.name == "update_task":
            args = function_call.args

            tool_result = update_task_tool(
                db=db,
                user_id=user_id,
                task_id=args["task_id"],
                title=args.get("title"),
                description=args.get("description"),
            )

        elif function_call.name == "delete_task":
            args = function_call.args

            tool_result = delete_task_tool(
                db=db,
                user_id=user_id,
                task_id=args["task_id"],
            )

        else:
            return f"Unknown tool: {function_call.name}"

        tool_response = types.Part.from_function_response(
            name=function_call.name,
            response={
                "result": tool_result,
            },
        )

        final_response = await asyncio.wait_for(
            gemini_client.aio.models.generate_content(
                model="gemini-3.6-flash",
                contents=[
                    types.Content(
                        role="user",
                        parts=[
                            types.Part.from_text(text=message)
                        ],
                    ),
                    candidate.content,
                    types.Content(
                        role="user",
                        parts=[tool_response],
                    ),
                ],
                config=types.GenerateContentConfig(
                    tools=[task_tools],
                ),
            ),
            timeout=30,
        )

        if final_response.text:
            return final_response.text

        if isinstance(tool_result, dict) and "error" in tool_result:
            return tool_result["error"]

        return "The request was processed, but the AI could not generate a response."

    if response.text:
        return response.text

    return "I couldn't generate a reseponse. Please try again."