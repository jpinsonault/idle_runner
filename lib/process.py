import psutil
import time

import win32api

from psutil._common import STATUS_SUSPENDED, STATUS_RUNNING, STATUS_STOPPED

import config


def run_stop_start_process(command):
    last_input = win32api.GetLastInputInfo()
    start_idle_time = time.time()
    counter = 0

    process = None

    while True:
        time.sleep(.5)
        new_last_input = win32api.GetLastInputInfo()

        if new_last_input != last_input:
            last_input = new_last_input
            start_idle_time = time.time()
            kill_process(process)
        else:
            total_idle_time = time.time() - start_idle_time
            if counter % 20 == 0:
                print("{}s left".format(int(config.idle_threshold_seconds - total_idle_time)))
            if total_idle_time > config.idle_threshold_seconds and process is None:
                process = start_process(get_program_command())

        counter += 1


def run_pausing_process(command, idle_threshold_seconds):
    last_input = win32api.GetLastInputInfo()
    start_idle_time = time.time()
    counter = 0

    process = start_process(command)

    while True:
        time.sleep(.5)
        new_last_input = win32api.GetLastInputInfo()

        if new_last_input != last_input:
            last_input = new_last_input
            start_idle_time = time.time()

            if process.status() == STATUS_RUNNING:
                pause_process(process)
        else:
            total_idle_time = time.time() - start_idle_time
            if counter % 20 == 0 and process.status() == STATUS_SUSPENDED:
                print("{}s left".format(int(idle_threshold_seconds - total_idle_time)))
            print(total_idle_time)
            if total_idle_time > idle_threshold_seconds and process.status() == STATUS_STOPPED:
                unpause_process(process)

        counter += 1


def start_process(command):
    print("Starting process: {}".format(" ".join(command)))
    return psutil.Popen(command)


def kill_process(process):
    print("Killing process: {}".format(process))
    process.kill()


def pause_process(process):
    print("Pausing process: {}".format(process))
    process.suspend()


def unpause_process(process):
    print("Unpausing process: {}".format(process))
    process.resume()


def get_program_command():
    return config.command
