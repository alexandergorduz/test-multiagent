from typing import List
from typing_extensions import TypedDict

from langchain_core.messages import BaseMessage




class MultiagentState(TypedDict):

    messages: List[BaseMessage]
    subagent_messages: List[BaseMessage]
    subagent_result: str
    route: str