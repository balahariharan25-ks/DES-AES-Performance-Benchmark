# =========================================
# DES vs AES Performance Benchmark (FINAL)
# =========================================

import time
import os
import psutil
import pandas as pd
import matplotlib.pyplot as plt

from Crypto.Cipher import AES, DES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad


# -------------------------------
# AES-256 Encryption (EAX Mode)
# -------------------------------
def aes_encrypt(data):
    key = get_random_bytes(32)
    cipher = AES.new(key, AES.MODE_EAX)

    cipher.encrypt_and_digest(data)


# -------------------------------
# DES Encryption (ECB Mode - SAFE)
# -------------------------------
def des_encrypt(data):
    key = get_random_bytes(8)
    cipher = DES.new(key, DES.MODE_ECB)

    padded_data = pad(data, 8)  # block size = 8
    cipher.encrypt(padded_data)


# -------------------------------
# Generate Data
# -------------------------------
def generate_data(size_mb):
    return b'a' * (size_mb * 1024 * 1024)


# -------------------------------
# Measure Performance
# -------------------------------
def measure(func, data):
    process = psutil.Process(os.getpid())

    mem_before = process.memory_info().rss
    start_cpu = process.cpu_times()
    start_time = time.time()

    func(data)

    end_time = time.time()
    end_cpu = process.cpu_times()
    mem_after = process.memory_info().rss

    time_taken = end_time - start_time
    cpu_used = end_cpu.user - start_cpu.user
    memory_used = mem_after - mem_before

    return time_taken, memory_used, cpu_used


# -------------------------------
# Run Benchmark
# -------------------------------
def run_benchmark():
    sizes = [1, 5, 10, 50, 100]  # MB
    results = []

    print("\nStarting Benchmark...\n")

    for size in sizes:
        print(f"Testing file size: {size} MB")

        data = generate_data(size)

        aes_runs = []
        des_runs = []

        # Run multiple times for accuracy
        for _ in range(3):
            aes_runs.append(measure(aes_encrypt, data))
            des_runs.append(measure(des_encrypt, data))

        # Average results
        aes_avg = [sum(x)/3 for x in zip(*aes_runs)]
        des_avg = [sum(x)/3 for x in zip(*des_runs)]

        results.append({
            "Size (MB)": size,
            "AES Time (s)": aes_avg[0],
            "AES Memory (bytes)": aes_avg[1],
            "AES CPU": aes_avg[2],
            "DES Time (s)": des_avg[0],
            "DES Memory (bytes)": des_avg[1],
            "DES CPU": des_avg[2],
        })

    print("\nBenchmark Completed Successfully!\n")
    return results


# -------------------------------
# Save Results
# -------------------------------
def save_results(results):
    df = pd.DataFrame(results)
    df.to_csv("results.csv", index=False)
    print("Results saved to results.csv")
    return df


# -------------------------------
# Plot Graphs
# -------------------------------
def plot_results(df):

    # Time
    plt.figure()
    plt.plot(df["Size (MB)"], df["AES Time (s)"], marker='o', label="AES-256")
    plt.plot(df["Size (MB)"], df["DES Time (s)"], marker='o', label="DES")
    plt.xlabel("File Size (MB)")
    plt.ylabel("Time (seconds)")
    plt.title("Encryption Time Comparison")
    plt.legend()
    plt.grid()

    # Memory
    plt.figure()
    plt.plot(df["Size (MB)"], df["AES Memory (bytes)"], marker='o', label="AES")
    plt.plot(df["Size (MB)"], df["DES Memory (bytes)"], marker='o', label="DES")
    plt.xlabel("File Size (MB)")
    plt.ylabel("Memory (bytes)")
    plt.title("Memory Usage Comparison")
    plt.legend()
    plt.grid()

    # CPU
    plt.figure()
    plt.plot(df["Size (MB)"], df["AES CPU"], marker='o', label="AES")
    plt.plot(df["Size (MB)"], df["DES CPU"], marker='o', label="DES")
    plt.xlabel("File Size (MB)")
    plt.ylabel("CPU Time (seconds)")
    plt.title("CPU Usage Comparison")
    plt.legend()
    plt.grid()

    plt.show()


# -------------------------------
# MAIN
# -------------------------------
if __name__ == "__main__":
    results = run_benchmark()
    df = save_results(results)
    plot_results(df)