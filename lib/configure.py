import os
from subprocess import call
from pathlib import Path

from lib.parse import Package

def install(package):
    if not package.source:
        return

def copy_config(package):
    if not package.config:
        return

def run_script(package):
    if not package.script:
        return

def enable_units(package):
    if not package.userunits:
        return

def configure(package):
    print(vars(package))
    install(package)
    copy_config(package)
    run_script(package)
    enable_units(package)
    
