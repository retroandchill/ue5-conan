import json
import os
import re
from typing import Optional, LiteralString

from conan.tools.files import copy
from conans.model.conan_file import ConanFile
from conans.model.conanfile_interface import ConanFileInterface

from ue5_conan.files.json.added_plugin import AddedPlugin
from ue5_conan.files.json.uproject_file import UProjectFile
from ue5_conan.files.project_structure import get_plugins_folder, find_plugin_name, find_uproject_file, \
    generate_plugin_name
from ue5_conan.generator.third_party_plugin import ThirdPartyPlugin


def plugin_already_in_list(uproject: UProjectFile, plugin_name: str):
    for plugin in uproject.plugins:
        if plugin.name == plugin_name:
            return True

    return False


class UnrealPluginDeps:
    def __init__(self, conanfile: ConanFile):
        self.conanfile = conanfile
        self.project_folder = self.conanfile.build_folder
        self.mark_precompiled = False
        self.wrap_external_dependencies = False
        self.plugin_names: dict[str, str] = {}

    def generate(self):
        plugins_folder = os.path.join(get_plugins_folder(self.project_folder), '.conan')

        uproject_file = find_uproject_file(self.project_folder)
        with open(uproject_file, 'r') as f:
            content = UProjectFile.model_validate(json.load(f))

        for require, dependency in self.conanfile.dependencies.items():
            plugin_name = find_plugin_name(dependency.package_folder)
            if plugin_name is not None:
                destination = os.path.join(plugins_folder, plugin_name)
                copy(self.conanfile, "*", dst=destination, src=dependency.package_folder)
                self.mark_dependencies_as_precompiled(destination)
            else:
                plugin_name = self.get_third_party_plugin_name(dependency)
                plugin_generator = ThirdPartyPlugin(plugin_name, dependency, self.wrap_external_dependencies)
                destination = os.path.join(plugins_folder, plugin_name)
                plugin_generator.generate(self.conanfile, destination)

            if not plugin_already_in_list(content, plugin_name):
                content.plugins.append(AddedPlugin.model_construct(name=plugin_name, enabled=True))

        with open(uproject_file, 'w') as f:
            json.dump(content.model_dump(exclude_none=True, by_alias=True), f, indent=4)

    def get_third_party_plugin_name(self, dependency: ConanFileInterface):
        if dependency.ref.name in self.plugin_names:
            return self.plugin_names[dependency.ref.name]

        return generate_plugin_name(dependency.ref.name)

    def mark_dependencies_as_precompiled(self, package_folder: LiteralString):
        if not self.mark_precompiled:
            return

        for dirpath, dirnames, files in os.walk(package_folder):
            for file in files:
                if not file.endswith('.Build.cs'):
                    continue

                with open(os.path.join(dirpath, file), 'r') as f:
                    content = f.read()

                match = re.search(r'public\s+\w+\s*\(\s*ReadOnlyTargetRules\s+(\w+)\s*\)\s*:\s*base\(\s*\1\s*\)\s*\{',
                                 content, re.MULTILINE)
                if match is None:
                    continue

                index = match.span(0)[1]
                content = content[:index] + os.linesep + 'bUsePrecompiled = true;' + os.linesep + content[index:]
                with open(os.path.join(dirpath, file), 'w') as f:
                    f.write(content)

