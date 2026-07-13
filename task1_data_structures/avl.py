"""
AVL Tree - self balancing BST, keyed on city_id.

After every insert/delete it checks the balance factor and does
rotations if needed so the height never gets worse than O(log n), no
matter what order stuff gets inserted in. This is basically bst.py but
with the rebalancing logic bolted on - compare the two files, that's
the whole task 1 experiment.
"""

class AVLNode:
    __slots__ = ("city", "left", "right", "height")

    def __init__(self, city):
        self.city = city
        self.left = None
        self.right = None
        self.height = 1


class AVLTree:
    def __init__(self):
        self.root = None
        self._size = 0

    # ---- helper stuff ----
    def _h(self, node):
        return node.height if node else 0

    def _balance_factor(self, node):
        return self._h(node.left) - self._h(node.right)

    def _update_height(self, node):
        node.height = 1 + max(self._h(node.left), self._h(node.right))

    def _rotate_right(self, y):
        x = y.left
        y.left = x.right
        x.right = y
        self._update_height(y)
        self._update_height(x)
        return x

    def _rotate_left(self, x):
        y = x.right
        x.right = y.left
        y.left = x
        self._update_height(x)
        self._update_height(y)
        return y

    def _rebalance(self, node):
        self._update_height(node)
        bf = self._balance_factor(node)
        if bf > 1:  # left side too heavy
            if self._balance_factor(node.left) < 0:
                node.left = self._rotate_left(node.left)  # left-right case, needs double rotation
            return self._rotate_right(node)
        if bf < -1:  # right side too heavy
            if self._balance_factor(node.right) > 0:
                node.right = self._rotate_right(node.right)  # right-left case
            return self._rotate_left(node)
        return node  # already balanced, nothing to do

    # ---- actual public methods ----
    def insert(self, city):
        self.root, inserted = self._insert(self.root, city)
        if inserted:
            self._size += 1

    def _insert(self, node, city):
        if node is None:
            return AVLNode(city), True
        if city.city_id < node.city.city_id:
            node.left, inserted = self._insert(node.left, city)
        elif city.city_id > node.city.city_id:
            node.right, inserted = self._insert(node.right, city)
        else:
            node.city = city
            return node, False
        return self._rebalance(node), inserted

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
        elif city_id > node.city.city_id:
            node.right, deleted = self._delete(node.right, city_id)
        else:
            deleted = True
            if node.left is None:
                return node.right, deleted
            if node.right is None:
                return node.left, deleted
            successor = node.right
            while successor.left is not None:
                successor = successor.left
            node.city = successor.city
            node.right, _ = self._delete(node.right, successor.city.city_id)
        if node is None:
            return None, deleted
        return self._rebalance(node), deleted

    def height(self):
        return self._h(self.root)

    def __len__(self):
        return self._size