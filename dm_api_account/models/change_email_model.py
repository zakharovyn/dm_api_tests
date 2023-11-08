from pydantic import BaseModel, StrictStr


class ChangeEmailModel(BaseModel):
    login: StrictStr
    password: StrictStr
    email: StrictStr
