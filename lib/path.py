from pathlib import Path

def local_path(*args):
    path = Path('./')
    for arg in args:
        path /= Path(arg)
    return path

def deploy_path(path):
    start = path.parts[0]
    target = path.parts[1:]
    if start == 'lain':
        return Path('~') / Path(*target)
