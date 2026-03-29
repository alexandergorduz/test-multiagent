from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage

from config import settings, SUMMARIZATION_THRESHOLD, MAX_KEEP_LAST_MESSAGES
from agents.common.state import MultiagentState
from agents.orchestrator.schemas import OrchestratorStructOut
from agents.orchestrator.system_prompts import ORCHESTRATOR_SYSTEM_PROMPT, ORCHESTRATOR_STRUCT_OUT_SYSTEM_PROMPT




orchestrator_llm = ChatOpenAI(
    api_key=settings.openai_api_key.get_secret_value(),
    model=settings.model_name,
    temperature=0.0,
    max_tokens=4096
)

orchestrator_llm_struct_out = orchestrator_llm.with_structured_output(OrchestratorStructOut)



def orchestrator_node(state: MultiagentState) -> MultiagentState:

    messages = state["messages"]
    subagent_result = state["subagent_result"]

    if len(messages) > SUMMARIZATION_THRESHOLD:

        print("---> Summarizing messages...\n\n\n")

        head = messages[:-MAX_KEEP_LAST_MESSAGES]
        tail = messages[-MAX_KEEP_LAST_MESSAGES:]

        while tail and not isinstance(tail[0], HumanMessage):

            head.append(tail.pop(0))

        messages_summary = orchestrator_llm.invoke(
            [SystemMessage(content=ORCHESTRATOR_SYSTEM_PROMPT)]
            + head
        )

        messages = [HumanMessage(content=messages_summary.content)] + tail

    if subagent_result != "":

        result = orchestrator_llm_struct_out.invoke(
            [SystemMessage(content=ORCHESTRATOR_STRUCT_OUT_SYSTEM_PROMPT)]
            + messages
            + [HumanMessage(content=f"=== SUBAGENT RESULT ===\n\n{subagent_result}\n\n=== END OF SUBAGENT RESULT ===")]
        )

    else:

        result = orchestrator_llm_struct_out.invoke(
            [SystemMessage(content=ORCHESTRATOR_STRUCT_OUT_SYSTEM_PROMPT)]
            + messages
        )

    route = result.route
    text = result.text

    if route == "end":

        return {
            "messages": messages + [AIMessage(content=text)],
            "subagent_result": "",
            "route": route
        }

    print(f"---> Subagent task:\n{text}\n\n\n")

    return {
        "messages": messages,
        "subagent_messages": [HumanMessage(content=text)],
        "subagent_result": "",
        "route": route
    }