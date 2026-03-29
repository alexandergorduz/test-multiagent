from typing import Any

from langchain_core.tools import tool

from agents.math_subagent.schemas import AddNumbersSchema, MultiplyNumbersSchema




@tool(args_schema=AddNumbersSchema)
def add_numbers(**kwargs: dict[str, Any]) -> str:
    """
    Tool to add two numbers together.
    """

    first_number = kwargs["first_number"]
    second_number = kwargs["second_number"]

    return f"{first_number} + {second_number} = {first_number + second_number}"



@tool(args_schema=MultiplyNumbersSchema)
def multiply_numbers(**kwargs: dict[str, Any]) -> str:
    """
    Tool to multiply two numbers together.
    """

    first_number = kwargs["first_number"]
    second_number = kwargs["second_number"]

    return f"{first_number} * {second_number} = {first_number * second_number}"



math_subagent_tools = [add_numbers, multiply_numbers]