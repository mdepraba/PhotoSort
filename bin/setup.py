import sys
from cx_Freeze import setup, Executable

base = None
base = "Win32GUI"

options = {
    "build_exe": {
        "includes": ["photo_manager"],
        "packages": ["os"],
        "include_files": ["photosort/photo_manager.py"]
    }
}

setup(
    name="PhotoSort",
    version="1.0",
    description="Aplikasi Pengorganisir Foto",
    executables=[Executable("photosort/gui.py", base=base, target_name="photosort")]
)
