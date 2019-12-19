import subprocess
import signal
import get_processes
import random


def kill_random_user_process(dry=False):
    user_process = get_processes.get_current_user_processes()
    num_processes = len(user_process)
    random_process = random.randint(0, num_processes-1)
    which_process = subprocess.Popen(
        ['ps', '-p', user_process[random_process]], stdout=subprocess.PIPE)
    which_out, _ = which_process.communicate()
    print(f"{'Dry Kill:' if dry else 'Real Kill:'}\n{(which_out.decode('UTF-8')).strip()}")
    if not dry:
        processes = subprocess.Popen(
            ['kill', user_process[random_process]], stdout=subprocess.PIPE)
        out, _ = processes.communicate()
        out_decoded = (out.decode('UTF-8')).strip()


def kill_random_any_process(dry=False, base=0):
    process = get_processes.get_all_processes()
    num_processes = len(process)
    out_decoded = "no process found"
    while "no process found" in out_decoded:
        random_process = random.randint(0, num_processes-1)
        while int(process[random_process]) < base:
            random_process = random.randint(0, num_processes-1)
        print(process[random_process])
        which_process = subprocess.Popen(
            ['ps', '-p', process[random_process]], stdout=subprocess.PIPE)
        which_out, _ = which_process.communicate()
        print(
            f"{'Dry Kill:' if dry else 'Real Kill:'}\n{(which_out.decode('UTF-8')).strip()}")
        if not dry:
            processes = subprocess.Popen(
                ['kill', process[random_process]], stdout=subprocess.PIPE)
            out, _ = processes.communicate()
            out_decoded = (out.decode('UTF-8')).strip()
            print(out_decoded)


def test():
    kill_random_user_process(dry=True)
    kill_random_any_process(dry=False, base=6000)


if __name__ == "__main__":
    test()
