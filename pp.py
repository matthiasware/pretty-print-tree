import numpy as np
import random


class Node:
    def __init__(self, s=0, left=None, right=None):
        self.s = s
        self.left = left
        self.right = right

    def __str__(self):
        return str(self.s)

    def __repr__(self):
        return self.__str__()


tree = Node("4",
            Node("2", Node("1"), Node("3")),
            Node("6", None, Node("7")))

tree = Node("11",
            Node("10"),
            Node("16",
                 Node("14",
                      Node("13", Node("12")),
                      Node("15"))))

tree = Node("111",
            Node("110"),
            Node("116",
                 Node("114",
                      Node("113", Node("112")),
                      Node("115"))))


def name_inorder(Node, n):
    if(not Node):
        return n
    n = name_inorder(Node.left, n)
    Node.s = n
    n = name_inorder(Node.right, n + 1)
    return n


def create_Nodes(maxdepth, n):
    if maxdepth < 0 or random.random() < 0.3:
        return None, 0
    n2 = Node()
    n2.left, n_Nodes_left = create_Nodes(maxdepth - 1, n)
    n2.s = n_Nodes_left + 1 if n2.left else n
    n2.right, n_Nodes_right = create_Nodes(maxdepth - 1, n2.s + 1)
    return n2, max(n_Nodes_right, n2.s)


def create_tree(maxdepth=3):
    root = Node()
    root.left, n_Nodes_left = create_Nodes(maxdepth - 1, 0)
    root.s = n_Nodes_left + 1 if root.left else 0
    root.right, n_Nodes_right = create_Nodes(maxdepth - 1, root.s + 1)
    return root


# tree = Node("1", Node("0"), Node("3", Node("2")))
# tree = Node("1", Node("0"), Node("2", None, Node("3")))


def pinorder(Node):
    if not Node:
        return
    pinorder(Node.left)
    print(Node.s)
    pinorder(Node.right)


def init_coordinates(Node, Nodes=None, xy=None, h=0):
    if Nodes is None:
        Nodes = {}
    if xy is None:
        xy = []
    if not Node:
        return
    init_coordinates(Node.left, Nodes, xy, h + 1)
    xy.append([len(xy), h])
    Nodes[Node.s] = len(xy) - 1
    print(Node.s, "=", "(", len(xy) - 1, h, ")")
    init_coordinates(Node.right, Nodes, xy, h + 1)
    return xy, Nodes


'''
If we move head over left Node,
we need shift every following Node
coordinate x: -1

TODO:
if:
-1---
0---2
-----3
set se below 2
'''


def compress_singeltons(Node, Nodes, xy, delta=0):
    # print(Node, delta)
    if not Node:
        return delta
    delta = compress_singeltons(Node.left, Nodes, xy, delta)
    Node_coords = xy[Nodes[Node.s]]
    Node_coords[0] -= delta
    if Node.left and not Node.right:
        Node_left_coords = xy[Nodes[Node.left.s]]
        Node_coords[0] = Node_left_coords[0]
        delta += 1
    elif Node.right and not Node.left:
        delta += 1
    delta = compress_singeltons(Node.right, Nodes, xy, delta)
    return delta


def print_coords2(Nodes, xy):
    x, y = zip(*xy)
    width = max(x)
    height = max(y)
    image = np.chararray((height + 1, width + 1))
    image[:] = '-'
    for Node, idx in Nodes.items():
        Node_x, Node_y = xy[idx]
        image[Node_y, Node_x] = Node
    print("".join([l.tostring().decode("utf-8") + "\n" for l in image]))


def draw_arms(n, Nodes, xy, image, width, height):
    n_coords = xy[Nodes[n.s]]
    if n.left:
        n_coords_left = xy[Nodes[n.left.s]]
        delta = n_coords[0] - n_coords_left[0]
        if delta == 0:
            image[n_coords_left[1]]
    if n.right:
        n_coords_right = xy[Nodes[n.left.s]]
        pass


def print_coords(tree, Nodes, xy):
    x, y = zip(*xy)
    # maxtokwidth = max(len(str(s)) for s in Nodes.keys())
    width = max(x)
    height = max(y)
    image = np.chararray((height, width))
    image[:] = '-'
    for Node, idx in Nodes.items():
        Node_x, Node_y = xy[idx]
        # Node_x = Node_x * maxtokwidth
        for i in range(len(Node)):
            image[Node_y, Node_x + i] = Node[i]
    print("".join([l.tostring().decode("utf-8") + "\n" for l in image]))


def max_token_width(n):
    maxwidth = len(str(n.s))
    if n.left:
        maxwidth = max(maxwidth, max_token_width(n.left))
    if n.right:
        maxwidth = max(maxwidth, max_token_width(n.right))
    return maxwidth

# REBALANCE TREE ?

def expand_coordinates(xy, Nodes):
    maxtokwidth = max(len(str(s)) for s in Nodes.keys())
    xy = [[x* maxtokenwidth, y * 2] for x, y in xy]
    return xy

if __name__ == "__main__":
    random.seed(6)
    random.seed(9)
    # pinorder(tree)
    # print("**** BUILD COORDINATES ***")
    # xy, Nodes = init_coordinates(tree)
    # print(xy)
    # print(Nodes)
    # print_coords(Nodes, xy)
    # print("*** COMPRESS SINGELTONS***")
    # compress_singeltons(tree, Nodes, xy)
    # print_coords(Nodes, xy)
    # root = create_tree(3)
    root = tree
    xy, Nodes = init_coordinates(root)
    print_coords(root, Nodes, xy)
    compress_singeltons(root, Nodes, xy)
    print_coords(root, Nodes, xy)
    xy = expand_Nodes(xy, Nodes)
    print_coords(root, Nodes, xy)
    # pinorder(tree)
