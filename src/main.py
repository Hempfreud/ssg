import os
import shutil
import sys

from copystatic import copy_static
from gencontent import generate_pages_recursive

default_basepath = "/"

def main():
    basepath = default_basepath
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    print("Deleting docs directory...")
    if os.path.exists("docs"):
        shutil.rmtree("docs")

    print("Copying static files to docs directory...")
    copy_static("static", "docs")

    generate_pages_recursive("content", "template.html", "docs", basepath)

if __name__ == "__main__":
    main()
