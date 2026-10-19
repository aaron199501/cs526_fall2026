"""Problem 1: verify the four traversal answers for the two given trees."""

from collections import deque


GENERAL_TREE = {
    "A": ("B", "C", "D"), "B": ("E", "F"), "C": (), "D": ("G",),
    "E": ("H",), "F": ("I",), "G": (), "H": (), "I": (),
}

BINARY_TREE = {
    "A": ("B", "C"), "B": ("D", "E"), "C": (None, "F"),
    "D": (None, "G"), "E": (None, None), "F": ("H", "I"),
    "G": (None, None), "H": (None, None), "I": (None, None),
}


def preorder(tree, root):
    result = [root]
    for child in tree[root]:
        result.extend(preorder(tree, child))
    return result


def breadth_first(tree, root):
    result, queue = [], deque([root])
    while queue:
        node = queue.popleft()
        result.append(node)
        queue.extend(tree[node])
    return result


def postorder(tree, root):
    result = []
    for child in tree[root]:
        result.extend(postorder(tree, child))
    result.append(root)
    return result


def inorder(tree, root):
    if root is None:
        return []
    left, right = tree[root]
    return inorder(tree, left) + [root] + inorder(tree, right)


def main():
    print("Problem 1 - General tree (children from left to right)")
    print("Preorder:      " + " ".join(preorder(GENERAL_TREE, "A")))
    print("Breadth-first: " + " ".join(breadth_first(GENERAL_TREE, "A")))
    print("Postorder:     " + " ".join(postorder(GENERAL_TREE, "A")))
    print("\nProblem 1 - Binary tree")
    print("Inorder:       " + " ".join(inorder(BINARY_TREE, "A")))


if __name__ == "__main__":
    main()
