from enum import Enum

def markdown_to_blocks(markdown):
    splitted = markdown.split("\n\n")
    blocks = []
    for block in splitted:
        if block == "":
            continue
        blocks.append(block.strip())
    return blocks

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"
    
def block_to_block_type(block):
    
    lines = block.splitlines()

    for i in range(1, 7):
        prefix = "#" * i + " "
        if block.startswith(prefix):
            return BlockType.HEADING
    
    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE
    
    is_quote = True
    for line in lines:
        if not line.startswith(">"):
            is_quote = False
            break
    if is_quote:
        return BlockType.QUOTE

    is_un_list = True
    for line in lines:
        if not line.startswith(("- ")):
            is_un_list = False
            break
    if is_un_list:
        return BlockType.UNORDERED_LIST

    is_ordered_list = True
    expected = 1

    for line in lines:
        num_str = ""
        for char in line:
            if char.isdigit():
                num_str += char
            else:
                break
    
        if num_str == "":
            is_ordered_list = False
            break

        number = int(num_str)
        if not line.startswith(f"{number}. "):
            is_ordered_list = False
            break

        if number != expected:
            is_ordered_list = False
            break

        expected += 1
    
    if is_ordered_list:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH