import config
from lib.process import run_pausing_process


def main():
    command = config.command
    idle_threshold_seconds = config.idle_threshold_seconds

    run_pausing_process(command, idle_threshold_seconds)


main()