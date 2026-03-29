from langgraph.graph import StateGraph, START, END

from config import GRAPH_IMAGE_PATH
from agents.common.state import MultiagentState
from agents.orchestrator.nodes import orchestrator_node
from agents.orchestrator.edges import router
from agents.math_subagent.nodes import math_subagent_node, math_subagent_tools_node, math_subagent_finalize_node
from agents.math_subagent.edges import math_subagent_should_continue
from agents.web_subagent.nodes import web_subagent_node, web_subagent_tools_node, web_subagent_finalize_node
from agents.web_subagent.edges import web_subagent_should_continue




def create_graph(checkpointer):

    multiagent = StateGraph(MultiagentState)

    multiagent.add_node("orchestrator", orchestrator_node)

    multiagent.add_node("math_subagent", math_subagent_node)
    multiagent.add_node("math_subagent_tools", math_subagent_tools_node)
    multiagent.add_node("math_subagent_finalize", math_subagent_finalize_node)

    multiagent.add_node("web_subagent", web_subagent_node)
    multiagent.add_node("web_subagent_tools", web_subagent_tools_node)
    multiagent.add_node("web_subagent_finalize", web_subagent_finalize_node)

    multiagent.add_edge(START, "orchestrator")
    multiagent.add_conditional_edges(
        "orchestrator",
        router,
        {
            "end": END,
            "web_subagent": "web_subagent",
            "math_subagent": "math_subagent"
        }
    )

    multiagent.add_conditional_edges(
        "math_subagent",
        math_subagent_should_continue,
        {
            "math_subagent_tools": "math_subagent_tools",
            "math_subagent_finalize": "math_subagent_finalize"
        }
    )
    multiagent.add_edge("math_subagent_tools", "math_subagent")
    multiagent.add_edge("math_subagent_finalize", "orchestrator")

    multiagent.add_conditional_edges(
        "web_subagent",
        web_subagent_should_continue,
        {
            "web_subagent_tools": "web_subagent_tools",
            "web_subagent_finalize": "web_subagent_finalize"
        }
    )
    multiagent.add_edge("web_subagent_tools", "web_subagent")
    multiagent.add_edge("web_subagent_finalize", "orchestrator")

    multiagent = multiagent.compile(checkpointer=checkpointer)

    with open(GRAPH_IMAGE_PATH, "wb") as file:
        file.write(multiagent.get_graph(xray=True).draw_mermaid_png())

    return multiagent