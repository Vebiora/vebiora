import configparser
import json
from pathlib import Path

APP_NAME = "Vebiora-ai"
VERSION = "Alpha 0.1.0"
default_path = Path(__file__).resolve().parent.parent


def create_settings(config_dir, model_path, data_path, memory_path, llama_, runtime_path=None):

    settings = {
        "app": {
            "name": APP_NAME,
            "version": VERSION,
            "models_path": str(model_path),
            "data_path": str(data_path),
            "memory_path": str(memory_path),
        },

        "runtime": { 
            "available": runtime_path is not None,
            "installed_by_vebiora": llama_,
            "path": str(runtime_path) if runtime_path else None
        },

        "commands": [
            {
                "name": "exit",
                "description": "Exit the program." 
            },
            {
                "name": "model",
                "description": "add model for ollama."
            },
            {
                "name": "help",
                "description": "Show available commands." 
            },
            {
                "name": "clear",
                "description": "Clear the screen." 
            },
            {
                "name": "save",
                "description": "Save the memory of the chat." 
            },
            {
                "name": "load",
                "description": "Load the memory of a saved chat." 
            },
            {
                "name": "mode",
                "description": "Change the mode of the model." 
            },
            {
                "name": "thinking",
                "description": "Turn on/off prompt reasoning." 
            },
        ],

        "agent": {
            "provider": "none"
        },


    "Mode_settings": {
        "default": {
            "temperature": 0.7,
            "max_tokens": 2048,
            "top_p": 0.95,
            "top_k": 40,
            "min_p": 0.02,
            "prompt": "",
            "repeat_penalty": 1.1,
            "thinking": False,
            "effort": "medium"
            },
        "developer": {
            "temperature": 0.15,
            "max_tokens": 6144,
            "top_p": 0.9,
            "top_k": 20,
            "min_p": 0.05,
            "prompt": "",
            "repeat_penalty": 1.05,
            "thinking": True,
            "effort": "high"
            },
        "security": {
            "temperature": 0.15,
            "max_tokens": 4096,
            "top_p": 0.85,
            "top_k": 15,
            "min_p": 0.02,
            "repeat_penalty": 1.1,
            "thinking": True,
            "effort": "high"
            },
        "audit": {
            "temperature": 0.1,
            "max_tokens": 4096,
            "top_p": 0.8,
            "top_k": 10,
            "min_p": 0.01,
            "repeat_penalty": 1.12,
            "thinking": True,
            "effort": "high"
        }
    },
}

    with open(config_dir / "settings.json", "w", encoding='utf-8') as f:
        json.dump(settings, f, indent=4)

def create_config_api(config_dir):
    config = configparser.ConfigParser()

    config["api"] = {
        "openai": "YourKeyHere",
        "anthropic": "YourKeyHere",
        "google": "YourKeyHere",
        "ollama": "YourURLHere"
    }

    with open(config_dir / "API.conf", "w", encoding='utf-8') as f:
        config.write(f)

def ask_(question, kind="yes_no", custom_def=None):
    if kind == "yes_no":
        while True:
            answer = input(f"{question} [y/N]: ").strip().lower()

            if answer in ("y", "yes"):
                return True
            if answer in ("","n", "no"):
                return False
            print("Invalid take.")
            

    if kind == "path":
        while True:
            if custom_def is None:
                path = input(f"{question}:\n> ").strip()

                if not path:
                    print("A path is required.")
                    continue
                
                return Path(path).expanduser().resolve()

            path = input(f"{question} [default='{custom_def}']:\n> ").strip()
            if not path:
                return Path(custom_def).expanduser().resolve()
            return Path(path).expanduser().resolve()

def main():
    llama_ = False
    runtime_path = None
    print("=" * 60)
    print(" "*20, "Vebiora AI Installer. by Mr-LoCOCO")
    print("=" * 60, "\n")
    print("Pick API provider (can be changed later) [enter to skip]:\n1. OpenAI\n2. Anthropic\n3. Google\n4. Ollama - (self-hosted)\n")
    print("-" * 40)
    app_path = ask_("Where shall we install our folders", kind="path", custom_def=default_path / APP_NAME)
    model_path = ask_("Where should we put the models", kind="path", custom_def=app_path /  "models")
    data_path = ask_("Where should we store the data", kind="path", custom_def=app_path / "data")
    memory_path = ask_("Where should we store the memory", kind="path", custom_def=data_path / "memories")
    config_path = ask_("Where should we store the settings", kind="path", custom_def=data_path / "conf")

    print("=" * 60)
    for path in (app_path, model_path, data_path, memory_path, config_path):
        path.mkdir(parents=True, exist_ok=True)
        
        print(f"Created: {path}")
    if llama_:
            runtime_path.mkdir(parents=True, exist_ok=True)
            print(f"Created: {runtime_path}")
    print("=" * 60)
    create_config_api(config_path)
    create_settings(config_dir=config_path, model_path=model_path, data_path=data_path, memory_path=memory_path, llama_=llama_, runtime_path=runtime_path)
    print(f"Created: {config_path / 'Settings.json'}")
    print(f"Created: {config_path / 'API.conf'}")
    
if __name__ == "__main__":
    main()