import os
import json
import logging

def save_to_json(data, file_name, folder_name=None):
    """
    Saves the scraped data to a JSON file in the 'data' directory, optionally within a 
    specified subfolder.

    Args:
        data (list): The data to save.
        file_name (str): The name of the file to save the data in.
        folder_name (str, optional): The name of the subfolder within 'data' to save the file.
        Defaults to None.
    """
    base_directory = 'data'

    if folder_name:
        directory = os.path.join(base_directory, folder_name)
    else:
        directory = base_directory

    if not os.path.exists(directory):
        os.makedirs(directory)

    file_path = os.path.join(directory, file_name)

    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        logging.info('Data successfully saved to %s', file_path)
    except IOError as e:
        logging.error('Failed to save data to %s: %s', file_path, str(e))

def load_from_json(file_name, folder_name=None):
    """
    Loads data from a JSON file located in the 'data' directory, optionally within a 
    specified subfolder.

    Args:
        file_name (str): The name of the file to load the data from.
        folder_name (str, optional): The name of the subfolder within 'data' to load the file from.
        Defaults to None.

    Returns:
        dict or list: The data loaded from the JSON file.
    """
    base_directory = 'data'

    # Construye la ruta del directorio
    if folder_name:
        directory = os.path.join(base_directory, folder_name)
    else:
        directory = base_directory

    file_path = os.path.join(directory, file_name)

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        logging.info('Data successfully loaded from %s', file_path)
        return data
    except FileNotFoundError:
        logging.error('File not found: %s', file_path)
        return None
    except json.JSONDecodeError as e:
        logging.error('Failed to decode JSON from %s: %s', file_path, str(e))
        return None
    except IOError as e:
        logging.error('Failed to load data from %s: %s', file_path, str(e))
        return None

def combine_json_files(input_folder, combined_filename, output_folder=None):
    """
    Combines all JSON files in the specified input folder (inside the 'data' directory)
    into a single JSON file.

    Args:
        input_folder (str): The folder inside 'data' containing the JSON files to combine.
        combined_filename (str): The name of the output combined JSON file.
        output_folder (str, optional): The folder to save the combined JSON file.
        Defaults to the current directory.
    """
    # Define the base directory for input files
    base_input_directory = os.path.join('data', input_folder)
    
    combined_data = {}

    # Loop through all files in the input folder
    for filename in os.listdir(base_input_directory):
        if filename.endswith(".json"):
            filepath = os.path.join(base_input_directory, filename)
            with open(filepath, "r", encoding="utf-8") as file:
                data = json.load(file)
                category_name = os.path.splitext(filename)[0]  # Remove the .json extension
                combined_data[category_name] = data

    # Determine the output directory
    if output_folder:
        output_directory = os.path.join('data', output_folder)
    else:
        output_directory = os.path.join('data', 'combined_output')

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    combined_filepath = os.path.join(output_directory, combined_filename)

    # Guarda los datos combinados en el archivo de salida
    with open(combined_filepath, "w", encoding="utf-8") as outfile:
        json.dump(combined_data, outfile, ensure_ascii=False, indent=4)

    print(f"Archivo JSON combinado guardado en {combined_filepath}")
