import time
import win32api
import psutil
import config
from math import floor

idle_threshold = 5*60

def main():
    process = None
    last_input = win32api.GetLastInputInfo()
    start_idle_time = time.time()
    counter = 0
    while True:
        time.sleep(.5)
        new_last_input = win32api.GetLastInputInfo()

        if new_last_input != last_input:
            last_input = new_last_input
            start_idle_time = time.time()
            kill_process(process)
            process = None
        else:
            total_idle_time = time.time() - start_idle_time
            if counter % 20 == 0:
                print("{}s left".format(int(idle_threshold - total_idle_time)))
            if total_idle_time > idle_threshold and process is None:
                process = start_process(get_program_command())

        counter += 1


def start_process(command):
    print("Starting process: {}".format(" ".join(command)))
    return psutil.Popen(command)


def kill_process(process):
    if process:
        print("Killing process: {}".format(process))
        process.kill()


def get_program_command():
    return config.command


main()