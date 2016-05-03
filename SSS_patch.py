# encoding: utf-8

"""
    Bugfix 3dsmax MentalRay 'subsurface.mi' file

    To apply: Start the 'SSS_patch.cmd' as admin!

    Written 2016 by Jens Diemer
    Open Source licenced under GPL v3+

    more info:
    http://forums.autodesk.com/t5/3ds-max-3ds-max-design-general/max-2016-backburner-renders-slower-update/m-p/6206899#M111981
"""

from __future__ import print_function

__version__="1.1"

import os
import re
import difflib
import shutil


MI_FILEPATH = os.path.join(
    os.path.expandvars("%ProgramW6432%"),
    "Autodesk\\3ds Max 2016\\NVIDIA\\shaders_standard\\mentalray\\include\\subsurface.mi",
)
TRIGGER='shader "env_shader" "misss_call_shader"'
SOURCE_RE = re.compile(
    '(?P<prefix>'
    'shader "env_shader" "misss_call_shader" \(\s*?'
    '"shader" = interface "[r|s]\.environment")'
    '(?P<suffix>\s*?\))'
)
REPLACE_STRING=(
    '\g<prefix>,\n'
    '        "mode" 4'
    '\g<suffix>'
)


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

    try:
        with open(filepath, "w") as f:
            f.write(new_content)
    except IOError as err:
        print("Save new content error:\n%s" % err)
        print("\nNote: You must start this script via Admin rights!\n")
        return
    else:
        print("New content Saved to:")
        print(filepath)


if __name__ == "__main__":
    patch(MI_FILEPATH, TRIGGER, SOURCE_RE, REPLACE_STRING)