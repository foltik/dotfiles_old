#!/bin/python
import os
import sys
import argparse
import curses
import lib.deploy as deploy
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

    actions = [
        ('--deploy', '-d', deploy.deploy, 'Run all options'),
        ('--install', '-s', deploy.install, 'Install package'),
        ('--config', '-c', deploy.export_config, 'Export package config'),
        ('--import-config', '-C', deploy.import_config, 'Import package config'),
        ('--script', '-x', deploy.run_script, 'Run package script'),
        ('--units', '-u', deploy.export_units, 'Export and enable package units'),
        ('--import-units', '-U', deploy.import_units, 'Import package units')
    ]

    for action in actions:
        parser.add_argument(action[0], action[1], dest='actions', action='append_const', const=action[2], help=action[3])

    args = parser.parse_args()

    if args.packages == []:
        os.environ.setdefault('ESCDELAY', '0')
        curses.wrapper(App)
        if run_installer:
            run()
    else:
        for action in args.actions:
            for package in args.packages:
                try:
                    pkg = next(pkg for pkg in parsed_packages if pkg.name == package)
                    print(str(action) + ': ' + str(pkg))
                    action(pkg)
                except StopIteration:
                    print('Package not found: ' + package)
                    sys.exit(1)
