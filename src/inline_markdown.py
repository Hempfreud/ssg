import re
from textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            parts = node.text.split(delimiter)

            if len(parts) % 2 == 0:
                raise ValueError("invalid markdown, unmatched delimiter")
            
            for i in range(len(parts)):
                part = parts[i]
                if part == "":
                    continue
                if i % 2 == 0:
                    new_node = TextNode(part, TextType.TEXT)
                else:
                    new_node = TextNode(part, text_type)
                new_nodes.append(new_node)
        else:
            new_nodes.append(node)

    return new_nodes

def extract_markdown_images(text):
    pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
    matches = re.findall(pattern, text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
            images = extract_markdown_images(node.text)
            if not images:
                new_nodes.append(node)
                continue
            parts = re.split(pattern, node.text)
            for i in range(len(parts)):
                part = parts[i]
                if part == "":
                    continue
                if i % 3 == 0:
                    new_nodes.append(TextNode(part, TextType.TEXT))
                elif i % 3 == 1:
                    alt_text = part
                elif i % 3 == 2:
                    url = part
                    new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
        else:
            new_nodes.append(node)

    return new_nodes

def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
            links = extract_markdown_links(node.text)
            if not links:
                new_nodes.append(node)
                continue
            parts = re.split(pattern, node.text)
            for i in range(len(parts)):
                part = parts[i]
                if part == "":
                    continue
                if i % 3 == 0:
                    new_nodes.append(TextNode(part, TextType.TEXT))
                elif i % 3 == 1:
                    link_text = part
                elif i % 3 == 2:
                    url = part
                    new_nodes.append(TextNode(link_text, TextType.LINK, url))
        else:
            new_nodes.append(node)

    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

    