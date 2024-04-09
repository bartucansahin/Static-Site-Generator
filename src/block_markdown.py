from htmlnode import HTMLNode, ParentNode, LeafNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node
from htmlnode import HTMLNode, ParentNode, LeafNode

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered = "unordered list"
block_type_ordered = "ordered list"

def markdown_to_blocks(markdown):
    lines = markdown.strip().split("\n")
    
    blocks = []
    current_block = ""
    for line in lines:
        line = line.strip()
        if line:
            current_block += line + "\n"
        else:
            if current_block:
                blocks.append(current_block.strip())
                current_block = ""

    if current_block:
        blocks.append(current_block.strip())
    
    return blocks

def block_to_block_type(md_block):
    if any(md_block.startswith(prefix) for prefix in ("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return block_type_heading
    
    if md_block.startswith("```") and md_block.endswith("```"):
        return block_type_code
    
    split = md_block.split("\n")
    for line in split:
        if line.startswith(">"):
            return block_type_quote
    
    for line in split:
        if any(line.startswith(prefix) for prefix in ("* ", "- ")):
            return block_type_unordered
    
    integer = 1
    is_ordered_list = False
    for line in split:
        if line.startswith(f"{integer}."):
            is_ordered_list = True
        integer += 1
    
    if is_ordered_list:
        return block_type_ordered
    
    return block_type_paragraph

def from_mdBlock_to_HTMLNode(md_block, block_type):
    html_nodes = []
    
    if isinstance(md_block, str):
        md_block = [md_block]
    
    if block_type == block_type_paragraph:
        leaf_node = LeafNode(None, md_block[0], None)
        html_nodes.append(ParentNode("p", [leaf_node], None))
    
    elif block_type == block_type_quote:
        leaf_node = LeafNode(None, md_block[0][1:].strip(), None)
        html_nodes.append(ParentNode("blockquote", [leaf_node], None))

    elif block_type == block_type_unordered:
        li_wrapped = []
        for block in md_block:
            lines = block.split('\n')
            for line in lines:
                new_line = line[1:].strip()
                li_wrapped.append(LeafNode("li", new_line))
        html_nodes.append(ParentNode("ul", li_wrapped))

    elif block_type == block_type_ordered:
        li_wrapped = []
        for block in md_block:
            lines = block.split('\n')
            for line in lines:
                if '.' in line:
                    new_line = line[line.index('.') + 1:].strip()
                    li_wrapped.append(LeafNode("li", new_line))
        html_nodes.append(ParentNode("ol", li_wrapped))

    elif block_type == block_type_code:
        for block in md_block:
            new_block = block.strip("```")
            pre_covered = LeafNode("pre", new_block)
            html_nodes.append(ParentNode("code", [pre_covered]))
    
    elif block_type == block_type_heading:
        heading_prefixes = {
            "# ": "h1",
            "## ": "h2",
            "### ": "h3",
            "#### ": "h4",
            "##### ": "h5",
            "###### ": "h6"
        }
        for prefix, tag in heading_prefixes.items():
            for block in md_block:
                if block.startswith(prefix):
                    block = block[len(prefix):]
                    leaf_node = LeafNode(None, block, None)
                    html_nodes.append(ParentNode(tag, [leaf_node], None))

    return html_nodes


    
def markdown_to_HTMLNode(markdown):
    block_by_block = markdown_to_blocks(markdown)
    children = []
    inline_leaf_nodes = []
    leaf_nodes_to_html = ""
    for block in block_by_block:
        text_nodes = text_to_textnodes(block)
        inline_leaf_nodes = [text_node_to_html_node(text_node) for text_node in text_nodes]
        leaf_nodes_to_html += ''.join(leaf_node.to_html() for leaf_node in inline_leaf_nodes) + "\n\n"


    new_blocks = markdown_to_blocks(leaf_nodes_to_html)
    for new_block in new_blocks:
        block_type = block_to_block_type(new_block)
        children.extend(from_mdBlock_to_HTMLNode(new_block, block_type))
    return ParentNode("div", children).to_html()
    

    