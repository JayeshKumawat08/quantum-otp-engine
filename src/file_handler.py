import os

def read_file_bytes(filepath: str) -> bytearray:
    """
    reads the file in binary mode and returns its content  as mutable binary code for inplace mutation
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Source file not found at: {filepath}")
    
    with open(filepath, "rb") as file_stream:
        raw_bytes = file_stream.read()
        
    return bytearray(raw_bytes)

def write_file_bytes(filepath: str, data: bytes | bytearray) -> None:
    """
    Writes raw bytes or a bytearray directly to disk in binary mode ('wb'),
    preventing character encoding corruption.
    """
    with open(filepath, "wb") as file_stream:
        file_stream.write(data)

