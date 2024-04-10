from block_markdown import markdown_to_HTMLNode


def extract_title(markdown):
    with open(markdown, "r") as md_file:
        file_contents = md_file.read()
    splitted_on_lines = file_contents.split("\n")
    if splitted_on_lines[0].startswith("# "):
        return splitted_on_lines[0].strip("# ")
    raise Exception("All pages need a h1 header")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    try:
        with open(from_path, "r") as from_file:
            markdown_content = from_file.read()

        with open(template_path, "r") as template_file:
            template_content = template_file.read()

        html_content = markdown_to_HTMLNode(markdown_content)
        title = extract_title(from_path)

        new_content = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html_content)

        with open(dest_path, "w") as dest_file:
            dest_file.write(new_content)

    except FileNotFoundError:
        raise Exception("File not found.")
    except Exception as e:
        raise Exception(f"Error generating page: {e}")

    