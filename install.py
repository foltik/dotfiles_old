#!/bin/python
import os
import sys
import argparse
import curses
import distutils.dir_util
import lib.deploy as deploy
from pathlib import Path
from lib.parse import parse
from lib.package import Category, Package
from lib.menu import Menu, ChecklistMenu

parsed_categories = parse('packages.yml')
parsed_packages = [pkg for pkglist in list(map(lambda c: c.packages, parsed_categories)) for pkg in pkglist]

run_installer = False
def run():
    for category in [c for c in parsed_categories if c.enabled]:
        for package in category.packages:
            configure(package)

def dump(package):
    print(package.name + ':')
    for k, v in package.getattrs():
        print('    ' + k, v)

def lookup_package(name):
    try:
        package = next(p for p in parsed_packages if p.name == name or p.alias == name)
        return package
    except StopIteration:
        raise Exception('Package not found: ' + name)

class App:
    def __init__(self, stdscreen):
        self.screen = stdscreen
        curses.curs_set(0)

        def exit_and_run():
            global run_installer
            run_installer = True
            main_menu.exit()

        package_options_menu = Category.config_menu(self.screen, parsed_categories)

        main_menu = Menu(self.screen, 'Main Menu', [
            ('Package Options', package_options_menu.display),
            ('Run Installer', exit_and_run)
        ])

        main_menu.display()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Foltik's super cool dotfiles install script")
    parser.add_argument('packages', metavar='pkg', type=str, nargs='*')
    parser.add_argument('--all', '-a', dest='all', action='store_const', const=True,
                        help='Run on all packages')

    actions = [
        ('--deploy', '-d', deploy.deploy, 'Run all options'),
        ('--install', '-s', deploy.install, 'Install package'),
        ('--config', '-c', deploy.export_config, 'Export package config'),
        ('--import-config', '-C', deploy.import_config, 'Import package config'),
        ('--script', '-x', deploy.run_script, 'Run package script'),
        ('--units', '-u', deploy.export_units, 'Export and enable package units'),
        ('--import-units', '-U', deploy.import_units, 'Import package units'),
        ('--enable-units', '-e', deploy.enable_units, 'Enable package units'),
        ('--dump', '-l', dump, 'Dump package attributes')
    ]

    for action in actions:
        parser.add_argument(action[0], action[1], dest='actions', action='append_const', const=action[2], help=action[3])

    args = parser.parse_args()

    if args.actions != None and args.packages == [] and args.all == True:
        for package in parsed_packages:
            for action in args.actions:
                action(package)
    elif args.actions != None and args.packages != []:
        for package in args.packages:
            for action in args.actions:
                action(lookup_package(package))
    else:
        os.environ.setdefault('ESCDELAY', '0')
        curses.wrapper(App)
        if run_installer:
            run()

    if Path('git').is_dir():
        distutils.dir_util.remove_tree('git')
