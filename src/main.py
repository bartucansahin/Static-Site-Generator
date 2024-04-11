import os
import shutil
from gencontent import generate_pages_recursive

def main():
    if os.path.exists("public"):
        shutil.rmtree("public")
    elif not os.path.exists("public"):
        os.mkdir("public")
    shutil.copytree("static", "public")

    generate_pages_recursive("content", "template.html", "public")

main()