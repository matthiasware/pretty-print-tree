import numpy as np


class node:
    def __init__(self, s="", left=None, right=None):
        self.s = s
        self.left = left
        self.right = right

    def __str__(self):
        return self.s

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


# tree = node("1", node("0"), node("3", node("2")))
# tree = node("1", node("0"), node("2", None, node("3")))


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
        node_right_coords = xy[nodes[node.right.s]]
        node_coords[0] = node_right_coords[0] - 1
        delta += 1
    delta = compress_singeltons(node.right, nodes, xy, delta)
    return delta


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


if __name__ == "__main__":
    pinorder(tree)
    print("**** BUILD COORDINATES ***")
    xy, nodes = init_coordinates(tree)
    print(xy)
    print(nodes)
    print_coords(nodes, xy)
    print("*** COMPRESS ***")
    compress_singeltons(tree, nodes, xy)
    print_coords(nodes, xy)
