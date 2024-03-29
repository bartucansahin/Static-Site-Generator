class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props:
            return ' '.join([f'{key}="{value}"' for key, value in self.props.items()])
        else:
            return ''

    def __repr__(self):
         return f"HTMLNode:{self.tag}, {self.value}, {self.children}, {self.props_to_html()}"
    
    def __eq__(self, other):
        if not isinstance(other, HTMLNode):
            return False
        return (self.tag == other.tag and
                self.value == other.value and
                self.children == other.children and
                self.props == other.props)
    
class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        if value is None:
            raise ValueError("LeafNode requires a value.")
        super().__init__(tag=tag, value=value, props=props)
        if self.children:
            raise ValueError("LeafNode cannot have children.")
    
    def to_html(self):
        if self.tag is None:
            return self.value
        elif self.props:
            return f"<{self.tag} {self.props_to_html()}>{self.value}</{self.tag}>"
        else:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        
class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None):
        super().__init__(tag=tag, children=children, props=props)
        if not children:
            raise ValueError("ParentNode has to have children")
        if not tag:
            raise ValueError("ParentNode has to have tags")
        for child in children:
            if not isinstance(child, (LeafNode, ParentNode, HTMLNode)):
                raise TypeError("Children of ParentNode must be instances of LeafNode, ParentNode or HTMLNode")
        
    def to_html(self):
        html_converted_str = ""
        for child in self.children:
            html_converted_str += child.to_html()
        result = f"<{self.tag}>{html_converted_str}</{self.tag}>"
        return result


