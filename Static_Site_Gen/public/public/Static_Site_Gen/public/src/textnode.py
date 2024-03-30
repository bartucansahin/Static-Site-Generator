from htmlnode import LeafNode

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    

    def __eq__(self, other):
        if isinstance(other, TextNode):
            return (self.text, self.text_type, self.url) == (other.text, other.text_type, other.url)
        return False
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
    
def text_node_to_html_node(text_node):
    verified_types = ["text", "bold", "italic", "code", "link", "image"]

    if not isinstance(text_node, TextNode):
        raise TypeError("Input must be an instance of TextNode")
    if text_node.text_type not in verified_types:
        raise ValueError("Invalid text type for TextNode instance")
    if text_node.text_type == "text" and not text_node.text:
        raise ValueError("Empty text content for a TextNode's text instance")
    if text_node.text_type == "link" and not text_node.url:
        raise ValueError("Link instance must have a URL")

    tag_mapping = {
        "text": ("", text_node.text, {}),
        "bold": ("b", text_node.text, {}),
        "italic": ("i", text_node.text, {}),
        "code": ("code", text_node.text, {}),
        "link": ("a", text_node.text, {"href": text_node.url["href"]} if text_node.text_type == "link" else {}),
        "image": ("img", "", {"src": text_node.url["src"], "alt": text_node.url["alt"]} if text_node.text_type == "image" else {}),
    }
    
    tag_name, content, attributes = tag_mapping[text_node.text_type]
    return LeafNode(tag_name, content, attributes if attributes else None)


