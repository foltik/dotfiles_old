import subprocess

def get_installed():
    return [line.split(' ')[0] for line in pacman('-Q').split('\n')[:-1]]

def install(package):
    pacman('-S ' + package)

def pacman(flags, sudo = False):
    cmd = ['sudo', 'pacman'] if sudo else ['pacman']
    cmd += ['--noconfirm', flags]
    proc = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    data = proc.communicate()

    if proc.returncode != 0:
        raise Exception('Command ' + ' '.join(cmd) + ' failed: ' + data[1].decode())

    return data[0].decode()
    
