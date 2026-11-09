import oqs
import time

message = b"Post Quantum Blockchain Research"

# Select Dilithium algorithm
alg_name = "ML-DSA-44"

# Key generation benchmark
start = time.perf_counter()

with oqs.Signature(alg_name) as signer:
    public_key = signer.generate_keypair()

    keygen_time = time.perf_counter() - start

    # Signing benchmark
    start = time.perf_counter()

    signature = signer.sign(message)

    sign_time = time.perf_counter() - start

    # Verification benchmark
    start = time.perf_counter()

    is_valid = signer.verify(message, signature, public_key)

    verify_time = time.perf_counter() - start

# Output
print("=== Dilithium Benchmark ===")
print(f"Algorithm:            {alg_name}")
print(f"Key Generation Time:  {keygen_time:.8f} seconds")
print(f"Signing Time:         {sign_time:.8f} seconds")
print(f"Verification Time:    {verify_time:.8f} seconds")
print(f"Public Key Size:      {len(public_key)} bytes")
print(f"Signature Size:       {len(signature)} bytes")
print(f"Verification Result:  {is_valid}")
