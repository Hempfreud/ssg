import unittest
from textnode import TextType, TextNode
from inline_markdown import (
    extract_markdown_images, 
    extract_markdown_links, 
    split_nodes_delimiter,
    split_nodes_link,
    split_nodes_image,
    text_to_textnodes
)

class TestSplitNodes(unittest.TestCase):
    def test_split_bold(self):
        old_nodes = [
            TextNode("This is **bold** text", TextType.TEXT),
            TextNode("This is normal text", TextType.TEXT),
        ]
        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
            TextNode("This is normal text", TextType.TEXT),
        ]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        self.assertEqual(new_nodes, expected_nodes)
    
    def test_split_italic(self):
        old_nodes = [
            TextNode("This is *italic* text", TextType.TEXT),
            TextNode("Another *example* here", TextType.TEXT),
        ]
        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
            TextNode("Another ", TextType.TEXT),
            TextNode("example", TextType.ITALIC),
            TextNode(" here", TextType.TEXT),
        ]
        new_nodes = split_nodes_delimiter(old_nodes, "*", TextType.ITALIC)
        self.assertEqual(new_nodes, expected_nodes)
    
    def test_split_text(self):
        old_nodes = [
            TextNode("No formatting here", TextType.TEXT),
        ]
        expected_nodes = [
            TextNode("No formatting here", TextType.TEXT),
        ]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        self.assertEqual(new_nodes, expected_nodes)

class TestExtractMarkdown(unittest.TestCase):
    def test_extract_images(self):
        text = "Here is an image ![alt text](http://example.com/image.png) in the text."
        expected = [("alt text", "http://example.com/image.png")]
        result = extract_markdown_images(text)
        self.assertEqual(result, expected)

    def test_extract_multiple_images(self):
        text = "First image ![first](http://example.com/first.png) and second image ![second](http://example.com/second.png)."
        expected = [("first", "http://example.com/first.png"), ("second", "http://example.com/second.png")]
        result = extract_markdown_images(text)
        self.assertEqual(result, expected)

    def test_extract_no_images(self):
        text = "This text has no images."
        expected = []
        result = extract_markdown_images(text)
        self.assertEqual(result, expected)

    def test_extract_links(self):
        text = "Here is a link [click here](http://example.com) in the text."
        expected = [("click here", "http://example.com")]
        result = extract_markdown_links(text)
        self.assertEqual(result, expected)

    def test_extract_multiple_links(self):
        text = "First link [first](http://example.com/first) and second link [second](http://example.com/second)."
        expected = [("first", "http://example.com/first"), ("second", "http://example.com/second")]
        result = extract_markdown_links(text)
        self.assertEqual(result, expected)

    def test_extract_no_links(self):
        text = "This text has no links."
        expected = []
        result = extract_markdown_links(text)
        self.assertEqual(result, expected)
    
    class TestSplitNodesImageLink(unittest.TestCase):
        def test_split_image(self):
            old_nodes = [
                TextNode("Here is an image ![alt text](http://example.com/image.png) in the text.", TextType.TEXT),
            ]
            expected_nodes = [
                TextNode("Here is an image ", TextType.TEXT),
                TextNode("alt text", TextType.IMAGE, "http://example.com/image.png"),
                TextNode(" in the text.", TextType.TEXT),
            ]
            new_nodes = split_nodes_image(old_nodes)
            self.assertEqual(new_nodes, expected_nodes)

        def test_split_link(self):
            old_nodes = [
                TextNode("Here is a link [click here](http://example.com) in the text.", TextType.TEXT),
            ]
            expected_nodes = [
                TextNode("Here is a link ", TextType.TEXT),
                TextNode("click here", TextType.LINK, "http://example.com"),
                TextNode(" in the text.", TextType.TEXT),
            ]
            new_nodes = split_nodes_link(old_nodes)
            self.assertEqual(new_nodes, expected_nodes)
    
    class TestTextToTextNodes(unittest.TestCase):
        def test_text_to_textnodes(self):
            text = "This is a sample text."
            expected_nodes = [
                TextNode("This is a sample text.", TextType.TEXT),
            ]
            result = text_to_textnodes(text)
            self.assertEqual(result, expected_nodes)
        
        def test_empty_text(self):
            text = ""
            expected_nodes = []
            result = text_to_textnodes(text)
            self.assertEqual(result, expected_nodes)

        def test_with_bold(self):
            text = "This is **bold** text."
            expected_nodes = [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text.", TextType.TEXT),
            ]
            result = text_to_textnodes(text)
            self.assertEqual(result, expected_nodes)

        def test_with_italic(self):
            text = "This is _italic_ text."
            expected_nodes = [
                TextNode("This is ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text.", TextType.TEXT),
            ]
            result = text_to_textnodes(text)
            self.assertEqual(result, expected_nodes)

        def test_with_code(self):
            text = "This is `code` text."
            expected_nodes = [
                TextNode("This is ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" text.", TextType.TEXT),
            ]
            result = text_to_textnodes(text)
            self.assertEqual(result, expected_nodes)

        def test_with_multiple_formats(self):
            text = "This is **bold**, _italic_, and `code` text."
            expected_nodes = [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(", ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(", and ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" text.", TextType.TEXT),
            ]
            result = text_to_textnodes(text)
            self.assertEqual(result, expected_nodes)
        
        def test_with_images_and_links(self):
            text = "Here is an image ![alt](http://example.com/image.png) and a link [click](http://example.com)."
            expected_nodes = [
                TextNode("Here is an image ", TextType.TEXT),
                TextNode("alt", TextType.IMAGE, "http://example.com/image.png"),
                TextNode(" and a link ", TextType.TEXT),
                TextNode("click", TextType.LINK, "http://example.com"),
                TextNode(".", TextType.TEXT),
            ]
            result = text_to_textnodes(text)
            self.assertEqual(result, expected_nodes)

if __name__ == "__main__":
    unittest.main()