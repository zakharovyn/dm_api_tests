from __future__ import annotations
from pydantic import BaseModel, Field, StrictStr, ConfigDict
from typing import Optional


class ChangeEmail(BaseModel):

    model_config = ConfigDict(extra='forbid')

    login: Optional[StrictStr] = Field(None, description='User login')
    password: Optional[StrictStr] = Field(None, description='User password')
    email: Optional[StrictStr] = Field(None, description='New user email')
