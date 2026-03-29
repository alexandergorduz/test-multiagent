from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, ToolMessage

from config import settings
from agents.common.state import MultiagentState
from agents.math_subagent.tools import math_subagent_tools, add_numbers, multiply_numbers
from agents.math_subagent.system_prompts import MATH_SUBAGENT_SYSTEM_PROMPT




math_subagent_llm = ChatOpenAI(
    api_key=settings.openai_api_key.get_secret_value(),
    model=settings.model_name,
    temperature=0.0,
    max_tokens=4096
).bind_tools(math_subagent_tools)



def math_subagent_node(state: MultiagentState) -> MultiagentState:

    subagent_messages = state["subagent_messages"]

    result = math_subagent_llm.invoke(
        [SystemMessage(content=MATH_SUBAGENT_SYSTEM_PROMPT)]
        + subagent_messages
    )

    return {
        "subagent_messages": subagent_messages + [result]
    }



def math_subagent_tools_node(state: MultiagentState) -> MultiagentState:

    subagent_messages = state["subagent_messages"]

    last_subagent_message = subagent_messages[-1]

    results = []

    for tool_call in last_subagent_message.tool_calls:

        print(f"---> Calling tool:\n{tool_call['name']} with parameters {tool_call['args']}\n\n\n")

        if tool_call["name"] == "add_numbers":

            try:

                result_content = add_numbers.invoke(tool_call["args"])

            except Exception as e:

                result_content = f"Something went wrong with the function {tool_call['name']} with parameters {tool_call['args']}. Error: {e}."

        elif tool_call["name"] == "multiply_numbers":

            try:

                result_content = multiply_numbers.invoke(tool_call["args"])

            except Exception as e:

                result_content = f"Something went wrong with the function {tool_call['name']} with parameters {tool_call['args']}. Error: {e}."

        else:

            result_content = f"The function {tool_call['name']} with parameters {tool_call['args']} is not supported."

        print(f"---> Tool output:\n{result_content}\n\n\n")

        results.append(ToolMessage(content=result_content, tool_call_id=tool_call["id"]))

    return {
        "subagent_messages": subagent_messages + results
    }



def math_subagent_finalize_node(state: MultiagentState) -> MultiagentState:

    subagent_messages = state["subagent_messages"]

    last_subagent_message = subagent_messages[-1]

    return {
        "subagent_messages": [],
        "subagent_result": last_subagent_message.content,
        "route": ""
    }