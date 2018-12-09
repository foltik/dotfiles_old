import os
import distutils.dir_util
import distutils.file_util
import subprocess
from pathlib import Path
from lib.diff import diff
from lib.package import Package
from lib.path import local_path, deploy_path
import lib.proc as proc
import lib.pacman as pacman
import lib.yay as yay
import lib.git as git

installed_packages = pacman.get_installed()

def copy(source, dest):
    print(source, '->', dest)
    if source.is_dir():
        distutils.dir_util.copy_tree(str(source), str(dest))
    else:
        distutils.file_util.copy_file(str(source), str(dest))

def import_paths(paths, base):
    if not isinstance(paths, list):
        paths = [paths]
    for path in paths:
        copy(deploy_path(path), path)

def export_paths(paths, base):
    if not isinstance(paths, list):
        paths = [paths]
    for path in paths:
        copy(path, deploy_path(path))


def install(package):
    if not package.install or not package.source:
        return
    if package.source == 'core' and package.name not in installed_packages:
        print('pacman -S', package.name)
        pacman.install(package.name)
    elif package.source == 'aur' and package.name not in installed_packages:
        print('yay -S', package.name)
        yay.install(package.name)
    elif package.source == 'git':
        print('git clone', package.name)
        git.clone(package.url, 'git/' + package.name)
        

def export_config(package):
    if not package.export_config or not package.config:
        return
    export_paths(package.config, '.config')

def import_config(package):
    if not package.config:
        return
    import_paths(package.config, '.config')

def diff_config(package):
    if not package.config:
        return
    for config in package.config:
        print(diff(config, deploy_path(config)))

def run_script(package):
    if not package.run_script or not package.script:
        return
    for script in package.script:
        print('fish', script)
        proc.exec(['fish', package.script])

        
def export_units(package):
    if not package.export_units or not package.userunit:
        return
    export_paths(package.userunit, '.config/systemd/user')

def import_units(package):
    if not package.userunit:
        return
    import_paths(package.userunit, 'lain/.config/systemd/user')

def diff_units(package):
    if not package.userunit:
        return
    for unit in package.userunit:
        print(diff(unit, deploy_path(unit)))
    
def enable_units(package):
    if not package.enable_units or not package.userunit:
        return
    for unit in package.userunit:
        print('systemctl --user enable', unit.name)
        #proc.exec(['systemctl', '--user', 'enable', unit.name])


def deploy(package):
    if not package.enabled:
        return
    install(package)
    export_config(package)
    run_script(package)
    export_units(package)
    
