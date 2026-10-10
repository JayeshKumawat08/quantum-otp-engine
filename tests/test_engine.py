import os
import sys

# to find src package
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.file_handler import read_file_bytes , write_file_bytes

# absoulte path for the folder 
BASE_DIR =  os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(BASE_DIR,"..","data","dummy.txt")
ouput_file = os.path.join(BASE_DIR,"..","output_test.bin")

# execute read
raw_data = read_file_bytes(input_file)
print(f"Successfully read {len(raw_data)} bytes.")
print(f"Byte Array List: {list(raw_data)}")

#execute wrie
write_file_bytes(ouput_file, raw_data)
print(f"Successfully wrote bytes to {ouput_file}")
