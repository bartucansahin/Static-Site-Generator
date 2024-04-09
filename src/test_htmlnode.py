import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node1 = HTMLNode(tag='div', value='Hello, world!', children=[], props={'class': 'container'} )
        node2 = HTMLNode(tag='a', value='Click me', children=[], props={'href': 'https://www.google.com', 'target': '_blank'} )


class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        node3 = LeafNode("p", "This is a paragraph of text.")
        node4 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})


class TestParentNode(unittest.TestCase):
    def test_nested_parent_nodes_with_attrs(self): #testing nested ParentNodes with attributes
        inner_node = ParentNode(
            "strong",
            [
                LeafNode("span", "Inner Bold text", {"class": "bold-text"}),
                LeafNode("span", "Inner Normal text", {"class": "normal-text"}),
            ],
        )
        outer_node = ParentNode(
            "div",
            [
                LeafNode("p", "Outer Normal text", {"class": "outer-paragraph"}),
                inner_node,
                LeafNode("p", "Outer Normal text", {"class": "outer-paragraph"}),
            ],
        )
        expected_html = '<div><p class="outer-paragraph">Outer Normal text</p><strong><span class="bold-text">Inner Bold text</span><span class="normal-text">Inner Normal text</span></strong><p class="outer-paragraph">Outer Normal text</p></div>'
        self.assertEqual(outer_node.to_html(), expected_html)

    def test_non_html_node_children(self): #testing another type of node than accepted
        class NonHTMLNode:
            pass
        with self.assertRaises(TypeError):
            node = ParentNode(
                "div",
                [
                    LeafNode("p", "Valid HTML content"),
                    NonHTMLNode(),
                    LeafNode("span", "Another valid HTML content"),
                ],
            )

    
    def test_to_html(self): #testing the method in a simpler way
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        expected_html = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(node.to_html(), expected_html)

    def test_invalid_children(self): #Testing invalid children
        with self.assertRaises(ValueError):
            node = ParentNode("div", [])

    def test_invalid_tag(self): #Testing invalid tags
        with self.assertRaises(ValueError):
            node = ParentNode(None, [LeafNode("span", "Text")])

