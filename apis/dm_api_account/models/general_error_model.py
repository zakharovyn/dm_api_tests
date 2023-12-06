from __future__ import annotations
from pydantic import BaseModel, Field, StrictStr, ConfigDict
from typing import Optional


class GeneralError(BaseModel):

    model_config = ConfigDict(extra='forbid')

    message: Optional[StrictStr] = Field(None, description='Client message')
