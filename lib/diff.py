import lib.proc as proc

def diff(file1, file2):
    cmd = ['diff', '-r', str(file1.resolve()), str(file2.expanduser())]
    subproc = proc.exec(cmd)

    delta = proc.communicate(subproc, cmd, [0, 1])
    
    ret = str(file1) + ' vs ' + str(file2) + ': '
    ret += delta if delta != '' else 'Files are identical.'
    return ret
