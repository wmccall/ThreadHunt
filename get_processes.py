import subprocess
import signal
import get_user


def get_pocesseses():
    processes = subprocess.Popen(['ps', '-aux'], stdout=subprocess.PIPE)
    out, _ = processes.communicate()
    out_decoded = out.decode('UTF-8')
    process_for_user = {}
    count = 0
    for row in out_decoded.split('\n'):
        if count != 0:
            split_row = ' '.join(row.split()).split()
            if len(split_row) >= 2:
                user = split_row[0]
                pid = split_row[1]
                if process_for_user.get(user) == None:
                    process_for_user[user] = []
                process_for_user[user].append(pid)
        count += 1
    return process_for_user


def get_current_user_processes():
    return get_pocesseses()[get_user.get_current_user()]


def get_all_processes():
    flat = []
    processes = get_pocesseses()
    for key in processes.keys():
        flat += processes[key]
    return flat


def test():
    print(f"All Processes By User:\n {get_pocesseses()}")
    print(f"Current User Processes:\n {get_current_user_processes()}")
    print(f"All Processes:\n {get_all_processes()}")


if __name__ == "__main__":
    test()
