from __future__ import annotations
from pydantic import BaseModel, Field, StrictStr, ConfigDict
from typing import Optional


class ChangePassword(BaseModel):

    model_config = ConfigDict(extra='forbid')

    login: Optional[StrictStr] = Field(None, description='User login')
    token: Optional[StrictStr] = Field(None, description='Password reset token')
    old_password: Optional[StrictStr] = Field(
        None, alias='oldPassword', description='Old password'
    )
    new_password: Optional[StrictStr] = Field(
        None, alias='newPassword', description='New password'
    )
