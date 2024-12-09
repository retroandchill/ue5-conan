import json
import os
from conan.tools.files import copy

from conan import ConanFile

from ue5_conan.files.json.added_plugin import AddedPlugin
from ue5_conan.files.json.uproject_file import UProjectFile
from ue5_conan.files.project_structure import get_plugins_folder, find_plugin_path, find_uproject_file, \
    create_plugin_path
from ue5_conan.files.template_files import get_template_file, BLANK_TEMPLATE_NAME


class UnrealPluginToolchain:
    def __init__(self, conanfile: ConanFile, plugin_name: str):
        self.conanfile = conanfile
        self.plugin_name = str(plugin_name)

    def generate(self):
        templates_path = get_template_file(self.conanfile.options.ue_install_location)
        temp_project_folder = self.get_build_folder()
        copy(self.conanfile, "*", dst=temp_project_folder, src=templates_path)

        target_plugin_directory = create_plugin_path(temp_project_folder, self.plugin_name)
        copy(self.conanfile, "*", dst=target_plugin_directory, src=self.conanfile.source_folder)

        uproject_file = find_uproject_file(temp_project_folder, BLANK_TEMPLATE_NAME)
        with open(uproject_file, 'r') as f:
            content = UProjectFile.model_validate(json.load(f))

        content.engine_association = str(self.conanfile.options.ue_version)
        content.plugins.append(AddedPlugin.model_construct(name=self.plugin_name, enabled=True))

        with open(uproject_file, 'w') as f:
            json.dump(content.model_dump(exclude_none=True, by_alias=True), f, indent=4)

    def get_build_folder(self):
        return os.path.join(self.conanfile.build_folder, "Build")