import json
import os
from xml.etree.ElementTree import ElementTree

from conan.tools.files import copy

from conan import ConanFile

from ue5_conan.files.json.added_plugin import AddedPlugin
from ue5_conan.files.json.uproject_file import UProjectFile
from ue5_conan.files.project_structure import find_uproject_file, create_plugin_path


class UnrealPluginToolchain:
    def __init__(self, conanfile: ConanFile, plugin_name: str):
        self.conanfile = conanfile
        self.plugin_folder = str(self.conanfile.source_folder)
        self.plugin_name = str(plugin_name)

    def generate(self):
        temp_project_folder = self.get_build_folder()
        os.mkdir(temp_project_folder)
        uproject = UProjectFile.model_construct(file_version=3,
                                                     plugins=[
                                                         AddedPlugin.model_construct(name=self.plugin_name, enabled=True)
                                                     ])
        uproject_file = find_uproject_file(temp_project_folder, 'HostProject')
        with open(uproject_file, 'w') as f:
            json.dump(uproject.model_dump(exclude_none=True, by_alias=True), f, indent=4)

        target_plugin_directory = create_plugin_path(temp_project_folder, self.plugin_name)
        copy(self.conanfile, "*", dst=target_plugin_directory, src=self.plugin_folder)


    def get_build_folder(self):
        return os.path.join(self.conanfile.build_folder, "Build")