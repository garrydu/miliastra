import json
import base64
from typing import Any, Dict

def decode_base64_fields(obj: Any, depth: int = 0, max_depth: int = 10) -> Any:
    """
    Recursively process the object and decode base64 strings where possible.
    Adds metadata to help identify decoded fields.
    """
    if depth > max_depth:
        return obj
    
    if isinstance(obj, dict):
        result = {}
        for key, value in obj.items():
            # Process the key to handle special suffixes
            clean_key = key
            field_type = None
            
            if '@' in key:
                clean_key, field_type = key.rsplit('@', 1)
            
            # Recursively process the value
            processed_value = decode_base64_fields(value, depth + 1, max_depth)
            
            # Store with metadata if it had a type annotation
            if field_type:
                result[key] = {
                    '_original_key': key,
                    '_type': field_type,
                    '_value': processed_value
                }
            else:
                result[key] = processed_value
                
        return result
    
    elif isinstance(obj, list):
        return [decode_base64_fields(item, depth + 1, max_depth) for item in obj]
    
    elif isinstance(obj, str):
        # Try to decode if it looks like base64
        if len(obj) > 20 and ('==' in obj[-2:] or len(obj) % 4 == 0):
            try:
                decoded = base64.b64decode(obj)
                return {
                    '_base64_decoded': True,
                    '_original': obj,
                    '_decoded_bytes': list(decoded[:100]),  # First 100 bytes as list
                    '_decoded_length': len(decoded),
                    '_decoded_hex': decoded[:50].hex()  # First 50 bytes as hex
                }
            except:
                pass
        return obj
    
    else:
        return obj


def convert_to_editable(input_file: str, output_file: str):
    """
    Convert the JSON file to a more editable format.
    """
    # Read the input JSON
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Process the data
    editable_data = decode_base64_fields(data)
    
    # Write to output file with pretty printing
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(editable_data, f, indent=2, ensure_ascii=False)
    
    print(f"Converted data saved to: {output_file}")
    print(f"Original structure preserved with metadata for reconstruction")


def reconstruct_original(editable_file: str, output_file: str):
    """
    Reconstruct the original format from the editable version.
    """
    with open(editable_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    def rebuild(obj: Any) -> Any:
        if isinstance(obj, dict):
            # Check if this is a metadata wrapper
            if '_original_key' in obj and '_type' in obj and '_value' in obj:
                return rebuild(obj['_value'])
            
            # Check if this is a base64 decoded object
            if '_base64_decoded' in obj and obj['_base64_decoded']:
                return obj['_original']
            
            # Otherwise recursively rebuild
            result = {}
            for key, value in obj.items():
                result[key] = rebuild(value)
            return result
        
        elif isinstance(obj, list):
            return [rebuild(item) for item in obj]
        
        else:
            return obj
    
    original_data = rebuild(data)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(original_data, f, ensure_ascii=False)
    
    print(f"Original format reconstructed and saved to: {output_file}")


# Example usage
if __name__ == "__main__":
    # Convert to editable format
    convert_to_editable("input.json", "editable.json")
    
    # To convert back to original format after editing:
    # reconstruct_original("editable.json", "output.json")
