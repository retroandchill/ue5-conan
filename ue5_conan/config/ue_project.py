import os
import re

from conan import ConanFile


def configure_ue_base_dir(conanfile: ConanFile):
    if conanfile.settings.os == "Windows":
        epic_games_path = os.path.join(os.environ["ProgramFiles"], "Epic Games")
    elif conanfile.settings.os == "macOS":
        epic_games_path = os.path.join("Users", "Shared", "Epic Games")
    else:
        raise FileNotFoundError(
            f"Can't detect the engine installation for the following platform: {conanfile.settings.os}")
    if conanfile.options.ue_version == None:
        versions = []
        for entry in os.scandir(epic_games_path):
            if not entry.is_dir():
                continue

            match = re.match(r'UE_(\d+\.\d+)', entry.name)
            if match is not None:
                versions.append(match.group(1))

        if len(versions) == 0:
            raise FileNotFoundError(f"Could not find engine installation in directory: {epic_games_path}")

        versions.sort(reverse=True)
        conanfile.options.ue_version = versions[0]
    conanfile.options.ue_install_location = os.path.join(epic_games_path, f"UE_{conanfile.options.ue_version}")

def configure_default_platform(conanfile: ConanFile):
    if conanfile.settings.os == "Windows":
        if conanfile.settings.arch == "x86_64":
            conanfile.options.platform = "Win64"
        elif conanfile.settings.arch == "x86":
            conanfile.options.platfrom = "Win32"
        else:
            raise ValueError(f"Invalid windows architecture: {conanfile.settings.arch}")

def configure_unreal_package(conanfile: ConanFile):
    if conanfile.options.ue_install_location == None:
        configure_ue_base_dir(conanfile)

    if conanfile.options.platform == None:
        configure_default_platform(conanfile)