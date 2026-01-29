import os
import shutil

from copystatic import copy_static
from gencontent import generate_page, generate_pages_recursive

def main():
    print("Deleting public directory...")
    if os.path.exists("public"):
        shutil.rmtree("public")

    print("Copying static files to public directory...")
    copy_static("static", "public")

    generate_pages_recursive("content", "template.html", "public")

if __name__ == "__main__":
    main()
