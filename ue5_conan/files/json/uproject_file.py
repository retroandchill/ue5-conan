from pydantic import BaseModel, Field

from ue5_conan.files.json.added_module import AddedModule
from ue5_conan.files.json.added_plugin import AddedPlugin

class UProjectFile(BaseModel):
    file_version: int = Field(alias="FileVersion")
    engine_association: str = Field(alias="EngineAssociation")
    category: str = Field(alias="Category")
    description: str = Field(alias="Description")
    modules: list[AddedModule] = Field(alias="Modules")
    plugins: list[AddedPlugin] = Field(alias="Plugins")
