from __future__ import annotations
from pydantic import BaseModel, Field, StrictStr, ConfigDict
from typing import Optional


class ResetPassword(BaseModel):

    model_config = ConfigDict(extra='forbid')

    login: Optional[StrictStr] = Field(None, description='Login')
    email: Optional[StrictStr] = Field(None, description='Email')
