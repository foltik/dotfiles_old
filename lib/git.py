import lib.proc as proc

def clone(url, dest):
    output = git(['clone', url, dest])

def git(flags):
    cmd = ['git'] + flags
    subproc = proc.exec(cmd)
    return proc.communicate(subproc, cmd)
