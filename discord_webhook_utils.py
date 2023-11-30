"""
Discord Webhook Action을 사용해, 디스코드 웹훅으로 정보를 전달하기 위한 유틸리티 코드.
5.3.0 버전을 기준으로 작성되었다.

해당 Action의 링크: https://github.com/marketplace/actions/discord-webhook-action

작성일: 2023.11.30
@Copyright 2023 Lapis0875 (Minjun Kim)
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Final, Optional

from models import JSON

class Defaults:
    """상수 값들."""
    STRING: Final[str] = "=@I_AM_DEFAULT_STRING_PLACEHOLDER@="
    ID: Final[int] = 0
    USERNAME: Final[str] = "Discord Webhook Action (v5)"
    URL: Final[str] = "https://github.com/Lapis0875/KoreanAirforceRatioAlarm"

"""
하단의 모델들은 모두 Discord API의 명세를 따라 구현되었습니다.
구체적으로 각 항목이 무슨 기능을 하는지 궁금하다면, Discord API의 공식 문서를 찾아보는 것을 권장합니다.
"""

@dataclass(repr=True, eq=False, order=False, slots=True)
class Field:
    """Discord에서 제공하는 Embed에 사용되는 Field 객체."""
    name: str
    value: str
    inline: bool = field(repr=False, default=False)

    def to_dict(self) -> JSON:
        """JSON 형식으로 객체를 직렬화합니다."""
        return {"name": self.name, "value": self.value, "inline": self.inline}

@dataclass(repr=True, eq=False, order=False, slots=True)
class Asset:
    """Discord의 Embed에서, thumbnail과 image, video에 사용 가능한 이미지 객체."""
    url: str
    proxy_url: Optional[str] = field(default=None)
    height: Optional[int] = field(default=None)
    width: Optional[int] = field(default=None)

    def to_dict(self) -> JSON:
        """JSON 형식으로 객체를 직렬화합니다."""
        payload: JSON = {"url": self.url}
        if self.proxy_url is not None:
            payload["proxy_url"] = self.proxy_url
        if self.height is not None:
            payload["height"] = self.height
        if self.width is not None:
            payload["width"] = self.width
        return payload

@dataclass(repr=True, eq=False, order=False, slots=True)
class Provider:
    """Discord의 Embed에 사용될 Provider 객체."""
    name: str
    url: Optional[str] = field(default=None)

    def to_dict(self) -> JSON:
        """JSON 형식으로 객체를 직렬화합니다."""
        payload: JSON = {"name": self.name}
        if self.url is not None:
            payload["url"] = self.url
        return payload

@dataclass(repr=True, eq=False, order=False, slots=True)
class Author:
    """Discord의 Embed에 사용될 Author 객체."""
    name: str
    url: Optional[str] = field(default=None)
    icon_url: Optional[str] = field(default=None)
    proxy_icon_url: Optional[str] = field(default=None)

    def to_dict(self) -> JSON:
        """JSON 형식으로 객체를 직렬화합니다."""
        payload: JSON = {"name": self.name}
        if self.url is not None:
            payload["url"] = self.url
        if self.icon_url is not None:
            payload["icon_url"] = self.icon_url
        if self.proxy_icon_url is not None:
            payload["proxy_icon_url"] = self.proxy_icon_url
        return payload

class EmbedTypes(Enum):
    """Discord에서 제공하는 Embed의 유형에 대한 Enum 객체."""
    Rich = "rich"
    Image = "image"
    Video = "video"
    GIFV = "gifv"
    Article = "article"
    Link = "link"

class Color(Enum):
    """
    Discord에서 사용 가능한 몇가지 색상의 정수값.
    원래는 hex로 계산해야하는데 귀찮아서 이거로...
    """
    Default = 0
    Aqua = 1752220
    DarkAqua = 1146986
    Green = 5763719
    DarkGreen = 2067276
    Blue = 3447003
    DarkBlue = 2123412
    Purple = 10181046
    DarkPurple = 7419530
    LuminousVividPink = 15277667
    DarkVividPink = 11342935
    Gold = 15844367
    DarkGold = 12745742
    Orange = 15105570
    DarkOrange = 11027200
    Red = 15548997
    DarkRed = 10038562
    Grey = 9807270
    DarkGrey = 9936031
    DarkerGrey = 8359053
    LightGrey = 12370112
    Navy = 3426654
    DarkNavy = 2899536
    Yellow = 16776960
    White = 16777215
    Greyple = 10070709
    Black = 2303786
    DarkButNotBlack = 2895667
    NotQuiteBlack = 2303786
    Blurple = 5793266
    DiscordGreen = 5763719
    DiscordYellow = 16705372
    Fuchsia = 15418782
    DiscordRed = 15548997

@dataclass(repr=True, eq=False, order=False, slots=True)
class Embed:
    """Discord에서 사용되는 Embed 객체."""
    type: EmbedTypes = field(default=EmbedTypes.Rich)
    title: Optional[str] = field(default=None)
    description: Optional[str] = field(default=None)
    url: Optional[str] = field(default=None)
    color: Optional[Color] = field(default=None)
    image: Optional[Asset] = field(default=None)
    thumbnail: Optional[Asset] = field(default=None)
    video: Optional[Asset] = field(default=None)
    provider: Optional[Provider] = field(default=None)
    author: Optional[Author] = field(default=None)
    fields: Optional[list[Field]] = field(default=None)
    
    def to_dict(self) -> JSON:
        """JSON 형식으로 객체를 직렬화합니다."""
        payload: JSON = {"type": self.type.value}
        if self.title is not None:
            payload["title"] = self.title
        if self.description is not None:
            payload["description"] = self.description
        if self.url is not None:
            payload["url"] = self.url
        if self.color is not None:
            payload["color"] = self.color.value
        if self.image is not None:
            payload["image"] = self.image.to_dict()
        if self.thumbnail is not None:
            payload["thumbnail"] = self.thumbnail.to_dict()
        if self.video is not None:
            payload["video"] = self.video.to_dict()
        if self.provider is not None:
            payload["provider"] = self.provider.to_dict()
        if self.author is not None:
            payload["author"] = self.author.to_dict()
        if self.fields is not None and len(self.fields):
            payload["fields"] = [f.to_dict() for f in self.fields]
        return payload

@dataclass(repr=True, eq=False, order=False, slots=True)
class WebhookMessage:
    """Discord 웹훅으로 전송될 메세지를 나타내는 데이터 객체."""
    content: str = field(repr=False, default=Defaults.STRING)
    thread_id: int = field(default=Defaults.ID)
    thread_name: str = field(default=Defaults.STRING)
    username: str = field(default=Defaults.USERNAME)
    avatar_url: str = field(default=Defaults.URL)
    tts: bool = field(default=False)
    embeds: list[Embed] = field(default_factory=list)
    suppress_embeds: bool = field(default=False)
    
    def set_embed_visible(self):
        self.suppress_embeds = False
    
    def set_embed_invisible(self):
        self.suppress_embeds = True
    
    def to_dict(self) -> JSON:
        """JSON 형식으로 객체를 변환합니다."""
        payload: JSON = {}
        if self.content is not Defaults.STRING:
            payload["content"] = self.content
        if self.thread_id is not Defaults.ID:
            payload["thread_id"] = self.thread_id
        if self.thread_name is not Defaults.STRING:
            payload["thread_name"] = self.thread_name
        if self.username is not Defaults.USERNAME:
            payload["username"] = self.username
        if self.avatar_url is not Defaults.URL:
            payload["avatar_url"] = self.avatar_url
        if self.tts:
            payload["tts"] = True
        if self.suppress_embeds:
            payload["flags"] = 1 << 2 # SUPPRESS_EMBEDS 비트필드만 활성화한 값.
        
        if len(self.embeds):
            payload["embeds"] = [e.to_dict() for e in self.embeds]
        
        return payload
    
