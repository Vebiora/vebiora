import sys
import time
import threading


def thinking_animation(stop_event):
    frames = [
        "⠋", "⠙", "⠹", "⠸", "⠼",
        "⠴", "⠦", "⠧", "⠇", "⠏",
    ]

    messages = [
        "thinking",
    ]

    # ANSI escape codes
    CYAN = "\033[96m"
    BLUE = "\033[94m"
    DIM = "\033[2m"
    RESET = "\033[0m"

    start = time.monotonic()
    frame = 0
    message_index = 0

    # Change the status message every ~1.5 seconds.
    message_timer = start

    try:
        while not stop_event.is_set():
            now = time.monotonic()
            elapsed = now - start

            # Rotate through status messages.
            if now - message_timer >= 3:
                message_index = (message_index + 1) % len(messages)
                message_timer = now

            spinner = frames[frame % len(frames)]
            status = messages[message_index]

            # Subtle animated dots.
            dots = "." * ((frame // 3) % 4)

            output = (
                f"{CYAN}{spinner}{RESET} "
                f"{BLUE}VebAI{RESET} "
                f"{status}{dots:<3} "
                f"{DIM}[{elapsed:05.1f}s]{RESET}"
            )

            # Clear the entire current line before drawing.
            sys.stdout.write(f"\r\033[2K{output}")
            sys.stdout.flush()

            frame += 1
            time.sleep(0.08)

    finally:
        # Leave the terminal clean when thinking is finished.
        sys.stdout.write("\r\033[2K")
        sys.stdout.flush()