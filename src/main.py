import os
import shutil

def main():
    if os.path.exists("public"):
        shutil.rmtree("public")
    elif not os.path.exists("public"):
        os.mkdir("public")
    shutil.copytree("static", "public")

main()