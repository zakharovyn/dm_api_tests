from pydantic import BaseModel, StrictStr, Field


class RegistrationModel(BaseModel):
    login: StrictStr = Field(default='test_value')
    email: StrictStr
    password: StrictStr = Field(min_length=8)
