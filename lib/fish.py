import lib.proc as proc

def fish(path):
    cmd = ['fish', str(path.expanduser())]
    subproc = proc.exec(cmd)
    return proc.communicate(subproc, cmd)
