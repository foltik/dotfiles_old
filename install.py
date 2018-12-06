#!/bin/python
import curses
import os
from lib.parse import parse
from lib.package import Category, Package
from lib.menu import Menu, ChecklistMenu
from lib.configure import configure

categories = parse('packages.yml')

run_installer = False
def run():
    for category in [c for c in categories if c.enabled]:
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

        package_options_menu = Category.config_menu(self.screen, categories)

        main_menu = Menu(self.screen, 'Main Menu', [
            ('Package Options', package_options_menu.display),
            ('Run Installer', exit_and_run)
        ])

        main_menu.display()

if __name__ == '__main__':
    os.environ.setdefault('ESCDELAY', '0')
    curses.wrapper(App)
    if run_installer:
        run()

