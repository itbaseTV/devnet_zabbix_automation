import subprocess
import platform


def ping_ok(sHost) -> bool:
    try:
        subprocess.check_output(
            "ping -{} 1 {}".format("n" if platform.system().lower() == "windows" else "c", sHost), shell=True
        )
    except Exception:
        return "FAILED"
    return "OK"


test_ip = '192.168.88.254'
print(ping_ok(test_ip))