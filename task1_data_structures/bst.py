"""
Plain Binary Search Tree, keyed on city_id. No balancing here on purpose
- this is the baseline I'm comparing the AVL tree against in the writeup.
If you insert in sorted order this basically turns into a linked list
(worst case), which is exactly the point - shows why AVL exists.
"""

class BSTNode:
    __slots__ = ("city", "left", "right")

    def __init__(self, city):
        self.city = city
        self.left = None
        self.right = None


class BST:
    def __init__(self):
        self.root = None
        self._size = 0

    def insert(self, city):
        self._size += 1
        if self.root is None:
            self.root = BSTNode(city)
            return
        node = self.root
        while True:
            if city.city_id < node.city.city_id:
                if node.left is None:
                    node.left = BSTNode(city)
                    return
                node = node.left
            elif city.city_id > node.city.city_id:
                if node.right is None:
                    node.right = BSTNode(city)
                    return
                node = node.right
            else:
                node.city = city  # same id already exists, just overwrite it
                self._size -= 1
                return

    def search(self, city_id):
        node = self.root
        while node is not None:
            if city_id == node.city.city_id:
                return node.city
            node = node.left if city_id < node.city.city_id else node.right
        return None

    def delete(self, city_id):
        self.root, deleted = self._delete(self.root, city_id)
        if deleted:
            self._size -= 1
        return deleted

    def _delete(self, node, city_id):
        if node is None:
            return None, False
        if city_id < node.city.city_id:
            node.left, deleted = self._delete(node.left, city_id)
            return node, deleted
        if city_id > node.city.city_id:
            node.right, deleted = self._delete(node.right, city_id)
            return node, deleted

        # this is the node we want gone
        if node.left is None:
            return node.right, True
        if node.right is None:
            return node.left, True

        # two kids case - swap in the in-order successor (smallest in the right subtree)
        successor = node.right
        while successor.left is not None:
            successor = successor.left
        node.city = successor.city
        node.right, _ = self._delete(node.right, successor.city.city_id)
        return node, True

    def height(self):
        # doing this iteratively with a stack instead of recursion because
        # the degenerate sorted-insert case makes a tree 10,000 deep and
        # that blows the recursion limit almost instantly
        if self.root is None:
            return 0
        stack = [(self.root, 1)]
        best = 0
        while stack:
            node, depth = stack.pop()
            best = max(best, depth)
            if node.left:
                stack.append((node.left, depth + 1))
            if node.right:
                stack.append((node.right, depth + 1))
        return best

    def __len__(self):
        return self._size