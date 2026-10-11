import os
import time
import requests

# ANU AWS API Configuration
API_KEY = "XU0mG0Vd4paXgbKeqyoT54A8sCiznHvO51QjzLb1"
API_URL = "https://api.quantumnumbers.anu.edu.au"

# Set to True during UI development to save your 100 requests/month quota
DEVELOPER_MODE = True


def fetch_quantum_entropy(required_bytes: int) -> bytearray:
    """Fetches random bytes from the ANU Quantum API in batches of up to 1024 bytes."""
    if DEVELOPER_MODE:
        print(f"[Dev Mode] Generating {required_bytes} bytes locally using os.urandom")
        return bytearray(os.urandom(required_bytes))

    collected = bytearray()
    batch_limit = 1024
    max_retries = 4

    while len(collected) < required_bytes:
        batch_size = min(batch_limit, required_bytes - len(collected))
        batch_data = None

        for attempt in range(1, max_retries + 1):
            try:
                response = requests.get(
                    API_URL,
                    params={"length": batch_size, "type": "uint8"},
                    headers={"x-api-key": API_KEY},
                    timeout=10,
                )
                response.raise_for_status()
                payload = response.json()

                if "data" in payload:
                    batch_data = payload["data"]
                    break
            except (requests.RequestException, ValueError) as err:
                wait_time = 2**attempt
                print(f"Request failed ({err}). Retrying in {wait_time}s ({attempt}/{max_retries})...")
                time.sleep(wait_time)

        if batch_data is None:
            raise ConnectionError(
                f"Failed to fetch quantum bytes from ANU after {max_retries} attempts."
            )

        collected.extend(batch_data)

        # Brief pause between batches to avoid rate limits
        if len(collected) < required_bytes:
            time.sleep(1.0)

    return collected