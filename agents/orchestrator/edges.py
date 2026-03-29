from agents.common.state import MultiagentState




def router(state: MultiagentState) -> str:

    route = state["route"]

    return route