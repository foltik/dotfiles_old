#!/bin/python
import curses
from lib.parse import Category, Package, parse
from lib.menu import Menu
from lib.configure import configure

categories = parse('packages.yml')

def noop():
    pass

class App:
    def __init__(self, stdscreen):
        self.screen = stdscreen
        curses.curs_set(0)

        submenu_items = [
            ('do stuff', noop)
        ]
        submenu = Menu(self.screen, submenu_items)

        main_menu_items = [
            ('install', noop),
            ('submenu', submenu.display)
        ]
        main_menu = Menu(self.screen, main_menu_items)
        main_menu.display()

if __name__ == '__main__':
    curses.wrapper(App)

