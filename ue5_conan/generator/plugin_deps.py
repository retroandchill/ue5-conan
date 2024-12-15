import json
import os
import re
from typing import Optional

from conan.tools.files import copy
from conans.model.conan_file import ConanFile
from conans.model.conanfile_interface import ConanFileInterface

from ue5_conan.files.project_structure import get_plugins_folder, find_plugin_name


class UnrealPluginDeps:
    def __init__(self, conanfile: ConanFile):
        self.conanfile = conanfile
        self.project_folder = self.conanfile.build_folder
        self.mark_precompiled = False

    def generate(self):
        plugins_folder = get_plugins_folder(self.project_folder)
        for require, dependency in self.conanfile.dependencies.items():
            plugin_name = find_plugin_name(dependency.package_folder)
            destination = os.path.join(plugins_folder, plugin_name)
            copy(self.conanfile, "*", dst=destination, src=dependency.package_folder)
            self.mark_dependencies_as_precompiled(destination)

    def mark_dependencies_as_precompiled(self, package_folder: str):
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
                    raise ValueError('Could not find assembly declaration!')

                index = match.span(0)[1]
                content = content[:index] + os.linesep + 'bUsePrecompiled = true;' + os.linesep + content[index:]
                with open(os.path.join(dirpath, file), 'w') as f:
                    f.write(content)

