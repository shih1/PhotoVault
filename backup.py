#!/usr/bin/env python3

import os
import shutil
from pathlib import Path
import yaml

CONFIG_FILE = "config.yaml"  # Name of the configuration file

def load_config():
    """Load configuration from the YAML file."""
    if not Path(CONFIG_FILE).exists():
        raise FileNotFoundError(f"Configuration file '{CONFIG_FILE}' not found. Please create it.")
    with open(CONFIG_FILE, "r") as file:
        return yaml.safe_load(file)

def get_files_in_directory(directory):
    """Get a set of all files in a directory, including subdirectories."""
    files = set()
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            file_path = os.path.relpath(os.path.join(root, filename), start=directory)
            files.add(file_path)
    return files

def backup_new_images(sd_card_path, backup_path):
    """Backup new images from the SD card to the external hard drive."""
    # Get files on the SD card and the backup path
    sd_card_files = get_files_in_directory(sd_card_path)
    backup_files = get_files_in_directory(backup_path)
    
    # Identify files that need to be copied
    new_files = sd_card_files - backup_files
    
    if not new_files:
        print("No new files to back up.")
        return
    
    # Copy new files
    for file in new_files:
        source_file = Path(sd_card_path) / file
        destination_file = Path(backup_path) / file
        destination_file.parent.mkdir(parents=True, exist_ok=True)  # Create directories if needed
        shutil.copy2(source_file, destination_file)  # Preserve file metadata
        print(f"Backed up: {file}")
    
    print("Backup complete!")

def main():
    # Load configuration
    try:
        config = load_config()
    except FileNotFoundError as e:
        print(e)
        return

    # Get paths from the configuration
    sd_card_path = config.get("sd_card_path")
    backup_path = config.get("backup_path")

    if not sd_card_path or not backup_path:
        print("Configuration file is missing required fields: 'sd_card_path' and 'backup_path'.")
        return

    # Check if the SD card is mounted
    if not Path(sd_card_path).exists():
        print("SD card not detected. Please insert the SD card.")
        return
    
    # Ensure the backup path exists
    Path(backup_path).mkdir(parents=True, exist_ok=True)
    
    # Backup new images
    backup_new_images(sd_card_path, backup_path)

if __name__ == "__main__":
    main()
