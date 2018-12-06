import os
from pathlib import Path
import lib.pacman as pacman
from lib.package import Package

installed_packages = pacman.get_installed()

def install(package):
    if not package.install or not package.source:
        return
    if package.source == 'core' and package.name not in installed_packages:
        res = pacman.install(package.name)
        

def copy_config(package):
    if not package.copy_config or not package.config:
        return

def run_script(package):
    if not package.run_script or not package.script:
        return

def enable_units(package):
    if not package.enable_units or not package.userunits:
        return

def configure(package):
    if not package.enabled:
        return
    #print(vars(package))
    install(package)
    copy_config(package)
    run_script(package)
    enable_units(package)
    
