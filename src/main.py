import subprocess
from dataclasses import dataclass
from pathlib import Path
from time import sleep

import psutil
import tomllib

STREAM_PROCESS = "nvstreamer.exe"
EXECUTABLE = "MonitorSwitcher.exe"


@dataclass
class Settings:
    executable_path = None | Path
    profile_path = None | Path
    monitor_profile = None | Path
    remote_profile = None | Path

    def set_config(self, config):
        self.executable_path = Path(config["executable"]["path"]).resolve() / EXECUTABLE
        self.profile_path = Path(f"{config['profile']['path']}").resolve()
        self.monitor_profile = Path(
            f"{self.profile_path}/{config['profile']['name']['monitor']}.xml"
        ).resolve()
        self.remote_profile = Path(
            f"{self.profile_path}/{config['profile']['name']['remote']}.xml"
        ).resolve()


@dataclass
class Commands:
    monitor: str = ""
    remote: str = ""
    extended: str = ""

    def make_commands(self, settings):
        self.monitor = f"{settings.executable_path} -load:{settings.monitor_profile}"
        self.remote = f"{settings.executable_path} -load:{settings.remote_profile}"


def load_config():
    current_dir = Path(__file__).resolve()
    config_path = current_dir.parents[1] / "config.toml"
    with open(config_path, "rb") as config_file:
        config = tomllib.load(config_file)
    return config


def main():
    settings = Settings()
    config = load_config()
    settings.set_config(config)

    commands = Commands()
    commands.make_commands(settings)

    subprocess.run(commands.monitor)
    while True:
        streaming = False
        for process in psutil.process_iter(["name"]):
            if process.name() == STREAM_PROCESS:
                streaming = True
                pid = process.pid
                break
        if streaming:
            nvidia_process = psutil.Process(pid)
            subprocess.run(commands.remote)
            nvidia_process.wait()
            subprocess.run(commands.monitor)
        else:
            sleep(2)


if __name__ == "__main__":
    main()
