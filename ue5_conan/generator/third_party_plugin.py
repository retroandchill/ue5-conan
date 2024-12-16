import os
import shutil
from pathlib import Path
from typing import LiteralString

import pystache
from conan.errors import ConanException
from conan.tools.files import copy
from conans.model.conan_file import ConanFile
from conans.model.conanfile_interface import ConanFileInterface

from ue5_conan.files.resources import read_resource_file, get_resource_file
from ue5_conan.generator.mustache.plugin_metadata import PluginMetadata, make_include_dir, make_link_library, \
    make_shared_library, make_define

TEMPLATE_BASE_DIR = os.path.join('templates', 'ThirdPartyTemplate')


def fill_out_template(template: str, metadata: PluginMetadata, output_file: str):
    template_content = read_resource_file(template)
    render = pystache.render(template_content, metadata)
    Path(os.path.dirname(output_file)).mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(render)


class ThirdPartyPlugin:
    def __init__(self, name: str, package_info: ConanFileInterface, always_wrap: bool = False):
        self.name = name
        self.package_info = package_info
        self.always_wrap = always_wrap

    def generate(self, conanfile: ConanFile, dest: LiteralString | str):
        if os.path.exists(dest):
            shutil.rmtree(dest)

        shared = self.is_shared()
        with_wrapper = shared or self.always_wrap
        plugin_metadata: PluginMetadata = {
            'plugin_name': self.name,
            'library_plugin_name': f'{self.name}Library' if with_wrapper else self.name,
            'version_name': self.package_info.ref.version,
            'description': self.package_info.description,
            'link_shared': shared,
            'with_wrapper': with_wrapper,
            'include_dirs': list(map(lambda d: make_include_dir(self.package_info.package_path, d), self.package_info.cpp_info.includedirs)),
            'link_libraries': list(map(lambda d: make_link_library(self.package_info.package_path, d), self.get_link_libraries())),
            'shared_libraries': self.get_shared_library_paths(),
            'public_defines': list(map(make_define, self.package_info.cpp_info.defines)),
        }
        fill_out_template(os.path.join(TEMPLATE_BASE_DIR, 'ThirdPartyTemplate.uplugin.mustache'),
                                 plugin_metadata, os.path.join(dest, f'{self.name}.uplugin'))

        source_dir = os.path.join(TEMPLATE_BASE_DIR, 'Source')
        if with_wrapper:
            wrapper_dir = os.path.join(source_dir, 'ThirdPartyTemplate')
            fill_out_template(os.path.join(wrapper_dir, 'ThirdPartyTemplate.Build.cs.mustache'),
                                   plugin_metadata, os.path.join(dest, 'Source', self.name, f'{self.name}.Build.cs'))
            fill_out_template(os.path.join(wrapper_dir, 'Public', 'ThirdPartyTemplate.h.mustache'),
                                   plugin_metadata, os.path.join(dest, 'Source', self.name, 'Public', f'{self.name}.h'))
            fill_out_template(os.path.join(wrapper_dir, 'Private', 'ThirdPartyTemplate.cpp.mustache'),
                                   plugin_metadata, os.path.join(dest, 'Source', self.name, 'Private', f'{self.name}.cpp'))

        library_dir = os.path.join(source_dir, 'ThirdParty', 'ThirdPartyTemplateLibrary')
        library_output = os.path.join(dest, 'Source', 'ThirdParty', plugin_metadata['library_plugin_name'])
        fill_out_template(os.path.join(library_dir, 'ThirdPartyTemplateLibrary.Build.cs.mustache'),
                               plugin_metadata, os.path.join(library_output, f'{plugin_metadata["library_plugin_name"]}.Build.cs'))

        copy(conanfile, '*', dst=os.path.join(dest, 'Resources'),
             src=get_resource_file(os.path.join(TEMPLATE_BASE_DIR, 'Resources')))
        for include_dir in self.package_info.cpp_info.includedirs:
            copy(conanfile, '*', dst=os.path.join(library_output, os.path.basename(include_dir)),
                 src=include_dir)
        for lib_dir in self.package_info.cpp_info.bindirs:
            copy(conanfile, '*', dst=os.path.join(library_output, os.path.basename(lib_dir)), src=lib_dir)
        for lib_dir in self.package_info.cpp_info.libdirs:
            copy(conanfile, '*', dst=os.path.join(library_output, os.path.basename(lib_dir)), src=lib_dir)

    def get_shared_library_paths(self):
        result = []
        for lib in map(lambda d: make_shared_library(self.package_info.package_path, d), self.get_dynamic_link_libraries()):
            lib['index'] = len(result)
            result.append(lib)
        return result

    def is_shared(self):
        try:
            return self.package_info.options.shared
        except ConanException:
            return False

    def get_link_libraries(self):
        for lib_dir in self.package_info.cpp_info.libdirs:
            for dirpath, dirnames, files in os.walk(lib_dir):
                for file in files:
                    if not file.endswith('.lib') and not file.endswith('.a') and not file.endswith('.so'):
                        continue
                    yield os.path.join(dirpath, file)

    def get_dynamic_link_libraries(self):
        for lib_dir in self.package_info.cpp_info.bindirs:
            yield from self.find_dynamic_libraries_in_dir(lib_dir)

        for lib_dir in self.package_info.cpp_info.libdirs:
            yield from self.find_dynamic_libraries_in_dir(lib_dir)

    @staticmethod
    def find_dynamic_libraries_in_dir(lib_dir):
        for dirpath, dirnames, files in os.walk(lib_dir):
            for file in files:
                if not file.endswith('.dll') and not file.endswith('.so') and not file.endswith('.dylib'):
                    continue

                yield os.path.join(dirpath, file)
