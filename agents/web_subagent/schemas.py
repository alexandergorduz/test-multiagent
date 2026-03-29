from pydantic import BaseModel, Field




class WebSearchSchema(BaseModel):

    query: str = Field(description="The query to search the web for.")