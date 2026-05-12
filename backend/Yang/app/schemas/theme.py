import json
from pydantic import BaseModel, ConfigDict, field_validator


class ThemeItem(BaseModel):
    key: str
    name: str
    description: str
    tickers: list[str]

    model_config = ConfigDict(from_attributes=True)

    @field_validator("tickers", mode="before")
    @classmethod
    def parse_tickers(cls, v):
        if isinstance(v, str):
            return json.loads(v)
        return v


class ThemeListResponse(BaseModel):
    items: list[ThemeItem]
    total: int
