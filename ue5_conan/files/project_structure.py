import os

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
    print(base)
    for dirpath, dirnames, filenames in os.walk(base):
        print(dirpath)
        if f'{plugin_name}.uplugin' in filenames:
            return dirpath

    raise FileNotFoundError(f'Could not find {plugin_name}.uplugin')

def find_uproject_file(project_folder: str, project_name: str):
    return os.path.join(project_folder, f'{project_name}.uproject')

