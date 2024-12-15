from typing import Optional

from pydantic import BaseModel, Field

from ue5_conan.files.json.added_module import AddedModule
from ue5_conan.files.json.added_plugin import AddedPlugin

class UProjectFile(BaseModel):
    file_version: int = Field(alias="FileVersion")
    engine_association: Optional[str] = Field(alias="EngineAssociation", default=None)
    category: Optional[str] = Field(alias="Category", default=None)
    description: Optional[str] = Field(alias="Description",default=None)
    modules: Optional[list[AddedModule]] = Field(alias="Modules", default=None)
    plugins: Optional[list[AddedPlugin]] = Field(alias="Plugins", default=None)
