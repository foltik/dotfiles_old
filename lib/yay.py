import lib.proc as proc

def install(package):
    output = yay(['-S', package], True)

def install_all(packages):
    output = yay(['-S'] + packages, True)

def yay(flags, sudo = False):
    cmd = ['yay', '--noconfirm'] + flags
    subproc = proc.sudo(cmd) if sudo else proc.exec(cmd)
    return proc.communicate(subproc, cmd)
