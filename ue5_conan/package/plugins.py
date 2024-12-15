import json
import os
from typing import Optional

from conan.tools.files import copy
from conans.model.conan_file import ConanFile

from ue5_conan.files.project_structure import BUILD_FOLDERS, SOURCE_FOLDERS


def package_plugin(conanfile: ConanFile, source_folder: Optional[str] = None):
    if source_folder is None:
        source_folder = conanfile.source_folder
    copy(conanfile, 'LICENSE', dst=conanfile.package_folder, src=source_folder)
    plugins = copy(conanfile, '*.uplugin', dst=conanfile.package_folder, src=source_folder)
    for plugin in plugins:
        with open(plugin, 'r') as f:
            content = json.load(f)

        content['Installed'] = True

        with open(plugin, 'w') as f:
            json.dump(content, f, indent=4)

    for folder in SOURCE_FOLDERS:
        copy(conanfile, '*', dst=os.path.join(conanfile.package_folder, folder),
             src=os.path.join(source_folder, folder))
    for folder in BUILD_FOLDERS:
        copy(conanfile, '*', dst=os.path.join(conanfile.package_folder, folder),
             src=os.path.join(conanfile.build_folder, folder))