import unittest
from block_markdown import markdown_to_blocks, block_to_block_type, BlockType

class TestMarkdownToBlocks(unittest.TestCase):
    
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_empty_markdown(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_with_leading_and_trailing_newlines(self):
        md = "\n\nThis is a paragraph with leading and trailing newlines\n\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is a paragraph with leading and trailing newlines"])

class TestBlockToBlockType(unittest.TestCase):

    def test_paragraph_block(self):
        block = "This is a simple paragraph."
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_heading_block(self):
        block = "### This is a heading"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_code_block(self):
        block = "```\nprint('Hello, World!')\n```"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.CODE)

    def test_quote_block(self):
        block = "> This is a quote.\n> It has multiple lines."
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_unordered_list_block(self):
        block = "- Item 1\n- Item 2\n- Item 3"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)

    def test_ordered_list_block(self):
        block = "1. First item\n2. Second item\n3. Third item"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)

if __name__ == "__main__":
    unittest.main()