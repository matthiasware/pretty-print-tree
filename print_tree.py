import random
import numpy as np


class Node:
    def __init__(self, s=0, left=None, right=None):
        self.s = s
        self.left = left
        self.right = right

    def __str__(self):
        return str(self.s)

    def __repr__(self):
        return self.__str__()


tree0 = Node("4",
             Node("2", Node("1"), Node("3")),
             Node("6", None, Node("7")))

tree1 = Node("11",
             Node("10"),
             Node("16",
                  Node("14",
                       Node("13", Node("12")),
                       Node("15"))))

tree2 = Node("001",
             Node("0"),
             Node("006",
                  Node("00004",
                       Node("03", Node("000002")),
                       Node("05"))))


def create_nodes(maxdepth, n):
    if maxdepth < 0 or random.random() < 0.3:
        return None, 0
    node = Node()
    node.left, n_left = create_nodes(maxdepth - 1, n)
    node.s = n_left + 1 if node.left else n
    node.right, n_right = create_nodes(maxdepth - 1, node.s + 1)
    return node, max(n_right, node.s)


def random_tree(maxdepth=3):
    root = Node()
    root.left, n_left = create_nodes(maxdepth - 1, 0)
    root.s = n_left + 1 if root.left else 0
    root.right, n_right = create_nodes(maxdepth - 1, root.s + 1)
    return root


def pinorder(node):
    if not node:
        return
    pinorder(node.left)
    print(node.s)
    pinorder(node.right)


def setup_datastructures(node, nodes=None, xy=None, h=0):
    if nodes is None:
        nodes = {}
    if xy is None:
        xy = []
    if not node:
        return
    setup_datastructures(node.left, nodes, xy, h + 1)
    xy.append([len(xy), h])
    nodes[node.s] = len(xy) - 1
    print(node.s, "=", "(", len(xy) - 1, h, ")")
    setup_datastructures(node.right, nodes, xy, h + 1)
    return xy, nodes


def pad_token(token, length):
    if len(token) == length:
        return token
    add_spaces = length - len(token)
    add_left = add_spaces // 2
    add_right = (add_spaces + 1) // 2
    return " " * add_left + token + " " * add_right


def draw_arms(node, nodes, xy, image, tokenwidth):
    if node is None:
        return
    coords = xy[nodes[node.s]]
    if node.left is not None:
        left_coords = xy[nodes[node.left.s]]
        x_diff = coords[0] - left_coords[0]
        y = left_coords[1] * 2 - 1
        for i in range(x_diff):
            image[y, left_coords[0] + i] = "-"
        draw_arms(node.left, nodes, xy, image, tokenwidth)
    if node.right is not None:
        right_coords = xy[nodes[node.right.s]]
        x_diff = right_coords[0] - coords[0]
        y = right_coords[1] * 2 - 1
        for i in range(x_diff):
            image[y, coords[0] + tokenwidth + i] = "-"
        draw_arms(node.right, nodes, xy, image, tokenwidth)


def print_tree(tree, nodes, xy):
    x, y = zip(*xy)
    node_names, _ = zip(*nodes.items())
    tokenwidth = max(len(name) for name in node_names)
    node_names = [pad_token(name, tokenwidth) for name in node_names]
    x = [xx * tokenwidth for xx in x]
    xy = [[xi, yi] for xi, yi in zip(x, y)]
    width = max(x) + tokenwidth
    height = max(y) * 2 + 1
    image = np.chararray((height, width))
    image[:] = ' '
    for node_x, node_y, node_name in zip(x, y, node_names):
        for i in range(tokenwidth):
            image[node_y * 2, node_x + i] = node_name[i]
    draw_arms(tree, nodes, xy, image, tokenwidth)
    print("".join([l.tostring().decode("utf-8") + "\n" for l in image]))


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
    delta = compress_singeltons(node.right, nodes, xy, delta)
    return delta


if __name__ == "__main__":
    tree = tree2
    pinorder(tree)
    xy, nodes_map = setup_datastructures(tree)
    print_tree(tree, nodes_map, xy)
    compress_singeltons(tree, nodes_map, xy)
    print_tree(tree, nodes_map, xy)
