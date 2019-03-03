import numpy as np
import random


class node:
    def __init__(self, s=0, left=None, right=None):
        self.s = s
        self.left = left
        self.right = right

    def __str__(self):
        return str(self.s)

    def __repr__(self):
        return self.__str__()


tree = node("4",
            node("2", node("1"), node("3")),
            node("6", None, node("7")))

tree = node("1",
            node("0"),
            node("6",
                 node("4",
                      node("3", node("2")),
                      node("5"))))


def name_inorder(node, n):
    if(not node):
        return n
    n = name_inorder(node.left, n)
    node.s = n
    n = name_inorder(node.right, n + 1)
    return n


def create_nodes(maxdepth, n):
    if maxdepth < 0 or random.random() < 0.3:
        return None, 0
    n2 = node()
    n2.left, n_nodes_left = create_nodes(maxdepth - 1, n)
    n2.s = n_nodes_left + 1 if n2.left else n
    n2.right, n_nodes_right = create_nodes(maxdepth - 1, n2.s + 1)
    return n2, max(n_nodes_right, n2.s)


def create_tree(maxdepth=3):
    root = node()
    root.left, n_nodes_left = create_nodes(maxdepth - 1, 0)
    root.s = n_nodes_left + 1 if root.left else 0
    root.right, n_nodes_right = create_nodes(maxdepth - 1, root.s + 1)
    return root


# tree = node("1", node("0"), node("3", node("2")))
tree = node("1", node("0"), node("2", None, node("3")))


def pinorder(node):
    if not node:
        return
    pinorder(node.left)
    print(node.s)
    pinorder(node.right)


def init_coordinates(node, nodes=None, xy=None, h=0):
    if nodes is None:
        nodes = {}
    if xy is None:
        xy = []
    if not node:
        return
    init_coordinates(node.left, nodes, xy, h + 1)
    xy.append([len(xy), h])
    nodes[node.s] = len(xy) - 1
    print(node.s, "=", "(", len(xy) - 1, h, ")")
    init_coordinates(node.right, nodes, xy, h + 1)
    return xy, nodes


'''
If we move head over left node,
we need shift every following node
coordinate x: -1

TODO:
if:
-1---
0---2
-----3
set se below 2
'''


def compress_singeltons(node, nodes, xy, delta=0):
    if not node:
        return delta
    delta = compress_singeltons(node.left, nodes, xy, delta)
    node_coords = xy[nodes[node.s]]
    node_coords[0] -= delta
    if node.left and not node.right:
        node_left_coords = xy[nodes[node.left.s]]
        node_coords[0] = node_left_coords[0]
        delta += 1
    elif node.right and not node.left:
        delta += 1
        node_right_coords = xy[nodes[node.right.s]]
        node_coords[0] = node_right_coords[0]
    delta = compress_singeltons(node.right, nodes, xy, delta)
    return delta


def compress_rows(node, nodes, xy, delta=0):
    pass


def print_coords(nodes, xy):
    x, y = zip(*xy)
    width = max(x)
    height = max(y)
    image = np.chararray((height + 1, width + 1))
    image[:] = '-'
    for node, idx in nodes.items():
        node_x, node_y = xy[idx]
        image[node_y, node_x] = node
    print("".join([l.tostring().decode("utf-8") + "\n" for l in image]))

# REBALANCE TREE ?


if __name__ == "__main__":
    random.seed(6)
    # pinorder(tree)
    # print("**** BUILD COORDINATES ***")
    # xy, nodes = init_coordinates(tree)
    # print(xy)
    # print(nodes)
    # print_coords(nodes, xy)
    # print("*** COMPRESS SINGELTONS***")
    # compress_singeltons(tree, nodes, xy)
    # print_coords(nodes, xy)
    root = create_tree(3)
    xy, nodes = init_coordinates(root)
    print_coords(nodes, xy)
    compress_singeltons(root, nodes, xy)
    print_coords(nodes, xy)
    # pinorder(tree)
