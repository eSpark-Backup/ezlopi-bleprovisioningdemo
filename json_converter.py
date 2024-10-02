import json
import base64

# Specify the path to your JSON file
json_file_path = 'provisioning_data.json'

# Read the JSON data from the file
with open(json_file_path, 'r') as json_file:
    json_data = json.load(json_file)
    minified_json = json.dumps(json_data, separators=(',', ':'))
    print(minified_json)
    base64_encoded = base64.b64encode(minified_json.encode('utf-8')).decode('utf-8')
    print(base64_encoded)
    # Chunk size
    chunk_size = 400

    # Calculate the number of chunks needed
    num_chunks = (len(base64_encoded) + chunk_size - 1) // chunk_size

    # Divide the Base64 string into chunks
    chunks = [base64_encoded[i:i + chunk_size] for i in range(0, len(base64_encoded), chunk_size)]

    # Create a list of dictionaries to store chunks
    chunk_list = []

    # Populate the list with dictionaries
    for idx, chunk in enumerate(chunks, start=1):
        chunk_data = {
            "total_len": len(base64_encoded),
            "len": len(chunk),
            "sequence": idx,
            "data": chunk
        }
        chunk_list.append(chunk_data)

    # Print the list of dictionaries
    for chunk_data in chunk_list:
        json_chunk = json.dumps(chunk_data, indent=4)
        print(json_chunk)
        print("\n")

    # print(chunk_list)

