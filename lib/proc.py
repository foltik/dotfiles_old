import subprocess

def exec(cmd, sudo = False):
    #print(cmd)
    return subprocess.Popen(['sudo'] + cmd if sudo else cmd,
                       stderr = subprocess.PIPE,
                       stdout = subprocess.PIPE,
                       stdin = subprocess.PIPE)

def communicate(proc, cmd, success_retvals = [0]):
    data = proc.communicate()

    if proc.returncode not in success_retvals:
        raise Exception('Command failed: "' + ' '.join(cmd) + '"' + data[1].decode())

    return data[0].decode()
