import logging
import argparse

# -- Verbose ----
Verbose_mode = False
class VebioraFormatter(logging.Formatter):
    COLORS = {
        logging.DEBUG: "\033[92m",
        logging.INFO: "\033[96m",
        logging.WARNING: "\033[93m",
        logging.ERROR: "\033[91m",
        logging.CRITICAL: "\033[95m"
    }
    RESET = "\033[0m"

    def format(self, record):
        color = self.COLORS.get(record.levelno, self.RESET)
        message = super().format(record)
        return f"{color}{message}{self.RESET}"
    
def setup_logging(verbose: bool) -> logging.Logger:
    logger = logging.getLogger("Vebiora")

    handler = logging.StreamHandler()
    handler.setFormatter(
        VebioraFormatter(
            "vebiora-Logger: (%(levelno)d) [%(levelname)s]: %(message)s" 
        )
    )

    logger.handlers.clear()
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)
    logger.propagate = False
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("http.client").setLevel(logging.WARNING)
    return logger

# -- Argparse ----
def build_parser() -> argparse.ArgumentParser:
    logger = setup_logging(Verbose_mode)
    logger.debug("created parser.")
    parser = argparse.ArgumentParser(description="Python porting for Vebiora-AI.")
    parser.add_argument("--config", "-c", action="store_true", help="Path to custom JSON file.")
    parser.add_argument("--prompt", "-p", type=str, help="Pass a query directly without launching the interactive prompt session.")
    parser.add_argument("--version", action="store_true", help="Show Version of Tool.")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show information that could help with debugging.")

    return parser