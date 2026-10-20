from datetime import datetime

class tools:
    def __int__(self):
        self.TOOLS = {
            "get_time": self.get_time
        }
    def get_time():
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    