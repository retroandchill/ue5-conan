import os
import shutil
from pathlib import Path
from typing import LiteralString

import pystache
from conan.tools.files import copy
from conans.model.conan_file import ConanFile
from conans.model.conanfile_interface import ConanFileInterface

from ue5_conan.files.resources import read_resource_file, get_resource_file
from ue5_conan.generator.mustache.plugin_metadata import PluginMetadata, make_include_dir

TEMPLATE_BASE_DIR = os.path.join('templates', 'ThirdPartyTemplate')


def fill_out_template(template: str, metadata: PluginMetadata, output_file: str):
    template_content = read_resource_file(template)
    render = pystache.render(template_content, metadata)
    Path(os.path.dirname(output_file)).mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(render)


class ThirdPartyPlugin:
    def __init__(self, name: str, package_info: ConanFileInterface):
        self.name = name
        self.package_info = package_info

    def generate(self, conanfile: ConanFile, dest: LiteralString | str):
        if os.path.exists(dest):
            shutil.rmtree(dest)


        plugin_metadata: PluginMetadata = {
            'plugin_name': self.name,
            'version_name': self.package_info.ref.version,
            'description': self.package_info.description,
            'link_shared': False,
            'include_dirs': list(map(lambda d: make_include_dir(self.package_info.package_path, d), self.package_info.cpp_info.includedirs))
        }
        fill_out_template(os.path.join(TEMPLATE_BASE_DIR, 'ThirdPartyTemplate.uplugin.mustache'),
                                 plugin_metadata, os.path.join(dest, f'{self.name}.uplugin'))

        source_dir = os.path.join(TEMPLATE_BASE_DIR, 'Source')
        wrapper_dir = os.path.join(source_dir, 'ThirdPartyTemplate')
        fill_out_template(os.path.join(wrapper_dir, 'ThirdPartyTemplate.Build.cs.mustache'),
                               plugin_metadata, os.path.join(dest, 'Source', self.name, f'{self.name}.Build.cs'))
        fill_out_template(os.path.join(wrapper_dir, 'Public', 'ThirdPartyTemplate.h.mustache'),
                               plugin_metadata, os.path.join(dest, 'Source', self.name, 'Public', f'{self.name}.h'))
        fill_out_template(os.path.join(wrapper_dir, 'Private', 'ThirdPartyTemplate.cpp.mustache'),
                               plugin_metadata, os.path.join(dest, 'Source', self.name, 'Private', f'{self.name}.cpp'))

        library_dir = os.path.join(source_dir, 'ThirdParty', 'ThirdPartyTemplateLibrary')
        library_output = os.path.join(dest, 'Source', 'ThirdParty', f'{self.name}Library')
        fill_out_template(os.path.join(library_dir, 'ThirdPartyTemplateLibrary.Build.cs.mustache'),
                               plugin_metadata, os.path.join(library_output, f'{self.name}Library.Build.cs'))

        print(os.path.join(TEMPLATE_BASE_DIR, 'Resources'))
        copy(conanfile, '*', dst=os.path.join(dest, 'Resources'),
             src=get_resource_file(os.path.join(TEMPLATE_BASE_DIR, 'Resources')))
        for include_dir in self.package_info.cpp_info.includedirs:
            copy(conanfile, '*', dst=os.path.join(library_output, 'include'),
                 src=include_dir)


