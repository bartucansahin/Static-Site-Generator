import re
from textnode import TextNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result_list = []

    for node in old_nodes:
        if not hasattr(node, 'text') or not hasattr(node, 'text_type'):
            raise ValueError("Each node must have at least two attributes: text, text_type")
        if not isinstance(node, TextNode):
            old_nodes.append(node)
            continue
        if node.text_type in ["bold", "italic", "code", "image", "link"]:
            result_list.append(node)
            continue

        text = node.text
        segments = text.split(delimiter)

        for index, segment in enumerate(segments):
            if segment:
                if ((text.startswith(delimiter) and text.count(delimiter) == 1) or (text.endswith(delimiter) and text.count(delimiter) == 1)):
                    raise ValueError("Delimiter is the only one in the segment: " + segment)
                if index % 2 == 0:
                    result_list.append(TextNode(segment, "text"))
                else:
                    result_list.append(TextNode(segment, text_type))
            else:
                pass

    return result_list

def extract_markdown_images(text):
    pattern = r"!\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_links(text):
    pattern = r"\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    return matches

def split_nodes_image(old_nodes):
    result_list = []

    for nodes in old_nodes:
        if not isinstance(nodes, TextNode):
            raise ValueError("Node has to be an instance of TextNode")

        text = nodes.text
        extracted_md_images = extract_markdown_images(text)

        if not extracted_md_images:
            result_list.append(nodes)
            continue

        start_index = 0

        for alt_text, url in extracted_md_images:
            img_start_index = text.find(f"![{alt_text}]({url})", start_index)
            if img_start_index == -1:
                result_list.append(TextNode(text[start_index:], "text"))
                break
            if img_start_index > start_index:
                result_list.append(TextNode(text[start_index:img_start_index] , "text"))
            result_list.append(TextNode(f"![{alt_text}]", "image", {"src": url, "alt": alt_text}))
            start_index = img_start_index + len(f"![{alt_text}]({url})")
        if start_index < len(text):
            result_list.append(TextNode( text[start_index:], "text"))

    return result_list

def split_nodes_link(old_nodes):
    result_list = []

    for node in old_nodes:
        if not isinstance(node, TextNode):
            raise ValueError("Node has to be an instance of TextNode")

        text = node.text
        extracted_md_links = extract_markdown_links(text)

        if not extracted_md_links:
            result_list.append(node)
            continue

        start_index = 0

        for alt_text, url in extracted_md_links:
            link_start_index = text.find(f"[{alt_text}]({url})", start_index)
            if link_start_index == -1:
                result_list.append(TextNode(text[start_index:], "text"))
                break
            if link_start_index > start_index:
                result_list.append(TextNode(text[start_index:link_start_index] , "text"))
            result_list.append(TextNode(f"[{alt_text}]", "link", {"href": url}))
            start_index = link_start_index + len(f"[{alt_text}]({url})")

        if start_index < len(text):
            result_list.append(TextNode( text[start_index:], "text"))

    return result_list

def text_to_textnodes(text):
    result_list = []
    original_text_node = TextNode(text, "text", url=None)
    
    result_list.extend(split_nodes_delimiter([original_text_node], "**", "bold"))

    italic_list = []
    for nodes in result_list:
        italic_list.extend(split_nodes_delimiter([nodes], "*", "italic"))
   
    
    code_list = []
    for nodes in italic_list:
        code_list.extend(split_nodes_delimiter([nodes], "`", "code"))
    

    image_list = []
    for nodes in code_list:
        image_list.extend(split_nodes_image([nodes]))
    

    link_list = []
    for nodes in image_list :
        link_list.extend(split_nodes_link([nodes]))
    
    return link_list
