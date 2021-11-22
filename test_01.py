from loguru import logger as log
from merkle_tree import MerkleTree, validate_with_root


def test_merkle_tree():
    values = [
        "hello world",
        "goodbye world",
        "very funny",
        "xx",
        "wow",
        "goodbye hello",
        "very sad",
        "xxx",
    ]

    log.debug("\nValues to build...")
    log.info(values)
    tree = MerkleTree(*values)
    current_root = tree.root.hash
    log.debug(f"New tree, with root = {current_root}")

    log.warning("value should change hash-root")
    tree.leaves[2].update("vaicalol")
    new_root = tree.root.hash
    log.debug(f"New hash root = {new_root}")

    assert current_root != new_root

    tree.leaves[2].update("lolcavai")
    log.debug(f"New hash root = {tree.root.hash}")

    log.warning("Proof & validating root")

    def check(value: str):
        log.debug(">>>> Testing against value = {}", value)
        proof = tree.get_proof(value)

        if not proof:
            log.debug("Invalid value")

        valid = validate_with_root(value, proof, tree.root.hash)
        log.debug(f"Is valid? {valid}")

    list(map(check, ["wow", "Wow", "lolcavai"]))
