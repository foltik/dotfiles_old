import lib.proc as proc

def install(package):
    output = yay(['-S', package])

def install_all(packages):
    output = yay(['-S'] + packages)

def yay(flags):
    cmd = ['yay', '--noconfirm'] + flags
    subproc = proc.exec(cmd)
    return proc.communicate(subproc, cmd)
