import os
import sys

#to find src directory files
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))

#importingother file into the main to use them
from src.file_handler import write_file_bytes,read_file_bytes
from src.quantum_api import fetch_quantum_entropy
from src.quantum_encryptor import QuantumEncryptor

def main():
    print("\t\t\tQUANTUM OTP CLI ORCHESTRATOR")

    #user input
    file_path = input("Enter the path of the file to encrypt (e.g., test.png): ").strip()
    if not os.path.exists(file_path):
        print(f"File {file_path} not found")
        return

    passphrase = input("Enter the Master Passphrase to lock the Quantum Key: ").strip()
    engine = QuantumEncryptor()

    #raw binary ingestion
    print('-'*40)
    print(f"/n Reading '{file_path} in raw binary mode...")
    payload_bytes = read_file_bytes(file_path)
    original_hash = engine.generate_checksum(payload_bytes)
    print()
    print(f"Payload SHA-256: {original_hash}")
    print('_'*40)

    #quantum key fetch
    print(f"/n Fetching {len(payload_bytes)} quantum bytes...")
    quantum_key = fetch_quantum_entropy(len(payload_bytes))
    print('-'*40)

    #multi threaded encryp
    print(f"/n Scrambling data via Bitwise XOR engine...")
    ciphertext = engine.execute_xor_cipher(payload_bytes,quantum_key)
    print('-'*40)

    #zero trust key valut
    print(f"/n Wrapping key into PBKDF2 valut...")
    salt, vaulted_key = engine.wrap_and_export_key(quantum_key,passphrase)

    #disk export
    base_name = os.path.splitext(file_path)[0]
    enc_path = base_name + ".enc"
    qkey_path = base_name + ".qkey"
    print('-'*40)

    #save ciphertext
    write_file_bytes(enc_path, ciphertext)
    write_file_bytes(qkey_path, salt + vaulted_key)
    print('-'*40)

    print("\n✅ SUCCESS: Payload mathematically encrypted.")
    print(f"🔒 Ciphertext exported to : {enc_path}")
    print(f"🔑 Vaulted Key exported to: {qkey_path}")

if __name__ == "__main__":
    main()