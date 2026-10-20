## imports
import json
import os
from pathlib import Path

## from imports
from ..utils.setups import setup_logging

## functions
Verbose_mode = False
logger = setup_logging(verbose=Verbose_mode)

## gets and builds paths
memories_path = Path(__file__).resolve().parent.parent.parent / "data" / "conf"

with open(memories_path / "settings.json", "r", encoding = "utf-8") as f:
    setting_data = json.load(f)

## memory class
class short_mem:
    def __init__(self, limit = 20):
        self.memory = [] ## this is where the memories will be stored
        self.limit = limit ## sets the limit on how much the conversation can be

    ## function to add content to the memory list.
    def Add(self, content):
        self.memory.append(content)
        logger.debug("added content to memory")
        
        ## if the limit is reached then it deletes the first conversation.
        if len(self.memory) > self.limit:
            self.memory.pop(0)

    ## function to load the list.
    def load(self):
        logger.debug("loading content from memory")
        return self.memory
        
    ## saves the list to a file.
    def Save(self, name):
        memory = self.load()

        save_path = setting_data["ai_settings"]["short_memory_path"] ## gets the file directory
        
        file_name = str(name).strip().replace(" ", "-") ## makes sure of no spaces
        
        full_path = os.path.join(save_path, f"{file_name}.json") ## makes the file path

        try:
            with open(full_path, "w", encoding = "utf-8") as f:
                json.dump(memory, f, indent = 2, ensure_ascii = False)
        
        except PermissionError:
            print(f"Error: Vebiora does not have permission to write '{full_path}'")

        size_kb = os.path.getsize(full_path) / 1024 ## calculates the file size.
        logger.debug("\nSaved memory in file.\n")

        print("\n[Memory:Save]" + "-" * 42)
        print("Status   : Saved")
        print(f"Name     : {file_name}")
        print(f"Location : {full_path}")
        print(f"Messages : {len(memory)}")
        print(f"Size     : {size_kb:.1f} KB")
        print("-" * 55)

    ## loads the list from a file
    def load_file   (self, name):
        save_path = setting_data["ai_settings"]["short_memory_path"] ## gets the path of files
        file_name = str(name).strip().replace(" ", "-") ## makes sure there is no spaces
        full_path = os.path.join(save_path, f"{name}.json") ## makes the file name

        ## if there is no file returns a error
        if not os.path.exists(full_path):
            logger.error(f"\nMemory '{file_name}' not found.")
            return False

        with open(full_path, "r", encoding = "utf-8") as f:
            self.memory = json.load(f)
        logger.debug("\nLoaded memory from file.\n")

        print("\n[Memory:Load]" + "-" * 42)
        print("Status   : Found")
        print(f"Name     : {file_name}")
        print(f"Location : {full_path}")
        print(f"Messages : {len(self.memory)}")
        print("-" * 55)