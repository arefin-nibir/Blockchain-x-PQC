import pandas as pd

# ==========================================
# Blockchain Parameters
# ==========================================

BLOCK_SIZE_BYTES = 1_000_000   # 1 MB block
BASE_TRANSACTION_SIZE = 250    # bytes

# ==========================================
# Benchmark Data
# ==========================================

data = {
    "Algorithm": [
        "ECDSA",
        "ML-DSA-44",
        "Falcon-512",
        "SLH-DSA-128f (SPHINCS+)"
    ],

    "Signature_Size": [
        71,
        2420,
        654,
        17088
    ]
}

df = pd.DataFrame(data)

# ==========================================
# Calculate Blockchain Metrics
# ==========================================

df["Transaction_Size"] = (
    BASE_TRANSACTION_SIZE +
    df["Signature_Size"]
)

df["Transactions_Per_Block"] = (
    BLOCK_SIZE_BYTES //
    df["Transaction_Size"]
)

# Relative TPS estimate
ecdsa_tps = df.loc[
    df["Algorithm"] == "ECDSA",
    "Transactions_Per_Block"
].values[0]

df["Relative_TPS"] = (
    df["Transactions_Per_Block"] /
    ecdsa_tps
)

# ==========================================
# Save Results
# ==========================================

df.to_csv("blockchain_simulation_results.csv", index=False)

print(df)

print("\nSimulation completed.")
print("Results saved to blockchain_simulation_results.csv")
