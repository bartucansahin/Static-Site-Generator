import unittest
from block_markdown import (markdown_to_blocks, block_to_block_type, block_type_code, block_type_heading, block_type_ordered,
block_type_paragraph, block_type_quote, block_type_unordered, from_mdBlock_to_HTMLNode, markdown_to_HTMLNode)
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestMarkdownToBlocks(unittest.TestCase):
    
    def setUp(self):
        self.markdown = (
            "# This is a heading\n\n"
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n"
            "* This is a list item\n"
            "* This is another list item"
        )
        self.expected_blocks = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is a list item\n* This is another list item"
        ]
    
    def test_markdown_to_blocks(self):
        blocks = markdown_to_blocks(self.markdown)
        self.assertEqual(blocks, self.expected_blocks)
    
    def test_empty_input(self):
        blocks = markdown_to_blocks('')
        self.assertEqual(blocks, [])

    def test_no_blocks(self):
        blocks = markdown_to_blocks('       \n\n\n\n\n\n       ')
        self.assertEqual(blocks, [])

class TestBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        md_block = "# This is a heading with multiple words and special characters *&^%$#@!"
        self.assertEqual(block_to_block_type(md_block), block_type_heading)
        
    def test_code(self):
        md_block = "```python\nprint('Hello, World!')\n```"
        self.assertEqual(block_to_block_type(md_block), block_type_code)
        
    def test_quote(self):
        md_block = "> This is a quote with multiple lines.\n> Here is the second line."
        self.assertEqual(block_to_block_type(md_block), block_type_quote)
        
    def test_unordered(self):
        md_block = "* Item 1\n* Item 2\n    * Nested Item 1\n    * Nested Item 2"
        self.assertEqual(block_to_block_type(md_block), block_type_unordered)
        
    def test_ordered(self):
        md_block = "1. Item 1\n2. Item 2\n    1. Nested Item 1\n    2. Nested Item 2\n 3. Nested Item 3"
        self.assertEqual(block_to_block_type(md_block), block_type_ordered)
        
    def test_paragraph(self):
        md_block = "This is a paragraph with multiple sentences. It contains punctuation marks such as commas, periods, and exclamation marks!"
        self.assertEqual(block_to_block_type(md_block), block_type_paragraph)
        
    def test_mixed(self):
        md_block = "# Heading\n```\nThis is a code block\n```> This is a quote\n* Unordered list\n1. Ordered list\nThis is a paragraph"
        self.assertEqual(block_to_block_type(md_block), block_type_heading)

class TestMarkdownConversion(unittest.TestCase):
    def test_paragraph_conversion(self):
        md_block = "This is a paragraph."
        expected_html = ParentNode(tag="p", children=[LeafNode(value="This is a paragraph.")])
        html_node = from_mdBlock_to_HTMLNode(md_block, block_type_paragraph)
        self.assertEqual(html_node, expected_html)

    def test_quote_conversion(self):
        md_block = ["> This is a quote."]
        expected_html = ParentNode(tag="blockquote", children=[LeafNode(value="This is a quote.")])
        html_node = from_mdBlock_to_HTMLNode(md_block, block_type_quote)
        self.assertEqual(html_node, expected_html)

    def test_unordered_list_conversion(self):
        md_block = ["* Item 1\n* Item 2\n* Item 3"]
        expected_html = ParentNode(tag="ul", children=[
            LeafNode(tag="li", value="Item 1"),
            LeafNode(tag="li", value="Item 2"),
            LeafNode(tag="li", value="Item 3")
        ])
        html_node = from_mdBlock_to_HTMLNode(md_block, block_type_unordered)
        self.assertEqual(html_node, expected_html)

    def test_ordered_list_conversion(self):
        md_block = ["1. Item 1\n2. Item 2\n3. Item 3"]
        expected_html = ParentNode(tag="ol", children=[
            LeafNode(tag="li", value="Item 1"),
            LeafNode(tag="li", value="Item 2"),
            LeafNode(tag="li", value="Item 3")
        ])
        html_node = from_mdBlock_to_HTMLNode(md_block, block_type_ordered)
        self.assertEqual(html_node, expected_html)

    def test_code_conversion(self):
        md_block = "```print('Hello, World!')```"
        expected_html = ParentNode(tag="code", children=[LeafNode(tag="pre", value="print('Hello, World!')")])
        html_node = from_mdBlock_to_HTMLNode(md_block, block_type_code)
        self.assertEqual(html_node, expected_html)

    def test_heading_conversion(self):
        md_block = ["### Heading"]
        expected_html = ParentNode(tag="h3", children=[LeafNode(value="Heading")])
        html_node = from_mdBlock_to_HTMLNode(md_block, block_type_heading)
        self.assertEqual(html_node, expected_html)

class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_single_paragraph(self):
        markdown = "This is a paragraph."
        expected_html = HTMLNode("div", None, [
            HTMLNode("p", "This is a paragraph.", None, None)
        ], None)
        self.assertEqual(markdown_to_HTMLNode(markdown), expected_html)

    def test_heading(self):
        markdown = "# Heading 1"
        expected_html = HTMLNode("div", None, [
            HTMLNode("h1", "Heading 1", None, None)
        ], None)
        self.assertEqual(markdown_to_HTMLNode(markdown), expected_html)

    def test_unordered_list(self):
        markdown = "- Item 1\n- Item 2\n- Item 3"
        expected_html = HTMLNode("div", None, [
            HTMLNode("ul", None, [
                LeafNode("li", "Item 1", None),
                LeafNode("li", "Item 2", None),
                LeafNode("li", "Item 3", None)
            ], None)
        ], None)
        self.assertEqual(markdown_to_HTMLNode(markdown), expected_html)

    def test_ordered_list(self):
        markdown = "1. Item 1\n2. Item 2\n3. Item 3"
        expected_html = HTMLNode("div", None, [
            HTMLNode("ol", None, [
                LeafNode("li", "Item 1", None),
                LeafNode("li", "Item 2", None),
                LeafNode("li", "Item 3", None)
            ], None)
        ], None)
        self.assertEqual(markdown_to_HTMLNode(markdown), expected_html)

    def test_quote(self):
        markdown = "> This is a quote."
        expected_html = HTMLNode("div", None, [
            HTMLNode("blockquote", "This is a quote.", None, None)
        ], None)
        self.assertEqual(markdown_to_HTMLNode(markdown), expected_html)

    def test_code_block(self):
        markdown = "```print('Hello, world!')```"
        expected_html = HTMLNode("div", None, [
            HTMLNode("code", None, [
                LeafNode("pre", "print('Hello, world!')", None)
            ], None)
        ], None)
        self.assertEqual(markdown_to_HTMLNode(markdown), expected_html)

class TestMarkdownToHTMLNode(unittest.TestCase):
     def test_markdown_to_HTMLNode_complex(self):
        markdown = """
        # Heading 1
        Paragraph with **bold** and *italic* text.
        ## Heading 2
        1. Ordered list item 1
        2. Ordered list item 2
        - Unordered list item 1
        - Unordered list item 2
        > Blockquote
        ```python
        print("Code block")
        """
        result_node = markdown_to_HTMLNode(markdown)
        print(result_node)


if __name__ == '__main__':
    unittest.main()