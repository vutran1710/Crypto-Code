from typing import Optional, Any, List
from hashlib import sha256
from pprint import pprint


def compute_hash(string: str):
    return sha256(string.encode("utf-8")).hexdigest()


class Node:
    hash: str
    indexes: List[int]
    left: Any = None
    right: Any = None
    parent = None
    is_leaf = False

    def __init__(
        self,
        indexes: List[int],
        value: str = None,
        left: Any = None,
        right: Any = None,
    ):
        self.indexes = indexes if len(indexes) < 2 else [min(indexes), max(indexes)]

        if value:
            self.hash = compute_hash(value)
            self.is_leaf = True
            return

        if left and right:
            self.left = left
            self.right = right
            self.hash = compute_hash(self.left.hash + self.right.hash)
            left.parent = right.parent = self

    def update(self, value: str = None):
        if self.is_leaf:
            self.hash = compute_hash(value)

        if not self.is_leaf:
            self.hash = compute_hash(self.left.hash + self.right.hash)

        if self.parent:
            self.parent.update()


class MerkleTree:
    leaves: List[Node]
    root = None

    def __init__(self, *values):
        self.leaves = [Node([i], value=v) for i, v in enumerate(values)]
        self.__build()

    def __build(self):
        root = None
        branch = self.leaves
        cnt = 0

        while True:
            branches = []

            for idx in range(0, len(branch), 2):
                left = branch[idx]
                right = branch[idx + 1] if idx + 1 < len(branch) else left
                indexes = left.indexes + right.indexes
                new_node = Node(indexes, left=left, right=right)
                branches.append(new_node)

            branch = branches

            if len(branch) == 1:
                root = branch[0]
                break

        self.root = root

    def get_proof(self, value):
        hash = compute_hash(value)
        node = next((c for c in self.leaves if c.hash == hash), None)
        result = []

        while node and node.parent:
            parent = node.parent
            proof = parent.left if node is parent.right else parent.right
            side = "right" if node is parent.right else "left"
            result.append((side, proof.hash))
            node = parent

        return result


def validate_with_root(value, proof, target_hash) -> bool:
    hash = compute_hash(value)

    for item in proof:
        side, proof_hash = item[:2]
        joint_hash = hash + proof_hash if side == "left" else proof_hash + hash
        hash = compute_hash(joint_hash)

    return hash == target_hash
