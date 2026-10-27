## imports
import json
import os
from pathlib import Path

from app.core.assistant import Brain
from app.memory.short_memory import short_mem

## from imports
from app.utils.setups import build_parser, setup_logging
from prompt_toolkit import PromptSession


## path builder
def build_path():
    logger = setup_logging(args.verbose)

    base_dir = Path(__file__).resolve().parent
    
    setting_path = base_dir / "data" / "conf" / "settings.json" ## gets the path for the settings file
    
    try:
        with open(setting_path, 'r', encoding='utf-8') as f:
            setting_data = json.load(f)
            logger.debug("Got setting data")

        return setting_data
    
    except FileNotFoundError:
        logger.error("file not found.")

    except Exception as e:  ## noqa: BLE001
        logger.error(f"Something happen: {e}")
## commands
def build_commands(command_text: str) -> bool: ## so if False then it will count as asking the ai else no. (good for plugging)

    if not command_text.startswith("/"):
         return False
    
    cmd = command_text[1:] ## filters the '/'
    end_command = True ## makes it more understandable

    commands = build_path()['commands'] ## gets the available commands
    names = {command['name'] for command in commands} ## gets the name for etch command

    ## if command is not available returns error
    if cmd not in names:
        print()
        logger.error(f"Unknown command: /{cmd}")
        return end_command


    if cmd == "exit":
        raise SystemExit
    
    if cmd  == "help":
        print("\n\033[94mCommands:\033[0m")
        for item in commands:
            print(f"  {item['name']} --> {item['description']}")
        return end_command
    
    if cmd == "mode":
         select_mode = input("\033[94mSelect mode:\033[0m ").strip().lower()
         brain.change_modes(mode=select_mode)
         return end_command
    
    if cmd == "clear":
         os.system('cls' if os.name == 'nt' else 'clear')
         return end_command
    
    if cmd == "save":
         file_name = input("\033[94mSave memory as:\033[0m ")
         short_memory.Save(name=file_name)
         return end_command
    
    if cmd == "load":
         file_name = input("\033[94Load memory:\033[0m ")
         short_memory.load_file(name=file_name)
         return end_command

    if cmd == "api":
         brain.Change_api()
         return end_command

## main
def main() -> None:
     while True:
        try:

            if build_path()['agent']['provider'] == "none":
                 logger.warning("The provider is none, we automatically started 'change_api'.")
                 brain.Change_api()

            user_input = str(session.prompt("\nYou: ")).lower().strip() ## gets user input
            if not user_input:
                 continue

            if build_commands(user_input):
                 continue

            answer = brain.Ask(user_input=user_input)

            print(f"\033[94mVebiora:\033[0m {answer['answer']}\n")

        except KeyboardInterrupt:
             break    

## misc
session = PromptSession()
short_memory = short_mem()
brain = Brain(short_memory)

## making of main
if __name__ == "__main__":
    parser = build_parser()
    args = parser.parse_args()
    logger = setup_logging(args.verbose)
    logger.debug("logger was created")

    if args.config:
            print(f"Config folder: {Path(__file__).resolve().parent / 'data' / 'conf' / 'settings.json'}")
    if args.version:
            print("Vebiora: 0.1.2")
    if args.prompt:
            brain = Brain(short_memory=short_mem())
            response = brain.Ask(args.prompt)
            print(f"VebAI: {response['answer']}")
    else:
         main()
