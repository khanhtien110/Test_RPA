import os
from datetime import datetime
import time
from Modules.TrackAndTrace import RPALogger


class RPATracker(RPALogger):
    def __init__(self, config):
        try:
            super().__init__(config.data["log_dir"], "Track", config.env)

            self.current_step = 0
            self.start_time = time.time()
            self.end_time = time.time()

            self.sub_step = 0
            self.sub_start_time = time.time()
            self.sub_end_time = time.time()
            self.is_sub_function = False

            self.is_init = True

        except Exception as e:
            print("Failed to init Logger")

    def end_tracking(self, is_end_program=True):
        # is_end_program == False means just end tracking sub function
        if is_end_program == True:
            self.end_time = time.time()
            total_seconds = self.end_time - self.start_time
            super().write_message(
                f"End tracking. Total {self.current_step} steps. Total {total_seconds:.2f} seconds."
            )
        else:
            self.sub_end_time = time.time()
            total_seconds = self.sub_end_time - self.sub_start_time
            super().write_message(
                f"End tracking sub function. Total {self.sub_step} steps. Total {total_seconds:.2f} seconds."
            )
            self.is_sub_function = False

    def start_tracking(self, message):
        # init message
        if self.is_init == True:
            super().write_message(f"Start tracking {message}")
            self.end_time = time.time()
            self.is_init = False
        else:
            self.sub_start_time = time.time()
            self.sub_step = 0
            self.is_sub_function = True
            super().write_message(f"Tracking sub function {message}")

    def track(self, message):
        with open(super().get_file_name(), "a") as file:
            self.current_step = self.current_step + 1
            file.write(super().format_message(message))
            self.end_time = time.time()
            if self.is_sub_function:
                self.sub_end_time = time.time()
                self.sub_step = self.sub_step + 1

    def write_message(self, message, is_track=True):
        if is_track:
            super().write_message(message)
        else:
            with open(super().get_file_name(), "a") as file:
                file.write(message)

    def debug(self, message):
        super().debug(message)
        self.end_time = time.time()
        if self.is_sub_function:
            self.sub_end_time = time.time()

    def info(self, message):
        super().info(message)
        self.end_time = time.time()
        if self.is_sub_function:
            self.sub_end_time = time.time()

    def error(self, message):
        super().error(message)
        self.end_time = time.time()
        if self.is_sub_function:
            self.sub_end_time = time.time()
