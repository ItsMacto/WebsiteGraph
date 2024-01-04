# pip install requests beautifulsoup4

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def get_all_links(url):
    # Send a GET request to the URL
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to retrieve the webpage: {e}")
        return []
    
    # Parse the content of the page
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all the anchor tags (<a>) and convert relative URLs to absolute URLs
    links = [urljoin(url, a['href']) for a in soup.find_all('a', href=True)]
    
    links = [link for link in links if ('en.wikipedia.org' in link)]
    
    return links


class Node:
    def __init__(self, url, depth):
        self.url = url
        self.depth = depth
        self.children = []
        self.isEdge = True
    
    def __str__(self):
        return f"URL: {self.url}, Depth: {self.depth}"

    def __repr__(self):
        return f"URL: {self.url}, Depth: {self.depth}"

    def __eq__(self, other):
        return self.url == other.url

    def __hash__(self):
        return hash(self.url)
    

class Graph:
    def __init__(self, url, max_depth):
        self.root = Node(url, 0)
        self.max_depth = max_depth
        self.nodes = set()
        self.nodes.add(self.root)
        self.build_graph(self.root)
    
    def __str__(self):
        return f"Graph with {len(self.nodes)} nodes"
    
    def __repr__(self):
        return f"Graph with {len(self.nodes)} nodes"
    
    def add_node(self, parent, url):
        node = Node(url, parent.depth + 1)
        print(node.depth)
        if node.depth <= self.max_depth and node not in self.nodes:
            self.nodes.add(node)
            parent.children.append(node)
            parent.isEdge = False
            return node
        return None
    
    def build_graph(self, node):
        if node.depth >= self.max_depth:
            return
        elif not node.isEdge:
            links = node.children
        
        else:
            links = get_all_links(node.url)
        for link in links:
            child = self.add_node(node, link)
            if child:
                self.build_graph(child)
    
    
    def print_graph(self):
        for node in self.nodes:
            print(node)
            if not node.isEdge:
                print(node.children)
            print()
    
    def get_nodes(self):
        return self.nodes
    
startingUrl = "https://en.wikipedia.org/wiki/Main_Page"
depth = 8



graph = Graph(startingUrl, depth)
print(graph.print_graph())
print(graph)