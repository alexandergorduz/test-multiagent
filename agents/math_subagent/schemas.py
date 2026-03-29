from pydantic import BaseModel, Field




class AddNumbersSchema(BaseModel):

    first_number: float = Field(description="The first number to add.")
    second_number: float = Field(description="The second number to add.")



class MultiplyNumbersSchema(BaseModel):

    first_number: float = Field(description="The first number to multiply.")
    second_number: float = Field(description="The second number to multiply.")