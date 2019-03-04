import random
import numpy as np


class Node:
    def __init__(self, token='', left=None, right=None):
        self.token = token
        self.left = left
        self.right = right

    def __str__(self):
        return str(self.token)

    def __repr__(self):
        return self.__str__()


class DS:
    def __init__(self):
        self.x = []
        self.y = []
        self.names = []

    def append(self, val):
        self.x.append(val[0])
        self.y.append(val[1])
        self.names.append(val[2])

    def token_length(self):
        return max(len(n) for n in self.names)

    def expand_names(self):
        length = self.token_length()
        names = []
        for name in self.names:
            if len(name) == length:
                names.append(name)
            else:
                add = length - len(name)
                left = add // 2
                right = (add + 1) // 2
                names.append(" " * left + name + " " * right)
        self.names = names

    def expand_x(self):
        length = self.token_length()
        self.x = [x * length for x in self.x]

    def expand_y(self):
        self.y = [y * 2 for y in self.y]

    def expand(self):
        self.expand_x()
        self.expand_y()
        self.expand_names()

    def __getitem__(self, k):
        return self.x[k], self.y[k], self.names[k]

    def __setitem__(self, k, v):
        self.x[k] = v[0]
        self.y[k] = v[1]
        self.names[k] = v[2]

    def __iter__(self):
        return iter(zip(self.x, self.y, self.names))

    def __str__(self):
        return str(list(zip(self.x, self.y, self.names)))

    def __repr__(self):
        return self.__str__()


def create_nodes(maxdepth, n):
    if maxdepth < 0 or random.random() < 0.3:
        return None, 0
    node = Node()
    node.left, n_left = create_nodes(maxdepth - 1, n)
    node.token = n_left + 1 if node.left else n
    node.right, n_right = create_nodes(maxdepth - 1, node.token + 1)
    return node, max(n_right, node.token)


def random_tree(maxdepth=3):
    root = Node()
    root.left, n_left = create_nodes(maxdepth - 1, 0)
    root.token = n_left + 1 if root.left else 0
    root.right, n_right = create_nodes(maxdepth - 1, root.token + 1)
    return root


def pinorder(node):
    if not node:
        return
    pinorder(node.left)
    print(node.token)
    pinorder(node.right)


def setup_datastructures_2(node, nodes=None, xy=None, h=0):
    if nodes is None:
        nodes = {}
    if xy is None:
        xy = []
    if not node:
        return
    setup_datastructures(node.left, nodes, xy, h + 1)
    xy.append([len(xy), h])
    nodes[node.token] = len(xy) - 1
    print(node.token, "=", "(", len(xy) - 1, h, ")")
    setup_datastructures(node.right, nodes, xy, h + 1)
    return xy, nodes


def setup_datastructures2(node, nodes=None, xy=None, h=0):
    if nodes is None:
        nodes = {}
    if xy is None:
        xy = []
    if not node:
        return
    setup_datastructures2(node.left, nodes, xy, h + 1)
    xy.append([len(xy), h])
    nodes[node.token] = len(xy) - 1
    print(node.token, "=", "(", len(xy) - 1, h, ")")
    setup_datastructures2(node.right, nodes, xy, h + 1)
    return xy, nodes


def setup_datastructures(node, ds=None, height=0, n_nodes=0):
    if ds is None:
        ds = DS()
    if not node:
        return ds, n_nodes
    ds, n_nodes = setup_datastructures(node.left, ds, height + 1, n_nodes)
    ds.append((n_nodes, height, node.token))
    node.token = n_nodes
    return setup_datastructures(node.right, ds, height + 1, n_nodes + 1)


def draw_arms(node, ds, image):
    if not node:
        return
    x, y, name = ds[node.token]
    y = y + 1
    if node.left:
        x_left = ds.x[node.left.token]
        diff = x - x_left
        for i in range(diff):
            image[y, x_left + i] = "-"
        draw_arms(node.left, ds, image)
    if node.right:
        print(node.right.token)
        x_right = ds.x[node.right.token]
        diff = x_right - x
        for i in range(diff):
            image[y, x + len(name) + i] = "-"
        draw_arms(node.right, ds, image)


def print_tree(node, ds):
    ds.expand()
    length = ds.token_length()
    width = max(ds.x) + length
    height = max(ds.y) + 1
    image = np.chararray((height, width))
    image[:] = ' '
    for node_x, node_y, node_name in ds:
        for i in range(length):
            image[node_y, node_x + i] = node_name[i]
    draw_arms(tree, ds, image)
    print("".join([l.tostring().decode("utf-8") + "\n" for l in image]))


def compress_singeltons(node, ds, delta=0):
    if not node:
        return delta
    delta = compress_singeltons(node.left, ds, delta)
    ds.x[node.token] -= delta
    if node.left and not node.right:
        ds.x[node.token] = ds.x[node.left.token]
        delta += 1
    elif node.right and not node.left:
        delta += 1
    delta = compress_singeltons(node.right, ds, delta)
    return delta


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

tree3 = Node("*",
             Node("2"),
             Node("ln",
                  Node("+",
                       Node("sin", Node("y")),
                       Node("5"))))


tree4 = Node("*",
             Node("+",
                  Node("ln",
                       Node("x")),
                  Node("3")),
             Node("sin",
                  Node("+",
                       Node("x"),
                       Node("y"))))


if __name__ == "__main__":
    tree = tree4
    pinorder(tree)
    ds, _ = setup_datastructures(tree)
    compress_singeltons(tree, ds)
    print_tree(tree, ds)
