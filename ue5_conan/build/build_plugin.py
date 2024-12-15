import os
import subprocess

from conan import ConanFile
from conan.errors import ConanException
from conan.tools.files import copy, rmdir

from ue5_conan.files.build_tools import get_unreal_build_tool_path
from ue5_conan.files.project_structure import get_build_folder, find_uproject_file, find_plugin_path, BUILD_FOLDERS


class UnrealPlugin:
    CONFIGS = [
        ('UnrealEditor', 'Development'),
        ('UnrealGame', 'Development'),
        ('UnrealGame', 'Shipping')
    ]

    def __init__(self, conanfile: ConanFile, plugin_name: str):
        self.conanfile = conanfile
        self.plugin_name = plugin_name

    def build(self):
        build_tool = get_unreal_build_tool_path(self.conanfile.options.ue_install_location,
                                                self.conanfile.settings.os)
        temp_project_folder = get_build_folder(self.conanfile.build_folder)
        project_path = find_uproject_file(temp_project_folder, 'HostProject')
        plugin_path = os.path.join(find_plugin_path(temp_project_folder, self.plugin_name),
                                   f'{self.plugin_name}.uplugin')
        for target, config in self.CONFIGS:
            base_cmd = [build_tool, target, str(self.conanfile.options.platform),
                        config, f'-Project={project_path}', f'-Plugin={plugin_path}',
                        '-BuildPluginAsLocal', '-NoUBTMakefiles', '-NoHotReload',
                        '-ForceUnity', '-DisableAdaptiveUnity']
            result = subprocess.run(base_cmd)

            if result.returncode != 0:
                raise ConanException("Build failed")


        target_plugin_directory = find_plugin_path(temp_project_folder, self.plugin_name)
        for folder in BUILD_FOLDERS:
            copy(self.conanfile, '*', dst=os.path.join(self.conanfile.build_folder, folder),
                 src=os.path.join(target_plugin_directory, folder))