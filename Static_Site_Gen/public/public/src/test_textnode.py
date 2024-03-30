import unittest

from textnode import TextNode, text_node_to_html_node
from htmlnode import LeafNode


class TestTextNode(unittest.TestCase):

    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_one_node_url_none(self):
        node1 = TextNode("Hello", "heading", None)
        node2 = TextNode("Hello", "heading", "https://example.com")
        self.assertNotEqual(node1, node2)

class TestTextNodeToHtmlNode(unittest.TestCase):

    def test_valid_text_node(self): #testing text type of TextNode instance
        text_node = TextNode("Hello", "text")
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)

    def test_invalid_text_node_type(self): #testing an invalid type
        with self.assertRaises(TypeError):
            text_node_to_html_node("invalid")

    def test_link_node(self): #testing link type of TextNode instance
        link_node = TextNode("OpenAI", "link", url={"href": "https://openai.com"})
        html_node = text_node_to_html_node(link_node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.props["href"], "https://openai.com")

    def test_image_type(self): #testing image type of TextNode instance
        image_node = TextNode(text_type="image", text="", url={"src": "example.jpg", "alt": "Example Image"})
        html_node = text_node_to_html_node(image_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, 'img')
        self.assertEqual(html_node.props['src'], 'example.jpg')
        self.assertEqual(html_node.props['alt'], 'Example Image')

    def test_empty_text_node(self): #testing an empty text type of TextNode instance
        empty_node = TextNode("", "text")
        with self.assertRaises(ValueError) as context:
            html_node = text_node_to_html_node(empty_node)
        self.assertEqual(str(context.exception), "Empty text content for a TextNode's text instance")

if __name__ == "__main__":
    unittest.main()
