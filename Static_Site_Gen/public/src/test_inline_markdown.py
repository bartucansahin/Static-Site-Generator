import unittest

from inline_markdown import (
    split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes
)
from textnode import TextNode

class TestSplitNodesDelimiter(unittest.TestCase):

    def test_delimiters_at_beginning_and_end(self):
        old_nodes = [TextNode("**bold**", "text")]
        delimiter = "**"
        text_type = "bold"
        expected_result = [TextNode("", "text"), TextNode("bold", "bold"), TextNode("", "text")]
        self.assertEqual(split_nodes_delimiter(old_nodes, delimiter, text_type), expected_result)

    def test_empty_input_list(self):
        self.assertEqual(split_nodes_delimiter([], '*', 'bold'), [])
    
    def test_non_textnode_objects(self):
        with self.assertRaises(ValueError):
            split_nodes_delimiter([1, 2, 3], '*', 'bold')

    def test_unmatched_opening_delimiter(self):
        with self.assertRaises(ValueError):
            split_nodes_delimiter([TextNode('*This is an example with an unmatched delimiter', 'text')], '*', 'bold')

    def test_unmatched_closing_delimiter(self):
        with self.assertRaises(ValueError):
            split_nodes_delimiter([TextNode('This is an example with an unmatched delimiter*', 'text')], '*', 'bold')
    
    def test_multiple_pairs_of_delimiters(self):
        input_nodes = [TextNode('This is some **bold** text', 'text')]
        expected_result = [
            TextNode('This is some ', 'text'),
            TextNode('bold', 'bold'),
            TextNode(' text', 'text')
        ]
        self.assertEqual(split_nodes_delimiter(input_nodes, '**', 'bold'), expected_result)

class TestMarkdownFunctions(unittest.TestCase):
    def test_extract_markdown_images(self):
        text_with_images = "This is a text with ![image1](https://i.imgur.com/zjjcJKZ.png) and ![image2](path/to/image2.png)"
        expected_result = [("image1", "https://i.imgur.com/zjjcJKZ.png"), ("image2", "path/to/image2.png")]
        self.assertEqual(extract_markdown_images(text_with_images), expected_result)

        text_without_images = "This is a text without any images."
        self.assertEqual(extract_markdown_images(text_without_images), [])
    
    def test_extract_markdown_links(self):
        text_with_links = "This is a text with [link1](https://www.example1.com) and [link2](https://www.example2.com)"
        expected_result = [("link1", "https://www.example1.com"), ("link2", "https://www.example2.com")]
        self.assertEqual(extract_markdown_links(text_with_links), expected_result)

        text_without_links = "This is a text without any links."
        self.assertEqual(extract_markdown_links(text_without_links), [])


class TestSplitNodesImage(unittest.TestCase):
    def test_no_images(self):
        node = TextNode("This is a plain text with no images.", "text")
        new_nodes = split_nodes_image([node])
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "This is a plain text with no images.")
        self.assertIsNone(new_nodes[0].url)

    def test_text_before_image(self):
        node = TextNode(
            "Some text before ![Image](https://example.com/image.png) the image.", "text"
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "Some text before ")
        self.assertEqual(new_nodes[1].text, "![Image](https://example.com/image.png)")
        self.assertEqual(new_nodes[2].text, " the image.")

    def test_only_images(self):
        node = TextNode(
            "![Image One](https://example.com/one.png)! [Image Two](https://example.com/two.png)",
            "text"
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(len(new_nodes), 2)
    
    def test_text_after_image(self):
        node = TextNode(
            "![Image](https://example.com/image.png) Some text after the image.", "text"
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text, "![Image](https://example.com/image.png)")
        self.assertEqual(new_nodes[1].text, " Some text after the image.")

    def test_no_alt_text(self):
        nodes_with_image_no_alt_text = [TextNode("This is an image: ![image](https://example.com/image.png)", "text")]
        result_list = split_nodes_image(nodes_with_image_no_alt_text)
        self.assertEqual(len(result_list), 2)
        self.assertIsInstance(result_list[0], TextNode)
        self.assertIsInstance(result_list[1], TextNode)
        self.assertEqual(result_list[0].text, "This is an image: ")
        self.assertEqual(result_list[0].text_type, "text")
        self.assertEqual(result_list[1].text, "![image](https://example.com/image.png)")
        self.assertEqual(result_list[1].text_type, "image")

class TestSplitNodesLink(unittest.TestCase):
    def test_no_markdown_links(self):
        node = TextNode("No markdown links here", "text")
        result = split_nodes_link([node])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "No markdown links here")

    def test_split_nodes_link_invalid_node(self):
        old_nodes = ["Invalid node"]
        with self.assertRaises(ValueError):
            split_nodes_link(old_nodes)

    class TestTextToTextNodes(unittest.TestCase):

        def test_text_to_textnodes(self):
            input_text = "This is **text** with an *italic* word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
            expected_output = [
                TextNode("This is ", "text", None),
                TextNode("text", "bold", None),
                TextNode(" with an ", "text", None),
                TextNode("italic", "italic", None),
                TextNode(" word and a ", "text", None),
                TextNode("code block", "code", None),
                TextNode(" and an ", "text", None),
                TextNode("image", "image", "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a ", "text", None),
                TextNode("link", "link", "https://boot.dev")
            ]

            result = text_to_textnodes(input_text)
            self.assertEqual(len(result), len(expected_output))

            for i in range(len(result)):
                self.assertEqual(result[i].text, expected_output[i].text)
                self.assertEqual(result[i].type, expected_output[i].type)
                self.assertEqual(result[i].url, expected_output[i].url)

if __name__ == '__main__':
    unittest.main()

