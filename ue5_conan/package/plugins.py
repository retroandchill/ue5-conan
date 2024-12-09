import os

from conan.tools.files import copy
from conans.model.conan_file import ConanFile

from ue5_conan.files.project_structure import BUILD_FOLDERS, SOURCE_FOLDERS


def package_plugin(conanfile: ConanFile):
    copy(conanfile, 'LICENSE', dst=conanfile.package_folder, src=conanfile.source_folder)
    copy(conanfile, '*.uplugin', dst=conanfile.package_folder, src=conanfile.source_folder)
    for folder in SOURCE_FOLDERS:
        copy(conanfile, '*', dst=os.path.join(conanfile.package_folder, folder),
             src=os.path.join(conanfile.source_folder, folder))
    for folder in BUILD_FOLDERS:
        copy(conanfile, '*', dst=os.path.join(conanfile.package_folder, folder),
             src=os.path.join(conanfile.build_folder, folder))