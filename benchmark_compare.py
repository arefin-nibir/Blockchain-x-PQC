import time
import csv
import oqs

from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes

# ==========================================
# Configuration
# ==========================================

message = b"Post Quantum Blockchain Research"
TRIALS = 50

results = []

# ==========================================
# ECDSA Benchmark
# ==========================================

ecdsa_keygen = []
ecdsa_sign = []
ecdsa_verify = []

for _ in range(TRIALS):

    start = time.perf_counter()

    private_key = ec.generate_private_key(ec.SECP256R1())
    public_key = private_key.public_key()

    ecdsa_keygen.append(time.perf_counter() - start)

    # Signing
    start = time.perf_counter()

    signature = private_key.sign(
        message,
        ec.ECDSA(hashes.SHA256())
    )

    ecdsa_sign.append(time.perf_counter() - start)

    # Verification
    start = time.perf_counter()

    public_key.verify(
        signature,
        message,
        ec.ECDSA(hashes.SHA256())
    )

    ecdsa_verify.append(time.perf_counter() - start)

results.append([
    "ECDSA",
    sum(ecdsa_keygen) / TRIALS,
    sum(ecdsa_sign) / TRIALS,
    sum(ecdsa_verify) / TRIALS,
    len(signature)
])

# ==========================================
# PQC Benchmark Function
# ==========================================

def benchmark_pqc_algorithm(alg_name):

    keygen_times = []
    sign_times = []
    verify_times = []

    for _ in range(TRIALS):

        with oqs.Signature(alg_name) as signer:

            # Key Generation
            start = time.perf_counter()

            public_key = signer.generate_keypair()

            keygen_times.append(time.perf_counter() - start)

            # Signing
            start = time.perf_counter()

            signature = signer.sign(message)

            sign_times.append(time.perf_counter() - start)

            # Verification
            start = time.perf_counter()

            signer.verify(message, signature, public_key)

            verify_times.append(time.perf_counter() - start)

    results.append([
        alg_name,
        sum(keygen_times) / TRIALS,
        sum(sign_times) / TRIALS,
        sum(verify_times) / TRIALS,
        len(signature)
    ])

# ==========================================
# Run PQC Benchmarks
# ==========================================

benchmark_pqc_algorithm("Dilithium2")

benchmark_pqc_algorithm("Falcon-512")

benchmark_pqc_algorithm("SPHINCS+-SHA2-128f-simple")

# ==========================================
# Save Results
# ==========================================

with open("benchmark_results.csv", "w", newline="") as file:

    writer = csv.writer(file)

    writer.writerow([
        "Algorithm",
        "Avg KeyGen Time",
        "Avg Sign Time",
        "Avg Verify Time",
        "Signature Size"
    ])

    writer.writerows(results)

# ==========================================
# Completion Message
# ==========================================

print("Benchmark completed.")
print("Results saved to benchmark_results.csv")
