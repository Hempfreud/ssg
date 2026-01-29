import shutil
import os

def copy_static(src, dst):
    if not os.path.exists(dst):
        os.makedirs(dst)

    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        print(f" * {s} -> {d}")
        if os.path.isdir(s):
            copy_static(s, d)
        elif os.path.isfile(s):
            shutil.copy(s, d)
                