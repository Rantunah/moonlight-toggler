import subprocess
from dataclasses import dataclass
from pathlib import Path
from time import sleep

import psutil
import tomllib

PROCESS = "nvstreamer.exe"


@dataclass
class Settings:
    executable_path = None
    profile_path = None
    tv_profile = None
    remote_desktop_profile = None

    def set_config(self, config):
        self.executable_path = Path(config["executable"]["path"])
        self.profile_path = Path(config["profile"]["path"])
        self.tv_profile = self.profile_path / Path(config["profile"]["name"]["tv"])
        self.desktop_profile = self.profile_path / Path(
            config["profile"]["name"]["desktop"]
        )


@dataclass
class Commands:
    tv: str = ""
    desktop: str = ""
    extended_displays: str = ""

    def make_commands(self, settings):
        self.tv = f"{settings.executable_path} -load:{settings.tv_profile}"
        self.desktop = f"{settings.executable_path} -load:{settings.desktop_profile}"


def load_config():
    current_dir = Path(__file__).resolve().parent
    config_path = current_dir.joinpath("config.toml")
    with open(config_path, "rb") as config_file:
        config = tomllib.load(config_file)
    return config


def main():
    settings = Settings()
    config = load_config()
    settings.set_config(config)

    commands = Commands()
    commands.make_commands(settings)

    subprocess.run(commands.tv)
    while True:
        streaming = False
        for process in psutil.process_iter(["name"]):
            if process.name() == PROCESS:
                streaming = True
                pid = process.pid
                break
        if streaming:
            nvidia_process = psutil.Process(pid)
            subprocess.run(commands.desktop)
            nvidia_process.wait()
            subprocess.run(commands.tv)
        else:
            sleep(2)


if __name__ == "__main__":
    main()
