class BLinkNode:
    def __init__(self, is_leaf=True, max_keys=3):
        self.is_leaf = is_leaf
        self.max_keys = max_keys
        self.keys = []
        self.values = []
        self.high_key = None
        self.right_link = None

class BLinkTree:
    """Lehman-Yao B-link Tree with concurrent right-traversals."""
    def __init__(self, max_keys=3):
        self.max_keys = max_keys
        self.root = BLinkNode(is_leaf=True, max_keys=max_keys)

    def search(self, key):
        curr = self.root
        while not curr.is_leaf:
            while curr.high_key is not None and key > curr.high_key:
                curr = curr.right_link
            idx = 0
            while idx < len(curr.keys) and key >= curr.keys[idx]:
                idx += 1
            curr = curr.values[idx]

        while curr.high_key is not None and key > curr.high_key:
            curr = curr.right_link

        for i, k in enumerate(curr.keys):
            if k == key:
                return curr.values[i]
        return None

    def insert(self, key, value):
        stack = []
        curr = self.root
        while not curr.is_leaf:
            while curr.high_key is not None and key > curr.high_key:
                curr = curr.right_link
            stack.append(curr)
            idx = 0
            while idx < len(curr.keys) and key >= curr.keys[idx]:
                idx += 1
            curr = curr.values[idx]

        while curr.high_key is not None and key > curr.high_key:
            curr = curr.right_link

        pos = 0
        while pos < len(curr.keys) and curr.keys[pos] < key:
            pos += 1
        if pos < len(curr.keys) and curr.keys[pos] == key:
            curr.values[pos] = value
            return

        curr.keys.insert(pos, key)
        curr.values.insert(pos, value)

        if len(curr.keys) > self.max_keys:
            self._split_and_propagate(curr, stack)

    def _split_and_propagate(self, node, stack):
        mid = len(node.keys) // 2
        new_node = BLinkNode(is_leaf=node.is_leaf, max_keys=self.max_keys)
        new_node.keys = node.keys[mid:]
        new_node.values = node.values[mid:]
        new_node.high_key = node.high_key
        new_node.right_link = node.right_link

        node.keys = node.keys[:mid]
        node.values = node.values[:mid]
        split_key = new_node.keys[0]
        node.high_key = split_key
        node.right_link = new_node

        if node == self.root:
            new_root = BLinkNode(is_leaf=False, max_keys=self.max_keys)
            new_root.keys = [split_key]
            new_root.values = [node, new_node]
            self.root = new_root
            return

        parent = stack.pop()
        pos = 0
        while pos < len(parent.keys) and parent.keys[pos] < split_key:
            pos += 1
        parent.keys.insert(pos, split_key)
        parent.values.insert(pos + 1, new_node)

        if len(parent.keys) > self.max_keys:
            self._split_and_propagate(parent, stack)

    def range_scan(self, min_key, max_key):
        curr = self.root
        while not curr.is_leaf:
            while curr.high_key is not None and min_key > curr.high_key:
                curr = curr.right_link
            idx = 0
            while idx < len(curr.keys) and min_key >= curr.keys[idx]:
                idx += 1
            curr = curr.values[idx]

        results = []
        while curr is not None:
            for k, v in zip(curr.keys, curr.values):
                if min_key <= k <= max_key:
                    results.append((k, v))
                elif k > max_key:
                    return results
            curr = curr.right_link
        return results
