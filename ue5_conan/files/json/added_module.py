from pydantic import BaseModel, Field


class AddedModule(BaseModel):
    name: str = Field(alias="Name")
    type: str = Field(alias="Type")
    loading_phase: str = Field(alias="LoadingPhase")