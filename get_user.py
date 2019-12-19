import subprocess
import signal


def get_current_user():
    processes = subprocess.Popen(['whoami'], stdout=subprocess.PIPE)
    out, _ = processes.communicate()
    out_decoded = (out.decode('UTF-8')).strip()
    return out_decoded


def test():
    print(f"Current User: {get_current_user()}")


if __name__ == "__main__":
    test()
