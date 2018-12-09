import lib.proc as proc

def get_installed():
    return [line.split(' ')[0] for line in pacman(['-Q']).split('\n')[:-1]]

def install(package):
    output = pacman(['-S', package], True)

def install_all(packages):
    output = pacman(['-S'] + packages, True)

def pacman(flags, sudo = False):
    cmd = ['pacman', '--noconfirm'] + flags
    subproc = proc.sudo(cmd) if sudo else proc.exec(cmd)
    return proc.communicate(subproc, cmd)
