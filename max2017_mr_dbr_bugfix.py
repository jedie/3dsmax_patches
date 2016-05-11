# encoding: utf-8

"""
    Bugfix 3dsmax 2017 MentalRay DRB installation

    To apply: Start the 'max2017_mr_dbr_bugfix.cmd' as admin!

    Written 2016 by Jens Diemer
    Open Source licenced under GPL v3+

    more info:
    http://forums.autodesk.com/t5/3ds-max-3ds-max-design-general/max-2017-mr-drb-satellite-doesn-t-start/m-p/6281098
"""

from __future__ import print_function

__version__="1.2"

import os
import difflib
import shutil


SERVICE_FILEPATH = os.path.join(
    os.path.expandvars("%SystemRoot%"),
    "System32\\drivers\\etc\\services",
)

SERVICE_NAME_STRING="mi-raysat_3dsmax%s_64"
SERVICE_STRING=(
    'mi-raysat_3dsmax%(ver)s_64 %(tcp)s/tcp                          #mental ray Satellite for Autodesk 3ds Max %(ver)s'
)

RAYRC="""registry "{_MI_REG_LIBRARY}" value ".\Plugins\NVIDIA\Shaders\shaders_standard\mentalray\shaders;.\Plugins\NVIDIA\Shaders\shaders_3rdparty\mentalray\shaders;.\Plugins\NVIDIA\Shaders\shaders_autoload\mentalray\shaders" end registry'"""

AUTODESK_ROOT = os.path.join(os.path.expandvars("%ProgramW6432%"), "Autodesk")
MAX_2016_ROOT = os.path.join(AUTODESK_ROOT, "3ds Max 2016")
MAX_2017_ROOT = os.path.join(AUTODESK_ROOT, "3ds Max 2017")

RAYRC_2017_FILEPATH=os.path.join(MAX_2017_ROOT, "rayrc")

LIBMDL_DLL_SRC = os.path.join(
    MAX_2017_ROOT, "Plugins\\NVIDIA\\Bin\\satellite\\libmdl.dll"
)
LIBMDL_DLL_DST = os.path.join(MAX_2017_ROOT, "libmdl.dll")





def create_file(filepath, content):
    try:
        with open(filepath, "w") as f:
            f.write(content)
    except IOError as err:
        print("Save new content error:\n%s" % err)
        print("\nNote: You must start this script via Admin rights!\n")
        return
    else:
        print("content saved to:")
        print(filepath)


def print_diff(old_content, new_content, filepath):
    print("="*79)
    diff = difflib.unified_diff(
        old_content.splitlines(), new_content.splitlines(),
        fromfile="OLD: %s" % os.path.basename(filepath),
        tofile='NEW: %s' % os.path.basename(filepath),
        n=1, lineterm=""
    )
    print("\n".join(diff))
    print("="*79)


def copyfile(src, dst):
    print("\ncopy '%s' -> '%s'..." % (src, dst))
    try:
        shutil.copyfile(src, dst)
    except IOError as err:
        print("Error:\n%s" % err)
        print("\nNote: You must start this script via Admin rights!\n")
        return
    else:
        print("copy, ok.")


def create_backup(filepath):
    copyfile(filepath, filepath+".bak")


def write_content(filepath, content):
    print("\nWrite new content to '%s'..." % filepath)
    try:
        with open(filepath, "w") as f:
            f.write(content)
    except IOError as err:
        print("Error:\n%s" % err)
        print("\nNote: You must start this script via Admin rights!\n")
        return
    else:
        print("OK\n")


def _setup_services(max_version, tcp_port):
    service_name = SERVICE_NAME_STRING % max_version

    with open(SERVICE_FILEPATH, "r") as f:
        content = f.read()

    if service_name in content:
        print("service for max %s exists already, ok." % max_version)
        return

    new_content = content
    new_content += "\n"
    new_content += SERVICE_STRING % {"ver": max_version, "tcp": tcp_port}

    print_diff(content, new_content, SERVICE_FILEPATH)

    create_backup(SERVICE_FILEPATH)
    write_content(SERVICE_FILEPATH, new_content)


def setup_services():
    if os.path.isdir(MAX_2016_ROOT):
        print("Setup service for max 2016")
        _setup_services("2016", "7524")
    else:
        print("No max 2016 found, ok.")

    if os.path.isdir(MAX_2017_ROOT):
        print("Setup service for max 2017")
        _setup_services("2017", "7526")
    else:
        print("No max 2017 found!")


if __name__ == "__main__":
    setup_services()

    print("\nWrite 'rayrc' file...")
    create_file(RAYRC_2017_FILEPATH, RAYRC)

    copyfile(LIBMDL_DLL_SRC, LIBMDL_DLL_DST)

    print("\n--- END ---")