from typing import Literal
from pydantic import BaseModel, Field




class OrchestratorStructOut(BaseModel):

    route: Literal[
        "end",
        "web_subagent",
        "math_subagent"
    ] = Field(
        description=(
            "The route to take based on the user's request."
            "`end`: The conversation is over or needs clarification."
            "`web_subagent`: The users request needs to be handled by the web subagent."
            "`math_subagent`: The users request needs to be handled by the math subagent."
        )
    )
    text: str = Field(
        description=(
            "The text to return to the user."
            "If the route is `end` - this is the answer or clarification to the user's request."
            "Otherwise, this is the task for the subagent to complete."
        )
    )