import os
import distutils
from pathlib import Path
import lib.pacman as pacman
from lib.package import Package

installed_packages = pacman.get_installed()

def copy(source, dest):
    print(source, '->', dest)
    if source.is_dir():
        pass#distutils.dir_util.copy_tree(source.absolute(), dest.absolute())
    else:
        pass#distutils.file_util.copy_file(source.absolute(), dest.absolute())

def import_item(path):
    copy(Path('~') / path, Path('./lain') / path)

def export_item(path):
    copy(Path('./lain') / path, Path('~') / path)

def install(package):
    if not package.install or not package.source:
        return
    if package.source == 'core' and package.name not in installed_packages:
        res = pacman.install(package.name)
        

def export_config(package):
    if not package.export_config or not package.config:
        return

    export_item(package.config)

def import_config(package):
    if not package.config:
        return

    import_item(package.config)

def run_script(package):
    if not package.run_script or not package.script:
        return

def export_units(package):
    if not package.export_units or not package.userunits:
        return

    for unit in package.userunits:
        export_item(unit)

def import_units(package):
    if not package.userunits:
        return

    for unit in package.userunits:
        import_item(unit)

def deploy(package):
    if not package.enabled:
        return
    install(package)
    export_config(package)
    run_script(package)
    export_units(package)
    
