import subprocess

def sudo(cmd):
    #print(['sudo'] + cmd)
    return subprocess.Popen(['sudo'] + cmd,
                       stderr = subprocess.PIPE,
                       stdout = subprocess.PIPE,
                       stdin = subprocess.PIPE)

def exec(cmd):
    #print(cmd)
    return subprocess.Popen(cmd,
                       stderr = subprocess.PIPE,
                       stdout = subprocess.PIPE,
                       stdin = subprocess.PIPE)

def communicate(proc, cmd):
    data = proc.communicate()

    if proc.returncode != 0:
        raise Exception('Command failed: ' + data[1].decode())

    return data[0].decode()
