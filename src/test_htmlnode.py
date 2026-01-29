import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("p", "This is a paragraph")
        node2 = HTMLNode("p", "This is a paragraph")
        self.assertEqual(node.tag, node2.tag)
        self.assertEqual(node.value, node2.value)
        self.assertEqual(node.children, node2.children)
        self.assertEqual(node.props, node2.props)

    def test_props_to_html(self):
        node = HTMLNode("a", "Click here", props={"href": "https://www.boot.dev", "target": "_blank"})
        node2 = HTMLNode("a", "Click here")
        node3 = HTMLNode("a", "Click here", props={})
        self.assertEqual(' href="https://www.boot.dev" target="_blank"', node.props_to_html())
        self.assertEqual("", node2.props_to_html())
        self.assertEqual("", node3.props_to_html())

    def test_repr(self):
        node = HTMLNode("div", None, children=[], props={"class": "container"})
        self.assertEqual("HTMLNode(div, None, [], {'class': 'container'})", repr(node))

class TestLeafNode(unittest.TestCase):
    def test_to_html_with_props(self):
        leaf = LeafNode("a", "Click here", props={"href": "https://www.boot.dev", "target": "_blank"})
        self.assertEqual('<a href="https://www.boot.dev" target="_blank">Click here</a>', leaf.to_html())

    def test_to_html_without_props(self):
        leaf = LeafNode("p", "This is a paragraph")
        self.assertEqual('<p>This is a paragraph</p>', leaf.to_html())

    def test_to_html_no_tag(self):
        leaf = LeafNode(None, "Just some text")
        self.assertEqual('Just some text', leaf.to_html())

    def test_to_html_no_value(self):
        leaf = LeafNode("span", None)
        with self.assertRaises(ValueError):
            leaf.to_html()

    def test_repr(self):
        leaf = LeafNode("img", None, props={"src": "image.png", "alt": "An image"})
        self.assertEqual("LeafNode(img, None, {'src': 'image.png', 'alt': 'An image'})", repr(leaf))
    
class TestParentNode(unittest.TestCase):
    def test_to_html_with_children_and_props(self):
        child1 = LeafNode("li", "Item 1")
        child2 = LeafNode("li", "Item 2")
        parent = ParentNode("ul", [child1, child2], props={"class": "list"})
        self.assertEqual('<ul class="list"><li>Item 1</li><li>Item 2</li></ul>', parent.to_html())
    
    def test_to_html_no_tag(self):
        child = LeafNode("p", "This is a paragraph")
        parent = ParentNode(None, [child])
        with self.assertRaises(ValueError):
            parent.to_html()

    def test_to_html_no_children(self):
        parent = ParentNode("div", None)
        with self.assertRaises(ValueError):
            parent.to_html()

    def test_to_html_empty_children(self):
        parent = ParentNode("div", [])
        self.assertEqual('<div></div>', parent.to_html())
    
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )


if __name__ == "__main__":
    unittest.main()