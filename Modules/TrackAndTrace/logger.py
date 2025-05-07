import os
from datetime import datetime
from abc import ABC

message_types = {
    1: "Debug",
    2: "Info",
    3: "Error",
}


class RPALogger:
    def __init__(self, pLog_dir, log_type, env):
        try:
            """
            Initialize the Logger class.

            :param log_dir: Directory to store log files.
            """

            if pLog_dir.strip() == "":
                pLog_dir = "C:\\RPA_Log\\Logs"

            self.log_dir = pLog_dir
            if not os.path.exists(self.log_dir):
                os.makedirs(self.log_dir)
            self.file_name = ""
            self.log_type = log_type
            self.env = env
        except Exception as e:
            print("Failed to init Logger")

    def get_file_name(self):
        now = datetime.now()
        self.file_name = (
            self.log_dir + f"\\{self.log_type}_" + now.strftime("%Y%m%d") + ".txt"
        )

        return self.file_name

    def format_message(self, message):
        now = datetime.now()
        formatted = now.strftime("%Y-%m-%d %H:%M:%S") + ": "
        formatted_message = formatted + message + "\n"

        return formatted_message

    def write_message(self, message):
        with open(self.get_file_name(), "a") as file:
            file.write(self.format_message(message))

    def debug(self, message):
        if self.env == "development":
            self.write_message(f"{message_types.get(1,"")} --> {message}")

    def info(self, message):
        self.write_message(f"{message_types.get(2,"")} --> {message}")

    def error(self, message):
        self.write_message(f"{message_types.get(3,"")} --> {message}")
