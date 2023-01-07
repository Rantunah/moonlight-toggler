import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from time import sleep

import psutil
import tomllib

GAMESTREAM_EXE = "nvstreamer.exe"
CONNECTED = (47984, "SYN_RECV")
STREAMING = (48010, "TIME_WAITING")
SWITCHER_EXE = "MonitorSwitcher.exe"

# Checks if the script is a file or an executable and sets a variable with the correct
# file / executable directory
script_dir: Path = Path("")
if getattr(sys, "frozen", False):
    script_dir = Path(sys.executable).parent.resolve()
elif __file__:
    script_dir = Path(__file__).parent.resolve()


@dataclass
class Settings:
    """Responsible for building the paths that are required for the script to work.

    Attributes:
        script_dir (Path): Folder directory of the script .py or .exe
        executable_path (Path):
        profile_path (Path):
        monitor_profile (Path):
        remote_profile (Path):
    """

    executable_path: Path = Path("")
    profile_path: Path = Path("")
    monitor_profile: Path = Path("")
    remote_profile: Path = Path("")

    def set_config(self, config: dict) -> None:
        """Processes the data from the 'config.toml' file and generates all the paths
        required for the script to work.

        Args:
            config (dict): Dict that was loaded from a 'config.toml' file
        """

        self.executable_path = (
            script_dir.joinpath(config["executable"]["path"]).resolve() / SWITCHER_EXE
        )
        self.profile_path = script_dir.joinpath(config["profile"]["path"]).resolve()
        self.monitor_profile = (
            self.profile_path / f"{config['profile']['name']['monitor']}.xml"
        )
        self.remote_profile = (
            self.profile_path / f"{config['profile']['name']['remote']}.xml"
        )


@dataclass
class Commands:
    """Responsible for building the commands the script passes to 'MonitorSwitcher.exe'"""

    monitor: str = ""
    remote: str = ""
    # NOT IMPLEMENTED YET
    extended: str = ""

    def make_commands(self, settings: Settings):
        """Takes the configuration loaded in settings and builds the commands that are
        passed to 'MonitorSwitcher.exe'

        Args:
            settings (Settings): Settings object with configuration from the 'config.toml'
        """
        self.monitor = f"{settings.executable_path} -load:{settings.monitor_profile}"
        self.remote = f"{settings.executable_path} -load:{settings.remote_profile}"


def load_config_file() -> dict:
    """Loads the 'config.toml' file that's located in the script's parent folder and
    returns it's contents. These contents are then used by a method in the Settings Class.

    Returns:
        dict: Contents from 'config.toml'
    """
    try:
        with open(script_dir.parent / "config.toml", "rb") as config_file:
            config = tomllib.load(config_file)
        return config
    except FileNotFoundError as config_error:
        config_error.add_note(f"Could not find 'config.toml' in {script_dir.parent}")


def check_port(port_status: tuple[int, str]) -> bool:
    """Checks a port for a connection's status and returns a bolean

    Args:
        port_status (tuple[int, str]): A tuple containing a port integer and a status string

    Returns:
        bool: True if there is a connection to the port with the specified status
    """

    # Iterable with all TCP connections
    connections = psutil.net_connections(kind="tcp")
    for connection in connections:
        # Check if the port has the specified status
        # port_status[0] is the port number and [1] is the status
        if (
            connection.laddr.port == port_status[0]  # type: ignore
            and connection.status == port_status[1]
        ):
            return True
    return False


def check_gamestream_exists() -> bool:
    """Checks if the streaming process is already running and returns a boolean value.

    Returns:
        bool: True if the streaming process is running
    """
    # Iterate through all processes' names and checks against them
    return GAMESTREAM_EXE in [
        process.info["name"] for process in psutil.process_iter(["name"])
    ]


def get_gamestream_pid() -> int:
    """Gets the PID of the GameStream process that's already running.

    Returns:
        int: PID of the GameStream process
    """
    # Iterate through all processes' names, pids and checks against them
    pid = [
        process.info["pid"]
        for process in psutil.process_iter(["name", "pid"])
        if process.info["name"] == GAMESTREAM_EXE
    ][0]
    return pid


def main():
    settings = Settings()
    # Load settings from the 'config.toml' and set the class attributes with that data
    config = load_config_file()
    settings.set_config(config)

    commands = Commands()
    # Set the MonitorSwitcher commands with the data from settings
    commands.make_commands(settings)

    # Always default to the monitor. Useful if the script is running at startup and
    # there is no output because the last used screen was the HDMI dongle.
    subprocess.run(commands.monitor)
    while True:
        # Check if already streaming
        streaming = check_gamestream_exists() or check_port(STREAMING)
        if streaming:
            # Switch to the remote screen
            subprocess.run(commands.remote)
            # Hack to allow the user to disconnect and reconnect manually to restore cursor scale.
            sleep(10)
            # Get a hold of the streaming service's PID and use it to wait for the process
            # to end to switch monitors
            gamestream_running = check_gamestream_exists()
            if gamestream_running:
                pid = get_gamestream_pid()
                nvidia_process = psutil.Process(pid)
                # Switch to the monitor after the stream ends.
                nvidia_process.wait()
                subprocess.run(commands.monitor)
        # Loop that starts the toggle behaviour
        while not streaming:
            if streaming:
                subprocess.run(commands.remote)
                break
            # Checks the TCP status for the configured port toggles the stream at the
            # earliest possible(tm) time
            streaming = check_port(CONNECTED)


if __name__ == "__main__":
    main()
