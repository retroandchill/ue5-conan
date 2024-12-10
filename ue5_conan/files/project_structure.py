import os
from typing import Optional

SOURCE_FOLDERS = ['Config', 'Resources', 'Source']
BUILD_FOLDERS = ['Binaries', 'Intermediate']

def get_build_folder(root_dir: str):
    return os.path.join(root_dir, 'Build')

def get_plugins_folder(project_folder: str):
    return os.path.join(project_folder, 'Plugins')

def create_plugin_path(project_folder: str, plugin_name: str):
    return os.path.join(get_plugins_folder(project_folder), plugin_name)

def find_plugin_path(project_folder: str, plugin_name: str):
    base = get_plugins_folder(project_folder)
    for dirpath, dirnames, filenames in os.walk(base):
        if f'{plugin_name}.uplugin' in filenames:
            return dirpath

    raise FileNotFoundError(f'Could not find {plugin_name}.uplugin')

def find_uproject_file(project_folder: str, project_name: Optional[str] = None):
    if project_name is not None:
        return os.path.join(project_folder, f'{project_name}.uproject')

    for dirpath, dirnames, filenames in os.walk(project_folder):
        for filename in filenames:
            if filename.endswith('.uproject'):
                return os.path.join(dirpath, filename)

def find_plugin_name(plugin_folder: str):
    for dirpath, dirnames, filenames in os.walk(plugin_folder):
        for filename in filenames:
            if filename.endswith('.uplugin'):
                return os.path.basename(filename).removesuffix('.uplugin')

    raise FileNotFoundError('Could not find any .uplugin files!')