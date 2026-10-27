## imports
import json
import sys
import threading
from pathlib import Path

import requests

## from imports
if __package__:
    from ..utils.animation import thinking_animation
    from ..utils.setups import setup_logging
else:
    ## Support running this file directly, when Python has no package context.
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
    from app.utils.animation import thinking_animation
    from app.utils.setups import setup_logging

## path construction
config_path = Path(__file__).resolve().parent.parent.parent / "data" / "conf"

## Functions
Verbose_mode = False
logger = setup_logging(verbose = Verbose_mode)
apis = {}


## load files
with open(config_path / "settings.json", "r") as f:
    setting_data = json.load(f)
with open(config_path / "prompts.json", "r") as f:
    prompts = json.load(f)
with open(config_path / "API.json", "r") as f:
    apis_data = json.load(f)


## build prompt
prompt_data = prompts["prompt"]


## brain class
class Brain:
    def __init__(self, short_memory):
        self.short_memory = short_memory
        self.mode = "default" ## Sets the default mode
        self.base_url = "http://Localhost:8000/v1/chat/completions" ## !! change this later !!
        self.api_key = "none" ## gets api key
        self.model = "Qwen3-30B-A3B-Q4_K_M.gguf" ## Gets model ## !! change this later !!

    ## change the api by checking if api is available in API.json.
    def Change_api(self):
        available_apis = [provider for provider, api in apis_data['providers'].items() if isinstance(api, str) and api.strip() and api.strip() not in ("YourKeyHere")]

        print("\n[Mode:api]" + "-" * 45)
        print("Available:", available_apis)

        if not available_apis:
            logger.error(f"No providers are configured. Check {config_path / 'settings.json'}.")
            return "None"
        
        selected_provider = input("Select provider: ").strip()
        print("-" * 55) 
        
        

        if selected_provider not in available_apis:
            logger.error("Provider not found.")
            return None

        if selected_provider in available_apis:
            logger.debug(f"Changed api to {selected_provider}")
            
            self.api_key = apis_data['providers'][selected_provider]

            setting_data['agent']['provider'] = selected_provider
            with open(config_path / "settings.json", "w") as f:
                json.dump(setting_data, f, indent=4)

    ## changes the mode of ask
    def change_modes(self,mode = "default"):
        modes_list = setting_data['agent']['Mode_settings'] ## gets the modes lists from settings

        print("\n[Mode:Change]" + "-" * 42)
        print("Received:", repr(mode))    
        print("Available:", list(modes_list.keys()))

        ## sets the mode to the default mode if the mode doesn't exits
        if mode not in modes_list:
            print(f"Error: We didn't find {mode}")
            mode = "default"

        ## if the mode exists then passes the mode down
        self.mode = mode
        print(f"Info: mode '{self.mode}' has been successfully set.")
        print("-" * 55)
        return mode

    ## converts raw data in json style
    def convert_data(self, content):
        content = content.decode('utf-8')
        return json.loads(content.removeprefix("data: ").strip())

    ## takes a request with specific settings and act like modes
    def Ask(self,user_input):
        if self.api_key == "none":
            provider = setting_data["agent"]["provider"]

            if provider == "none":
                provider  = self.Change_api()
                if not provider:
                    logger.critical(f"No API provider selected. check 'API.json' at `{config_path}`.")
                    raise RuntimeError("No API provider selected")

            self.api_key = apis_data["providers"].get(provider)

            if not self.api_key:
                raise RuntimeError(f"Invalid API endpoint for provider: {provider}")


        if Verbose_mode == False:
            print()

        logger.debug("getting request data from settings")
        logger.debug(f"Brain called a request with mode={self.mode}")
        
        mode = self.mode ## we get the passed mode

        ## gets the prompt for the selected mode
        system_prompt = "\n".join(
            "\n".join(prompt)
            for prompt in prompt_data[mode].values() )

        ## gets settings for the passed mode
        settings = setting_data['agent']['Mode_settings'][mode]

        ## makes a animation for thinking
        stop_animation = threading.Event() ## this makes the animation to stop
        thinking_thread = threading.Thread(
                target=thinking_animation,
                args=(stop_animation,) )
        
        self.short_memory.Add({"role": "user", "content": user_input}) ## ads user content so the ai will remember
        thinking_thread.start() ## starts the thinking animation
        try:
            ## makes a request with the settings of the selected mode, then returns the answer.
            response = requests.post(
                self.api_key,
                
                json={
                    "stream": True,
                    "model": self.model,
                    "messages":[
                        {
                            "role": "system",
                            "content": system_prompt
                            
                        },
                        *self.short_memory.load()
                    ],
                    "temperature": settings["temperature"],
                    "max_tokens": settings["max_tokens"],
                    "effort": settings["effort"],
                    "top_p": settings["top_p"],
                    "top_k": settings["top_k"],
                    "min_p": settings["min_p"],
                    "repeat_penalty": settings["repeat_penalty"],
                    "extra_body": {"chat_template_kwargs": {"enable_thinking": settings["thinking"]}},
                },
                stream=True,
                timeout=(3, None) ## gets an error if in 3 seconds the server doesn't respond.
            )

            sections = []
            reasoning_sections = []

            
            response.raise_for_status() ## gets the web status
            for content in response.iter_lines():
                if content == b'':
                    continue
                if content == b'data: [DONE]':
                    break

                if text := self.convert_data(content)['choices'][0]['delta'].get('content'):
                    sections.append(text)
                if reasoning := self.convert_data(content)['choices'][0]['delta'].get('reasoning_content'):
                    reasoning_sections.append(reasoning)


            self.short_memory.Add({"role": "assistant", "content": "".join(sections)}) ## ads it's own content so the ai will remember what he said

            return {
                "answer": "".join(sections),
                "selections": sections,
                "reasoning_content": "".join(reasoning_sections),
            }
                
            

            
        
        except requests.exceptions.ConnectionError as e:
            logger.error("Could not connect to AI endpoint (endpoint='%s'): %s", self.api_key, e)
            raise RuntimeError("AI service is unavailable") from e
        
        except requests.exceptions.Timeout as e:
            logger.error("AI endpoint timed out (endpoint='%s'): %s ", self.api_key, e)
            sys.exit() 

        finally:
            stop_animation.set()
            thinking_thread.join()
            logger.debug("Brain added user_input in memory")
            logger.debug(f"Received response with model={self.model}")
            logger.debug("Brain added assistant content in memory\n")
           