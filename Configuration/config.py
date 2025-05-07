import json
import os
import atexit

from robocorp import vault, storage


class Config:
    _instance = None

    def __new__(cls, *args, **kwargs):
        # If no instance exists, create it
        if not cls._instance:
            cls._instance = super(Config, cls).__new__(cls)
        return cls._instance

    def __init__(self, env):
        if not hasattr(
            self, "initialized"
        ):  # Ensure the object is only initialized once
            # jsConfig = storage.get_json("RPA_Asset_1st")
            self.env = env
            self.file_path = "Configuration/config.json"
            if self.env == "development":
                self.file_path = "Configuration/config_development.json"
            self.data = {}
            self.load_config()
            self.initialized = True  # Mark the object as initialized

    def load_config(self):
        """Load or reload configuration from the file."""
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as file:
                self.data = json.load(file)

                # current execution path
                self.set_value("code_base_local_path", os.getcwd())

                # set locators path
                default_locators_path = self.get_value("default_locators_path")
                locators_path = (
                    self.get_value("code_base_local_path")
                    + "\\"
                    + (
                        "locators.json"
                        if default_locators_path == None
                        else default_locators_path
                    )
                )
                self.set_value("locators_path", locators_path)
        else:
            raise FileNotFoundError(f"Config file not found: {self.file_path}")

    def get_value(self, key, default=None):
        """Retrieve a value from the config with a default fallback."""
        return self.data.get(key, default)

    def set_value(self, key, value):
        """Update a configuration value dynamically."""
        self.data[key] = value
        self.__state_change = True

    def __save_config(self):
        """Save the current configuration back to the file.
        auto_reload (bool): If True, reload the configuration after saving.
        """
        with open(self.file_path, "w") as file:
            json.dump(self.data, file, indent=4)

    def del_key(self, key):
        if self.get_value(key) != None:
            del self.data[key]
            self.__state_change = True

    def save_on_exit(self):
        """Save the configuration when the program exits."""
        if self.__state_change:
            print("Saving config...")
            self.__save_config()
            print("Finish saving config!")

    def state_has_change(self):
        return self.__state_change
