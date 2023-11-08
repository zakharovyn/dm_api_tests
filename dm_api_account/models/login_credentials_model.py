from pydantic import BaseModel, StrictStr, StrictBool, Field


class LoginCredentialsModel(BaseModel):
    login: StrictStr
    password: StrictStr
    remember_me: StrictBool = Field(None, alias='rememberMe')
