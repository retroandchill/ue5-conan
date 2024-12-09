from typing import Optional

from pydantic import BaseModel, Field


class AddedPlugin(BaseModel):
    name: str = Field(alias="Name")
    enabled: bool = Field(alias="Enabled")
    target_allow_list: Optional[list[str]] = Field(alias="TargetAllowList", default=None)