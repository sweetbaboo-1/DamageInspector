import json

def parse_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
    except json.JSONDecodeError:
        print(f"Error: Unable to parse JSON file - {file_path}")

file_path = 'heroIDs.json'  # Replace with your actual file path
parsed_data = parse_json_file(file_path)
