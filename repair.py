import os
from colorama import Fore
import pyfiglet
import time
import shutil
import json

terminalWidth = shutil.get_terminal_size().columns
terminalHeight = shutil.get_terminal_size().lines

asciiArt = pyfiglet.figlet_format("Opulis Text Editor", font="slant")

# Center each line horizontally
centeredArt = "\n".join([line.center(terminalWidth) for line in asciiArt.split("\n")])

# Calculate vertical padding
paddingLines = (terminalHeight - len(centeredArt.split("\n"))) // 2
verticalPadding = "\n" * paddingLines

    # Print centered ASCII art
print(Fore.LIGHTRED_EX + verticalPadding + centeredArt + verticalPadding + Fore.RESET)

time.sleep(4)
os.system('cls')
config = {
            "autosave": {
                "enabled": True,
                "intervalLarge": 10,
                "intervalSmall": 3,
                "path": "autosave/",
                "largeConsideration": 3000,

            },

            "appearance": {
                "theme": "ocean",
                "marginChar": "│",
                "wordwrap": False,
                "syntaxTheme": "medusa",

            },

            "hotkeys": {
                "tabSize": 4,
                "indentWithTabs": True,

            },
            "intro": True,
            "creditScreen": True,
            "pluginsEnabled": True, # For future use
        }

print("Welcome to Opulis Repair")
print("This tool will help you repair your Opulis installation.")

def repair():

    print("Please select an option:")
    print("1. Repair Configuration")
    print("2. Perform a Full Repair")
    print("3. Exit")

    # Get user input
    choice = input("Enter your choice (1, 2 or 3): ")

    if choice == "1":
        print("Repairing configuration...")
        # Check if the config file exists
        if os.path.exists("config.json"):
            # If it exists, delete it
            os.remove("config.json")
            print("Configuration file deleted.")
        else:
            print("Configuration file not found.")
        # Create a new config file with default settings
        with open("config.json", "w") as f:
            f.write(json.dumps(config, indent=4))
        print("New configuration file created.")

        print("Configuration repair completed.")


    elif choice == "2":
        print("Performing a full repair...")
        # Check if the autosave directory exists
        if os.path.exists("autosave"):
            # If it exists, delete it
            shutil.rmtree("autosave")
            print("Autosave directory deleted.")
        else:
            print("Autosave directory not found.")
        # Create a new autosave directory
        os.makedirs("autosave", exist_ok=True)
        print("New autosave directory created.")

        # Check if the config file exists
        if os.path.exists("config.json"):
            # If it exists, delete it
            os.remove("config.json")
            print("Configuration file deleted.")
        else:
            print("Configuration file not found.")

        # Create a new config file with default settings
        with open("config.json", "w") as f:
            f.write(json.dumps(config, indent=4))
        print("New configuration file created.")

        if os.path.exists("error.log"):
            # If it exists, delete it
            os.remove("error.log")
            print("Error log file deleted.")
        
        if os.path.exists("editor.log"):
            # If it exists, delete it
            os.remove("editor.log")
            print("Editor log file deleted.")

        print("Full repair completed.")

    elif choice == "3":
        print("Exiting...")
        exit()

    else:
        print("Invalid choice.")
        time.sleep(2)
        os.system('cls')
        repair()

if __name__ == "__main__":
    repair()

