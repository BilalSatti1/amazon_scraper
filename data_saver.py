import json

def save_to_json(data, file_name: str):
    """Saves scraped data to a JSON file."""
    try:
        with open(file_name, "w") as file:
            json.dump(data, file, indent=4)
        print(f"Data saved to {file_name}")
    except Exception as e:
        print(f"Error saving file {file_name}: {e}")
