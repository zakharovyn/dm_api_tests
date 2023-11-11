from __future__ import annotations
from pydantic import BaseModel, Field, StrictStr, ConfigDict
from typing import Dict, List, Optional


class BadRequestError(BaseModel):

    model_config = ConfigDict(extra='forbid')

    message: Optional[StrictStr] = Field(None, description='Client message')
    invalid_properties: Optional[Dict[str, List[StrictStr]]] = Field(
        None,
        alias='invalidProperties',
        description='Key-value pairs of invalid request properties',
    )
