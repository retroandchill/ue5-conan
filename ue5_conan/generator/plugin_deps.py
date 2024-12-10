import json
import os

from conan.tools.files import copy
from conans.model.conan_file import ConanFile

from ue5_conan.files.json.added_plugin import AddedPlugin
from ue5_conan.files.json.uproject_file import UProjectFile
from ue5_conan.files.project_structure import get_plugins_folder, find_uproject_file, find_plugin_name


class UnrealPluginDeps:
    def __init__(self, conanfile: ConanFile):
        self.conanfile = conanfile
        self.project_folder = self.conanfile.build_folder

    def generate(self):
        plugins_folder = get_plugins_folder(self.project_folder)

        uproject_file = find_uproject_file(self.project_folder)
        with open(uproject_file, 'r') as f:
            content = UProjectFile.model_validate(json.load(f))

        for require, dependency in self.conanfile.dependencies.items():
            plugin_name = find_plugin_name(dependency.package_folder)
            print(dependency.package_folder)
            destination = os.path.join(plugins_folder, plugin_name)
            copy(self.conanfile, "*", dst=destination, src=dependency.package_folder)
            content.plugins.append(AddedPlugin.model_construct(name=plugin_name, enabled=True))

        with open(uproject_file, 'w') as f:
            json.dump(content.model_dump(exclude_none=True, by_alias=True), f, indent=4)