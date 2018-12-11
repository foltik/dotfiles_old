import lib.proc as proc

def enable(unit, user):
    flags = (['--user'] if user else []) + ['enable', unit]
    output = systemd(flags)

def systemd(flags):
    cmd = ['systemctl'] + flags
    subproc = proc.exec(cmd)
    return proc.communicate(subproc, cmd)
