import os
import sys
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter

# Ensure backend modules can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.quantum_api import fetch_quantum_entropy
from src.quantum_encryptor import QuantumEncryptor

# MATHEMATICAL & VISUALIZATION FUNCTIONS

def calculate_shannon_entropy(data: bytes | bytearray) -> float:
    """Calculates the mathematical Shannon Entropy of the data (Max: 8.0)."""
    if not data: return 0.0
    counts = Counter(data)
    entropy = 0.0
    for count in counts.values():
        probability = count / len(data)
        if probability > 0:
            entropy -= probability * np.log2(probability)
    return entropy

def plot_histogram(data: bytes | bytearray, title: str, color: str):
    """Generates a Byte Frequency Histogram (0-255)."""
    fig, ax = plt.subplots(figsize=(6, 3))
    counts = Counter(data)
    frequencies = [counts.get(i, 0) for i in range(256)]
    
    ax.bar(range(256), frequencies, color=color, alpha=0.8, width=1.0)
    ax.set_title(title, fontsize=10, fontweight='bold')
    ax.set_xlim(0, 255)
    ax.grid(True, alpha=0.3)
    ax.set_facecolor('#f8f9fa')
    return fig

def plot_bit_balance(data: bytes | bytearray, title: str):
    """Generates a Pie Chart showing the ratio of 1s vs 0s at the machine level."""
    # Count total 1s by converting each byte to binary, then subtract from total bits for 0s
    total_ones = sum(bin(byte).count('1') for byte in data)
    total_zeros = (len(data) * 8) - total_ones
    
    fig, ax = plt.subplots(figsize=(3, 3))
    ax.pie([total_zeros, total_ones], labels=['Zeroes (0)', 'Ones (1)'], autopct='%1.2f%%', 
           colors=['#cfd8dc', '#37474f'], startangle=90, 
           wedgeprops={'edgecolor': 'white', 'linewidth': 1.5})
    ax.set_title(title, fontsize=10, fontweight='bold')
    return fig

# STREAMLIT DASHBOARD UI

def render_dashboard():
    st.set_page_config(page_title="Quantum OTP Vault", layout="wide")
    
    st.title("🛡️ Zero-Trust Data Vault")
    st.markdown("Defeating the **Harvest Now, Decrypt Later** threat via True Physical Randomness.")
    st.divider()
    
    # 1. File & Password Ingestion
    col_input1, col_input2 = st.columns(2)
    with col_input1:
        uploaded_file = st.file_uploader("Upload Target Payload (Any format: PDF, PNG, TXT)", type=None)
    with col_input2:
        st.markdown("<br>", unsafe_allow_html=True) # Spacing
        passphrase = st.text_input("Enter Master Passphrase (To lock the Quantum Key):", type="password")
    
    if uploaded_file is not None and passphrase:
        # Load raw binary bypassing UTF-8
        raw_bytes = bytearray(uploaded_file.read())
        engine = QuantumEncryptor()
        
        st.success(f"Payload Ingested: {uploaded_file.name} | Size: {len(raw_bytes) / 1024:.2f} KB")
        
        if st.button("Execute Quantum Encryption", type="primary"):
            with st.spinner("Fetching Quantum Entropy & Scrambling Data..."):
                
                # Baseline Metrics
                original_entropy = calculate_shannon_entropy(raw_bytes)
                original_hash = engine.generate_checksum(raw_bytes)
                
                # Cryptographic Execution
                quantum_key = fetch_quantum_entropy(len(raw_bytes))
                
                # Pass a copy of raw_bytes so we don't mutate the original before graphing
                ciphertext = engine.execute_xor_cipher(bytearray(raw_bytes), quantum_key)
                
                # Zero-Trust Key Vaulting
                salt, vaulted_key = engine.wrap_and_export_key(quantum_key, passphrase)
                cipher_entropy = calculate_shannon_entropy(ciphertext)
                
                st.divider()
                
                # 2. Side-by-Side Visual Proof Layout
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Classical File (Vulnerable)")
                    st.metric("Shannon Entropy", f"{original_entropy:.4f} / 8.0000")
                    st.pyplot(plot_histogram(raw_bytes, "Original Byte Distribution (Spiky = Predictable)", "#d32f2f"))
                    st.pyplot(plot_bit_balance(raw_bytes, "Original Bit Ratio (Skewed)"))
                    
                with col2:
                    st.subheader("Quantum-Seeded OTP (Secure)")
                    st.metric("Shannon Entropy", f"{cipher_entropy:.4f} / 8.0000")
                    st.pyplot(plot_histogram(ciphertext, "Ciphertext Byte Distribution (Flat = True Random)", "#1976d2"))
                    st.pyplot(plot_bit_balance(ciphertext, "Ciphertext Bit Ratio (Perfect 50/50)"))
                
                st.divider()
                
                # 3. Secure File Export
                st.subheader("Secure Export")
                st.info(f"Baseline SHA-256 Integrity Hash: {original_hash}")
                
                dl_col1, dl_col2 = st.columns(2)
                with dl_col1:
                    st.download_button(
                        label="⬇️ Download Ciphertext (.enc)",
                        data=bytes(ciphertext),  # <--- Added bytes() cast here
                        file_name=f"{os.path.splitext(uploaded_file.name)[0]}.enc",
                        mime="application/octet-stream"
                    )
                with dl_col2:
                    st.download_button(
                        label="⬇️ Download Vaulted Key (.qkey)",
                        data=bytes(salt + vaulted_key),  # <--- Added bytes() cast here
                        file_name=f"{os.path.splitext(uploaded_file.name)[0]}.qkey",
                        mime="application/octet-stream"
                    )

if __name__ == "__main__":
    render_dashboard()