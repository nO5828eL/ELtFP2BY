# 代码生成时间: 2025-09-02 08:50:45
import json
def convert_json(input_data, output_format='json'):    """Converts input data to the specified format.

    Args:
        input_data (str): The input data to be converted, expected to be a valid JSON string.
        output_format (str): The desired output format, default is 'json'.

    Returns:
        str: The converted data in the specified format.
    """    try:        # Try to load the input data as JSON        data = json.loads(input_data)    except json.JSONDecodeError as e:        # Handle JSON decoding errors        raise ValueError("Invalid JSON input") from e    # Convert data to the desired format    if output_format == 'json':        return json.dumps(data, indent=4)    elif output_format == 'yaml':        import yaml        # Convert JSON to YAML        return yaml.dump(data, default_flow_style=False)    else:        raise ValueError("Unsupported output format")

def main():    # Example usage of the converter    input_json = "{"name": "John", "age": 30}"    try:        converted_data = convert_json(input_json, 'yaml')        print("Converted Data:", converted_data)    except ValueError as e:        print("Error:", e)
if __name__ == "__main__":
    main()