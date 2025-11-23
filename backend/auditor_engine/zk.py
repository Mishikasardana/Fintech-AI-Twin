import hashlib, json, time

def generate_zk_proof(data: dict):
    fake_hash = hashlib.sha256(json.dumps(data).encode()).hexdigest()
    return {
        "proof_id": f"zk_{int(time.time())}",
        "valid": True,
        "hash": fake_hash
    }
