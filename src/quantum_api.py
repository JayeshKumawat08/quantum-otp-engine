import os
import requests
import warnings

def fetch_quuatum_entropy(required_bytes : int) -> bytearray:
    """
    Fetches true random numbers from the ANU Quantum API in 1024-byte batches.
    Falls back to os.urandom if the network connection fails or times out.
    """

    collected_bytes = bytearray()
    batch_limit = 1024

    while len(collected_bytes) < required_bytes:
        #calculte how many bytes still remaining for this loop
        batch_size = min(batch_limit, required_bytes - len(collected_bytes))

        try:
            response = requests.get(
                url = "https://qrng.anu.edu.au/API/jsonI.php",
                params = {"length" : batch_size, "type" : "uint8"},
                timeout = 5.0
            )
            response.raise_for_status()
            data = response.json()

            if data.get("success"):
                #append the newly fetched quantum bytes to our running total
                collected_bytes.extend(data["data"])
            else:
                raise ValueError("API returned unsuccessful status.")

        except (requests.RequestException, ValueError) as e:
            #if the network drops, fallback to the OS entropy to prevent crashing.
            warnings.warn(f"ANU API unreachable ({e}). Failing back to OS CSPRNG")
            remaining_bytes =  remaining_bytes - len(collected_bytes)
            collected_bytes.extend(os.urandom(remaining_bytes))
            break

    return collected_bytes


