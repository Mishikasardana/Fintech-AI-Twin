import hashlib
import json
from typing import List, Union


def sha256(data: Union[str, bytes, dict, list]) -> str:
    """Safe hashing for strings, bytes, dicts, lists."""
    
    # If dict or list → convert to canonical JSON
    if isinstance(data, (dict, list)):
        data = json.dumps(data, sort_keys=True)

    # If string → encode to bytes
    if isinstance(data, str):
        data = data.encode("utf-8")

    # Ensure now data is bytes
    return hashlib.sha256(data).hexdigest()


def merkle_root(leaves: List[Union[str, bytes]]) -> str:
    """Compute Merkle root from list of leaves."""
    if not leaves:
        return ""

    # Normalize leaves into SHA hashes
    level = [sha256(l) for l in leaves]

    while len(level) > 1:

        # If odd number → duplicate last
        if len(level) % 2 == 1:
            level.append(level[-1])

        new_level = []
        for i in range(0, len(level), 2):
            combined = (level[i] + level[i + 1]).encode("utf-8")
            new_level.append(sha256(combined))

        level = new_level

    return level[0]
