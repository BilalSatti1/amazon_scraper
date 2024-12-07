import json

def read_queries(file_path: str) -> list:
    """Reads queries from a JSON file."""
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except Exception as e:
        print(f"Error reading input file: {e}")
        return []
