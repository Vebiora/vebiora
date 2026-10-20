import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.memory.short_memory import short_mem
from app.core.assistant import Brain
times = 0
if __name__ == "__main__":
    while times < 2:
        short_memory = short_mem()
        brain = Brain(short_memory)
        mode_select = input("\nmode: ")
        brain.change_modes(mode=mode_select)
        user_input = input("Say: ")

        answer = brain.Ask(user_input=user_input)
        print(answer)
        #print(f"Content: {answer["choices"][0]["message"]["content"]}")
        #print(f"Thinking: {answer["choices"][0]["message"]["reasoning_content"]}")
        times += 1
