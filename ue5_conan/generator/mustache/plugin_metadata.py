import os
from pathlib import PurePosixPath, Path
from typing import TypedDict


class IncludeDir(TypedDict):
    dirname: str

def make_include_dir(base: Path, dirname: str) -> IncludeDir:
    return {
        "dirname": str(PurePosixPath(os.path.relpath(dirname, base)))
    }

class PluginMetadata(TypedDict):
    plugin_name: str
    version_name: str
    description: str
    link_shared: bool
    include_dirs: list[IncludeDir]