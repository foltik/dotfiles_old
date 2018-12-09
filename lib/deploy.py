import os
import distutils
import subprocess
from pathlib import Path
from lib.package import Package
import lib.proc as proc
import lib.pacman as pacman
import lib.yay as yay
import lib.git as git

installed_packages = pacman.get_installed()

def copy(source, dest):
    print(source, '->', dest)
    if source.is_dir():
        pass#distutils.dir_util.copy_tree(source.absolute(), dest.absolute())
    else:
        pass#distutils.file_util.copy_file(source.absolute(), dest.absolute())

def import_path(paths):
    if not isinstance(paths, list):
        paths = [paths]
    for path in paths:
        copy(Path('~') / path, Path('./lain') / path)

def export_path(paths):
    if not isinstance(paths, list):
        paths = [paths]
    for path in paths:
        copy(Path('./lain') / path, Path('~') / path)

def install(package):
    if not package.install or not package.source:
        return
    if package.source == 'core':# and package.name not in installed_packages:
        print('pacman', package.name)
        #pacman.install(package.name)
    elif package.source == 'aur':# and package.name not in installed_packages:
        print('yay', package.name)
        #yay.install(package.name)
    elif package.source == 'git':
        print('git', package.name)
        #git.clone(package.url, 'git/' + package.name)
        

def export_config(package):
    if not package.export_config or not package.config:
        return
    export_path(package.config)

def import_config(package):
    if not package.config:
        return
    import_path(package.config)

def run_script(package):
    if not package.run_script or not package.script:
        return
    print('fish', package.script)
    #proc.exec(['fish', package.script.absolute()])

def export_units(package):
    if not package.export_units or not package.userunits:
        return
    export_path(package.userunits)

def import_units(package):
    if not package.userunits:
        return
    import_path(package.userunits)

def enable_units(package):
    if not package.enable_units or not package.userunits:
        return
    for unit in package.userunits:
        print('systemctl --user enable', unit.name)
        #proc.exec(['systemctl', '--user', 'enable', unit.name])

def deploy(package):
    if not package.enabled:
        return
    install(package)
    export_config(package)
    run_script(package)
    export_units(package)
    
