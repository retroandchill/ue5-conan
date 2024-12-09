import os


def get_unreal_build_tool_folder(install_dir: str):
    return os.path.join(str(install_dir), 'Engine', 'Binaries', 'DotNet', 'UnrealBuildTool')

def get_unreal_build_tool_name(host_os: str):
    if host_os == 'Windows':
        return 'UnrealBuildTool.exe'

    raise NotImplementedError(f"Can't find the build tools for platform {host_os}")

def get_unreal_build_tool_path(install_dir: str, host_os: str):
    return os.path.join(get_unreal_build_tool_folder(install_dir), get_unreal_build_tool_name(host_os))