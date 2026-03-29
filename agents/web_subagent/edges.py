from agents.common.state import MultiagentState




def web_subagent_should_continue(state: MultiagentState) -> str:

    subagent_messages = state["subagent_messages"]

    last_subagent_message = subagent_messages[-1]

    if last_subagent_message.tool_calls:

        print(f"---> Agent thought:\n{last_subagent_message.content}\n\n\n")

        return "web_subagent_tools"

    return "web_subagent_finalize"