from block_markdown import markdown_to_HTMLNode


def extract_title(markdown):
    with open(markdown, "r") as md_file:
        file_contents = md_file.read()
    splitted_on_lines = file_contents.split("\n")
    if splitted_on_lines[0].startswith("# "):
        return splitted_on_lines[0][1:].strip()
    raise Exception("All pages need a h1 header")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as from_path_file:
        from_path_file_contents = from_path_file.read()

    with open(template_path, "r") as template_file:
        template_path_file_cont = template_file.read()
    
    html = markdown_to_HTMLNode(from_path_file_contents)
    title = extract_title(from_path_file_contents)

    new_content = template_path_file_cont.replace("{{ Title }}", title).replace("{{ Content }}", html)
    

    