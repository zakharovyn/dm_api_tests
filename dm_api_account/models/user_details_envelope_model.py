from dm_api_account.models.user_envelope_model import Roles, Rating
from pydantic import BaseModel, StrictStr, Field, StrictInt
from typing import Optional, List
from datetime import datetime
from enum import Enum


class PagingSetting(BaseModel):
    posts_per_page: StrictInt = Field(None, alias='postsPerPage')
    comments_per_page: StrictInt = Field(None, alias='commentsPerPage')
    topics_per_page: StrictInt = Field(None, alias='topicsPerPage')
    messages_per_page: StrictInt = Field(None, alias='messagesPerPage')
    entities_per_page: StrictInt = Field(None, alias='entitiesPerPage')


class ColorSchema(Enum):
    MODERN = 'Modern'
    PALE = 'Pale'
    CLASSIC = 'Classic'
    CLASSIC_PALE = 'ClassicPale'
    NIGHT = 'Night'


class UserSettings(BaseModel):
    color_schema: list[ColorSchema] = Field(None, alias='colorSchema')
    nanny_greetings_message: StrictStr = Field(None, alias='nannyGreetingsMessage')
    paging: PagingSetting


class BbParseMode(Enum):
    COMMON = 'Common'
    INFO = 'Info'
    POST = 'Post'
    CHAT = 'Chat'


class InfoBdText(BaseModel):
    value: StrictStr
    parse_mode: BbParseMode


class UserDetails(BaseModel):
    login: StrictStr
    roles: List[Roles]
    medium_picture_url: Optional[StrictStr] = Field(None, alias='mediumPictureUrl')
    small_picture_url: Optional[StrictStr] = Field(None, alias='smallPictureUrl')
    status: Optional[StrictStr]
    rating: Rating
    online: Optional[datetime]
    name: Optional[StrictStr]
    location: Optional[StrictStr]
    registration: Optional[datetime]
    icq: StrictStr
    skype: StrictStr
    origin_picture_url: Optional[StrictStr] = Field(None, alias='originPictureUrl')
    info: InfoBdText
    settings: UserSettings


class UserDetailsEnvelopeModel(BaseModel):
    resource: UserDetails
    metadate: Optional[StrictStr] = None
