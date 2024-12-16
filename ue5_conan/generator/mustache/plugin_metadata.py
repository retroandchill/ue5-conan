import os
from pathlib import PurePosixPath, Path
from typing import TypedDict

from conans.model.conanfile_interface import ConanFileInterface


class IncludeDir(TypedDict):
    dirname: str

def make_include_dir(base: Path, dirname: str) -> IncludeDir:
    return {
        'dirname': os.path.relpath(dirname, base).replace(os.path.sep, '/')
    }

class LinkLibrary(TypedDict):
    library_name: str

def make_link_library(base: Path, library_name: str) -> LinkLibrary:
    return {
        'library_name': os.path.relpath(library_name, base).replace(os.path.sep, '/')
    }

class SharedLibrary(TypedDict):
    library_name: str
    simple_name: str
    index: int

def make_shared_library(base: Path, library_name: str) -> SharedLibrary:
    full_path = os.path.relpath(library_name, base).replace(os.path.sep, '/')
    return {
        "library_name": full_path,
        'simple_name': os.path.basename(full_path) if full_path.endswith('.dll') else full_path,
        'index': 0
    }

class PluginMetadata(TypedDict):
    plugin_name: str
    library_plugin_name: str
    version_name: str
    description: str
    link_shared: bool
    with_wrapper: bool
    include_dirs: list[IncludeDir]
    link_libraries: list[LinkLibrary]
    shared_libraries: list[SharedLibrary]