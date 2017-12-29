from multiprocessing import Process

from lib.process import run_pausing_process
import json


def main():
    config = load_config("config.json")
    start_commands(config)


def start_commands(command_configs):
    processes = []
    for command_config in command_configs:
        process = Process(target=run_pausing_process, args=(command_config["command"], command_config["idle_threshold_seconds"]))
        process.start()
        processes.append(process)

    for process in processes:
        process.join()


def load_config(config_path):
    with open(config_path, 'r') as json_file:
        return json.load(json_file)


if __name__ == '__main__':
    main()