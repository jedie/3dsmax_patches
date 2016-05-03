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

__version__="1.1"

import os
import re
import difflib
import shutil


MI_FILEPATH = os.path.join(
    os.path.expandvars("%SystemRoot%"),
    "System32\\drivers\\etc\\services",
)
TRIGGER='mi-raysat_3dsmax2016_64'
SOURCE_RE = re.compile(
    '(mi-raysat_3dsmax2016_64\s+?7524/tcp\s+?#mental ray Satellite for Autodesk 3ds Max 2017)'
)
REPLACE_STRING=(
    'mi-raysat_3dsmax2017_64 7526/tcp                          #mental ray Satellite for Autodesk 3ds Max 2017'
)

RAYRC="""registry "{_MI_REG_LIBRARY}" value ".\Plugins\NVIDIA\Shaders\shaders_standard\mentalray\shaders;.\Plugins\NVIDIA\Shaders\shaders_3rdparty\mentalray\shaders;.\Plugins\NVIDIA\Shaders\shaders_autoload\mentalray\shaders" end registry'"""

MAX_ROOT = os.path.join(
    os.path.expandvars("%ProgramW6432%"), "Autodesk", "3ds Max 2017",
)
print("MAX_ROOT:", MAX_ROOT)
RAYRC_FILEPATH=os.path.join(MAX_ROOT, "rayrc")

LIBMDL_DLL_SRC = os.path.join(
    MAX_ROOT, "Plugins\\NVIDIA\\Bin\\satellite\\libmdl.dll"
)
LIBMDL_DLL_DST = os.path.join(MAX_ROOT, "libmdl.dll")


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


def patch(filepath, trigger_string, source_re, replace_string):
    print("Patch file: %s" % filepath)

    with open(filepath, "r") as f:
        content = f.read()

    trigger_count = content.count(trigger_string)
    print("Found %i trigger strings: %r" % (trigger_count, trigger_string))

    new_content, count = source_re.subn(REPLACE_STRING, content)
    print("Patch count:", count)

    if count==0:
        print("ERROR: Search text not found!")
        print("Already patched?!?")
        return

    if count!=trigger_count:
        print("WARNING: Wrong patch count!")

    print("="*79)
    diff = difflib.unified_diff(
        content.splitlines(), new_content.splitlines(),
        fromfile="OLD: %s" % os.path.basename(filepath),
        tofile='NEW: %s' % os.path.basename(filepath),
        n=1, lineterm=""
    )
    print("\n".join(diff))
    print("="*79)

    bak_filepath = filepath+".bak"
    if os.path.isfile(bak_filepath):
        print("\nBackup file exists: %s" % bak_filepath)
    else:
        print("\nCreate backup file...")
        try:
            shutil.copyfile(filepath, bak_filepath)
            with open(filepath, "w") as f:
                f.write(new_content)
        except IOError as err:
            print("Backup error:\n%s" % err)
            print("\nNote: You must start this script via Admin rights!\n")
            return
        else:
            print("Backup done: %s" % bak_filepath)

    print("\nWrite patched file...")
    create_file(filepath, new_content)

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




if __name__ == "__main__":
    patch(MI_FILEPATH, TRIGGER, SOURCE_RE, REPLACE_STRING)

    print("\nWrite 'rayrc' file...")
    create_file(RAYRC_FILEPATH, RAYRC)

    copyfile(LIBMDL_DLL_SRC, LIBMDL_DLL_DST)

    print("\n--- END ---")