import asyncio
import logging

from google.genai import types
from google.genai.errors import ServerError
from sqlalchemy.orm import Session

from app.ai_agent.client import gemini_client
from app.ai_agent.tools import (
    get_tasks_tool,
    create_task_tool,
    update_task_tool,
    delete_task_tool,
)

logger = logging.getLogger("uvicorn.error")


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

MAX_STEPS = 5
SYSTEM_INSTRUCTION = """
You are the AI task management assistant for TaskFlow.

Your job is to help the authenticated user manage their tasks using the available tools.

Rules:
- Complete all actions requested by the user before giving the final answer.
- If the request requires multiple tools, continue using tools until all requested actions are completed.
- Never imitate or describe a tool call as plain text. Use the actual tool instead.
- Never claim that an action succeeded unless the tool result confirms it.
- Do not invent task IDs or task data.
"""

async def generate_response(
    message: str,
    db: Session,
    user_id: int,
) -> str:
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=message),
            ],
        )
    ]

    for step in range(MAX_STEPS):
        logger.info("AI agent step %s", step)
        try:
            response = await asyncio.wait_for(
                gemini_client.aio.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=contents,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_INSTRUCTION,
                        tools=[task_tools],
                    ),
                ),
                timeout=30,
            )

        except asyncio.TimeoutError:
            return (
                "The AI service took too long to respond. "
                "Please try again."
            )


        except ServerError:
            return (
                "The AI service is temporarily unavailable. "
                "Please try again shortly."
            )

        candidate = response.candidates[0]
        part = candidate.content.parts[0]

        if part.function_call:
            function_call = part.function_call
            logger.info(
                "AI agent tool call: %s args=%s",
                function_call.name,
                function_call.args,
            )

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


            logger.info(
                "AI agent tool result: %s",
                tool_result,
            )

            tool_response = types.Part.from_function_response(
                name=function_call.name,
                response={
                    "result": tool_result,
                },
            )

            contents.append(candidate.content)

            contents.append(
                types.Content(
                    role="user",
                    parts=[tool_response],
                )
            )

            continue

        if response.text:
            logger.info(
                "AI agent finished after step %s",
                step,
            )
            return response.text

        return "I couldn't generate a response. Please try again."

    return "The agent reached the maximum number of steps."