import json
import os

class Config:
    """ Read and write the config file.
    
    The config contains two paths:
    * stellaris_dir: Contains gamefiles, e.g., "/<...>/SteamLibrary/steamapps/common/Stellaris".
    * mod_dir: Contains mods, e.g., "/home/<user>/.local/share/Paradox\ Interactive/Stellaris/mod".

    The location of the config is _config_path
    """

    def __init__(self, config_path = ".better_tech_info.conf"):
        self.stellaris_dir = ""
        self.mod_dir = ""
        self._config_path = config_path
        self._stellaris_dir_key = 'stellaris-dir'
        self._mod_dir_key = 'mod-dir'

        # file_not_found is used to not raise an error in the except block.
        file_not_found = False
        try:
            self._read_config()
        except FileNotFoundError:
            file_not_found = True
        if file_not_found:
            self._find_stellaris_dir()
            self._find_mod_dir()
            self._write_config()

    def _read_config(self):
        with open(self._config_path, 'r') as f:
            d = json.load(f)
            self.stellaris_dir = d[self._stellaris_dir_key]
            self.mod_dir = d[self._mod_dir_key]

    def _write_config(self):
        with open(self._config_path, 'w') as f:
            json.dump({
                self._stellaris_dir_key: self.stellaris_dir,
                self._mod_dir_key: self.mod_dir
            }, f, indent=4)

    def _find_stellaris_dir(self):
        self._ask_for_stellaris_dir()
    
    def _find_mod_dir(self):
        self._ask_for_mod_dir()

    def _ask_for_stellaris_dir(self):
        while True:
            print("Please enter the path of the stellaris gamefiles.")
            print("It should be something like /<...>/SteamLibrary/steamapps/common/Stellaris")
            self.stellaris_dir = input("Path: ")
            print()
            if os.path.isdir(self.stellaris_dir):
                break
            print("{dir} does not exist or is no directory.".format(dir=self.stellaris_dir))
            print()
    
    def _ask_for_mod_dir(self):
        while True:
            print("Please enter the path of the stellaris mod folder.")
            print("It should be something like /home/<user>/.local/share/Paradox\ Interactive/Stellaris/mod")
            self.mod_dir = input("Path: ")
            print()
            if os.path.isdir(self.mod_dir):
                break
            print("{dir} does not exist or is no directory.".format(dir=self.mod_dir))
            print()


if __name__ == '__main__':
    c = Config()
    print(c.stellaris_dir)
    print(c.mod_dir)

