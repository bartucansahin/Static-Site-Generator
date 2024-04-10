import os
import shutil
from gencontent import generate_page

def main():
    if os.path.exists("public"):
        shutil.rmtree("public")
    elif not os.path.exists("public"):
        os.mkdir("public")
    shutil.copytree("static", "public")

    generate_page("content/index.md", "template.html", "public/index.html")

main()